"""Live first-write recall for a migration run (the recall_sweep_digest arm of a2h-replay-bench, wired into a real run).

PreToolUse hook. At each agent's first explicit write (same rule as the shadow snapshots, shadow_snapshot.py) it
forks that agent's own transcript into a read-only recall worker (same model, Read/Glob/Grep, empty cwd, settings
limited to project/local, so no hooks, skills or CLAUDE.md of the run are loaded), runs the recall steps
(default sweep3) over the library, and denies that write once with the digest (one line per lesson: title ->
the worker's reminder, body path). Explicit writes of the same agent issued while its recall runs wait for it
and are denied with the same digest, so nothing lands before the agent has seen it. Fails open: a worker error,
timeout or an empty answer lets the write through. Compatible with shadow_snapshot.py (runs in parallel with it,
writes nothing to the project or the shadow repo).

Agent transcript: main session = transcript_path; subagent = <transcript_path without .jsonl>/subagents/
agent-<agent_id>.jsonl (the hook payload carries agent_id but no agent transcript path), cut before the message
holding the pending tool call.

Everything goes under --root: config.json, state/ (one marker per session+agent), forks/<agent>-<n>/ (worker
session, prompt, stream, result), recall-index.jsonl (one row per decision), hook-errors.log.

Model access: with no --slot the worker uses the migration session's own endpoint, credentials and model (this
hook's environment; the forked session file goes into that CLAUDE_CONFIG_DIR). With --slot it gets its own
endpoint/key from the slot csv and a private config dir, and shares no quota with the migration.

usage:
  py recall_hook.py install --project P --root R --library L [--slot glm-03[,glm-0x] --keys K] [--method sweep3]
                            [--model M] [--effort high] [--max-workers 16] [--worker-timeout 1800]
  py recall_hook.py hook --root R                      (stdin = hook JSON; what install puts into settings)
  py recall_hook.py test --root R --transcript T --agent-id A --tool-use-id U   (fork + recall once, no hook)
  py recall_hook.py log --root R
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recall_core as bench  # noqa: E402  (same names as in a2h-replay-bench harness/bench.py)
from shadow_snapshot import explicit_write  # noqa: E402  (one write rule for snapshots and recall)

POLL_S = 2


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def safe(text):
    return re.sub(r"[^A-Za-z0-9._-]", "_", text)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def log(root, row):
    with (root / "recall-index.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(row, ts=now()), ensure_ascii=False) + "\n")


def read_marker(path):
    try:
        return json.loads(path.read_text(encoding="utf-8") or "{}")
    except (OSError, ValueError):   # being rewritten right now
        return {"status": "running"}


def deny(text):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": text}}


class Lib:
    """What bench.digest_lines needs from an App."""
    def __init__(self, path):
        self.path = Path(path)

    def recall_library(self):
        return self.path


# ---------------------------------------------------------------- fork + worker

def agent_transcript(payload):
    main = payload.get("transcript_path") or ""
    aid = payload.get("agent_id")
    if not aid:
        return Path(main)
    base = main[:-6] if main.endswith(".jsonl") else main
    return Path(base) / "subagents" / f"agent-{aid}.jsonl"


def fork_rows(path, tool_use_id, sid, cwd):
    """The agent's transcript up to (not including) the message that holds the pending tool call."""
    rows = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue   # a line still being written
    cut = len(rows)
    for i, r in enumerate(rows):
        msg = r.get("message") or {}
        if r.get("type") == "assistant" and isinstance(msg.get("content"), list) and any(
                isinstance(b, dict) and b.get("type") == "tool_use" and b.get("id") == tool_use_id for b in msg["content"]):
            mid, cut = msg.get("id"), i
            while cut > 0 and rows[cut - 1].get("type") == "assistant" and (rows[cut - 1].get("message") or {}).get("id") == mid:
                cut -= 1
            break
    out = []
    for r in rows[:cut]:
        r.update(sessionId=sid, isSidechain=False, cwd=str(cwd))
        r.pop("agentId", None)
        r.pop("attributionAgent", None)
        out.append(json.dumps(r, ensure_ascii=False))
    return out, cut, len(rows)


def acquire_slot(root, n, wait_s, stale_s):
    slots = root / "slots"
    slots.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + wait_s
    while True:
        for i in range(n):
            p = slots / f"{i}.lock"
            try:
                fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return p
            except FileExistsError:
                try:
                    if time.time() - p.stat().st_mtime > stale_s:   # a worker that died without releasing
                        p.unlink()
                except FileNotFoundError:
                    pass
        if time.time() > deadline:
            return None
        time.sleep(POLL_S)


QUOTA_CODES = ("1310", "1113")   # GLM: 7-day / 5-hour usage cap reached; balance exhausted


def quota_hit(stream):
    """The worker died on a usage cap of its slot (not a transient 429)."""
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines() if stream.exists() else []:
        if '"api_error_status":429' in line.replace(" ", "") and any(f"[{c}]" in line for c in QUOTA_CODES):
            return True
    return False


def run_with_fallback(cfg, root, *args):
    """Run the worker on the first slot not known to be capped; on a cap, mark the slot and try the next one."""
    if not cfg["slots"]:   # no slot: the migration session's own endpoint, credentials and model
        d, res, text = run_worker(dict(cfg, slot=None), root, *args)
        res["slot"] = "inherit"
        return d, res, text
    capped_f = root / "capped-slots.json"
    for slot in cfg["slots"]:
        capped = json.loads(capped_f.read_text(encoding="utf-8")) if capped_f.exists() else {}
        if slot in capped:
            continue
        d, res, text = run_worker(dict(cfg, slot=slot), root, *args)
        res["slot"] = slot
        if res["exit"] != 0 and quota_hit(d / "stream.jsonl"):
            capped[slot] = now()
            capped_f.write_text(json.dumps(capped), encoding="utf-8")
            log(root, {"decision": "slot-capped", "agent_id": "-", "slot": slot, "fork": str(d)})
            continue
        return d, res, text
    raise RuntimeError("every recall slot is capped")


def inherit_env():
    """No slot: the worker runs on this hook's environment, i.e. the migration session's endpoint and credentials
    (and its CLAUDE_CONFIG_DIR, so a login stored there works too). The user's CLAUDE.md files and auto memory are
    off; user settings and hooks are excluded by --setting-sources on the command line."""
    drop = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PROJECT_DIR", "CLAUDE_CODE_SSE_PORT")
    env = {k: v for k, v in os.environ.items() if k not in drop}
    env.update(CLAUDE_CODE_DISABLE_CLAUDE_MDS="1", CLAUDE_CODE_DISABLE_AUTO_MEMORY="1",
               CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1", DISABLE_AUTOUPDATER="1")
    return env


def worker_model(transcript):
    """The agent's own model: ANTHROPIC_MODEL if set, else the model of its latest reply, with [1m] because a forked
    transcript can be long; None leaves the choice to Claude Code."""
    if os.environ.get("ANTHROPIC_MODEL"):
        return os.environ["ANTHROPIC_MODEL"]
    model = None
    for line in Path(transcript).read_text(encoding="utf-8", errors="replace").splitlines():
        if '"assistant"' not in line:
            continue
        try:
            m = (json.loads(line).get("message") or {}).get("model")
        except ValueError:
            continue
        if m and not m.startswith("<"):
            model = m
    return model + "[1m]" if model and "[" not in model else model


def run_worker(cfg, root, transcript, tool_use_id, tool, params, label):
    n = 1
    while (root / "forks" / f"{label}-{n}").exists():
        n += 1
    d = root / "forks" / f"{label}-{n}"
    cwd = d / "cwd"
    cwd.mkdir(parents=True)
    sid = str(uuid.uuid4())
    if cfg.get("slot"):
        cfg_dir, env = d / "cfg", bench.slot_env(cfg["slot"], d / "cfg")
    else:
        env = inherit_env()
        cfg_dir = Path(env.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    proj = cfg_dir / "projects" / re.sub(r"[^a-zA-Z0-9]", "-", str(cwd))
    proj.mkdir(parents=True)
    rows, cut, total = fork_rows(transcript, tool_use_id, sid, cwd)
    (proj / f"{sid}.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    lib = Path(cfg["library"])
    method = cfg["method"]
    prompt = (bench.RECALL_HEAD.format(goal=bench.RECALL_GOAL[method],
                                       pending=bench.pending_text({"tool": tool, "input": params}, lambda x: x))
              + bench.RECALL_STEPS[method].format(root=lib.as_posix(), catalog=bench.topic_catalog(lib))
              + bench.RECALL_OUT[method])
    (d / "prompt.md").write_text(prompt, encoding="utf-8")
    (d / "fork.json").write_text(json.dumps({"transcript": str(transcript), "rows_kept": cut, "rows_total": total,
                                             "tool_use_id": tool_use_id}, ensure_ascii=False), encoding="utf-8")
    claude = os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude"
    model = cfg["model"] or worker_model(transcript)
    cmd = [claude, "-p", "--resume", sid] + (["--model", model] if model else []) + [
           "--effort", cfg["effort"],
           "--tools", "Read,Glob,Grep", "--dangerously-skip-permissions", "--setting-sources", "project,local",
           "--max-turns", "200", "--output-format", "stream-json", "--verbose"]
    t0, code = time.time(), None
    with (d / "stream.jsonl").open("wb") as out, (d / "stderr.log").open("wb") as err:
        try:
            code = subprocess.run(cmd, cwd=cwd, env=env, input=prompt.encode("utf-8"), stdout=out, stderr=err,
                                  timeout=cfg["worker_timeout"]).returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    res = {"exit": code, "seconds": round(time.time() - t0), "fork_rows": cut} | bench.parse_recall(d, lib)
    (d / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    text = bench.INJECT_DIGEST.format(lessons=bench.digest_lines(Lib(lib), res)) if res["lessons"] else None
    return d, res, text


# ---------------------------------------------------------------- hook

def handle(root, payload):
    if payload.get("hook_event_name") != "PreToolUse":
        return None
    tool, params = payload.get("tool_name", ""), payload.get("tool_input") or {}
    if not explicit_write(tool, params):
        return None
    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    if cfg.get("keys"):
        bench.KEYS = Path(cfg["keys"])
    session = payload.get("session_id") or "nosession"
    actor = payload.get("agent_id") or "__main__"
    state = root / "state" / digest(session) / safe(actor)
    state.mkdir(parents=True, exist_ok=True)
    marker = state / "recall.json"
    base = {"session_id": session, "agent_id": actor, "agent_type": payload.get("agent_type"),
            "tool_use_id": payload.get("tool_use_id"), "tool": tool,
            "target": params.get("file_path") or params.get("notebook_path") or str(params.get("command") or "")[:200]}
    try:
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, json.dumps({"status": "running", "started": time.time()}).encode())
        os.close(fd)
    except FileExistsError:
        # another write of this agent. Arriving while its recall runs (a sibling call of the same turn): wait and
        # deny with the same digest, so nothing lands before the agent has seen it. Arriving after: let it through.
        info = read_marker(marker)
        if info.get("status") != "running":
            return None
        deadline = time.time() + cfg["worker_timeout"] + cfg["slot_wait"] + 60
        while info.get("status") == "running" and time.time() < deadline:
            time.sleep(POLL_S)
            info = read_marker(marker)
        if not info.get("text"):
            return None
        log(root, dict(base, decision="deny-sibling", fork=info.get("fork")))
        return deny(info["text"])
    info = {"status": "error", "first_tool_use_id": payload.get("tool_use_id")}
    try:
        slot = acquire_slot(root, cfg["max_workers"], cfg["slot_wait"], cfg["worker_timeout"] + 300)
        if slot is None:
            log(root, dict(base, decision="allow", reason="no free worker slot"))
            info["status"] = "skipped"
            return None
        try:
            d, res, text = run_with_fallback(cfg, root, agent_transcript(payload), payload.get("tool_use_id"), tool,
                                             params, safe(actor)[:24])
        except RuntimeError as e:
            log(root, dict(base, decision="allow", reason=str(e)))
            return None
        finally:
            slot.unlink(missing_ok=True)
        u = res.get("usage") or {}
        info.update(status="done", fork=str(d), text=text)
        log(root, dict(base, decision="deny" if text else "allow", fork=str(d), exit=res["exit"], slot=res.get("slot"),
                       seconds=res["seconds"], lessons=res["lessons"], fork_rows=res["fork_rows"],
                       tokens_in=(u.get("billed_input") or 0) + (u.get("billed_cache_read") or 0),
                       tokens_out=u.get("billed_output")))
        return deny(text) if text else None
    finally:
        marker.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------- install / test / log

def install(a):
    root, project = Path(a.root), Path(a.project)
    root.mkdir(parents=True, exist_ok=True)
    slots = [x.strip() for x in (a.slot or "").split(",") if x.strip()]
    if not a.library or not (Path(a.library) / "index.md").is_file():
        raise SystemExit(f"no memory library (index.md) at {a.library}")
    cfg = {"library": str(Path(a.library)), "method": a.method, "model": a.model, "effort": a.effort, "slots": slots,
           "max_workers": a.max_workers, "worker_timeout": a.worker_timeout, "slot_wait": a.slot_wait,
           "project": str(project)}
    if a.method not in bench.RECALL_STEPS:
        raise SystemExit(f"unknown method {a.method}")
    if slots:
        keys = Path(a.keys).expanduser().resolve()
        if not keys.is_file():
            raise SystemExit(f"no key csv at {keys} (--keys or RECALL_KEYS)")
        cfg["keys"] = str(keys)   # the hook runs in Claude Code's environment, which may not carry RECALL_KEYS
        bench.KEYS = keys
        for x in slots:
            bench.key(x)   # fails early on a missing slot (the key itself is never printed)
    (root / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    local = project / ".claude" / "settings.local.json"
    settings = json.loads(local.read_text(encoding="utf-8")) if local.exists() else {}
    settings.setdefault("autoMemoryEnabled", False)
    py = sys.executable.replace("\\", "/")
    cmd = f'"{py}" -B -X utf8 "{Path(__file__).resolve().as_posix()}" hook --root "{root.as_posix()}"'
    entry = {"matcher": "Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell",
             "hooks": [{"type": "command", "command": cmd, "timeout": a.worker_timeout + a.slot_wait + 120}]}
    pre = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    pre[:] = [e for e in pre if "recall_hook.py" not in json.dumps(e)] + [entry]
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"installed": str(local), "root": str(root), "hooks": sorted(settings["hooks"])}, ensure_ascii=False))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["install", "hook", "test", "log"])
    ap.add_argument("--root", required=True)
    ap.add_argument("--project")
    ap.add_argument("--library", help="install: the memory library workers read (use an isolated copy)")
    ap.add_argument("--keys", default=str(bench.KEYS), help="slot csv (slot,api_key,base_url); default RECALL_KEYS")
    ap.add_argument("--slot", default="", help="worker key slot(s), comma-separated: later ones take over when one is "
                    "capped; none = the migration session's own endpoint and credentials")
    ap.add_argument("--method", default="sweep3")
    ap.add_argument("--model", default="", help="worker model; default = the recalled agent's own model")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--max-workers", type=int, default=16)
    ap.add_argument("--worker-timeout", type=int, default=1800)
    ap.add_argument("--slot-wait", type=int, default=1800)
    ap.add_argument("--transcript")
    ap.add_argument("--agent-id")
    ap.add_argument("--tool-use-id")
    a = ap.parse_args()
    root = Path(a.root)
    if a.cmd == "install":
        install(a)
    elif a.cmd == "hook":
        try:
            raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
            out = handle(root, json.loads(raw) if raw.strip() else {})
            if out:
                sys.stdout.write(json.dumps(out, ensure_ascii=False))
        except Exception:
            with (root / "hook-errors.log").open("a", encoding="utf-8") as f:
                f.write(f"--- {now()}\n{traceback.format_exc()}\n")
        sys.exit(0)
    elif a.cmd == "test":
        cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
        rows = [json.loads(x) for x in Path(a.transcript).read_text(encoding="utf-8").splitlines() if x.strip()]
        call = next(b for r in rows if r.get("type") == "assistant" for b in (r.get("message") or {}).get("content") or []
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("id") == a.tool_use_id)
        d, res, text = run_with_fallback(cfg, root, Path(a.transcript), a.tool_use_id, call["name"], call.get("input") or {},
                                         "test-" + safe(a.agent_id or "main"))
        print(json.dumps({"fork": str(d), "exit": res["exit"], "seconds": res["seconds"], "fork_rows": res["fork_rows"],
                          "lessons": len(res["lessons"])}, ensure_ascii=False))
        print(text or "(no digest)")
    elif a.cmd == "log":
        for line in (root / "recall-index.jsonl").read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            print(f"{r['ts']} {r['decision']:<14} {str(r.get('agent_type') or '-'):<24} {r['agent_id'][:18]:<18} "
                  f"{r.get('seconds', '')!s:>5}s {len(r.get('lessons') or [])} lessons  {r.get('target', '')[-60:]}")


if __name__ == "__main__":
    main()
