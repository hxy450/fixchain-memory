# -*- coding: utf-8 -*-
r"""把知识文件里还没发布的改句写成一份 memory.py apply --plan 认的提案（不调模型；只读 store 和知识文件，只写 --out）。

对象：HEAD 快照里 active、知识文件里有未发布改句的经验（给了 --lessons 就只看这几条）。
  - 「未发布」的判法用同目录 render.py 的 published：把这条经验的字段按 memory.py export 的版式排成正文（「# 标题」、
    「## 何时使用」、「## 适用情境」、「## 例外与边界」的「- 」各项、「## 原因」、「## 做法」的「1. 」各步、「## 可选检查」），
    依次看每处改句；已发布的（新句在、原句不在新句之外出现）跳过。按版式而不按字段判，是因为早先并入的知识文件里有
    「新开一节」（原句「## 原因」）和「列表追加」（新句里带「\n- 」）两种写法，它们发布以后只在版式里认得出来。
  - 其余每处：原句（去首尾空白）在这条经验的各字段里合起来恰好出现一处 → 在那个字段里换成新句（后一处改句对着前一处
    换过的字段找）；否则记下（经验号、第几处、原句前 40 字、出现几处）。落在 how、unless、check 某一项里、新句却带换行的
    也记下（一项拆成几项搬不回提案，rules.md U2）。有一处记下的，整份提案不写。
  - 提案：{"base_revision": HEAD, "upsert": [每条经验 HEAD 里的全部字段（不含 version），套上改句], "retire": []}；
    evidence、requires、topic、status 原样。
之后照维护流程 apply、lint、export --link-cards（knowledge/skill/references/tools.md 第 7 节）。

用法：
  py -3.12 -B -X utf8 publish_plan.py --store S --knowledge K --out PLAN.json [--lessons ID …]
K 是仓库的 knowledge/（下有 lessons/）。ID 可写 8 位以上前缀，lesson- 可省。
退出码：0 = 写好了提案，或没有未发布的改句（打印「无」、不写文件）；1 = 有原句对不上（列出、不写文件）；2 = 参数或 store 读不了。"""
import sys

sys.dont_write_bytecode = True
import argparse, copy, glob, io, json, os  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R  # noqa: E402  判「已发布」用它的 published，不另写一套

KEYS = ("id", "title", "topic", "when", "description", "unless", "why", "how", "check", "evidence", "requires", "status")
TEXT = ("title", "when", "description", "why")
LISTS = ("how", "unless", "check")


def load_json(p):
    return json.load(io.open(p, encoding="utf-8"))


def slots(v):
    out = [(k, None) for k in TEXT if isinstance(v.get(k), str)]
    for k in LISTS:
        if isinstance(v.get(k), list):
            out += [(k, j) for j, x in enumerate(v[k]) if isinstance(x, str)]
    return out


def get(v, k, j):
    return v[k] if j is None else v[k][j]


def body_md(v):
    """经验正文的版式（memory.py export 的 _lesson_text，到「## 可选检查」为止），只用来判改句是否已发布。"""
    lines = [f"# {v.get('title', '')}", "", "## 何时使用", "", v.get("when", ""), ""]
    if v.get("description"):
        lines += ["## 适用情境", "", v["description"], ""]
    if v.get("unless"):
        lines += ["## 例外与边界", "", *[f"- {x}" for x in v["unless"]], ""]
    lines += ["## 原因", "", v.get("why", ""), "", "## 做法", "", *[f"{i}. {x}" for i, x in enumerate(v.get("how") or [], 1)], ""]
    if v.get("check"):
        lines += ["## 可选检查", "", *[f"- {x}" for x in v["check"]], ""]
    return "\n".join(lines)


def publish_one(L, d):
    """-> (套好的字段或 None, 套上的处数, 问题列表)。"""
    v = {k: copy.deepcopy(L[k]) for k in KEYS if k in L}
    lid, n, problems = L["id"], 0, []
    for i, c in enumerate(d.get("changes") or [], 1):
        b, a = (c.get("before") or "").strip(), (c.get("after") or "").strip()
        if not b or not a:
            problems.append((lid, i, b[:40], "缺原句或新句"))
            continue
        if R.published(body_md(v), b, a):
            continue
        sl = slots(v)
        tot = sum(get(v, k, j).count(b) for k, j in sl)
        hit = [(k, j) for k, j in sl if get(v, k, j).count(b)]
        if tot != 1:
            problems.append((lid, i, b[:40], f"在各字段里出现 {tot} 处"))
            continue
        k, j = hit[0]
        if j is not None and "\n" in a:
            problems.append((lid, i, b[:40], f"落在 {k} 第 {j + 1} 项里，新句带换行"))
            continue
        if j is None:
            v[k] = v[k].replace(b, a)
        else:
            v[k][j] = v[k][j].replace(b, a)
        n += 1
    return (v if n else None), n, problems


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument("--store", required=True)
    ap.add_argument("--knowledge", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lessons", nargs="+")
    a = ap.parse_args(argv)
    try:
        head = load_json(os.path.join(a.store, "HEAD.json"))["revision"]
        lessons = load_json(os.path.join(a.store, "snapshots", head + ".json"))["lessons"]
    except (OSError, KeyError, ValueError) as e:
        print(f"publish_plan.py：读不了 store：{e}", file=sys.stderr)
        return 2
    if a.lessons:
        ids = []
        for x in a.lessons:
            x = x.strip().lower()
            x = x if x.startswith("lesson-") else "lesson-" + x
            hit = [k for k in lessons if k.startswith(x)]
            if len(x) < 15 or len(hit) != 1:
                print(f"publish_plan.py：--lessons {x} 要 8 位以上的前缀，在 HEAD 里对上 {len(hit)} 条", file=sys.stderr)
                return 2
            ids.append(hit[0])
        ids = list(dict.fromkeys(ids))
    else:
        ids = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(a.knowledge, "lessons", "lesson-*.json")))
    ups, problems, counts, skipped = [], [], [], []
    for lid in ids:
        L = lessons.get(lid)
        p = os.path.join(a.knowledge, "lessons", lid + ".json")
        if not L or L.get("status") != "active":
            if a.lessons:
                skipped.append(f"{lid[7:15]}（{'store 里没有' if not L else L.get('status')}）")
            continue
        if not os.path.exists(p):
            if a.lessons:
                skipped.append(f"{lid[7:15]}（没有知识文件）")
            continue
        v, n, pr = publish_one(L, load_json(p))
        problems += pr
        if v is not None:
            ups.append(v)
            counts.append(f"{lid[7:15]} {n}")
    if skipped:
        print("不做的：" + "、".join(skipped))
    if problems:
        print(f"原句对不上 {len(problems)} 处，不写提案：")
        for lid, i, b, why in problems:
            print(f"  {lid[7:15]} 第 {i} 处：{why}：{b}…")
        return 1
    if not ups:
        print(f"无：{len(ids)} 个对象里没有未发布的改句，不写提案（store HEAD {head[:8]}）")
        return 0
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"base_revision": head, "upsert": ups, "retire": []}, f, ensure_ascii=False, indent=2)
    print(f"提案写到 {a.out}：base {head[:8]}，{len(ups)} 条经验、{sum(int(x.split()[1]) for x in counts)} 处改句"
          f"（{'、'.join(counts)}）；接着 apply、lint、export --link-cards")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
