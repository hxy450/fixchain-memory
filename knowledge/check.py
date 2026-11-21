# -*- coding: utf-8 -*-
r"""Check knowledge files against knowledge/RULES.md (read only, no model call, writes nothing).

  python knowledge/check.py knowledge/lessons [--only <id 8 chars,…>] [--legacy-ok] [--app-name NAME …]

Per lesson-<id>.json in the dir (not recursive; _*.json skipped):
  - json parses; "lesson" equals the file name's id; the lesson is in this repository's memory/ (a lesson that the store
    has retired is listed, not an error, and its changes are not checked).
  - entries: a list; each entry has step, fact, scope, source, kind, origin as non-empty strings; kind is one of KINDS;
    at most MAX_ENTRIES entries.
  - source, fact, scope, code: no machine path (drive letter, a users directory, the local app-data directory) and no
    「file:line」 reference (x.ext:12, x.ext#L12, x.ext 第 12 行).
  - fact, scope: no migrated app's name (APP_NAMES plus every --app-name, case-insensitive). The names of held-out
    evaluation apps are not kept in this repository: pass them with --app-name.
  - changes: a list; each has where, before, after, basis, type (non-empty). Checked against this lesson's text (the text
    the shadow sees: cut at 「## 来源」/「## 同源经验」, no ID line, no topic link), exactly or with whitespace optional.
    In this repository the changes are published into the lessons (memory/ is exported from a store that carries them):
    a published change has its after in the text (when a later change's before lies inside it, the after as the later
    change left it) and its before nowhere outside the afters. A change not published yet (a new knowledge file) is
    listed, not an error, when its before is found exactly once (the prompt generator / render.py stop otherwise).
A file is old-format when it has no "lesson" key (the third version's files use "id") and none of its entries has a scope
key (a file with "lesson", or with some scopes, is checked as a new file). With --legacy-ok, in an old-format file these
are listed, not errors: the "id" key (it must still equal the file name), entries without scope,
more than MAX_ENTRIES entries, kind 「卡里验证」 (a kind of the third version). Everything else stays an error.
Exit 1 when there is any error (or an --only id has no file), else 0. Standard library only."""
import sys

sys.dont_write_bytecode = True
import argparse, json, re  # noqa: E401,E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "memory"                 # read only
STORE = ROOT / "store"                # read only: only to tell a retired lesson from a missing one
KINDS = ("鸿蒙接口", "安卓平台", "依赖库")
LEGACY_KINDS = ("卡里验证",)
MAX_ENTRIES = 6
ENTRY_KEYS = ("step", "fact", "scope", "source", "kind", "origin")
CHANGE_KEYS = ("where", "before", "after", "basis", "type")
TEXT_FIELDS = ("source", "fact", "scope", "code")
NAME_FIELDS = ("fact", "scope")
# migrated apps (add here, or pass --app-name). Short names are matched as whole words; the rest as substrings, case-insensitive.
APP_NAMES = ["cofi", "gameoflife", "game of life", "antennapod"]
MACHINE_RX = [("盘符路径", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")),
              ("Users 目录", re.compile(r"(?i)(?<![A-Za-z0-9])users[\\/]")),
              ("AppData", re.compile(r"(?i)appdata"))]
FILE_EXT = "java|kt|kts|xml|ets|ts|js|mjs|json5?|md|py|gradle|properties|txt|c|cc|cpp|h|hpp|aidl|smali|ya?ml|html?|css"
LINE_RX = re.compile(rf"(?i)[\w$-]+\.(?:{FILE_EXT})\s*(?:[:：]\s*\d+(?![\w.])|#L\d+|[（(]?\s*第\s*\d+\s*行)")
SRC_RX = re.compile(r"\n## (?:来源|同源经验)")
ID_RX = re.compile(r"^lesson-[0-9a-f]{20}$")


def app_rx(name):
    e = re.escape(name)
    return re.compile(rf"(?i)(?<![a-z0-9]){e}(?![a-z0-9])" if len(name) < 6 else rf"(?i){e}")


def lib_text(path):
    """The lesson text as the prompt generator / knowledge/render.py takes it."""
    t = SRC_RX.split(path.read_text(encoding="utf-8"), maxsplit=1)[0]
    t = re.sub(r"(?m)^\[本主题\]\(index\.md\)\n\n?", "", t)
    t = re.sub(r"(?m)^ID：`lesson-[0-9a-f]+`.*\n\n?", "", t)
    return "\n" + t.strip() + "\n"


def store_status():
    try:
        head = json.loads((STORE / "HEAD.json").read_text(encoding="utf-8"))["revision"]
        snap = json.loads((STORE / "snapshots" / f"{head}.json").read_text(encoding="utf-8"))
        return {k: v.get("status") for k, v in snap["lessons"].items()}
    except (OSError, KeyError, ValueError):
        return {}


def loose(s):
    parts = [re.escape(x) for x in re.split(r"\s+", s.strip()) if x]
    return re.compile(r"\s*".join(parts))


def found(text, before):
    """-> number of places the sentence is found (exactly, else with whitespace optional)."""
    n = text.count(before)
    return n if n else len(list(loose(before).finditer(text)))


def nonempty(v):
    return isinstance(v, str) and v.strip() != ""


def check_file(f, lib, legacy_ok, app_rx_list, status):
    """-> (errors, legacy notes, info)."""
    err, leg = [], []
    stem = f.stem
    if not ID_RX.match(stem):
        return [f"文件名不是 lesson-<20 位十六进制>.json"], [], {}
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"json 解析不了：{e}"], [], {}
    if not isinstance(d, dict):
        return ["顶层不是对象"], [], {}
    entries, changes = d.get("entries"), d.get("changes")
    if not isinstance(entries, list):
        err.append("entries 不是列表（或缺）")
        entries = []
    if changes is None:
        changes = []
    elif not isinstance(changes, list):
        err.append("changes 不是列表")
        changes = []
    old = "lesson" not in d and not any(isinstance(e, dict) and "scope" in e for e in entries)

    def soft(msg):
        (leg if (legacy_ok and old) else err).append(msg)
    if "lesson" in d:
        if d["lesson"] != stem:
            err.append(f"lesson 「{d['lesson']}」和文件名不一致")
    elif d.get("id") == stem:
        soft("用的是 id 键，不是 lesson")
    else:
        err.append("缺 lesson 键（id 也和文件名不一致）")
    retired = stem not in lib and status.get(stem) == "retired"
    if retired:
        leg.append("store 里已退役：memory/ 里没有，改句不核")
    elif stem not in lib:
        err.append("memory/ 里没有这条经验")
    if len(entries) > MAX_ENTRIES:
        soft(f"entries {len(entries)} 条，超过 {MAX_ENTRIES} 条")
    no_scope = 0
    for k, e in enumerate(entries, 1):
        if not isinstance(e, dict):
            err.append(f"第 {k} 条不是对象")
            continue
        for key in ENTRY_KEYS:
            if key == "scope" and "scope" not in e and legacy_ok and old:
                no_scope += 1                    # listed once per file below
                continue
            if not nonempty(e.get(key)):
                err.append(f"第 {k} 条 {key} 缺或为空")
        kind = e.get("kind")
        if nonempty(kind) and kind not in KINDS:
            if kind in LEGACY_KINDS:
                soft(f"第 {k} 条 kind 「{kind}」（第三版的类别）")
            else:
                err.append(f"第 {k} 条 kind 「{kind}」不是 {' / '.join(KINDS)} 之一")
        for fld in TEXT_FIELDS:
            v = e.get(fld)
            if not isinstance(v, str):
                continue
            for what, rx in MACHINE_RX:
                m = rx.search(v)
                if m:
                    err.append(f"第 {k} 条 {fld} 有本机路径（{what}）：…{v[max(0, m.start() - 15):m.end() + 25]}…")
            refs = [m.group(0) for m in LINE_RX.finditer(v)]
            if refs:
                err.append(f"第 {k} 条 {fld} 有「文件:行号」引用：{'、'.join(refs)}")
        for fld in NAME_FIELDS:
            v = e.get(fld)
            if isinstance(v, str):
                hits = [n for n, rx in app_rx_list if rx.search(v)]
                if hits:
                    err.append(f"第 {k} 条 {fld} 有被迁移应用的名字：{'、'.join(hits)}")
    if no_scope:
        leg.append(f"{no_scope} / {len(entries)} 条没有 scope")
    text = lib_text(lib[stem]) if stem in lib else None
    pairs = [((c.get("before") or "").strip(), (c.get("after") or "").strip()) if isinstance(c, dict) else ("", "") for c in changes]
    eff = []
    for k, (_, a) in enumerate(pairs):
        for b2, a2 in pairs[k + 1:]:
            if b2 and b2 in a:
                a = a.replace(b2, a2, 1)
        eff.append(a)
    masked = text
    if text is not None:
        for a in sorted((x for x in eff if x), key=len, reverse=True):
            masked = loose(a).sub("\u0000", masked)
    for k, c in enumerate(changes, 1):
        if not isinstance(c, dict):
            err.append(f"改句第 {k} 处不是对象")
            continue
        miss = [key for key in CHANGE_KEYS if not nonempty(c.get(key))]
        if miss:
            err.append(f"改句第 {k} 处〔{c.get('where')}〕缺 {'、'.join(miss)}")
        b, a = pairs[k - 1]
        if b and a and text is not None:
            if found(text, eff[k - 1]):                  # published: the after is there, the before is gone
                n = found(masked, b)
                if n:
                    err.append(f"改句第 {k} 处〔{c.get('where')}〕after 已在正文里，before 在 after 之外却还出现 {n} 处：{b[:50]}…")
                continue
            n = found(text, b)                           # not published yet: the before must be found exactly once
            if n == 1:
                leg.append(f"改句第 {k} 处〔{c.get('where')}〕还没发布进正文（before 唯一可定位）")
            elif n == 0:
                err.append(f"改句第 {k} 处〔{c.get('where')}〕after 不在正文里，before 也找不到：{b[:50]}…")
            else:
                err.append(f"改句第 {k} 处〔{c.get('where')}〕after 不在正文里，before 出现 {n} 处（要能唯一定位）：{b[:50]}…")
    return err, leg, {"entries": len(entries), "changes": len(changes), "old_format": old}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="the knowledge dir (lesson-<id>.json files), e.g. knowledge/lessons")
    ap.add_argument("--only", default="", help="comma-separated 8-character id prefixes")
    ap.add_argument("--legacy-ok", action="store_true", help="old-format files: list their old-format items, not as errors")
    ap.add_argument("--app-name", action="append", default=[], help="one more app name to keep out of fact / scope (repeatable)")
    a = ap.parse_args()
    d = Path(a.dir)
    if not d.is_dir():
        print(f"不是目录：{d}")
        return 2
    app_rx_list = [(n, app_rx(n)) for n in APP_NAMES + [x.strip() for x in a.app_name if x.strip()]]
    only = [x.strip().replace("lesson-", "")[:8] for x in a.only.split(",") if x.strip()]
    files = sorted(f for f in d.glob("lesson-*.json"))
    if only:
        files = [f for f in files if f.stem[7:15] in only]
    lib = {p.name[:-len(".lesson.md")]: p for p in LIB.rglob("lesson-*.lesson.md")}
    status = store_status()
    n_err, n_leg, n_old = 0, 0, 0
    print(f"目录 {d}；{len(files)} 个文件" + (f"（--only {','.join(only)}）" if only else "") + ("；--legacy-ok" if a.legacy_ok else "")
          + f"；应用名 {len(app_rx_list)} 个")
    for x in only:
        if not any(f.stem[7:15] == x for f in files):
            print(f"  {x}｜错误｜目录里没有这条经验的文件")
            n_err += 1
    for f in files:
        err, leg, info = check_file(f, lib, a.legacy_ok, app_rx_list, status)
        n_err += len(err)
        n_leg += len(leg)
        n_old += bool(info.get("old_format"))
        status_word = "有错" if err else ("只列出" if leg else "通过")
        print(f"{f.stem[7:15]}｜{status_word}｜条目 {info.get('entries', '?')}、改句 {info.get('changes', '?')}")
        for x in err:
            print(f"    错误：{x}")
        for x in leg:
            print(f"    列出：{x}")
    print(f"\n合计：{len(files)} 个文件，错误 {n_err} 处，只列出 {n_leg} 处（旧格式文件 {n_old} 个）。" + ("通过" if not n_err else "不通过"))
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
