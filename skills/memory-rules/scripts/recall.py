# -*- coding: utf-8 -*-
"""召回（docs/rules-v2-design.md 第 8 节）。粗筛不用模型、不用向量库：只靠 rules/keys.jsonl 和子代理的视野。

coarse  输入：产物种类（--product）、读过的文件或目录（--read，可多个）、交回的文件或目录（--wrote，可多个）。
        从这些文件里抽标识符当 query（整体词和拆开的部分都算，切法见 rulelib.ident_terms；读过的目录只取 --read-ext 的文件，
        交回的目录只取 --wrote-ext 的文件）。对同一产物的规矩打分：每条规矩的文档 = keys 两栏（--fields keys），或 keys 加
        标题和触发全文里的标识符（--fields keys+text）；IDF 在当前视图的同一产物规矩上算；得分 = query 与文档的 IDF 余弦。
        有 probe 的规矩在交回的文件里逐行搜它的正则，搜到的得分加 --probe-bonus，并列出命中的文件和行号。取前 --k 条，
        每条给出得分、命中的词（按贡献排，前 8 个）和 probe 命中。--query read 时只用读过的文件当 query（交回的文件仍用来搜 probe）。
        --level family：按族打分，族的文档 = 族的一行加族里所有规矩的 keys 两栏（标识符的整体词和部分词），IDF 在当前视图同一产物
        的族上算；输出前 --k 个族的短号、路径、族名、得分、命中的词和规矩条数。只当排序提示用。
        --products 代码,资源：几个产物各自打分后合在一起按得分取前 --k（不是各取 --k）；不写时只看 --product。
        --as-tree（隐含 --level family）：把入选的前 --k 个族按「产物 → 主题 → 族」排成一棵小树打印，格式和 show map 一样紧凑
        （主题一行带它的一行说明，下面是入选的族「短号 族名（条数）」），只含入选的族和它们所在的主题，不带得分和命中的词。
        --with-lines（隐含 --as-tree）：每个入选的族另起一行，下面带族的一行和每条规矩的一行（规矩号｜标题｜第一个触发），
        通用查法只写规矩号和标题（全文用 show <规矩号> 取）。
lines   把一批规矩号渲染成第三层的那一行。
body    取规矩正文（第四层 .md）。
show    一次打印多个索引节点或规矩正文，让审的 agent 少调用几次。节点写法：
          map                一页地图：各产物的 <产物目录>/map.md（每个主题一行，下面是「短号 族名（条数）」）；
          f017               族的短号：族名、族的一行、通用查法全文、每条规矩一行（规矩号｜标题｜第一个触发），不带链接；
          规矩号              规矩正文；
          index              顶层索引；<产物目录>/<主题…>、<产物目录>/<主题…>/<族目录>：那一层的 index.md
                             （前面带不带 rules/、后面带不带 /index.md 都行）。
        --products 代码,资源：只列这些产物（地图和顶层只出这些产物的部分，别的产物下的节点跳过）。
--rules <目录>：用另一份导出（默认分支根目录下的 rules/；在部署包的 scripts/ 里跑时默认就是部署包），keys.jsonl 取其中的。
body、show 取规矩正文时默认去掉来源一节的逐张明细（只留「来源：N 张卡，M 个应用」一行）；--with-sources 连明细一起给（给人看）。
部署包（build_index.py --deploy-out）的 keys.jsonl 不带来源，--exclude-apps、--cases-in 在那里用不了，视图要在建部署包时给。
视图（四个子命令都支持）：
  --exclude-apps A,B     去掉只出自这些应用的规矩（规矩的应用全在这个集合里）。
  --cases-in <前缀>       只用这个快照（store/snapshots/<前缀>*.json，要恰好一个）里已有的卡产出的规矩：规矩的 sources 全在
                          这个快照里（--cases-mode any 时只要有一张在）。
用法： py -3 -X utf8 skills/memory-rules/scripts/recall.py coarse --product 代码 --read <文件或目录…> --wrote <文件或目录…>
                [--k 30] [--fields keys|keys+text] [--query read|read+wrote] [--level rule|family] [--rules DIR] [--json]
       py -3 -X utf8 skills/memory-rules/scripts/recall.py coarse --level family --k 12 --as-tree [--with-lines] [--products 代码,资源]
                --read <…> --wrote <…>
       py -3 -X utf8 skills/memory-rules/scripts/recall.py lines <规矩号…> [--rules DIR]
       py -3 -X utf8 skills/memory-rules/scripts/recall.py body <规矩号…> [--rules DIR]
       py -3 -X utf8 skills/memory-rules/scripts/recall.py show map [--products 代码,资源] [--rules DIR]
       py -3 -X utf8 skills/memory-rules/scripts/recall.py show f017 f123 rule-… code/ui index [--products 代码,资源] [--rules DIR]"""
import sys

sys.dont_write_bytecode = True
import argparse, glob, io, json, os, re  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rulelib as L  # noqa: E402

READ_EXT = ".java,.kt,.xml,.gradle,.kts,.json,.json5,.properties,.txt,.md,.pro"
WROTE_EXT = ".ets,.ts,.json,.json5"
PRODUCT_NAMES = {v: k for k, v in L.PRODUCT_DIRS.items()}
MAP_WIDTH = 120          # 和 build_index.py 的地图一样的折行宽度


def load_index(p):
    with io.open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def view(rules, exclude_apps=None, cases_in=None, cases_mode="all"):
    out = rules
    if exclude_apps:
        ex = set(exclude_apps)
        out = [r for r in out if not (r.get("apps") and set(r["apps"]) <= ex)]
    if cases_in:
        hits = glob.glob(os.path.join(L.STORE, "snapshots", cases_in + "*.json"))
        if len(hits) != 1:
            raise SystemExit(f"--cases-in {cases_in}：快照要恰好一个，找到 {len(hits)} 个")
        cases = set(L.jload(hits[0])["cases"])
        test = all if cases_mode == "all" else any
        out = [r for r in out if r.get("sources") and test(c in cases for c in r["sources"])]
    return out


def files_of(paths, exts):
    exts = tuple(e.strip().lower() for e in exts.split(",") if e.strip())
    out = []
    for p in paths or []:
        if os.path.isdir(p):
            for root, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in ("build", "node_modules", "oh_modules", ".hvigor", ".git")]
                out += [os.path.join(root, f) for f in sorted(fs) if f.lower().endswith(exts)]
        elif os.path.isfile(p):
            out.append(p)
    return out


PROV = re.compile(r"^- case-[0-9A-Za-z]+（[^）\n]*）：.*(?:\n|$)", re.M)
WITH_SOURCES = False      # --with-sources：规矩正文连来源明细一起给（给人看时用）；默认只留「来源：N 张卡，M 个应用」那一行


def strip_sources(text):
    """去掉来源一节的逐张明细（库导出的规矩页带，给 agent 的输出默认不带）。"""
    return text if WITH_SOURCES else PROV.sub("", text)


def read_text(p):
    try:
        return io.open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def doc_terms(r, fields):
    k = r.get("keys") or {}
    t = L.ident_terms(" ".join(list(k.get("read") or []) + list(k.get("product") or [])))
    if fields == "keys+text":
        text = " ".join([r.get("title") or ""] + [(x.get("read") or "") + " " + (x.get("wrong") or "") for x in r.get("triggers") or []])
        t = L.merge_terms(t, L.ident_terms(text))
    return t


def probe_hits(r, wrote_files, cache):
    p = r.get("probe")
    if not isinstance(p, dict) or not p.get("pattern"):
        return []
    try:
        rx = re.compile(p["pattern"])
    except re.error:
        return []
    hits = []
    for f in wrote_files:
        if f not in cache:
            cache[f] = read_text(f).splitlines()
        for i, line in enumerate(cache[f], 1):
            if rx.search(line):
                hits.append(f"{f}:{i}")
                if len(hits) >= 5:
                    return hits
    return hits


def coarse(rules, product, read_texts, wrote_files, k=30, fields="keys", query="read+wrote", probe_bonus=0.3):
    """返回 [{rank, id, score, cosine, matched, probe, title, line}]（全部排好，按 k 截断前的完整名次也在 rank 里）。"""
    pool = [r for r in rules if r.get("product") == product]
    docs = [doc_terms(r, fields) for r in pool]
    idf, _ = L.idf_table(docs)
    texts = list(read_texts) + ([read_text(f) for f in wrote_files] if query == "read+wrote" else [])
    q = L.ident_terms("\n".join(texts))
    qv = L.vector(q, idf)
    cache, out = {}, []
    for r, d in zip(pool, docs):
        dv = L.vector(d, idf)
        cos = L.cosine(qv, dv)
        contrib = sorted(((qv[0][t] * x, t) for t, x in dv[0].items() if t in qv[0]), reverse=True)
        ph = probe_hits(r, wrote_files, cache)
        out.append({"id": r["id"], "score": round(cos + (probe_bonus if ph else 0.0), 4), "cosine": round(cos, 4),
                    "matched": [t for _, t in contrib[:8]], "probe": ph, "title": r.get("title"), "line": r.get("line")})
    out.sort(key=lambda x: (-x["score"], x["id"]))
    for i, x in enumerate(out, 1):
        x["rank"] = i
    return out[:k] if k else out


def coarse_families(rules, product, read_texts, wrote_files, k=10, query="read+wrote"):
    """按族打分：[{rank, family_dir, name, score, matched, rules}]。"""
    by = {}
    for r in rules:
        if r.get("product") != product or not r.get("family_dir"):
            continue
        f = by.setdefault(r["family_dir"], {"name": r.get("family_name") or "", "line": r.get("family_line") or "", "keys": [], "n": 0,
                                            "short": r.get("family_short") or ""})
        kk = r.get("keys") or {}
        f["keys"] += list(kk.get("read") or []) + list(kk.get("product") or [])
        f["n"] += 1
    fds = sorted(by)
    docs = [L.ident_terms(" ".join(by[d]["keys"]) + " " + by[d]["line"]) for d in fds]
    idf, _ = L.idf_table(docs)
    texts = list(read_texts) + ([read_text(f) for f in wrote_files] if query == "read+wrote" else [])
    qv = L.vector(L.ident_terms("\n".join(texts)), idf)
    out = []
    for d, doc in zip(fds, docs):
        dv = L.vector(doc, idf)
        contrib = sorted(((qv[0][t] * x, t) for t, x in dv[0].items() if t in qv[0]), reverse=True)
        out.append({"short": by[d]["short"], "family_dir": d, "name": by[d]["name"], "line": by[d]["line"], "rules": by[d]["n"],
                    "score": round(L.cosine(qv, dv), 4), "matched": [t for _, t in contrib[:8]]})
    out.sort(key=lambda x: (-x["score"], x["family_dir"]))
    for i, x in enumerate(out, 1):
        x["rank"] = i
    return out[:k] if k else out


def merged(results, k):
    """几个产物各自排好的结果合在一起，按得分重排、重编名次，取前 k。"""
    key = (lambda x: (-x["score"], x.get("family_dir") or x.get("id")))
    out = sorted((x for res in results for x in res), key=key)
    for i, x in enumerate(out, 1):
        x["rank"] = i
    return out[:k] if k else out


def topic_label(base, pdir, t, cache):
    """主题目录 → (「一级 / 二级」的中文名, 主题的一行)。从导出的 <产物>/<主题>/index.md 读：第一行「# 中文名」，
    紧跟着的一段不是小标题的就是主题的一行（build_index.py 就是这样写的）。"""
    def one(td):
        if td not in cache:
            ls = read_text(os.path.join(base, pdir, *td.split("/"), "index.md")).splitlines()
            name = ls[0][2:].strip() if ls and ls[0].startswith("# ") else td.split("/")[-1]
            line = ls[2].strip() if len(ls) > 2 and ls[2].strip() and not ls[2].startswith("#") else ""
            cache[td] = (name, line)
        return cache[td]
    segs = t.split("/")
    return " / ".join(one("/".join(segs[:k]))[0] for k in range(1, len(segs) + 1)), one(t)[1]


def as_tree(res, rules, base, k, with_lines=False):
    """粗筛出的族排成一棵小树（文本）。res 是 coarse_families 的结果（已截到前 k）。"""
    rows = {}
    for r in rules:
        if r.get("family_dir"):
            rows.setdefault(r["family_dir"], []).append(r)

    def order(x):
        s = x.get("short") or ""
        return (int(s[1:]) if s[1:].isdigit() else 10 ** 9, x["family_dir"])
    pdirs = sorted({x["family_dir"].split("/")[0] for x in res})
    names = "、".join(PRODUCT_NAMES.get(p, p) for p in pdirs) or "（没有）"
    out = [f"粗筛出的一部分：按读过和交回的文件取前 {k} 个族，入选 {len(res)} 个（{names}）；只列入选的族和它们所在的主题，"
           f"不是全库。全库地图用 recall.py show map 看，族的全部内容用 show <短号>。"]
    cache = {}
    for pdir in pdirs:
        fs = [x for x in res if x["family_dir"].split("/")[0] == pdir]
        out += ["", f"{PRODUCT_NAMES.get(pdir, pdir)}：入选 {len(fs)} 个族"]
        by_t = {}
        for x in fs:
            by_t.setdefault("/".join(x["family_dir"].split("/")[1:-1]), []).append(x)
        allt = set()
        for t in by_t:
            segs = t.split("/")
            allt |= {"/".join(segs[:j]) for j in range(1, len(segs) + 1)}
        for t in sorted(allt):
            label, line = topic_label(base, pdir, t, cache.setdefault(pdir, {}))
            out.append(label + (f"：{line}" if line else ""))
            items = sorted(by_t.get(t, []), key=order)
            if with_lines:
                for x in items:
                    out.append(f"  {x['short']} {x['name']}（{x['rules']}）")
                    out.append(f"    agent 会看到什么：{x['line']}")
                    fr = rows.get(x["family_dir"], [])
                    out += [f"    通用查法：{r['id']}｜{r.get('title')}" for r in fr if r.get("general")]
                    out += ["    " + (r.get("line") or r["id"]).lstrip("- ") for r in fr if not r.get("general")]
                continue
            cur = ""
            for it in (f"{x['short']} {x['name']}（{x['rules']}）" for x in items):
                if cur and len(cur) + 1 + len(it) > MAP_WIDTH:
                    out.append("  " + cur)
                    cur = it
                else:
                    cur = f"{cur}；{it}" if cur else it
            if cur:
                out.append("  " + cur)
    return "\n".join(out)


def show(nodes, base, by_id, products=None):
    """打印多个节点：index、主题、族的 index.md，或规矩正文。products 是产物名的列表（只列这些产物）。"""
    dirs = {L.PRODUCT_DIRS.get(p, p) for p in products} if products else None
    out = []
    fam_rows = {}
    for r in by_id.values():
        if r.get("family_short"):
            fam_rows.setdefault(r["family_short"], []).append(r)
    for raw in nodes:
        n = raw.strip().replace("\\", "/").strip("/")
        n = re.sub(r"^rules/", "", n)
        n = re.sub(r"/?index\.md$", "", n)
        if n == "map":                # 一页地图：每个产物的 map.md
            pds = sorted(d for d in os.listdir(base) if os.path.isfile(os.path.join(base, d, "map.md")))
            texts = [read_text(os.path.join(base, d, "map.md")).rstrip() for d in pds if not dirs or d in dirs]
            out.append(("map", "\n\n".join(texts) or "（没有地图）"))
            continue
        if re.fullmatch(r"f\d{3,}", n):    # 族的短号
            rows = fam_rows.get(n)
            if not rows:
                out.append((n, "（视图里没有这个族）"))
                continue
            if dirs and rows[0]["family_dir"].split("/")[0] not in dirs:
                out.append((n, f"（不在 {','.join(products)} 里，跳过）"))
                continue
            gens = [r for r in rows if r.get("general")]
            lines = [f"{n} {rows[0].get('family_name')}（{len(rows)} 条）", f"agent 会看到什么：{rows[0].get('family_line')}"]
            for g in gens:
                lines += ["通用查法：", strip_sources(read_text(os.path.join(base, *g["path"].split("/")))).rstrip()]
            members = [r for r in rows if not r.get("general")]
            if members:
                lines += ["规矩："] + [(r.get("line") or r["id"]).lstrip("- ") for r in members]
            out.append((n, "\n".join(lines)))
            continue
        if n in ("", "index", "top"):
            text = read_text(os.path.join(base, "index.md"))
            if dirs:      # 只留开头的说明和这些产物的段（每段以「## 产物名（产物目录）」开头）
                keep, section = [], None
                for line in text.splitlines():
                    m = re.match(r"^## .*（([a-z]+)）\s*$", line)
                    if m:
                        section = m.group(1)
                    if section is None or section in dirs:
                        keep.append(line)
                text = "\n".join(keep)
            out.append(("index", text))
            continue
        if n.startswith("rule-"):
            r = by_id.get(n)
            if not r:
                out.append((n, "（视图里没有这条规矩）"))
                continue
            if dirs and r["path"].split("/")[0] not in dirs:
                out.append((n, f"（不在 {','.join(products)} 里，跳过）"))
                continue
            out.append((n, strip_sources(read_text(os.path.join(base, *r["path"].split("/"))))))
            continue
        if dirs and n.split("/")[0] not in dirs:
            out.append((n, f"（不在 {','.join(products)} 里，跳过）"))
            continue
        p = os.path.join(base, *n.split("/"), "index.md")
        out.append((n, strip_sources(read_text(p)) if os.path.isfile(p) else "（没有这个节点）"))
    return "\n\n".join(f"==== {k} ====\n{v.rstrip()}" for k, v in out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["coarse", "lines", "body", "show"])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--rules", help="导出的 rules/ 目录（默认分支根目录下的 rules/）")
    ap.add_argument("--index", help="keys.jsonl（默认取 --rules 目录里的）")
    ap.add_argument("--products", help="show：只列这些产物；coarse：这几个产物合在一起按得分取前 --k（逗号分隔，产物名或产物目录）")
    ap.add_argument("--as-tree", action="store_true", help="coarse：入选的族排成「产物 → 主题 → 族」的小树（隐含 --level family）")
    ap.add_argument("--with-lines", action="store_true", help="coarse：小树里每个族带族的一行和每条规矩的一行（隐含 --as-tree）")
    ap.add_argument("--level", choices=["rule", "family"], default="rule")
    ap.add_argument("--product", default="代码")
    ap.add_argument("--read", nargs="*", default=[])
    ap.add_argument("--wrote", nargs="*", default=[])
    ap.add_argument("--read-ext", default=READ_EXT)
    ap.add_argument("--wrote-ext", default=WROTE_EXT)
    ap.add_argument("--k", type=int, default=30)
    ap.add_argument("--fields", choices=["keys", "keys+text"], default="keys")
    ap.add_argument("--query", choices=["read", "read+wrote"], default="read+wrote")
    ap.add_argument("--probe-bonus", type=float, default=0.3)
    ap.add_argument("--exclude-apps")
    ap.add_argument("--cases-in")
    ap.add_argument("--cases-mode", choices=["all", "any"], default="all")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--with-sources", action="store_true", help="body / show：规矩正文连来源明细（卡号、应用、各项出自哪条结论）一起给，给人看时用")
    a = ap.parse_args()
    global WITH_SOURCES
    WITH_SOURCES = a.with_sources
    here = os.path.dirname(os.path.abspath(__file__))
    pack = os.path.dirname(here) if os.path.isfile(os.path.join(here, "..", "keys.jsonl")) else None   # 部署包里：scripts/ 的上一级就是库
    base = os.path.abspath(a.rules) if a.rules else (os.path.dirname(os.path.abspath(a.index)) if a.index else (pack or os.path.join(L.ROOT, "rules")))
    index = a.index or os.path.join(base, "keys.jsonl")
    allrows = load_index(index)
    if (a.exclude_apps or a.cases_in) and allrows and not any("sources" in r for r in allrows):
        raise SystemExit("这份库（部署包）的 keys.jsonl 不带来源，--exclude-apps / --cases-in 用不了；视图要在建部署包时给："
                         "build_index.py --deploy-out <目录> --exclude-apps … / --cases-in …")
    rules = view(allrows, a.exclude_apps.split(",") if a.exclude_apps else None, a.cases_in, a.cases_mode)
    by_id = {r["id"]: r for r in rules}
    if a.cmd == "show":
        print(show(a.ids, base, by_id, a.products.split(",") if a.products else None))
        return
    if a.cmd == "coarse":
        read = [read_text(f) for f in files_of(a.read, a.read_ext)]
        wrote = files_of(a.wrote, a.wrote_ext)
        prods = [PRODUCT_NAMES.get(p.strip(), p.strip()) for p in a.products.split(",") if p.strip()] if a.products else [a.product]
        a.as_tree = a.as_tree or a.with_lines
        if a.level == "family" or a.as_tree:
            res = merged([coarse_families(rules, p, read, wrote, 0, a.query) for p in prods], a.k)
            if a.as_tree:
                print(as_tree(res, rules, base, a.k, a.with_lines))
            elif a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                for x in res:
                    print(f"{x['rank']:3d}  {x['score']:.3f}  {x['short']}  {x['name']}（{x['rules']} 条）  {x['family_dir']}  ［{', '.join(x['matched'])}］")
            return
        res = merged([coarse(rules, p, read, wrote, 0, a.fields, a.query, a.probe_bonus) for p in prods], a.k)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print(f"视图里 {'、'.join(prods)} 的规矩 {sum(1 for r in rules if r.get('product') in prods)} 条；读过的文件 {len(read)} 个，交回的 {len(wrote)} 个")
            for x in res:
                print(f"{x['rank']:3d}  {x['score']:.3f}  {x['id']}  {x['title'][:50]}  ［{', '.join(x['matched'])}］" + (f"  probe: {x['probe'][0]}" if x["probe"] else ""))
    elif a.cmd == "lines":
        for rid in a.ids:
            print(by_id[rid]["line"] if rid in by_id else f"- {rid}｜（视图里没有这条）")
    else:
        for rid in a.ids:
            if rid not in by_id:
                print(f"（视图里没有 {rid}）")
                continue
            print(strip_sources(read_text(os.path.join(base, *by_id[rid]["path"].split("/")))))


if __name__ == "__main__":
    main()
