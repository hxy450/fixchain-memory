# -*- coding: utf-8 -*-
r"""归并时知识这一步的三件机械事（不调模型；只用标准库；plan、check 只读，readme 只改 README 的覆盖表那一段）。

  plan    对照归并开始时的 store 版本（--base）和现在的 HEAD，把有变化的经验分成四类，列出每条现有知识文件的格式和该做什么：
            新增      base 里没有，或 base 里不是 active、现在是 active                  → 整条做
            正文改了  title、when、description、unless、why、how、check 任一不同          → 没有知识文件或旧格式：整条做；
                                                                                         新格式：只做新句和新卡
            只补来源  只有 evidence、requires 或 topic 不同（topic 变了的另标「换了目录」）→ 默认不动
            退役      现在是 retired                                                     → 不做
          现在既不是 active 也不是 retired（candidate、disputed）的，照分类列出，该做什么写「不做（状态 …）」。
          知识文件的格式：没有 / 旧格式（sdk 里没有 docs_commit）/ 新格式（列出 sdk.verified_on）。
  check   门槛：对象是 plan 里新增和正文改了、现在 active 的经验（给了 --lessons 就只看这几条，入口 ② 用）。逐条核：
            知识文件在、新格式、sdk.verified_on 不早于 --since（默认 = base 之后第一个快照 created_at 的本地日期）；
            没有未发布的改句（判法用同目录 render.py 的 published / apply_changes：依次看每处，已发布的不算，
            其余都算未发布）；对这些文件跑同目录 check.py --require-new --memory M 加透传的选项，退出码 0；
            K 的上一级 shadow/exclude.json 里每个经验号在 HEAD 快照里、且 active（没有这个文件就不核、写明）。
          全过退出码 0，否则 1。输出几行结论，可以直接贴进 REPORT.md。
  readme  重生成 <repo>/knowledge/README.md 里逐条覆盖表（表头「| id | 主题 | 规则 | …」下面的 `| \`lesson-…\` |` 各行），
          只动这一段：每个知识文件一行，按（主题路径，经验号）排；只列 HEAD 里 active、memory/ 里有的经验，其余的在
          标准输出列出（不进表）。表外的数字和说明不改，要手改的照打印的提示。

用法（K = 仓库的 knowledge/，M = 一份导出的 memory/）：
  py -3.12 -B -X utf8 gate.py plan  --store S --base REV --knowledge K [--json]
  py -3.12 -B -X utf8 gate.py check --store S --base REV --knowledge K --memory M [--since YYYY-MM-DD] [--lessons ID …]
                                    [透传给 check.py 的选项：--docs D --app-name N … --sources --oh-ets … 等]
  py -3.12 -B -X utf8 gate.py readme --repo R
REV、ID 可以写 8 位以上的前缀（ID 前面的 lesson- 可省）。
退出码：plan 0（参数或 store 读不了时 2）；check 0 = 门槛全过、1 = 有没过的、2 = 参数或 store 读不了；
readme 0 = 写好了（或本来就一样）、1 = 表找不到或有知识文件对不上经验、2 = 参数错。"""
import sys

sys.dont_write_bytecode = True
import argparse, datetime, glob, io, json, os, re, subprocess  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R  # noqa: E402  判「已发布」、套改句、取正文都用它，不另写一套

BODY = ("title", "when", "description", "unless", "why", "how", "check")
SOURCE = ("evidence", "requires", "topic")
NEW, CHANGED, SOURCE_ONLY, RETIRED = "新增", "正文改了", "只补来源", "退役"
ORDER = (NEW, CHANGED, SOURCE_ONLY, RETIRED)
TABLE_HEAD = "| id | 主题 | 规则 | 条目（带成立范围） | 改句（已进正文） | 标题 |"
ROW_RX = re.compile(r"^\| `lesson-[0-9a-f]+` \|")


class Fail(Exception):
    pass


# ---------------------------------------------------------------- store
def load_json(p):
    return json.load(io.open(p, encoding="utf-8"))


def head_rev(store):
    try:
        return load_json(os.path.join(store, "HEAD.json"))["revision"]
    except (OSError, KeyError, ValueError) as e:
        raise Fail(f"读不了 {store}/HEAD.json：{e}")


def resolve(store, rev):
    rev = (rev or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{8,64}", rev):
        raise Fail(f"版本号要写 8 位以上的十六进制前缀：{rev}")
    hits = [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(store, "snapshots", rev + "*.json"))]
    if len(hits) != 1:
        raise Fail(f"{rev} 在 {store}/snapshots 里对上 {len(hits)} 个快照")
    return hits[0]


def snapshot(store, rev):
    try:
        return load_json(os.path.join(store, "snapshots", rev + ".json"))
    except (OSError, ValueError) as e:
        raise Fail(f"读不了快照 {rev[:8]}：{e}")


def local_date(stamp):
    """快照 created_at（UTC 的 ISO 时间）→ 本机时区的日期。核实日期是人按本地日期写的，UTC 日期可能晚一天。"""
    t = datetime.datetime.fromisoformat(stamp)
    if t.tzinfo is None:
        t = t.replace(tzinfo=datetime.timezone.utc)
    return t.astimezone().date().isoformat()


def first_after(store, head, base):
    """从 HEAD 顺着 parent 往回走，返回 parent 是 base 的那个快照（base 之后第一个）；HEAD 就是 base 时返回 None。"""
    rev, seen = head, set()
    while rev and rev != base and rev not in seen:
        seen.add(rev)
        s = snapshot(store, rev)
        if s.get("parent") == base:
            return s
        rev = s.get("parent")
    if rev == base and head == base:
        return None
    raise Fail(f"base {base[:8]} 不在 HEAD {head[:8]} 的 parent 链上")


# ---------------------------------------------------------------- 知识文件
def kfile(K, lid):
    return os.path.join(K, "lessons", lid + ".json")


def kstate(K, lid):
    """-> (状态文字, 知识文件内容或 None)。新格式 = sdk 里有 docs_commit。"""
    p = kfile(K, lid)
    if not os.path.exists(p):
        return "没有", None
    try:
        d = load_json(p)
    except (OSError, ValueError) as e:
        return f"读不了（{e}）", None
    sdk = d.get("sdk") if isinstance(d.get("sdk"), dict) else {}
    if not sdk.get("docs_commit"):
        return "旧格式", d
    return f"新格式 {sdk.get('verified_on') or '（没写 verified_on）'}", d


def is_new(d):
    return isinstance(d, dict) and isinstance(d.get("sdk"), dict) and bool(d["sdk"].get("docs_commit"))


# ---------------------------------------------------------------- plan
def classify(base, head):
    """-> [{id, kind, status, fields, moved}]，按 ORDER、经验号排。"""
    bl, hl = base.get("lessons") or {}, head.get("lessons") or {}
    out = []
    for lid in sorted(hl):
        h, b = hl[lid], bl.get(lid)
        st = h.get("status")
        if st == "retired":
            if b is not None and b.get("status") == "retired":
                continue
            out.append({"id": lid, "kind": RETIRED, "status": st, "fields": [], "moved": False})
            continue
        if b is None or (st == "active" and b.get("status") != "active"):
            out.append({"id": lid, "kind": NEW, "status": st, "fields": [], "moved": False})
            continue
        body = [k for k in BODY if h.get(k) != b.get(k)]
        src = [k for k in SOURCE if h.get(k) != b.get(k)]
        if body:
            out.append({"id": lid, "kind": CHANGED, "status": st, "fields": body + src, "moved": "topic" in src})
        elif src:
            out.append({"id": lid, "kind": SOURCE_ONLY, "status": st, "fields": src, "moved": "topic" in src})
        elif b.get("status") != st:
            out.append({"id": lid, "kind": CHANGED, "status": st, "fields": ["status"], "moved": False})
    return sorted(out, key=lambda r: (ORDER.index(r["kind"]), r["id"]))


def todo(row, ks):
    if row["kind"] == RETIRED:
        return "不做"
    if row["status"] != "active":
        return f"不做（状态 {row['status']}）"
    if row["kind"] == NEW:
        return "整条做"
    if row["kind"] == CHANGED:
        return "只做新句和新卡" if ks.startswith("新格式") else "整条做"
    return "默认不动（新卡和已有条目冲突或补出成立条件的，按入口 ① 的 2 做）"


def make_plan(a):
    head = head_rev(a.store)
    base = resolve(a.store, a.base)
    hs, bs = snapshot(a.store, head), snapshot(a.store, base)
    rows = classify(bs, hs)
    for r in rows:
        ks, _ = kstate(a.knowledge, r["id"])
        r["knowledge"] = ks
        r["todo"] = todo(r, ks)
        r["title"] = (hs["lessons"][r["id"]].get("title") or "")
    return head, base, rows


def cmd_plan(a):
    head, base, rows = make_plan(a)
    count = {k: sum(1 for r in rows if r["kind"] == k) for k in ORDER}
    if a.json:
        print(json.dumps({"store_head": head, "base": base, "counts": count, "lessons": rows}, ensure_ascii=False, indent=1))
        return 0
    print(f"store HEAD {head[:8]}，base {base[:8]}：" + "，".join(f"{k} {n}" for k, n in count.items()))
    if not rows:
        print("（两个版本之间没有经验变化）")
        return 0
    print("| 类别 | 经验 | 变了的栏 | 知识文件 | 该做什么 | 标题 |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        f = "、".join(r["fields"]) + ("（换了目录）" if r["moved"] else "")
        t = r["title"] if len(r["title"]) <= 30 else r["title"][:30] + "…"
        print(f"| {r['kind']} | `{r['id'][7:15]}` | {f or '—'} | {r['knowledge']} | {r['todo']} | {t} |")
    return 0


# ---------------------------------------------------------------- check
def lesson_ids(snap, ids):
    out = []
    for x in ids:
        x = x.strip().lower()
        x = x if x.startswith("lesson-") else "lesson-" + x
        hit = [k for k in snap["lessons"] if k.startswith(x)]
        if len(x) < 15 or len(hit) != 1:
            raise Fail(f"--lessons {x}：要 8 位以上的前缀，在 HEAD 里对上 {len(hit)} 条")
        out.append(hit[0])
    return list(dict.fromkeys(out))


def unpublished(text, changes, lid):
    """依次看每处改句：render.published 认已发布的不算；其余算未发布，并像 render.py 一样套上再看下一处。"""
    n, problems = 0, []
    for c in changes:
        b, a = (c.get("before") or "").strip(), (c.get("after") or "").strip()
        if b and a and R.published(text, b, a):
            continue
        n += 1
        text, _, p = R.apply_changes(text, [c], lid)
        problems += p
    return n, problems


def cmd_check(a, passthrough):
    head = head_rev(a.store)
    base = resolve(a.store, a.base)
    hs = snapshot(a.store, head)
    lines, bad = [], []
    if a.lessons:
        targets = lesson_ids(hs, a.lessons)
        origin = f"--lessons 给的 {len(targets)} 条"
    else:
        _, _, rows = make_plan(a)
        targets = [r["id"] for r in rows if r["kind"] in (NEW, CHANGED) and r["status"] == "active"]
        nn = sum(1 for r in rows if r["kind"] == NEW and r["status"] == "active")
        origin = f"新增和正文改了的 active 经验 {len(targets)} 条（新增 {nn}、正文改了 {len(targets) - nn}）"
    since = a.since
    if since and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", since):
        raise Fail("--since 要写 YYYY-MM-DD")
    if not since:
        s = first_after(a.store, head, base)
        since = local_date(s["created_at"]) if s and s.get("created_at") else None
    lines.append(f"gate check：store HEAD `{head[:8]}`，base `{base[:8]}`；对象是{origin}；"
                 + (f"核实日期不早于 {since}" if since else "base 就是 HEAD、没给 --since，核实日期不核"))
    # 1 知识文件在、新格式、核实日期
    files, miss, old, early = [], [], [], []
    for lid in targets:
        if hs["lessons"][lid].get("status") != "active":
            bad.append(f"{lid[7:15]} 在 HEAD 里不是 active（{hs['lessons'][lid].get('status')}）")
        ks, d = kstate(a.knowledge, lid)
        if d is None:
            miss.append(f"{lid[7:15]}（{ks}）")
            continue
        files.append((lid, d))
        if not is_new(d):
            old.append(lid[7:15])
            continue
        v = (d.get("sdk") or {}).get("verified_on") or ""
        if since and not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) and v >= since):
            early.append(f"{lid[7:15]}（{v or '没写'}）")
    ok1 = not (miss or old or early)
    lines.append(f"- 知识文件：{len(targets) - len(miss)}/{len(targets)} 在，新格式 {len(files) - len(old)} 个"
                 + (f"，核实日期都不早于 {since}" if since and not early else "")
                 + ("" if ok1 else "；没过：" + "；".join(
                     x for x in (("没有知识文件 " + "、".join(miss)) if miss else "",
                                 ("旧格式 " + "、".join(old)) if old else "",
                                 ("核实日期早于 " + since + "：" + "、".join(early)) if early else "") if x)))
    if not ok1:
        bad.append("知识文件")
    # 2 未发布的改句（对着 --memory 的正文）
    lib = {os.path.basename(p).split(".")[0]: p
           for p in glob.glob(os.path.join(a.memory, "**", "lesson-*.lesson.md"), recursive=True)}
    if not lib:
        raise Fail(f"--memory {a.memory} 里没有 lesson-*.lesson.md（要给 export 的输出目录本身）")
    n_un, un_rows, nomem, probs = 0, [], [], []
    n_ch = 0
    for lid, d in files:
        p = lib.get(lid)
        if not p:
            nomem.append(lid[7:15])
            continue
        chs = d.get("changes") or []
        n_ch += len(chs)
        n, pr = unpublished(R.body(p), chs, lid)
        probs += pr
        if n:
            n_un += n
            un_rows.append(f"{lid[7:15]} {n} 处")
    ok2 = not (n_un or nomem)
    lines.append(f"- 未发布的改句：{n_un} 处（{len(files)} 个文件共 {n_ch} 处改句，对着 {a.memory} 的正文）"
                 + ("" if not un_rows else "：" + "、".join(un_rows) + "（照「并入经验库」第 2 步用 publish_plan.py 发布）")
                 + ("" if not nomem else "；memory 里没有：" + "、".join(nomem)))
    for x in probs:
        lines.append("  套不上：" + x)
    if not ok2:
        bad.append("未发布的改句")
    # 3 知识检查
    if files:
        cmd = [sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "check.py"),
               *[kfile(a.knowledge, lid) for lid, _ in files], "--require-new", "--memory", a.memory, *passthrough]
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        out = r.stdout.splitlines()
        summ = [x for x in out if re.match(r"^(\d+ 个知识文件|出处核对：|错误 \d+ 处|要人看的 \d+ 处)", x)]
        shown = " ".join(x.strip() for x in summ) or "（没有汇总行）"
        lines.append(f"- 知识检查（check.py --require-new --memory …{(' ' + ' '.join(passthrough)) if passthrough else ''}）："
                     f"退出码 {r.returncode}；{shown}")
        if r.returncode:
            bad.append("知识检查")
            errs = []
            take = False
            for x in out:
                if re.match(r"^错误 \d+ 处", x):
                    take = True
                    continue
                if re.match(r"^要人看的 \d+ 处", x):
                    take = False
                if take:
                    errs.append(x)
            for x in errs[:30]:
                lines.append("  " + x.strip())
            if len(errs) > 30:
                lines.append(f"  …另有 {len(errs) - 30} 处，单独跑 check.py 看全")
    else:
        lines.append("- 知识检查：没有要查的知识文件，没跑")
    # 4 shadow/exclude.json
    ex = os.path.join(os.path.dirname(os.path.abspath(a.knowledge)), "shadow", "exclude.json")
    if not os.path.exists(ex):
        lines.append("- shadow/exclude.json：库里没有，不核")
    else:
        try:
            ids = [x.get("id") for x in load_json(ex).get("lessons") or []]
        except (OSError, ValueError, AttributeError) as e:
            ids, err = None, str(e)
        if ids is None:
            lines.append(f"- shadow/exclude.json：读不了（{err}）")
            bad.append("exclude.json")
        else:
            wrong = []
            for x in ids:
                x = str(x or "")
                hit = [k for k in hs["lessons"] if k.startswith(x)] if len(x) >= 15 else []
                if len(hit) != 1:
                    wrong.append(f"{x[7:15] or x}（HEAD 里没有）")
                elif hs["lessons"][hit[0]].get("status") != "active":
                    wrong.append(f"{x[7:15]}（{hs['lessons'][hit[0]].get('status')}）")
            lines.append(f"- shadow/exclude.json：{len(ids)} 条，" + ("都在 HEAD 里且 active" if not wrong else
                                                                    "没过：" + "、".join(wrong)))
            if wrong:
                bad.append("exclude.json")
    bad = list(dict.fromkeys(bad))
    lines.append("结论：" + ("通过（退出码 0）" if not bad else "没过：" + "、".join(bad) + "（退出码 1）"))
    print("\n".join(lines))
    return 1 if bad else 0


# ---------------------------------------------------------------- readme
def rule_of(d):
    sdk = d.get("sdk") if isinstance(d.get("sdk"), dict) else {}
    if sdk.get("docs_date") or sdk.get("docs_commit"):      # 和仓库 knowledge/render.py 认新格式的判据相同
        return "新格式"
    return "第七版" if "lesson" in d else "第三版"


def trunc(t):
    return t if len(t) <= 34 else t[:34] + "…"


def cmd_readme(a):
    repo = a.repo
    P = os.path.join(repo, "knowledge", "README.md")
    raw = io.open(P, "rb").read()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    if lines.count(TABLE_HEAD) != 1:
        print(f"README 里表头「{TABLE_HEAD}」出现 {lines.count(TABLE_HEAD)} 次，不改")
        return 1
    i0 = lines.index(TABLE_HEAD)
    j = i0 + 2
    while j < len(lines) and ROW_RX.match(lines[j]):
        j += 1
    head = head_rev(os.path.join(repo, "store"))
    lessons = snapshot(os.path.join(repo, "store"), head)["lessons"]
    M = os.path.join(repo, "memory")
    paths = {}
    for p in glob.glob(os.path.join(M, "**", "lesson-*.lesson.md"), recursive=True):
        paths[os.path.basename(p)[:-len(".lesson.md")]] = (os.path.relpath(os.path.dirname(p), M).replace(os.sep, "/"), p)
    rows, skipped, unpub = [], [], []
    for f in sorted(glob.glob(os.path.join(repo, "knowledge", "lessons", "lesson-*.json"))):
        d = load_json(f)
        lid = d.get("id") or d.get("lesson") or os.path.basename(f)[:-5]
        L = lessons.get(lid)
        if not L or L.get("status") != "active" or lid not in paths:
            skipped.append(f"{lid[7:15]}（{'store 里没有' if not L else L.get('status') if L.get('status') != 'active' else 'memory 里没有'}）")
            continue
        topic, lp = paths[lid]
        ents = d.get("entries") or []
        nsc = sum(1 for e in ents if isinstance(e, dict) and (e.get("scope") or "").strip())
        chs = d.get("changes") or []
        if chs:
            n, _ = unpublished(R.body(lp), chs, lid)
            if n:
                unpub.append(f"{lid[7:15]} {n} 处")
            ch = f"{len(chs)}（{'是' if not n else '否'}）"
        else:
            ch = "0"
        rows.append(((topic, lid), f"| `{lid}` | {topic} | {rule_of(d)} | {len(ents)}（{nsc}） | {ch} | {trunc(L.get('title') or '')} |"))
    rows.sort()
    new_lines = lines[:i0 + 2] + [r for _, r in rows] + lines[j:]
    text = "\n".join(new_lines)
    out = (text.replace("\n", "\r\n") if crlf else text).encode("utf-8")
    same = out == raw
    if not same:
        io.open(P, "wb").write(out)
    print(f"覆盖表 {len(rows)} 行（原来 {j - i0 - 2} 行）：" + ("README 没变" if same else "已重写表那一段"))
    if unpub:
        print("改句还没发布进正文的（表里写「否」）：" + "、".join(unpub))
    if skipped:
        print("没进表的知识文件（经验不是 active 或 memory 里没有；README 里「退役经验的知识文件」那段要手改）：" + "、".join(skipped))
    if not same:
        print("表外的数字（知识文件数、条目总数、有条目的条数、并入记录）没改，照新表核一遍")
    return 1 if skipped else 0


# ---------------------------------------------------------------- main
def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", allow_abbrev=False)
    c = sub.add_parser("check", allow_abbrev=False)
    for x in (p, c):
        x.add_argument("--store", required=True)
        x.add_argument("--base", required=True)
        x.add_argument("--knowledge", required=True, help="仓库的 knowledge/（下有 lessons/）")
    p.add_argument("--json", action="store_true")
    c.add_argument("--memory", required=True, help="最新版本的一份导出的 memory/")
    c.add_argument("--since")
    c.add_argument("--lessons", nargs="+")
    r = sub.add_parser("readme", allow_abbrev=False)
    r.add_argument("--repo", required=True)
    a, rest = ap.parse_known_args(argv)
    if rest and a.cmd != "check":
        ap.error("不认识的参数：" + " ".join(rest))
    try:
        if a.cmd == "plan":
            return cmd_plan(a)
        if a.cmd == "check":
            return cmd_check(a, rest)
        return cmd_readme(a)
    except Fail as e:
        print("gate.py：" + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
