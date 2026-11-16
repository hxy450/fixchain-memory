# -*- coding: utf-8 -*-
"""第 5 步「导出」：按 docs/rules-v2-design.md 第 3、4 节写出 rules/ 目录树、keys.jsonl 和 manifest.json。

读：规矩目录（--rules，默认 store/rules/）、归族结果（--families，默认 store/families/ 下的 families.json 和 topics.json）、
    work/cards_index.json（每张卡的应用）、store/HEAD.json（卡库版本）。
写（--out，默认 rules/；先清空再写）：
  index.md                                    第一层：各产物下的一级主题，每个主题一行（中文名、规矩数、主题的一行「agent 手里有
                                              什么东西时该进来看」）
  <产物>/<主题>/index.md                       第二层：主题的一行，主题下的子主题（各带一行）和触发族（族名、规矩数、agent 会看到什么）；
                                              多级主题每级一个 index.md
  <产物>/<主题>/<族>/index.md                  第三层：族名、agent 会看到什么、通用查法的全文，加每条规矩的一行（标题和触发）
  <产物>/<主题>/<族>/<规矩号>.md                第四层：规矩正文（render.one 的样子，来源按 sources 和应用算）
  keys.jsonl                                  每条规矩一行：id、product、title、keys、probe、triggers、line（第三层那一行）、path、
                                              family、family_key、family_dir、family_name、family_line、topic、general、status、
                                              sources、apps
  manifest.json                               条数（按产物、族、主题、通用查法、disputed）、构建时间、所依据的卡库版本、分支提交、应用清单、
                                              族的短号 → 族的路径
  <产物>/map.md                                一页地图：每个主题一行（中文名、条数、主题的一行），下面是它直接挂的族「短号 族名（条数）」，
                                              用「；」隔开；不带链接（recall.py show map 打印的就是它）
  <产物>/index.md                              这个产物的一级主题（中文名、条数、一行、链接），并指向同目录的 map.md
  cards.md                                    卡和规矩的对照：按应用分节，每张卡一行（卡号、卡的标题、它支持的规矩号和标题）；
                                              没有产出规矩的卡也列，注明原因（候选里 left_out 的原因汇总）
规矩页（第四层）和族页里的通用查法，来源一节在「来源：N 张卡，M 个应用」下面逐张列出卡号、应用和各项出自哪条结论
（render.provenance）；manifest.json 的 inputs 写相对分支根目录的路径，不写本机路径。
--deploy-out <目录>：另写一份给 agent 的部署包：同一棵树（可用 --products 只留几个产物，--exclude-apps / --cases-in 取视图），
  规矩页只留来源的计数一行，不写 cards.md 和 manifest.json，keys.jsonl 不带 sources、apps，另带 scripts/recall.py、rulelib.py
  和一页 README.md；评测时拷进试验目录的就是它。--no-library 时只写部署包。
族的短号取 families.json 的 short（families.py apply 按族号顺序给，f001 起）；没有或重复时这里按顺序补。
产物目录名固定：规格 spec、计划与派工 plan、代码 code、资源 resource。每条规矩必须恰好在一个族里（族的成员或族的通用查法），
同一产物同一主题下族目录不能重名、族目录不能和同一层的子主题同名，否则停。主题层数不限（超限拆分时会按需加深）。主题的中文名和一行取 topics.json（理主题之后是 {"name", "line"}；只有中文名的旧写法也认）。
用法： py -3 -X utf8 skills/memory-rules/scripts/build_index.py [--rules DIR] [--families DIR] [--out DIR] [--api N]
         [--deploy-out DIR [--products 代码,资源] [--exclude-apps A,B] [--cases-in 前缀] [--no-library]]"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, importlib.util, json, os, shutil, subprocess, time  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rulelib as L  # noqa: E402

_spec = importlib.util.spec_from_file_location("render_build", os.path.join(HERE, "render.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
PRODUCT_NAMES = {v: k for k, v in L.PRODUCT_DIRS.items()}


def tname(v):
    return v.get("name", "") if isinstance(v, dict) else (v or "")


def tline(v):
    return v.get("line", "") if isinstance(v, dict) else ""


MAP_WIDTH = 120


def map_text(pdir, tps, names, count):
    """一个产物的一页地图：每个主题一行（中文名：主题的一行），下面是这个主题直接挂的族，每个族「短号 族名（条数）」，
    用「；」隔开，一行排不下就折到下一行（缩进两格）。二级主题写成「一级 / 二级」。不带链接和别的修饰。"""
    nfam = sum(len(fl) for fl in tps.values())
    nrule = sum(x["n"] for fl in tps.values() for x in fl)
    out = [f"{PRODUCT_NAMES.get(pdir, pdir)}：{nfam} 个族，{nrule} 条规矩。用短号取族（如 recall.py show f001）。", ""]
    allt = set()
    for t in tps:
        segs = t.split("/")
        allt |= {"/".join(segs[:k]) for k in range(1, len(segs) + 1)}
    for t in sorted(allt):
        segs = t.split("/")
        label = " / ".join(tname(names.get("/".join(segs[:k]))) or segs[k - 1] for k in range(1, len(segs) + 1))
        line = tline(names.get(t))
        out.append(f"{label}（{count[t]} 条）" + (f"：{line}" if line else ""))
        items = [f"{x['f']['short']} {x['f']['name']}（{x['n']}）" for x in tps.get(t, [])]
        cur = ""
        for it in items:
            if cur and len(cur) + 1 + len(it) > MAP_WIDTH:
                out.append("  " + cur)
                cur = it
            else:
                cur = f"{cur}；{it}" if cur else it
        if cur:
            out.append("  " + cur)
    return "\n".join(out)


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n") + "\n")


def check_tree(rules, fams):
    owner, bad = {}, []
    paths = collections.Counter((f.get("product_dir") or L.PRODUCT_DIRS[f["product"]], f["topic"], f["dir"]) for f in fams)
    bad += [f"同一产物同一主题下族目录重名：{k}（先理主题或改目录名）" for k, c in paths.items() if c > 1]
    tdirs = {(pd, "/".join(t.split("/")[:k])) for pd, t, _ in paths for k in range(1, len(t.split("/")) + 1)}
    bad += [f"族目录和子主题同名：{pd}/{t}/{d}" for pd, t, d in paths if (pd, f"{t}/{d}") in tdirs]
    for f in fams:
        for rid in f["rules"] + ([f["general"]] if f.get("general") else []):
            if rid in owner and owner[rid] is not f:
                bad.append(f"{rid} 在两个族里（{owner[rid]['family']}、{f['family']}）")
            owner[rid] = f
            if rid not in rules:
                bad.append(f"{f['family']} 里的 {rid} 在规矩目录里没有")
    for rid in rules:
        if rid not in owner:
            bad.append(f"{rid} 不在任何族里")
    return bad


def rel_path(p):
    """相对分支根目录的路径（用 /）；不在分支里的只留最后一级目录名（不写本机路径）。"""
    a = os.path.abspath(p)
    try:
        r = os.path.relpath(a, L.ROOT)
    except ValueError:
        r = os.path.basename(a)
    return os.path.basename(a) if r.startswith("..") else r.replace("\\", "/")


def build(out, rules, fams, topics, head, api, app_of, library=True):
    """写一棵树。library=True 是库本身的导出（规矩页带来源明细、写反向对照表 cards.md 和 manifest.json）；
    False 是给 agent 的部署包（规矩页只留来源的计数一行，不写 cards.md 和 manifest.json，keys.jsonl 不带 sources、apps）。"""
    os.makedirs(out, exist_ok=True)
    for x in os.listdir(out):          # 清空目录里的东西（目录本身留着：别的程序开着它时删不掉）
        p = os.path.join(out, x)
        shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)

    def apps(rid):
        return sorted({app_of.get(c) or f"（未记录：{c}）" for c in rules[rid].get("sources") or []})

    def page(r):
        src = r.get("sources") or []
        n, m = R.counts(src)
        return R.one(r, n, m, api, sources=src if library else None)

    keys_lines, tree = [], collections.defaultdict(lambda: collections.defaultdict(list))
    for f in fams:
        pdir = f.get("product_dir") or L.PRODUCT_DIRS[f["product"]]
        fdir = os.path.join(out, pdir, *f["topic"].split("/"), f["dir"])
        rel = "/".join([pdir, f["topic"], f["dir"]])
        gens = [x for x in ([f["general"]] if f.get("general") else []) + [r for r in f["rules"] if rules[r].get("general")]]
        gens = list(dict.fromkeys(gens))
        body = [f"# {f['name']}", "", f"agent 会看到什么：{f['line']}", ""]
        for g in gens:
            text = page(rules[g])
            body += ["## 通用查法", "", "### " + text[2:] if text.startswith("# ") else text, ""]
        members = [r for r in f["rules"] if r not in gens]
        if members:
            body += ["## 规矩", ""] + [R.index_line(rules[r], r) for r in members]
        write(os.path.join(fdir, "index.md"), "\n".join(body))
        for rid in list(dict.fromkeys(gens + f["rules"])):
            r = rules[rid]
            write(os.path.join(fdir, rid + ".md"), page(r))
            row = {"id": rid, "product": r.get("product"), "title": r.get("title"), "keys": r.get("keys"), "probe": r.get("probe"),
                   "triggers": r.get("triggers"), "line": R.index_line(r, rid), "path": f"{rel}/{rid}.md",
                   "family": f["family"], "family_short": f["short"], "family_key": f.get("key"), "family_dir": rel,
                   "family_name": f["name"], "family_line": f["line"], "topic": f["topic"], "general": bool(r.get("general")),
                   "status": r.get("status")}
            if library:
                row.update(sources=r.get("sources") or [], apps=apps(rid))
            keys_lines.append(row)
        tree[pdir][f["topic"]].append({"f": f, "n": len(f["rules"]) + (1 if f.get("general") and f["general"] not in f["rules"] else 0)})
    # 第二层：每个主题（含多级主题的每一级）一个 index.md；每个产物目录一个 index.md（一级主题，指向 map.md）
    top = ["# 规矩库", "", f"卡库版本：`{head}`；规矩 {len(rules)} 条。按产物进入，再按主题、触发族往下找。", ""]
    for pdir in sorted(tree):
        tps = tree[pdir]
        names = topics.get(pdir, {})
        levels = collections.defaultdict(set)
        for t in tps:
            segs = t.split("/")
            for k in range(1, len(segs) + 1):
                levels["/".join(segs[:k - 1])].add("/".join(segs[:k]))
        count = collections.Counter()
        for t, fl in tps.items():
            segs = t.split("/")
            for k in range(1, len(segs) + 1):
                count["/".join(segs[:k])] += sum(x["n"] for x in fl)

        def nm(t):
            return tname(names.get(t)) or t

        def ln(t):
            x = tline(names.get(t))
            return f"：{x}" if x else ""
        for t in sorted(set(x for v in levels.values() for x in v)):
            lines = [f"# {nm(t)}", ""] + ([tline(names.get(t)), ""] if tline(names.get(t)) else [])
            subs = sorted(levels.get(t, []))
            if subs:
                lines += ["## 子主题", ""] + [f"- [{nm(s)}]({s.split('/')[-1]}/index.md)（{count[s]} 条）{ln(s)}" for s in subs] + [""]
            fl = tps.get(t, [])
            if fl:
                lines += ["## 触发族", ""] + [f"- [{x['f']['name']}]({x['f']['dir']}/index.md)（{x['n']} 条）：{x['f']['line']}" for x in fl]
            write(os.path.join(out, pdir, *t.split("/"), "index.md"), "\n".join(lines))
        firsts = [f"- [{nm(t)}]({t}/index.md)（{count[t]} 条）{ln(t)}" for t in sorted(levels.get("", []))]
        nfam = sum(len(fl) for fl in tps.values())
        nrule = sum(x["n"] for fl in tps.values() for x in fl)
        write(os.path.join(out, pdir, "index.md"), "\n".join(
            [f"# {PRODUCT_NAMES.get(pdir, pdir)}（{pdir}）", "",
             f"{nfam} 个族，{nrule} 条规矩。整个产物的族一页看完见 [map.md](map.md)（每个主题一行，下面是「短号 族名（条数）」）。", "",
             "## 一级主题", ""] + firsts))
        top += [f"## {PRODUCT_NAMES.get(pdir, pdir)}（{pdir}）", ""]
        top += [f"- [{nm(t)}]({pdir}/{t}/index.md)（{count[t]} 条）{ln(t)}" for t in sorted(levels.get("", []))] + [""]
        write(os.path.join(out, pdir, "map.md"), map_text(pdir, tps, names, count))
    write(os.path.join(out, "index.md"), "\n".join(top))
    with open(os.path.join(out, "keys.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
        for x in keys_lines:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    return keys_lines, tree


def cards_table(out, rules, idx, candidates_dir):
    """反向对照表 cards.md：按应用分节，每张卡一行：卡号｜卡的标题｜它支持的规矩（规矩号和标题）；
    没有产出规矩的卡也列，注明原因（候选里没有规矩的，汇总 left_out 的原因；有候选但都不在这份导出里的，写明）。"""
    by_card = collections.defaultdict(list)
    for rid, r in rules.items():
        for c in r.get("sources") or []:
            by_card[c].append(rid)
    apps = collections.defaultdict(list)
    for x in idx.get("index") or []:
        apps[x.get("app") or "（未记录应用）"].append(x)
    lines = ["# 卡和规矩的对照", "",
             "每张卡一行：卡号｜卡的标题｜它支持的规矩（规矩号和标题，按规矩里引它的那几项算）。没有产出规矩的卡注明原因。", ""]
    n_with, n_without = 0, 0
    for app in sorted(apps, key=lambda s: s.lower()):
        lines += [f"## {app}", ""]
        for x in sorted(apps[app], key=lambda y: y["case"]):
            c, title = x["case"], (x.get("title") or "").replace("｜", "|")
            rs = sorted(by_card.get(c, []), key=lambda rid: (rules[rid].get("product") or "", rules[rid].get("title") or ""))
            if rs:
                n_with += 1
                lines.append(f"- {c}｜{title}｜规矩 {len(rs)} 条：" + "；".join(f"{rid} {rules[rid].get('title')}" for rid in rs))
                continue
            n_without += 1
            cp = os.path.join(candidates_dir, c + ".json")
            if not os.path.isfile(cp):
                why = "还没有提炼"
            else:
                o = L.jload(cp)
                if o.get("rules"):
                    why = f"候选 {len(o['rules'])} 条，都不在这份导出里"
                else:
                    cnt = collections.Counter((y.get("reason") or "").split("：")[0] for y in o.get("left_out") or [] if isinstance(y, dict))
                    why = "没有写成规矩：" + ("、".join(f"{k} {v}" for k, v in cnt.most_common()) or "没写原因")
            lines.append(f"- {c}｜{title}｜没有产出规矩（{why}）")
        lines.append("")
    lines[2:2] = [f"共 {n_with + n_without} 张卡：产出规矩的 {n_with} 张，没有产出的 {n_without} 张。", ""]
    write(os.path.join(out, "cards.md"), "\n".join(lines))
    return n_with, n_without


def view_filter(rules, fams, products=None, exclude_apps=None, cases_in=None, app_of=None):
    """部署包的视图：只留这些产物；去掉只出自这些应用的规矩；只留来源全在这个快照里的规矩。族跟着去掉不在视图里的规矩，空了的族去掉。"""
    keep = {}
    snap = None
    if cases_in:
        hits = [p for p in os.listdir(os.path.join(L.STORE, "snapshots")) if p.startswith(cases_in)]
        if len(hits) != 1:
            raise SystemExit(f"--cases-in {cases_in}：快照要恰好一个，找到 {len(hits)} 个")
        snap = set(L.jload(os.path.join(L.STORE, "snapshots", hits[0]))["cases"])
    ex = set(exclude_apps or [])
    for rid, r in rules.items():
        if products and r.get("product") not in products:
            continue
        src = r.get("sources") or []
        if ex and src and {app_of.get(c) or "" for c in src} <= ex:
            continue
        if snap is not None and not (src and all(c in snap for c in src)):
            continue
        keep[rid] = r
    out = []
    for f in fams:
        g = dict(f, rules=[x for x in f["rules"] if x in keep])
        if g.get("general") and g["general"] not in keep:
            g["general"] = None
        if g["rules"] or g.get("general"):
            out.append(g)
    return keep, out


RECALL_FILES = ("recall.py", "rulelib.py")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default=os.path.join(L.STORE, "rules"))
    ap.add_argument("--families", default=os.path.join(L.STORE, "families"))
    ap.add_argument("--candidates", default=os.path.join(L.STORE, "candidates"), help="反向对照表里没有产出规矩的卡，从候选里取原因")
    ap.add_argument("--out", default=os.path.join(L.ROOT, "rules"))
    ap.add_argument("--deploy-out", help="另写一份给 agent 的部署包到这个目录（不带来源明细、对照表和 manifest，带 recall.py）")
    ap.add_argument("--products", help="部署包只留这些产物（逗号分隔，产物名或产物目录）")
    ap.add_argument("--exclude-apps", help="部署包里去掉只出自这些应用的规矩（评测时去掉留出的应用）")
    ap.add_argument("--cases-in", help="部署包只留来源全在这个快照里的卡产出的规矩")
    ap.add_argument("--no-library", action="store_true", help="只写部署包，不重写 --out 的库导出")
    ap.add_argument("--api")
    a = ap.parse_args()
    api = a.api or R.api_version()
    rules = L.load_rules(a.rules)
    fams = L.jload(os.path.join(a.families, "families.json"))
    topics = L.jload(os.path.join(a.families, "topics.json"), {})
    idx = L.jload(L.INDEX, {"index": []})
    app_of = {x["case"]: x.get("app") or "" for x in idx["index"]}
    head = L.jload(os.path.join(L.STORE, "HEAD.json"))["revision"]
    bad = check_tree(rules, fams)
    if bad:
        print(f"有 {len(bad)} 处对不上，没有导出：")
        for b in bad[:40]:
            print("  - " + b)
        sys.exit(1)
    width = max(3, len(str(len(fams))))
    shorts = collections.Counter(f.get("short") for f in fams)
    for k, f in enumerate(fams, 1):    # 短号：families.json 里有就用；没有或重复时按顺序补
        if not f.get("short") or shorts[f.get("short")] > 1:
            f["short"] = f"f{k:0{width}d}"
    if not a.no_library:
        keys_lines, tree = build(a.out, rules, fams, topics, head, api, app_of, library=True)
        n_with, n_without = cards_table(a.out, rules, idx, a.candidates)
        try:
            commit = subprocess.run(["git", "-C", L.ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        except OSError:
            commit = ""
        by_prod = collections.Counter(r.get("product") for r in rules.values())
        man = {"rules": len(rules), "by_product": dict(by_prod), "families": len(fams),
               "topics": sum(len({t for t in tree[p]}) for p in tree), "general": sum(1 for r in rules.values() if r.get("general")),
               "disputed": sum(1 for r in rules.values() if r.get("status") == "disputed"),
               "cards": len({c for r in rules.values() for c in r.get("sources") or []}), "cards_without_rules": n_without,
               "apps": sorted({x for k in keys_lines for x in k["apps"]}),
               "library_revision": head, "built_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "branch_commit": commit,
               "inputs": {"rules": rel_path(a.rules), "families": rel_path(a.families)}, "harmony_api": api,
               "family_short": {f["short"]: "/".join([f.get("product_dir") or L.PRODUCT_DIRS[f["product"]], f["topic"], f["dir"]]) for f in fams}}
        L.jsave(os.path.join(a.out, "manifest.json"), man)
        print(f"导出到 {a.out}：规矩 {len(rules)} 条（{dict(by_prod)}），族 {len(fams)} 个，主题 {man['topics']} 个，通用查法 {man['general']} 条，"
              f"keys.jsonl {len(keys_lines)} 行；对照表 cards.md：产出规矩的卡 {n_with} 张，没有产出的 {n_without} 张")
    if a.deploy_out:
        prods = {PRODUCT_NAMES.get(p.strip(), p.strip()) for p in a.products.split(",")} if a.products else None
        dr, df = view_filter(rules, fams, prods, a.exclude_apps.split(",") if a.exclude_apps else None, a.cases_in, app_of)
        keys_lines, tree = build(a.deploy_out, dr, df, topics, head, api, app_of, library=False)
        sd = os.path.join(a.deploy_out, "scripts")
        os.makedirs(sd)
        for x in RECALL_FILES:
            shutil.copy2(os.path.join(HERE, x), os.path.join(sd, x))
        write(os.path.join(a.deploy_out, "README.md"), "\n".join([
            "# 规矩库（部署包）", "",
            "给审的 agent 查库用。先看 `index.md` 或各产物的 `map.md`，再用短号取族、用规矩号取正文：", "",
            "```", "python scripts/recall.py show map --rules .", "python scripts/recall.py show f017 rule-… --rules .",
            "python scripts/recall.py coarse --level family --as-tree --with-lines --product 代码 --read <读过的文件…> --wrote <交回的文件…> --rules .",
            "```", "", "规矩页不带来源明细（库本身的导出里有）。"]))
        print(f"部署包写到 {a.deploy_out}：规矩 {len(dr)} 条，族 {len(df)} 个，keys.jsonl {len(keys_lines)} 行" +
              (f"；只留 {sorted(prods)}" if prods else "") + (f"；去掉只出自 {a.exclude_apps} 的规矩" if a.exclude_apps else "") +
              (f"；只留快照 {a.cases_in} 里的卡" if a.cases_in else ""))


if __name__ == "__main__":
    main()
