# -*- coding: utf-8 -*-
"""一次性的迁移：把候选和规矩里 refs 的 where 从本机绝对路径改写成可移植的定位（写法见 sources.py 的说明）。

  鸿蒙 SDK   …/sdk/default/openharmony/ets/…  →  openharmony/ets/…（hms 同理）
  Android SDK …/Android/Sdk/platforms/android-36/…  →  platforms/android-36/…（sources/… 同理）
  文档副本   …/work/ohdocs/zh-cn/application-dev/…  →  zh-cn/application-dev/…
  依赖库     …/.gradle/caches/…/transformed/<artifact>-<version>/<包内路径>  →  <group>:<artifact>:<version> <包内路径>，
             坐标按内容认：在 Gradle 缓存 modules-2 里找 artifact、version 对得上、且包内这个文件和 transforms 里的一字不差的 aar；
             version 栏统一写成「<group>:<artifact> <version>」。
路径后面的符号名、小节名原样保留；路径里的 \\ 换成 /。每改一条都用新写法解析一遍（sources.resolve），解析出的文件内容要和
原来那个本机文件一样（去掉空白比），对不上的不改。认不出来源、坐标认不出或认出不止一个的，原样留着，列进报告。
用法： py -3 -X utf8 skills/memory-rules/scripts/migrate_refs.py <目录或文件…> [--dry-run] [--report 报告.json]
  目录里的 case-*.json、rule-*.json 都改（examples/ 也一样）。--dry-run 只出报告，不写文件。"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, json, os, re, zipfile  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources as S  # noqa: E402

FALLBACK = {      # 本机根目录没配、或路径不在配的根目录下时，按目录的样子认
    "harmony-dts": re.compile(r"(?i)^.*?[\\/]sdk[\\/]default[\\/]((?:openharmony|hms)[\\/].*)$"),
    "android-sdk": re.compile(r"(?i)^.*?[\\/]Android[\\/]Sdk[\\/]((?:platforms|sources|build-tools|platform-tools|extras)[\\/].*)$"),
    "oh-docs": re.compile(r"(?i)^.*?[\\/]ohdocs[\\/]((?:zh-cn|en)[\\/].*)$"),
}
LIB = re.compile(r"(?i)^(?P<caches>.*?[\\/]caches)[\\/].*?[\\/]transformed[\\/](?P<name>[^\\/]+)[\\/](?P<inner>.*)$")


def norm(s):
    return re.sub(r"\s+", "", s or "")


def local_path(w):
    """old 写法：where 开头的本机文件路径（以已知扩展名结尾、确实存在的最长前缀）。"""
    ends = [m.end() for m in S.EXT.finditer(w)]
    for e in reversed(ends):
        if os.path.isfile(w[:e]):
            return w[:e]
    return None


_zips, _coord_cache = {}, {}


def zentry(p, inner):
    try:
        if p not in _zips:
            _zips[p] = zipfile.ZipFile(p)
        z = _zips[p]
        return z.read(inner).decode("utf-8", errors="replace") if inner in z.namelist() else None
    except (OSError, zipfile.BadZipFile):
        return None


def find_coord(caches, name, inner, content):
    """transformed 目录名 + 包内路径 + 文件内容 → [(group, artifact, version)]（内容一字不差的那些）。"""
    key = (caches, name, inner)
    if key in _coord_cache:
        return _coord_cache[key]
    m2 = os.path.join(caches, "modules-2", "files-2.1")
    splits = [(name[:m.start()], name[m.start() + 1:]) for m in re.finditer(r"-(?=\d)", name)]
    cands = []
    for g in (os.listdir(m2) if os.path.isdir(m2) else []):
        for art, ver in splits:
            if os.path.isdir(os.path.join(m2, g, art, ver)):
                cands.append((g, art, ver))
        if not splits:           # 目录名里没有版本号（如 navigation-common-release）：按名字前缀找所有版本
            base = re.sub(r"-release$", "", name)
            gd = os.path.join(m2, g)
            for art in os.listdir(gd) if os.path.isdir(gd) else []:
                if art == base or art.startswith(base + "-"):
                    for ver in os.listdir(os.path.join(gd, art)):
                        cands.append((g, art, ver))
    hit = []
    want = norm(content)
    for g, art, ver in cands:
        for p in glob.glob(os.path.join(m2, g, art, ver, "*", "*.aar")):
            t = zentry(p, inner)
            if t is not None and norm(t) == want:
                hit.append((g, art, ver))
                break
    _coord_cache[key] = hit
    return hit


def rel_under(root, path):
    if not root:
        return None
    a, b = os.path.normcase(os.path.abspath(root)), os.path.normcase(os.path.abspath(path))
    if b.startswith(a + os.sep):
        return os.path.abspath(path)[len(os.path.abspath(root)) + 1:].replace("\\", "/")
    return None


def migrate_ref(f, stats, bad, where_from):
    w = (f.get("where") or "").strip()
    kind = f.get("kind")
    if not S.is_absolute(w):
        stats["already"] += 1
        return False
    p = local_path(w)
    if not p:
        bad.append({"from": where_from, "kind": kind, "where": w[:200], "why": "找不到原来的本机文件"})
        return False
    tail = w[len(p):]
    old_text = io.open(p, encoding="utf-8", errors="replace").read()
    if kind == "android-lib":
        m = LIB.match(p)
        if not m:
            bad.append({"from": where_from, "kind": kind, "where": w[:200], "why": "不是 Gradle 缓存 transforms 里的文件"})
            return False
        inner = m.group("inner").replace("\\", "/")
        hits = find_coord(m.group("caches"), m.group("name"), inner, old_text)
        if len(hits) > 1 and len({(g, a_) for g, a_, _ in hits}) == 1:
            # 同一个构件的几个版本里这个文件一字不差：取最低的版本（引文在哪个版本里都一样）
            hits = sorted(hits, key=lambda h: [int(x) if x.isdigit() else x for x in re.split(r"[.\-]", h[2])])[:1]
            stats["lowest_version_chosen"] += 1
        if len(hits) != 1:
            bad.append({"from": where_from, "kind": kind, "where": w[:200],
                        "why": "Gradle 缓存 modules-2 里找不到内容一样的 aar" if not hits else f"认出不止一个坐标：{hits}"})
            return False
        g, a, v = hits[0]
        new = f"{g}:{a}:{v} {inner}{tail}"
        newver = f"{g}:{a} {v}"
    else:
        rk = S.KIND_ROOT.get(kind)
        rel = rel_under(S.roots().get(rk), p) if rk else None
        if rel is None and kind in FALLBACK:
            mm = FALLBACK[kind].match(p)
            rel = mm.group(1).replace("\\", "/") if mm else None
        if rel is None:
            bad.append({"from": where_from, "kind": kind, "where": w[:200], "why": "认不出属于哪个来源的根目录"})
            return False
        new = rel + tail
        newver = None
    state, text, _, _ = S.resolve(kind, new)
    if state != "ok" or norm(text) != norm(old_text):
        bad.append({"from": where_from, "kind": kind, "where": w[:200], "new": new[:200],
                    "why": f"新写法解析出来的文件和原来的不一样（{state}）"})
        return False
    f["where"] = new
    if newver and f.get("version") != newver:
        f["version"] = newver
        stats["version_rewritten"] += 1
    stats[kind] += 1
    return True


def refs_in(o):
    if isinstance(o.get("rules"), list):
        for i, r in enumerate(o["rules"], 1):
            for j, f in enumerate(r.get("refs") or [], 1):
                if isinstance(f, dict):
                    yield f"第 {i} 条 出处 {j}", f
    for j, f in enumerate(o.get("refs") or [], 1):
        if isinstance(f, dict):
            yield f"出处 {j}", f


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report")
    a = ap.parse_args()
    files = []
    for x in a.paths:
        files += sorted(glob.glob(os.path.join(x, "case-*.json")) + glob.glob(os.path.join(x, "rule-*.json"))) if os.path.isdir(x) else [x]
    stats, bad, changed_files = collections.Counter(), [], 0
    for p in files:
        raw = io.open(p, encoding="utf-8").read()
        o = json.loads(raw)
        ch = False
        for w, f in refs_in(o):
            stats["refs"] += 1
            ch |= migrate_ref(f, stats, bad, f"{os.path.basename(p)} {w}")
        if ch:
            changed_files += 1
            if not a.dry_run:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(json.dumps(o, ensure_ascii=False, indent=1) + "\n")
    rep = {"files": len(files), "files_changed": changed_files, "refs": stats["refs"], "already_portable": stats["already"],
           "rewritten": {k: v for k, v in stats.items() if k in S.KIND_ROOT}, "version_rewritten": stats["version_rewritten"],
           "not_rewritten": len(bad), "not_rewritten_by_reason": collections.Counter(b["why"].split("：")[0] for b in bad),
           "not_rewritten_list": bad, "roots": S.roots()}
    if a.report:
        with open(a.report, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
    print(f"文件 {len(files)} 个（改了 {changed_files} 个）；refs {stats['refs']} 条：已是可移植写法 {stats['already']}，"
          f"改写 {sum(rep['rewritten'].values())}（{rep['rewritten']}），依赖库的 version 改写 {stats['version_rewritten']}；"
          f"没改的 {len(bad)} 条 {dict(rep['not_rewritten_by_reason'])}" + ("（--dry-run，没写文件）" if a.dry_run else ""))
    for b in bad[:20]:
        print("  - ", b)


if __name__ == "__main__":
    main()
