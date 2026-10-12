"""Deploy migration recording and memory recall onto an a2h target project: shadow git snapshots at every
dispatch / first explicit write / end, the Claude Code hooks that drive them, and the first-write recall hook over
this repository's memory library. App-agnostic: the project (already carrying its .claude agents and skills), the
migration prompt and the model launch stay yours. No model is involved here; only the migration and the recall
workers call one.

usage:
  python3 deploy/deploy.py install --project P                  recording + recall with this branch's memory/
  python3 deploy/deploy.py install --project P [--no-recall] [--shadow S] [--memory LIB] [--recall-root R]
                           [--recall-slot glm-03[,glm-0x] --keys K] [--method sweep3]
  python3 deploy/deploy.py status  --project P [--shadow S]
  python3 deploy/deploy.py finish  --project P [--shadow S] [--archive ZIP] [--forbid PATH ...] [--notes FILE] [--force]

Defaults: S = <parent of P>/_shadow/<name of P>, R = <parent of P>/_recall/<name of P>,
ZIP = <parent of P>/a2h-migration-archive/<name of P>-execute-YYYYMMDD.zip.
Recall workers use the migration session's own endpoint, credentials and model unless --recall-slot names key
slots in a csv (columns slot,api_key,base_url; --keys or RECALL_KEYS), which keeps their quota separate.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import zipfile

E2E = Path(__file__).resolve().parent
MEMORY = E2E.parent / "memory"   # this branch's library
SHADOW_TOOL = E2E / "shadow_snapshot.py"
RECALL_TOOL = E2E / "recall_hook.py"
SHADOW_EVENTS = [("SubagentStart", "*"), ("UserPromptSubmit", None),
                 ("PreToolUse", "Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell"),
                 ("SubagentStop", "*"), ("Stop", None)]
SKIP_DIRS = {"build", "oh_modules", ".hvigor", ".idea", ".preview", "node_modules", "__pycache__"}


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace",
                          check=True, **kw).stdout


def fwd(p):
    return str(p).replace("\\", "/")


def roots(a):
    project = Path(a.project).resolve()
    shadow = Path(a.shadow).resolve() if a.shadow else project.parent / "_shadow" / project.name
    recall = Path(a.recall_root).resolve() if a.recall_root else project.parent / "_recall" / project.name
    return project, shadow, recall


def load(a):
    project, shadow, _ = roots(a)
    f = shadow / "deploy.json"
    if not f.exists():
        raise SystemExit(f"no deploy.json in {shadow}: run install first")
    return json.loads(f.read_text(encoding="utf-8")), f


# ---------------------------------------------------------------- install

def write_shadow_hooks(project, shadow):
    local = project / ".claude" / "settings.local.json"
    settings = json.loads(local.read_text(encoding="utf-8")) if local.exists() else {}
    settings["autoMemoryEnabled"] = False
    cmd = (f'"{fwd(sys.executable)}" -B -X utf8 "{fwd(SHADOW_TOOL)}" hook '
           f'--root "{fwd(shadow)}" --project "{fwd(project)}"')
    hooks = settings.setdefault("hooks", {})
    for event, matcher in SHADOW_EVENTS:
        entry = {"hooks": [{"type": "command", "command": cmd, "timeout": 60}]}
        if matcher:
            entry = {"matcher": matcher, **entry}
        hooks[event] = [e for e in hooks.get(event, []) if "shadow_snapshot.py" not in json.dumps(e)] + [entry]
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")


def install(a):
    project, shadow, recall = roots(a)
    if not project.is_dir():
        raise SystemExit(f"no project at {project}: prepare it first (template + .claude), then install")
    if (shadow / "repo.git").exists():
        raise SystemExit(f"shadow repository already exists: {shadow}")
    memory = None if a.no_recall else Path(a.memory or MEMORY).resolve()
    if memory and not (memory / "index.md").is_file():
        raise SystemExit(f"no memory library (index.md) at {memory}")
    write_shadow_hooks(project, shadow)
    lib = None
    if memory:
        lib = recall / "library" / "memory"
        if lib.exists():
            raise SystemExit(f"memory copy already exists: {lib}")
        # isolated copy: recall workers read only this, nothing that sits next to the original library
        shutil.copytree(memory, lib)
        print(run([sys.executable, "-B", "-X", "utf8", RECALL_TOOL, "install", "--project", project, "--root", recall,
                   "--library", lib, "--method", a.method]
                  + (["--slot", a.recall_slot] if a.recall_slot else [])
                  + (["--keys", Path(a.keys).expanduser().resolve()] if a.recall_slot and a.keys else [])).strip())
    # baseline commit after the hooks are in: the tree the migration starts from, settings included
    print(run([sys.executable, "-B", "-X", "utf8", SHADOW_TOOL, "init", "--root", shadow, "--project", project,
               "--label", "scaffold"]).strip())
    cfg = {"project": str(project), "shadow": str(shadow), "recall": str(recall) if lib else None,
           "memory_source": str(memory) if memory else None, "memory_revision": memory_revision(memory),
           "recall_slots": (a.recall_slot.split(",") if a.recall_slot else ["inherit"]) if lib else [],
           "installed": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    (shadow / "deploy.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"installed": str(project), "shadow": str(shadow), "recall": cfg["recall"],
                      "next": "start the migration in the project as usual"}, ensure_ascii=False))


def memory_revision(memory):
    """The library's knowledge revision and git commit, so a run records exactly which memory it recalled from."""
    if not memory:
        return None
    out = {}
    try:
        out["revision"] = json.loads((memory / "manifest.json").read_text(encoding="utf-8")).get("memory_revision")
    except (OSError, ValueError):
        pass
    try:
        out["commit"] = run(["git", "-C", memory, "rev-parse", "HEAD"]).strip()
        out["branch"] = run(["git", "-C", memory, "rev-parse", "--abbrev-ref", "HEAD"]).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return out or None


# ---------------------------------------------------------------- status / finish

def index(shadow):
    f = Path(shadow) / "index.jsonl"
    return [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines()] if f.exists() else []


def sessions(recs):
    return {r["session_id"]: Path(r["transcript_path"]) for r in recs
            if r.get("agent_id") == "__main__" and r.get("transcript_path")}


def transcript_files(main):
    sub = main.with_suffix("") / "subagents"
    return [main] + (sorted(sub.glob("agent-*.jsonl")) if sub.is_dir() else [])


def usage(files):
    seen, first, last_text = {}, None, None
    for f in files:
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            m = o.get("message") or {}
            if f == files[0] and o.get("timestamp"):
                first = first or o["timestamp"]
                if o.get("type") == "assistant" and isinstance(m.get("content"), list) and \
                        any(c.get("type") == "text" for c in m["content"]):
                    last_text = o["timestamp"]
            if o.get("type") == "assistant" and isinstance(m, dict) and m.get("usage"):
                seen[(f.name, m.get("id"))] = m["usage"]
    return {"api_calls": len(seen), "first": first, "last_text": last_text,
            "input": sum((u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
                         + (u.get("cache_creation_input_tokens") or 0) for u in seen.values()),
            "output": sum(u.get("output_tokens") or 0 for u in seen.values())}


def minutes(t0, t1):
    from datetime import datetime
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))  # noqa: E731
    return round((f(t1) - f(t0)).total_seconds() / 60) if t0 and t1 else None


def recall_summary(root):
    f = Path(root) / "recall-index.jsonl" if root else None
    if not f or not f.exists():
        return None
    rows = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    first = [r for r in rows if r.get("decision") in ("deny", "allow") and "exit" in r]
    n_lessons = lambda r: r.get("lessons") if isinstance(r.get("lessons"), int) else len(r.get("lessons") or [])  # noqa: E731
    return {"recalls": len(first), "injected": sum(r["decision"] == "deny" for r in first),
            "failed_open": [r["agent_id"] for r in first if r["exit"] != 0],
            "lessons": sum(n_lessons(r) for r in first),
            "seconds_mean": round(sum(r.get("seconds", 0) for r in first) / len(first)) if first else 0,
            "worker_input": sum(r.get("tokens_in", 0) for r in first),
            "worker_output": sum(r.get("tokens_out", 0) for r in first)}


def status(a):
    cfg, _ = load(a)
    recs = index(cfg["shadow"])
    events = {}
    for r in recs:
        events[r["event"]] = events.get(r["event"], 0) + 1
    out = {"project": cfg["project"], "finished": cfg.get("finished"), "shadow_events": events,
           "sessions": [str(p) for p in sessions(recs).values()], "recall": recall_summary(cfg.get("recall"))}
    for p in sessions(recs).values():
        if p.exists():
            out["main_transcript_idle_min"] = round((time.time() - p.stat().st_mtime) / 60)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def norm(s):
    """Comparable path text: forward slashes, lower case; on Windows also C:/ for Git Bash's /c/."""
    s = s.replace("\\\\", "/").replace("\\", "/").lower()
    return re.sub(r"(?<![a-z])/c/", "c:/", s) if os.name == "nt" else s


def leak_scan(cfg, files, forbid):
    """Tool calls (migration agents and recall workers) that touch a forbidden path; the run's own shadow
    repository is always off limits for the migration agents."""
    rules = [(norm(fwd(Path(p).resolve())), True) for p in forbid] + [(norm(fwd(cfg["shadow"])), False)]
    rules = [(p, re.compile(re.escape(p) + r"(?![a-z0-9._-])"), workers_too) for p, workers_too in rules]
    hits = []
    for f in files:
        worker = "forks" in f.parts
        for i, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            if '"tool_use"' not in line:
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            for c in (o.get("message") or {}).get("content") or []:
                if not isinstance(c, dict) or c.get("type") != "tool_use":
                    continue
                s = norm(json.dumps(c.get("input"), ensure_ascii=False))
                bad = sorted({p for p, rx, workers_too in rules if (workers_too or not worker) and rx.search(s)})
                if bad:
                    hits.append({"file": str(f), "line": i, "tool": c.get("name"), "paths": bad})
    return {"files": len(files), "forbidden": [p for p, _, w in rules if w], "hits": hits}


def finish(a):
    cfg, cfg_file = load(a)
    shadow, project = Path(cfg["shadow"]), Path(cfg["project"])
    mains = sessions(index(shadow))
    if not mains:
        raise SystemExit("no main session recorded in the shadow index")
    idle = min((time.time() - p.stat().st_mtime) / 60 for p in mains.values() if p.exists())
    if idle < 10 and not a.force:
        raise SystemExit(f"main transcript changed {idle:.0f} min ago: the run may still be going (use --force)")
    print(run([sys.executable, "-B", "-X", "utf8", SHADOW_TOOL, "resync", "--root", shadow]).strip())
    g = ["git", "--git-dir", shadow / "repo.git", "--work-tree", project]
    if run(g + ["status", "--porcelain"]).strip():
        run(g + ["add", "-A"])
        run(g + ["commit", "-q", "--no-verify", "-m", "finish - -", "-m", "tree at finish (after the last end event)"])
    if not run(g + ["tag", "-l", "execute-end"]).strip():
        run(g + ["tag", "-a", "execute-end", "-m", f"execute-end {time.strftime('%Y-%m-%dT%H:%M:%S%z')}"])
    execute_end = run(g + ["rev-parse", "execute-end^{commit}"]).strip()

    files = [f for p in mains.values() for f in transcript_files(p) if f.exists()]
    per = [usage(transcript_files(p)) for p in mains.values()]
    rec = recall_summary(cfg.get("recall"))
    workers = sorted(Path(cfg["recall"]).glob("forks/*/stream.jsonl")) if cfg.get("recall") else []
    leaks = leak_scan(cfg, files + workers, a.forbid or [])
    stats = {"wall_min": minutes(per[0]["first"], per[-1]["last_text"]),
             "subagents": sum(len(transcript_files(p)) - 1 for p in mains.values()),
             "api_calls": sum(u["api_calls"] for u in per), "input": sum(u["input"] for u in per),
             "output": sum(u["output"] for u in per), "recall": rec, "execute_end": execute_end,
             "leak_hits": len(leaks["hits"])}
    (shadow / "finish.json").write_text(json.dumps({"stats": stats, "leaks": leaks}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")

    out = Path(a.archive).resolve() if a.archive else \
        project.parent / "a2h-migration-archive" / f"{project.name}-execute-{time.strftime('%Y%m%d')}.zip"
    if out.exists():
        raise SystemExit(f"{out} exists")
    out.parent.mkdir(parents=True, exist_ok=True)
    counts = {"project": 0, "sessions": 0, "shadow": 0, "recall": 0}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(project):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in fn:
                p = Path(dp, f)
                z.write(p, "project/" + p.relative_to(project).as_posix())
                counts["project"] += 1
        for p in mains.values():
            sub = p.with_suffix("") / "subagents"
            for f in [p] + (sorted(sub.iterdir()) if sub.is_dir() else []):
                if f.is_file():
                    z.write(f, "sessions/" + f.relative_to(p.parent.parent).as_posix())
                    counts["sessions"] += f.suffix == ".jsonl"
        for name in ("repo.git", "state", "index.jsonl", "index.clean.jsonl", "deploy.json", "finish.json"):
            src = shadow / name
            for p in ([Path(dp, f) for dp, _, fn in os.walk(src) for f in fn] if src.is_dir()
                      else [src] if src.exists() else []):
                z.write(p, "shadow/" + p.relative_to(shadow).as_posix())
                counts["shadow"] += 1
        if cfg.get("recall"):
            r = Path(cfg["recall"])
            for p in [r / "config.json", r / "recall-index.jsonl"] + sorted(r.glob("forks/*/result.json")) \
                    + sorted(r.glob("forks/*/prompt.md")):
                if p.exists():
                    z.write(p, "recall/" + p.relative_to(r).as_posix())
                    counts["recall"] += 1
        haps = sorted(project.glob("entry/build/default/outputs/default/*.hap"))
        for h in haps:
            z.write(h, "hap/" + h.name)
        notes = Path(a.notes).read_text(encoding="utf-8") if a.notes else "（无）\n"
        z.writestr("README.md", readme(cfg, stats, counts, haps, notes))
    cfg.update(finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"), archive=str(out))
    cfg_file.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"archive": str(out), "mb": round(out.stat().st_size / 1e6, 1), **stats,
                      "leak_report": str(shadow / "finish.json")}, ensure_ascii=False, indent=1))


def readme(cfg, st, counts, haps, notes):
    rec = st["recall"]
    if cfg.get("recall") and rec:
        recall_line = (f"首写召回 {rec['recalls']} 次，注入 {rec['injected']} 次，失败放行 {len(rec['failed_open'])} 次"
                       f"（{', '.join(rec['failed_open']) or '-'}）；worker 输入 {rec['worker_input'] / 1e6:.1f}M、"
                       f"输出 {rec['worker_output'] / 1e6:.2f}M token；经验库副本来自 {cfg['memory_source']}"
                       f"（{json.dumps(cfg.get('memory_revision'), ensure_ascii=False)}）")
    elif cfg.get("recall"):
        recall_line = f"装了首写召回（经验库副本来自 {cfg['memory_source']}），没有召回记录"
    else:
        recall_line = "无 memory 召回"
    lines = [
        f"# {Path(cfg['project']).name} · a2h-execute 结束时的状态", "",
        f"- 打包时间：{time.strftime('%Y-%m-%d %H:%M:%S %z')}；由 fixchain-memory `deploy/deploy.py finish` 生成",
        f"- 记忆：{recall_line}",
        f"- 迁移：{st['wall_min']} 分钟（主会话首条到最后一条回复），{st['subagents']} 个子 agent，{st['api_calls']} 次 API 调用，"
        f"输入 {st['input'] / 1e6:.1f}M token（含缓存读取）、输出 {st['output'] / 1e6:.2f}M",
        f"- 防抄扫描：工具调用里碰到禁区 {st['leak_hits']} 次（明细在 shadow/finish.json）", "",
        "## 内容",
        f"- project/：工程（不含 {', '.join(sorted(SKIP_DIRS))}），{counts['project']} 个文件",
        f"- sessions/：生成期会话（主会话 + subagents/ 转录与 meta），{counts['sessions']} 个转录",
        "- shadow/：影子仓 repo.git（工程外 git-dir，work-tree=工程）、index.jsonl、index.clean.jsonl、state/、deploy.json、finish.json",
        "  - 每个 agent 在派发 / 首次显式写入前 / 结束各一次提交，refs/agents/<agent>/<事件>",
        f"  - 标签：scaffold（迁移前）、execute-end = {st['execute_end']}",
        "  - 用法：git --git-dir shadow/repo.git --work-tree <目录> checkout <ref> -- .",
    ]
    if counts["recall"]:
        lines.append(f"- recall/：召回配置、recall-index.jsonl、每次召回的 prompt 与结果，{counts['recall']} 个文件")
    if haps:
        lines.append(f"- hap/：{', '.join(h.name for h in haps)}")
    return "\n".join(lines) + f"\n\n## 已知（打包时）\n\n{notes}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["install", "status", "finish"])
    ap.add_argument("--project", required=True, help="the migration's target project directory")
    ap.add_argument("--shadow", help="shadow root (default <parent>/_shadow/<name>)")
    ap.add_argument("--memory", help="install: memory library to recall from, copied into the recall root "
                    "(default: memory/ of this branch)")
    ap.add_argument("--no-recall", action="store_true", help="install: recording only, no memory recall")
    ap.add_argument("--recall-root", help="default <parent>/_recall/<name>")
    ap.add_argument("--recall-slot", help="install: worker key slot(s), comma-separated; default: the migration "
                    "session's own endpoint and credentials")
    ap.add_argument("--keys", help="install: slot csv (slot,api_key,base_url); default RECALL_KEYS")
    ap.add_argument("--method", default="sweep3", help="install: recall steps (recall_core.RECALL_STEPS)")
    ap.add_argument("--archive", help="finish: zip path")
    ap.add_argument("--forbid", nargs="*", help="finish: paths the agents must not have touched (earlier runs, archives, ...)")
    ap.add_argument("--notes", help="finish: text file appended to the archive README")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    {"install": install, "status": status, "finish": finish}[a.cmd](a)


if __name__ == "__main__":
    main()
