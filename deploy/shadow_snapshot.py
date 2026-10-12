"""Event-driven shadow snapshots of a migration project: one commit per agent at
dispatch, right before its first explicit write, and at its end.

The shadow repository lives outside the project (--git-dir elsewhere, --work-tree
= project), so neither the pipeline's own git nor the agents ever see it. The
hook never blocks or denies anything: errors go to <root>/hook-errors.log.

Events (Claude Code hooks):
  SubagentStart     -> dispatch     (subagent; actor = agent_id)
  UserPromptSubmit  -> dispatch     (main session; actor = __main__)
  PreToolUse        -> first-write  (first explicit write per session+actor, taken
                                     before the tool runs; same write rules as the
                                     migloop memory-recall hook used in 5.31/5.32)
  SubagentStop      -> end          (also archives the subagent transcript)
  Stop              -> end          (main turn end; also archives the main transcript)

usage:
  shadow_snapshot.py init --root <shadow-root> --project <project> [--label scaffold]
  shadow_snapshot.py hook --root <shadow-root> --project <project>   (stdin = hook JSON)
  shadow_snapshot.py log  --root <shadow-root> [--agent <id-prefix>] [--all]
  shadow_snapshot.py resync --root <shadow-root>      (after a run: complete transcript copies + index.clean.jsonl)
  shadow_snapshot.py mark --root <shadow-root> --project <project> --id FIX-03 --title "..."   (one repair = one commit)
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

EXCLUDE = [
    "build/", "oh_modules/", ".hvigor/", ".idea/", ".preview/", "node_modules/", ".cxx/",
    "*.hap", "*.app", "*.har.tmp", "__pycache__/", "*.pyc",
]
LOCK_STALE_S = 120
LOCK_WAIT_S = 45


# ---- explicit-write detection: copied from migloop-memory-recall claude_hook.py (5.32) ----

def shell_tokens(command):
    pattern = re.compile(r'''(?P<space>[ \t\r]+)|(?P<comment>\#[^\n]*)|(?P<op>&>>|&>|>>|>&|<<-?|&&|\|\||[;|&<>\n])|(?P<word>(?:'[^']*'|"(?:\\.|`.|[^"\\])*"|\\.|`.|[^\s;|&<>(){}'"`\\])+ )''', re.X)
    tokens, pos = [], 0
    while pos < len(command):
        match = pattern.match(command, pos)
        if not match:
            return []
        pos = match.end()
        if match.lastgroup in {"space", "comment"}:
            continue
        if match.lastgroup == "op" and match.group().startswith("<<"):
            break
        tokens.append((match.lastgroup, match.group()))
    return tokens


def literal_word(word):
    if len(word) >= 2 and word[0] == word[-1] and word[0] in "\"'":
        return word[1:-1]
    return word


def file_destination(word, tool):
    value = literal_word(word)
    if not value or value.lower() in {"/dev/null", "/dev/stdout", "/dev/stderr", "nul", "nul:", "con", "con:", "-"}:
        return False
    if value.startswith(("/dev/fd/", "/proc/self/fd/")):
        return False
    if not word.startswith("'") and ("$" in value or "`" in value):
        return False
    return True


def explicit_write(tool, params):
    if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
        return "native:" + tool
    if tool not in {"Bash", "PowerShell"}:
        return None
    tokens = shell_tokens(params.get("command", ""))
    segments, segment = [], []
    for index, (kind, value) in enumerate(tokens):
        if kind == "op" and value in {">", ">>", "&>", "&>>"}:
            if index + 1 < len(tokens) and tokens[index + 1][0] == "word" and file_destination(tokens[index + 1][1], tool):
                return "shell:redirect"
        if kind == "op" and value in {";", "&&", "||", "|", "&", "\n"}:
            segments.append(segment)
            segment = []
        else:
            segment.append((kind, value))
    segments.append(segment)
    for segment in segments:
        if not segment or segment[0][0] != "word":
            continue
        words = [literal_word(value) for kind, value in segment if kind == "word"]
        name = words[0].replace("\\", "/").rsplit("/", 1)[-1].lower()
        args = words[1:]
        if any(a.lower() in {"--help", "--version", "--dry-run", "-?"} or a.lower().startswith("-whatif") for a in args):
            continue
        operands = [a for a in args if not a.startswith("-")]
        if name in {"cp", "mv", "copy-item", "move-item"} and len(operands) >= 2:
            return "shell:" + name
        if name in {"set-content", "add-content", "out-file"} and operands:
            return "shell:" + name
        if name == "tee" and any(file_destination(raw, tool) for kind, raw in segment[1:] if kind == "word" and not literal_word(raw).startswith("-")):
            return "shell:tee"
        if name == "sed" and any(a == "--in-place" or a.startswith("--in-place=") or re.fullmatch(r"-[a-zA-Z]*i(?:\..*)?", a) for a in args) and operands:
            return "shell:sed-in-place"
        if name == "apply_patch":
            return "shell:apply_patch"
    return None


# ---- shadow repository ----

class Shadow:
    def __init__(self, root, project):
        self.root = Path(root)
        self.project = Path(project)
        self.git_dir = self.root / "repo.git"

    def git(self, *args, check=True):
        cmd = ["git", "--git-dir", str(self.git_dir), "--work-tree", str(self.project), *args]
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=check)

    def init(self, label):
        if (self.git_dir / "HEAD").exists():
            raise SystemExit(f"shadow repo already exists: {self.git_dir}")
        self.root.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.git_dir)], check=True)
        for k, v in (("core.bare", "false"), ("core.worktree", str(self.project)), ("user.name", "shadow"),
                     ("user.email", "shadow@localhost"), ("core.autocrlf", "false"), ("core.longpaths", "true"),
                     ("core.quotepath", "false"), ("gc.auto", "0")):
            self.git("config", k, v)
        (self.git_dir / "info").mkdir(exist_ok=True)
        (self.git_dir / "info" / "exclude").write_text("\n".join(EXCLUDE) + "\n", encoding="utf-8")
        meta = {"event": label, "project": str(self.project), "ts": now()}
        sha = self.commit(label, "-", "-", meta)
        self.git("tag", "-a", label, "-m", f"{label} {now()}")
        print(json.dumps({"shadow": str(self.git_dir), "baseline": sha, "tag": label}, ensure_ascii=False))

    def commit(self, event, actor, agent_type, meta):
        self.git("add", "-A")
        stat = self.git("diff", "--cached", "--shortstat").stdout.strip() or "no tree change"
        subject = f"{event} {agent_type or '-'} {actor}"
        body = json.dumps(dict(meta, stat=stat), ensure_ascii=False)
        self.git("commit", "-q", "--allow-empty", "--no-verify", "-m", subject, "-m", body)
        return self.git("rev-parse", "HEAD").stdout.strip()

    # lock shared by concurrent hook processes (parallel agents)
    def lock(self):
        path = self.root / ".snapshot.lock"
        deadline = time.time() + LOCK_WAIT_S
        while True:
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return path
            except FileExistsError:
                try:
                    if time.time() - path.stat().st_mtime > LOCK_STALE_S:
                        path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.time() > deadline:
                    raise TimeoutError("snapshot lock busy")
                time.sleep(0.05)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) + f".{int(time.time() * 1000) % 1000:03d}"


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def safe_ref(text):
    return re.sub(r"[^A-Za-z0-9._-]", "_", text)


def long_path(path):
    """Windows extended-length form, so transcript paths past MAX_PATH still resolve."""
    text = os.path.abspath(str(path))
    if os.name == "nt" and not text.startswith("\\\\?\\"):
        return "\\\\?\\" + text
    return text


def archive_transcript(shadow, src, session, name):
    if not src or not os.path.isfile(long_path(src)):
        return None
    dest = shadow.root / "transcripts" / safe_ref(session) / name
    os.makedirs(long_path(dest.parent), exist_ok=True)
    shutil.copy2(long_path(src), long_path(dest))
    return str(dest)


def handle(shadow, payload):
    event_name = payload.get("hook_event_name")
    session = payload.get("session_id") or "nosession"
    actor = payload.get("agent_id") or "__main__"
    agent_type = payload.get("agent_type")
    tool, params = payload.get("tool_name", ""), payload.get("tool_input") or {}
    state = shadow.root / "state" / digest(session) / safe_ref(actor)

    if event_name == "SubagentStart":
        event = "dispatch"
    elif event_name == "UserPromptSubmit":
        event = "dispatch"
    elif event_name == "PreToolUse":
        rule = explicit_write(tool, params)
        if not rule or (state / "first-write.json").exists():
            return
        event = "first-write"
    elif event_name == "SubagentStop":
        # Claude Code's internal side agents fire SubagentStop with no SubagentStart, no agent_type and
        # no transcript (2048 run: 288 of 557 records); only agents we saw dispatched get an end commit
        if not agent_type and not (state / "dispatch.count").exists():
            return
        event = "end"
    elif event_name == "Stop":
        event = "end"
    else:
        return

    lock = shadow.lock()
    try:
        state.mkdir(parents=True, exist_ok=True)
        if event == "first-write":
            if (state / "first-write.json").exists():   # lost a race with a sibling call
                return
        seq_file = state / f"{event}.count"
        seq = int(seq_file.read_text()) + 1 if seq_file.exists() else 1
        meta = {"event": event, "seq": seq, "ts": now(), "hook": event_name, "session_id": session,
                "agent_id": actor, "agent_type": agent_type, "tool_use_id": payload.get("tool_use_id"),
                "transcript_path": payload.get("transcript_path"),
                "agent_transcript_path": payload.get("agent_transcript_path")}
        if event == "first-write":
            meta.update(tool=tool, write_rule=explicit_write(tool, params),
                        target=params.get("file_path") or params.get("notebook_path") or (params.get("command") or "")[:300])
        if event == "end":
            if actor == "__main__":
                main_tp = payload.get("transcript_path")
                meta["archived_transcript"] = archive_transcript(shadow, main_tp, session, "main.jsonl")
                # resync every subagent transcript of this session (their tails may land after SubagentStop)
                if main_tp:
                    sub_dir = Path(main_tp[:-6] if main_tp.endswith(".jsonl") else main_tp) / "subagents"
                    if os.path.isdir(long_path(sub_dir)):
                        for fn in os.listdir(long_path(sub_dir)):
                            if fn.endswith((".jsonl", ".json")):
                                archive_transcript(shadow, str(sub_dir / fn), session, fn)
            else:
                meta["archived_transcript"] = archive_transcript(shadow, payload.get("agent_transcript_path"), session, f"agent-{actor}.jsonl")
        sha = shadow.commit(event, actor, agent_type, meta)
        owner = actor if actor != "__main__" else f"main-{safe_ref(session)[:12]}"
        ref = f"refs/agents/{safe_ref(owner)}/{event}" + (f"-{seq}" if seq > 1 else "")
        shadow.git("update-ref", ref, sha)
        seq_file.write_text(str(seq))
        if event == "first-write":
            (state / "first-write.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        with (shadow.root / "index.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(dict(meta, commit=sha, ref=ref), ensure_ascii=False) + "\n")
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def is_ghost(rec, recs):
    """End record of an internal side agent: never dispatched, no agent_type (see SubagentStop above)."""
    if rec.get("event") != "end" or rec.get("agent_id") == "__main__" or rec.get("agent_type"):
        return False
    return not any(r.get("event") == "dispatch" and r.get("agent_id") == rec.get("agent_id")
                   and r.get("session_id") == rec.get("session_id") for r in recs)


def resync(root):
    """After a run: re-copy every archived session's transcripts (the main transcript's tail is still being
    flushed when the last Stop hook archives it), and write index.clean.jsonl without ghost records."""
    recs = [json.loads(line) for line in (root / "index.jsonl").read_text(encoding="utf-8").splitlines()]
    done = set()
    for r in recs:
        session, tp = r.get("session_id"), r.get("transcript_path")
        if r.get("agent_id") != "__main__" or not tp or session in done:
            continue
        done.add(session)
        archive_transcript(Shadow(root, "."), tp, session, "main.jsonl")
        sub_dir = Path(tp[:-6] if tp.endswith(".jsonl") else tp) / "subagents"
        if os.path.isdir(long_path(sub_dir)):
            for fn in os.listdir(long_path(sub_dir)):
                if fn.endswith((".jsonl", ".json")):
                    archive_transcript(Shadow(root, "."), str(sub_dir / fn), session, fn)
    clean = [r for r in recs if not is_ghost(r, recs)]
    (root / "index.clean.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in clean), encoding="utf-8")
    print(json.dumps({"sessions_resynced": len(done), "records": len(recs), "clean": len(clean),
                      "ghost": len(recs) - len(clean)}))


def mark(shadow, fix_id, title):
    """Explicit checkpoint after one repair: commit the whole tree as event 'fix', ref refs/fixes/<id>[-n]."""
    if not fix_id:
        raise SystemExit("mark needs --id")
    lock = shadow.lock()
    try:
        state = shadow.root / "state" / "fixes"
        state.mkdir(parents=True, exist_ok=True)
        seq_file = state / f"{safe_ref(fix_id)}.count"
        seq = int(seq_file.read_text()) + 1 if seq_file.exists() else 1
        meta = {"event": "fix", "seq": seq, "ts": now(), "hook": "mark", "fix_id": fix_id, "title": title,
                "agent_id": "__fix__", "agent_type": "fix"}
        sha = shadow.commit("fix", fix_id, "fix", meta)
        ref = f"refs/fixes/{safe_ref(fix_id)}" + (f"-{seq}" if seq > 1 else "")
        shadow.git("update-ref", ref, sha)
        seq_file.write_text(str(seq))
        with (shadow.root / "index.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(dict(meta, commit=sha, ref=ref), ensure_ascii=False) + "\n")
        print(json.dumps({"fix": fix_id, "commit": sha, "ref": ref,
                          "stat": shadow.git("show", "--shortstat", "--format=", sha).stdout.strip()}, ensure_ascii=False))
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "hook", "log", "resync", "mark"])
    ap.add_argument("--id", help="mark: fix id, e.g. FIX-03")
    ap.add_argument("--title", default="", help="mark: one-line description of the fix")
    ap.add_argument("--root", required=True)
    ap.add_argument("--project")
    ap.add_argument("--label", default="scaffold")
    ap.add_argument("--agent")
    ap.add_argument("--all", action="store_true", help="log: include ghost end records")
    a = ap.parse_args()
    if a.cmd == "init":
        Shadow(a.root, a.project).init(a.label)
        return
    if a.cmd == "resync":
        resync(Path(a.root))
        return
    if a.cmd == "mark":
        mark(Shadow(a.root, a.project), a.id, a.title)
        return
    if a.cmd == "log":
        idx = Path(a.root) / "index.jsonl"
        recs = [json.loads(line) for line in idx.read_text(encoding="utf-8").splitlines()] if idx.exists() else []
        for r in recs:
            if is_ghost(r, recs) and not a.all:
                continue
            if a.agent and not str(r.get("agent_id", "")).startswith(a.agent):
                continue
            print(f"{r['ts']}  {r['event']:<11} {str(r.get('agent_type') or '-'):<26} {r['agent_id']:<20} {r['commit'][:10]}  {r.get('target') or ''}")
        return
    # hook mode: never block the agent
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
        handle(Shadow(a.root, a.project), json.loads(raw) if raw.strip() else {})
    except Exception:
        try:
            Path(a.root).mkdir(parents=True, exist_ok=True)
            with (Path(a.root) / "hook-errors.log").open("a", encoding="utf-8") as f:
                f.write(f"--- {now()}\n{traceback.format_exc()}\n")
        except Exception:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
