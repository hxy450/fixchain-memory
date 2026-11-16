# -*- coding: utf-8 -*-
"""第 4 步「归族和建主题」的脚本：propose 出触发族的提案，apply 落盘子代理的归族输出；第一次建库时再用 topics-list /
topics-check 做一遍全局的「理主题」。

propose：读规矩目录（--rules，默认 store/rules/）。通用查法（general: true）不参与聚类，它们由归族的决定挂到族上。
  加 --new-only 时只给还没归进任何族（families.json 里没有、已有的决定也没放进族）的规矩出提案：增量归并，或第一次建库时
  第一轮有 move_out 之后的下一轮。同一 product 内，每条规矩的文档 = keys.read
  （没有 keys.read 的用各触发 read 栏的标识符），切词和相似度同 rulelib.py（IDF 余弦）。相似度不低于 --threshold 的连边取连通分量，
  超过 --max-size（默认 20）条的提高阈值再拆；落单的规矩并到和它平均相似度最高、还没满的族（平均相似度要大于 --attach-min），
  都不行的自成一族。每个提案只带规矩的 id、title、product、triggers、keys（归族的子代理不看正文）。
  --new-only 时每个提案附上同一产物下和它最相近的 --existing-top 个已有族（默认 8；族名、族的一行、主题、目录名、相似度），
  相近按「提案里各规矩的 keys.read 和标题」对「族的一行、族名和族里各规矩的 keys.read」的 IDF 余弦算。
  写（--out，默认 store/families/）：proposals/<提案号>.json（带 round：第几轮）、batches/family-NNN.txt（每批若干提案文件的
  路径，相对分支根目录、用 /；读的时候相对和绝对路径都认，每批规矩合计不超过 --per-batch 条，默认 80），propose_report.json 和 propose_report_r<轮>.json（相似度、族大小的分布）。
  从头出（不加 --new-only）时先清掉 proposals/、batches/，decisions/ 里已有决定就拒绝（会对不上）；--new-only 时已有的提案、批次、
  决定都不动，提案号和批次号接在已有最大号后面，还有提案没写决定时拒绝。
apply：读 proposals/ 和 decisions/<提案号>.json（子代理写的，格式见 references/family-brief.md）：
    {"proposal": "fam-0001",
     "families": [{"name": "族名", "dir": "英文短横线目录名", "line": "agent 会看到什么（一行）",
                   "topic": {"dir": "主题目录（可多级，用 / 分）", "name": "主题中文名"},
                   "rules": ["rule-…", …（按排列顺序）], "general": null 或 一条通用查法规矩（候选格式加 "general": true）,
                   "same": [{"rules": ["rule-…", "rule-…"], "reason": "一句话"}]（族里从标题和触发看是同一条的，可以没有）}],
     "move_out": [{"rule": "rule-…", "reason": "…"}]}
  每个族的标识是「提案号#序号」（key），理主题时用它指族；每个族另有短号（f001 起，按族号顺序，一次导出里唯一），给审的 agent 用。
  same 的检查：每组至少两条不同的规矩、都在这个族的 rules 里、一条规矩不出现在两组里、要写理由（按子代理写的原样查）。
  补并：same-groups 把 same 组做成合并组；合并落盘（apply_merge.py --prefix same）之后，apply 按 --merge 目录的 merge_map.json
  把提案和决定里被并掉的规矩号换成留下的那条并去重——所以补并和理主题可以并行跑，都写完了再 apply。
  检查：每个提案都有决定；提案里的每条规矩恰好进了一个族，或被列进 move_out；不在任何提案里的规矩号不许出现；族名、族的一行
  非空；目录名是小写英文、数字和短横线（主题每一级都是）。第一次建库（--fresh）时子代理写的主题只当建议：同一主题目录的中文名
  前后不一、同一主题下族目录重名只报提示；有理主题的决定（topic_decisions/<产物目录>.json）时用它覆盖各族的主题、合并标出的族，
  再查同一主题下族目录不重名。增量（不加 --fresh）时主题按决定原样落，中文名不一致和重名都算错。
  通用查法：general 必须是 true，规矩号按 product 和标题算，sources 取它 support 里引到的卡，status 为 active，写进规矩目录，
  并跑 check_rules.py 查它（--format-only 时只查格式）。
  写 families.json（每族：族号、短号、key、product、主题、目录名、族名、一行、规矩顺序、通用查法的规矩号、same）、topics.json（按产物目录分，
  主题目录 → {"name": 中文名, "line": 主题的一行}）；move_out 的规矩写进 unplaced.json，有的话退出码为 1（要再提案一轮）。
  几轮：proposals/ 和 decisions/ 里各轮的都一起读（每个提案各自检查）；前一轮 move_out、后一轮放进了族的不算待挪。
  同一产物、同一主题、同一目录名的族并进排在前面的那个（先于理主题；同一批里有意写成同名的、下一轮归进已有族的都这样并；
  两边都带通用查法时后一条作为族里另一条通用查法留着）。已有 families.json 时（增量，不加 --fresh），也这样并进已有族。
  增量（不加 --fresh）只落还没落过的轮（apply_state.json 记着落过哪几轮；没有这个文件时按 families.json 里的族出自哪些提案推），
  已有的族连同理过、拆过的主题原样留着，不用 topic_decisions/；新族的主题照决定写（新起的主题可以在 topic 里带 line）。
  基础库建成后加过增量或拆过主题节点时，apply --fresh 拒绝（会把这些冲掉）。
  拆族的提案（带 split_of，split-families 出的）：拆出来的族都留在原族的主题下，在原族的位置替换原族；general 可以写原族
  通用查法的规矩号（沿用），没有沿用的原通用查法落盘时删掉；拆出来的族目录名不能和同一主题下别的族、子主题重名。
oversize：列出超限的节点（规矩超过 --max-rules 条的族；直接子项超过 --max-children 个的主题节点，含产物根），写 oversize.json，
  有就退出码 1。基础库建完、每期增量落完都跑一次。
split-families：给每个超限的族出一个拆分提案（新的一轮，编号接着排；附原族的名字、一行、主题、通用查法和同主题下已有的目录名），
  子代理照 family-brief.md「拆一个超限的族」写决定、apply --check --proposals 自检，apply（不加 --fresh）落盘。
topic-split-lists：给每个超限的主题节点出一份清单 topic_splits/lists/ts-NNNN.json（直接子项：子主题和族），批次 batches/topic-split-NNN.txt；
  子代理照 topic-brief.md「拆一个超限的主题节点」写 topic_splits/decisions/ts-NNNN.json：新的下一级主题（一级目录名、中文名、
  一行）和每个子项去哪（留在原节点写 ""）。topic-split-check --split ts-NNNN 自检；topic-split-apply 按顺序落盘（族挪进新主题，
  子主题整棵挪下去，topics.json 加上新主题），层数不限，哪里密就在哪里加一层。
topics-list：第一次建库、apply --fresh 之后跑。按 families.json 给每个产物写一份清单 topic_lists/<产物目录>.json：每个族的 key、族名、
  族的一行、规矩条数、有没有通用查法、建议的主题（子代理写的），以及建议主题的汇总。理主题的子代理照 references/topic-brief.md
  读它，写 topic_decisions/<产物目录>.json。
topics-check：检查一份理主题的决定（给理主题的子代理自检用，apply 也用同一套检查）：每个族恰好出现一次；主题目录每级是
  小写英文、数字和短横线，每个多级主题的上级也要列出（层数不限；任务书建议第一次理主题时 1–2 级）；子主题和族的目录不同名；每个主题有中文名和一行；同一层里中文名不重复；每个节点（产物根和每个主题）
  的直接子项（子主题加直接挂的族，合并后的算一个）不超过 20 个；没有空主题；合并的族存在、不重复出现，并进去的和被并的不能
  都带通用查法（那种列进 review 给人看）；合并之后同一主题下族目录不重名。
用法： py -3 -X utf8 skills/memory-rules/scripts/families.py propose [--rules DIR] [--out DIR] [--threshold 0.3] [--max-size 20]
                                                                       [--attach-min 0.05] [--per-batch 80] [--new-only] [--existing-top 8]
  通用查法的自检（apply 时）写到 work/ 下每次调用自己的临时目录（general_check-*），用完删掉。
       py -3 -X utf8 skills/memory-rules/scripts/families.py apply [--rules DIR] [--out DIR] [--format-only] [--fresh] [--no-topic-decisions]
       py -3 -X utf8 skills/memory-rules/scripts/families.py apply --check --proposals <提案号,…>   归族的子代理自检用（不落盘）
       py -3 -X utf8 skills/memory-rules/scripts/families.py same-groups [--merge DIR] [--merge-per-batch 40]   补并组 → merge/groups/same-*.json
       py -3 -X utf8 skills/memory-rules/scripts/families.py topics-list [--out DIR]
       py -3 -X utf8 skills/memory-rules/scripts/families.py topics-check --product <产物或产物目录> [--out DIR]   理主题的子代理自检用
       py -3 -X utf8 skills/memory-rules/scripts/families.py oversize [--max-rules 20] [--max-children 20]
       py -3 -X utf8 skills/memory-rules/scripts/families.py split-families [--max-rules 20] [--per-batch 80]
       py -3 -X utf8 skills/memory-rules/scripts/families.py topic-split-lists [--max-children 20]
       py -3 -X utf8 skills/memory-rules/scripts/families.py topic-split-check --split ts-NNNN      拆主题节点的子代理自检用
       py -3 -X utf8 skills/memory-rules/scripts/families.py topic-split-apply"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, os, re, shutil, subprocess, tempfile  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rulelib as L  # noqa: E402

CLAIM_CASE = re.compile(r"^(case-[0-9A-Za-z]+)#")
MAX_CHILDREN = 20       # 每个主题节点（含产物根）的直接子项上限
MAX_RULES = 20          # 每个族的规矩条数上限（不算通用查法）
PRODUCT_OF_DIR = {v: k for k, v in L.PRODUCT_DIRS.items()}


def tname(v):
    return v.get("name", "") if isinstance(v, dict) else (v or "")


def tline(v):
    return v.get("line", "") if isinstance(v, dict) else ""


def read_terms(r):
    ks = (r.get("keys") or {}).get("read") or []
    text = " ".join(ks) if ks else " ".join(t.get("read") or "" for t in r.get("triggers") or [])
    return L.ident_terms(text)


def existing_families(a):
    return [] if getattr(a, "fresh", False) else L.jload(os.path.join(a.out, "families.json"), [])


def nearest_families(prop_rules, old, rules, top):
    """和提案最相近的已有族（同一产物）：[(相似度, 族)]，最多 top 个。"""
    if not old:
        return []
    fdocs = []
    for f in old:
        text = f"{f.get('name') or ''} {f.get('line') or ''}"
        t = L.merge_terms(L.ident_terms(text), L.cjk_terms(text),
                          *[read_terms(rules[r]) for r in f["rules"] if r in rules])
        fdocs.append(t)
    ptext = " ".join(r.get("title") or "" for r in prop_rules)
    pdoc = L.merge_terms(L.ident_terms(ptext), L.cjk_terms(ptext), *[read_terms(r) for r in prop_rules])
    idf, _ = L.idf_table(fdocs + [pdoc])
    pv = L.vector(pdoc, idf)
    sc = sorted(((L.cosine(pv, L.vector(d, idf)), k) for k, d in enumerate(fdocs)), key=lambda x: (-x[0], x[1]))
    return [(s, old[k]) for s, k in sc[:top] if s > 0]


def max_num(paths, rx):
    ns = [int(m.group(1)) for p in paths if (m := re.fullmatch(rx, os.path.basename(p)))]
    return max(ns) if ns else 0


def placed_in_decisions(out, alias):
    """已有决定里放进了族的规矩（换成补并后留下的规矩号）。"""
    s = set()
    for dp in glob.glob(os.path.join(out, "decisions", "fam-*.json")):
        for f in L.jload(dp).get("families") or []:
            s |= {alias.get(r, r) for r in f.get("rules") or []}
    return s


def cmd_propose(a):
    alias = load_alias(a.merge)
    pdir, bdir, ddir = (os.path.join(a.out, x) for x in ("proposals", "batches", "decisions"))
    old_props = sorted(glob.glob(os.path.join(pdir, "fam-*.json")))
    if a.new_only:
        pending = [os.path.basename(p)[:-5] for p in old_props if not os.path.isfile(os.path.join(ddir, os.path.basename(p)))]
        if pending:
            raise SystemExit(f"已有 {len(pending)} 个提案还没有决定（{', '.join(pending[:8])}…）：先写完决定、apply 之后再出下一轮")
    elif glob.glob(os.path.join(ddir, "fam-*.json")):
        raise SystemExit(f"{ddir} 里已有决定：从头出提案会和它们对不上。要出下一轮用 --new-only；真要从头来，先把 proposals/、"
                         "batches/、decisions/ 挪走")
    old = existing_families(a) if a.new_only else []
    all_rules = L.load_rules(a.rules)
    # 通用查法不参加聚类（它们由归族的决定挂到族上）；--new-only 时已经在族里、或已有决定放进了族的规矩也不再出
    done = ({rid for f in old for rid in f["rules"]} | placed_in_decisions(a.out, alias)) if a.new_only else set()
    rules = {k: v for k, v in all_rules.items() if k not in done and not v.get("general")}
    by_prod = collections.defaultdict(list)
    for rid, r in rules.items():
        by_prod[r.get("product")].append(rid)
    if a.new_only:      # 下一轮：提案号、批次号接在已有的后面，已有的提案、批次和决定都不动
        first_prop = max_num(old_props, r"fam-(\d+)\.json") + 1
        first_batch = max_num(glob.glob(os.path.join(bdir, "family-*.txt")), r"family-(\d+)\.txt") + 1
        rnd = max([L.jload(p).get("round") or 1 for p in old_props] or [0]) + 1
    else:
        for p in (pdir, bdir):
            if os.path.exists(p):
                shutil.rmtree(p)
        first_prop, first_batch, rnd = 1, 1, 1
    os.makedirs(pdir, exist_ok=True)
    os.makedirs(bdir, exist_ok=True)
    props, sims_all, sizes, attached, alone = [], [], collections.Counter(), 0, 0
    for prod in sorted(by_prod, key=str):
        ids = sorted(by_prod[prod])
        terms = [read_terms(rules[i]) for i in ids]
        idf, _ = L.idf_table(terms)
        vecs = [L.vector(t, idf) for t in terms]
        sims = L.pair_sims(vecs)
        sims_all += list(sims.values())
        parts = [m for m, _ in L.split_by_threshold(list(range(len(ids))), sims, a.threshold, a.max_size)]
        fams = [m for m in parts if len(m) > 1]
        for m in [m for m in parts if len(m) == 1]:
            i = m[0]
            best, bj = 0.0, None
            for j, f in enumerate(fams):
                if len(f) >= a.max_size:
                    continue
                avg = sum(sims.get((min(i, x), max(i, x)), 0.0) for x in f) / len(f)
                if avg > best:
                    best, bj = avg, j
            if bj is not None and best > a.attach_min:
                fams[bj].append(i)
                attached += 1
            else:
                fams.append([i])
                alone += 1
        for f in fams:
            f.sort()
            pair = [sims.get((x, y), 0.0) for k, x in enumerate(f) for y in f[k + 1:]]
            sizes[len(f)] += 1
            props.append({"product": prod, "avg_similarity": round(sum(pair) / len(pair), 3) if pair else None,
                          "rules": [{"id": ids[i], "title": rules[ids[i]].get("title"), "product": prod,
                                     "triggers": rules[ids[i]].get("triggers"), "keys": rules[ids[i]].get("keys")} for i in f]})
    attached_old = []
    for k, p in enumerate(props, first_prop):
        p["proposal"] = f"fam-{k:04d}"
        o = {"proposal": p["proposal"], "round": rnd, "product": p["product"], "avg_similarity": p["avg_similarity"], "rules": p["rules"]}
        if a.new_only:      # 增量：附上同一产物下最相近的已有族，规矩可以归进去（族的 topic、dir 写成和已有的一样）
            near = nearest_families([rules[r["id"]] for r in p["rules"]], [f for f in old if f["product"] == p["product"]], all_rules,
                                    a.existing_top)
            tps = L.jload(os.path.join(a.out, "topics.json"), {}).get(prod_dir_of(p["product"]), {})
            o["existing_families"] = [{"topic": f["topic"], "topic_name": tname(tps.get(f["topic"])), "dir": f["dir"], "name": f["name"],
                                       "line": f["line"], "similarity": round(s, 3)} for s, f in near]
            attached_old.append(len(near))
        L.jsave(os.path.join(a.out, "proposals", p["proposal"] + ".json"), o)
    batches, cur, n = [], [], 0
    for p in props:
        m = len(p["rules"])
        if cur and n + m > a.per_batch:
            batches.append(cur)
            cur, n = [], 0
        cur.append(L.relpath(os.path.join(a.out, "proposals", p["proposal"] + ".json")))
        n += m
    if cur:
        batches.append(cur)
    names = []
    for k, b in enumerate(batches, first_batch):
        names.append(f"family-{k:03d}.txt")
        with open(os.path.join(bdir, names[-1]), "w", encoding="utf-8", newline="\n") as f:
            f.write("".join(x + "\n" for x in b))
    rep = {"params": L.rel_params(a), "round": rnd, "rules": len(rules), "by_product": {str(p): len(v) for p, v in by_prod.items()},
           "proposals": len(props), "proposal_ids": [props[0]["proposal"], props[-1]["proposal"]] if props else [],
           "family_sizes": dict(sorted(sizes.items())), "singles_attached": attached, "singles_alone": alone,
           "pair_similarity_quantiles": L.quantiles(sims_all), "batches": names,
           "existing_families_attached": dict(collections.Counter(attached_old)) if a.new_only else None}
    L.jsave(os.path.join(a.out, "propose_report.json"), rep)
    L.jsave(os.path.join(a.out, f"propose_report_r{rnd}.json"), rep)
    print(f"第 {rnd} 轮：" + (f"提案 {props[0]['proposal']}–{props[-1]['proposal']}，批次 {names[0]}–{names[-1]}；" if props else ""))
    print(f"规矩 {len(rules)} 条（{rep['by_product']}）→ 提案 {len(props)} 个，分 {len(batches)} 批；"
          f"落单并进别的族 {attached} 条、自成一族 {alone} 条" + (f"；每个提案附的已有族个数 {rep['existing_families_attached']}" if a.new_only else ""))
    print("族大小分布：", rep["family_sizes"])
    print("相似度分位数：", rep["pair_similarity_quantiles"])


# ---------------------------------------------------------------- 理主题

def prod_dir_of(x):
    return L.PRODUCT_DIRS.get(x, x)


def has_general(f, rules):
    return bool(f.get("general")) or any((rules.get(r) or {}).get("general") for r in f["rules"])


def check_topic_decision(fams, d, rules, prod_dir):
    """理主题的决定 d 对这个产物的族 fams（带 key）。返回错误列表。"""
    bad = []
    keys = {f["key"]: f for f in fams}
    tops = d.get("topics") or []
    tdirs = {}
    for k, t in enumerate(tops, 1):
        w = f"主题 {k}"
        dr = (t.get("dir") or "").strip()
        segs = dr.split("/")
        if not dr or not all(L.DIR_RX.match(s) for s in segs):
            bad.append(f"{w}：目录「{dr}」每级要是小写英文、数字和短横线（用 / 分级）")
        for x in ("name", "line"):
            if not (t.get(x) or "").strip():
                bad.append(f"{w}（{dr}）：{x} 不能为空")
        if dr in tdirs:
            bad.append(f"{w}：主题目录 {dr} 列了两次")
        tdirs[dr] = t
    for dr in tdirs:
        if "/" in dr and dr.rsplit("/", 1)[0] not in tdirs:
            bad.append(f"主题 {dr} 的上级 {dr.rsplit('/', 1)[0]} 没有列出")
    by_level = collections.defaultdict(list)
    for dr, t in tdirs.items():
        by_level[dr.rsplit("/", 1)[0] if "/" in dr else ""].append(t.get("name"))
    for parent, ns in by_level.items():
        for n_, c in collections.Counter(ns).items():
            if c > 1:
                bad.append(f"同一层（{parent or '产物根'}）里有 {c} 个主题都叫「{n_}」")
    seen = collections.Counter()
    topic_of = {}
    for x in d.get("families") or []:
        k_ = x.get("family")
        seen[k_] += 1
        if k_ not in keys:
            bad.append(f"族 {k_} 不在清单里")
        if x.get("topic") not in tdirs:
            bad.append(f"族 {k_} 的主题 {x.get('topic')} 没有在 topics 里列出")
        topic_of[k_] = x.get("topic")
    for k_ in keys:
        if seen[k_] == 0:
            bad.append(f"族 {k_} 没有归到主题")
        elif seen[k_] > 1:
            bad.append(f"族 {k_} 出现了 {seen[k_]} 次")
    merged_away, in_merge = {}, collections.Counter()
    for k, m in enumerate(d.get("merge") or [], 1):
        into, frm = m.get("into"), m.get("from") or []
        if not (m.get("reason") or "").strip():
            bad.append(f"合并 {k}：要写理由")
        if into not in keys or not frm or any(x not in keys for x in frm):
            bad.append(f"合并 {k}：into / from 要是清单里的族（{into} ← {frm}）")
            continue
        for x in [into] + frm:
            in_merge[x] += 1
        if sum(has_general(keys[x], rules) for x in [into] + frm) > 1:
            bad.append(f"合并 {k}：{into} ← {frm} 里有两个以上的族带通用查法，不能自动合并，列进 review")
        for x in frm:
            merged_away[x] = into
    for x, c in in_merge.items():
        if c > 1:
            bad.append(f"族 {x} 出现在 {c} 个合并里")
    # 合并之后：每个节点的直接子项、同一主题下族目录不重名、没有空主题
    children = collections.Counter()
    fam_dirs = collections.defaultdict(list)
    for k_, t in topic_of.items():
        if k_ in merged_away or k_ not in keys:
            continue
        children[t] += 1
        fam_dirs[t].append(keys[k_]["dir"])
    for dr in tdirs:
        parent = dr.rsplit("/", 1)[0] if "/" in dr else ""
        children[parent] += 1
    for node, c in children.items():
        if c > MAX_CHILDREN:
            bad.append(f"{node or '产物根'} 的直接子项有 {c} 个，超过 {MAX_CHILDREN}")
    for dr in tdirs:
        if children[dr] == 0:
            bad.append(f"主题 {dr} 下面什么都没有")
    for t, ds in fam_dirs.items():
        for n_, c in collections.Counter(ds).items():
            if c > 1:
                bad.append(f"主题 {t} 下有 {c} 个族的目录都叫 {n_}（要么合并，要么改目录名）")
    for dr in tdirs:                   # 子主题和族在同一个目录下，名字不能撞
        parent = dr.rsplit("/", 1)[0] if "/" in dr else ""
        if dr.split("/")[-1] in fam_dirs.get(parent, []):
            bad.append(f"主题 {parent} 下的子主题 {dr.split('/')[-1]} 和一个族的目录同名")
    for k, rv in enumerate(d.get("review") or [], 1):
        if not all(x in keys for x in rv.get("families") or []) or not (rv.get("reason") or "").strip():
            bad.append(f"review {k}：families 要是清单里的族，要写理由")
    return bad


def apply_topic_decision(fams, d):
    """把理主题的决定用到这个产物的族上：覆盖主题、合并族。返回 (新的族列表, {主题目录: {name, line}})。"""
    keys = {f["key"]: f for f in fams}
    topic_of = {x["family"]: x["topic"] for x in d.get("families") or []}
    away = set()
    for m in d.get("merge") or []:
        into = keys[m["into"]]
        for x in m["from"]:
            src = keys[x]
            into["rules"] += [r for r in src["rules"] if r not in into["rules"]]
            into["general"] = into.get("general") or src.get("general")
            into["same"] = (into.get("same") or []) + (src.get("same") or [])
            into.setdefault("merged_from", []).append(x)
            if src.get("joined_from"):
                into.setdefault("joined_from", []).extend(src["joined_from"])
            away.add(x)
    out = []
    for f in fams:
        if f["key"] in away:
            continue
        f["topic"] = topic_of[f["key"]]
        out.append(f)
    return out, {t["dir"]: {"name": t["name"], "line": t["line"]} for t in d.get("topics") or []}


def cmd_topics_list(a):
    fams = L.jload(os.path.join(a.out, "families.json"))
    topics = L.jload(os.path.join(a.out, "topics.json"), {})
    rules = L.load_rules(a.rules) if os.path.isdir(a.rules) else {}
    by_prod = collections.defaultdict(list)
    for f in fams:
        by_prod[f.get("product_dir") or prod_dir_of(f["product"])].append(f)
    os.makedirs(os.path.join(a.out, "topic_lists"), exist_ok=True)
    for pd, fl in sorted(by_prod.items()):
        names = topics.get(pd, {})
        sug = collections.Counter(f["topic"] for f in fl)
        o = {"product": PRODUCT_OF_DIR.get(pd, pd), "product_dir": pd, "families_count": len(fl), "max_children": MAX_CHILDREN,
             "families": [{"family": f["key"], "name": f["name"], "line": f["line"], "rules": len(f["rules"]),
                           "general": has_general(f, rules), "dir": f["dir"],
                           "suggested_topic": {"dir": f["topic"], "name": tname(names.get(f["topic"]))}} for f in fl],
             "suggested_topics": [{"dir": t, "name": tname(names.get(t)), "families": c} for t, c in sorted(sug.items())]}
        L.jsave(os.path.join(a.out, "topic_lists", pd + ".json"), o)
        print(f"{pd}：族 {len(fl)} 个，建议的主题 {len(sug)} 个 → topic_lists/{pd}.json")


def cmd_topics_check(a):
    pd = prod_dir_of(a.product)
    lst = L.jload(os.path.join(a.out, "topic_lists", pd + ".json"))
    dp = os.path.join(a.out, "topic_decisions", pd + ".json")
    if not os.path.isfile(dp):
        raise SystemExit(f"没有 {dp}")
    fams = [{"key": x["family"], "dir": x["dir"], "rules": [], "general": x["general"]} for x in lst["families"]]
    bad = check_topic_decision(fams, L.jload(dp), {}, pd)
    for b in bad[:80]:
        print("  - " + b)
    d = L.jload(dp)
    print(f"{pd}：族 {len(fams)} 个，主题 {len(d.get('topics') or [])} 个，合并 {len(d.get('merge') or [])} 处，review {len(d.get('review') or [])} 处；"
          f"违反 {len(bad)} 处")
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- 补并：族里标出的「同一条」

def load_alias(merge_dir):
    """补并之后被并掉的规矩号 → 留下的规矩号（merge_map.json 里以规矩号为临时号、指向别的规矩号的条目；串着的取到底）。"""
    mp = L.jload(os.path.join(merge_dir, "merge_map.json"), {}) if merge_dir else {}
    alias = {k: v for k, v in mp.items() if k.startswith("rule-") and v != k}

    def final(x):
        seen = set()
        while x in alias and x not in seen:
            seen.add(x)
            x = alias[x]
        return x
    return {k: final(k) for k in alias}


def dedupe(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def check_same(f, rs, w, bad):
    """族里标出的「同一条」：每组至少两条不同的规矩、都在这个族里、一条规矩不出现在两组里、要写理由。"""
    used = collections.Counter()
    for j, s in enumerate(f.get("same") or [], 1):
        grp = s.get("rules") if isinstance(s, dict) else None
        if not isinstance(grp, list) or len(set(grp)) < 2:
            bad.append(f"{w} same 第 {j} 组：rules 至少要两条不同的规矩")
            grp = grp if isinstance(grp, list) else []
        if not isinstance(s, dict) or not (s.get("reason") or "").strip():
            bad.append(f"{w} same 第 {j} 组：要写理由")
        for r in set(grp):
            if r not in rs:
                bad.append(f"{w} same 第 {j} 组：{r} 不在这个族的 rules 里")
            used[r] += 1
    for r, c in used.items():
        if c > 1:
            bad.append(f"{w}：{r} 出现在 {c} 个 same 组里")


def cmd_same_groups(a):
    """把各提案决定里标出的 same 组做成合并用的组文件 merge/groups/same-NNNN.json（成员都是已有规矩，带全文，标 existing；
    成员顺序照 same 里写的，排在前面的那条合并后留号），并出批次清单 merge/batches/same-NNN.txt（每批规矩合计不超过 --merge-per-batch）。
    组号稳定：每组按「族的 key + same 里原样写的规矩号」认；以前出过的组，组文件、组号都不动；新标出的组号接在已有最大号后面
    （所以第二轮归族的决定加进来之后，第一轮的组号不变，新的往后排）。决定改了、不再标的旧组：还没有合并决定的删掉，已有合并决定的
    留着并报出来。批次清单只列还没有合并决定、也没列进以前任何 same 批次的组，编号接在已有的后面。"""
    rules = L.load_rules(a.rules)
    alias = load_alias(a.merge)
    gdir, bdir, mdir = (os.path.join(a.merge, x) for x in ("groups", "batches", "decisions"))
    os.makedirs(gdir, exist_ok=True)
    os.makedirs(bdir, exist_ok=True)
    old = {}
    for p in glob.glob(os.path.join(gdir, "same-*.json")):
        g = L.jload(p)
        old[(g.get("family"), tuple(g.get("marked") or [m["tmp"] for m in g["members"]]))] = g["group"]
    nxt = max_num(glob.glob(os.path.join(gdir, "same-*.json")), r"same-(\d+)\.json") + 1
    seen, new, skipped = set(), [], []
    for pp in sorted(glob.glob(os.path.join(a.out, "proposals", "fam-*.json"))):
        pid = os.path.basename(pp)[:-5]
        dp = os.path.join(a.out, "decisions", pid + ".json")
        if not os.path.isfile(dp):
            continue
        prod = L.jload(pp)["product"]
        for k, f in enumerate(L.jload(dp).get("families") or [], 1):
            for s in f.get("same") or []:
                marked = list(s.get("rules") or []) if isinstance(s, dict) else []
                sig = (f"{pid}#{k}", tuple(marked))
                if sig in old:
                    seen.add(sig)
                    continue
                rs = dedupe([alias.get(r, r) for r in marked])
                miss = [r for r in rs if r not in rules]
                if len(rs) < 2 or miss:
                    skipped.append({"family": sig[0], "rules": marked, "why": "已经并过" if len(rs) < 2 else f"规矩不在：{miss}"})
                    continue
                g = {"group": f"same-{nxt:04d}", "product": prod, "source": "same", "family": sig[0], "family_name": f.get("name"),
                     "reason": s.get("reason"), "marked": marked, "threshold": None, "pairs": [],
                     "members": [{"tmp": r, "case": None, "index": None, "existing": True, "rule": rules[r]} for r in rs]}
                nxt += 1
                L.jsave(os.path.join(gdir, g["group"] + ".json"), g)
                new.append(g["group"])
    stale_kept, stale_removed = [], []
    for sig, gid in old.items():
        if sig in seen:
            continue
        if os.path.isfile(os.path.join(mdir, gid + ".json")):
            stale_kept.append(gid)
        else:
            os.remove(os.path.join(gdir, gid + ".json"))
            stale_removed.append(gid)
    bfiles = glob.glob(os.path.join(bdir, "same-*.txt"))
    listed = {os.path.basename(x.strip()) for b in bfiles for x in io.open(b, encoding="utf-8") if x.strip()}
    pending = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(gdir, "same-*.json"))
                     if os.path.basename(p) not in listed and not os.path.isfile(os.path.join(mdir, os.path.basename(p))))
    batches, cur, m = [], [], 0
    for gid in pending:
        n_ = len(L.jload(os.path.join(gdir, gid + ".json"))["members"])
        if cur and m + n_ > a.merge_per_batch:
            batches.append(cur)
            cur, m = [], 0
        cur.append(L.relpath(os.path.join(gdir, gid + ".json")))
        m += n_
    if cur:
        batches.append(cur)
    first_b = max_num(bfiles, r"same-(\d+)\.txt") + 1
    names = []
    for n, b in enumerate(batches, first_b):
        names.append(f"same-{n:03d}.txt")
        with open(os.path.join(bdir, names[-1]), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(x + "\n" for x in b))
    total = len(glob.glob(os.path.join(gdir, "same-*.json")))
    print(f"补并组：已有 {len(seen)} 个不动，新出 {len(new)} 个" + (f"（{new[0]}–{new[-1]}）" if new else "") +
          f"，现在共 {total} 个；新批次 {len(names)} 个" + (f"（{names[0]}–{names[-1]}，{len(pending)} 组）" if names else "") +
          f"；跳过 {len(skipped)} 组")
    if stale_removed or stale_kept:
        print(f"  决定里不再标的旧组：删掉 {stale_removed}；已有合并决定、留着的 {stale_kept}（要人看）")
    for s in skipped[:10]:
        print("  跳过：", s)


# ---------------------------------------------------------------- 超限的节点就地拆（树按需加深）

def n_rules(f, rules):
    """族里的规矩条数（不算通用查法）。"""
    return sum(1 for r in f["rules"] if not (rules.get(r) or {}).get("general"))


def tree_children(fams):
    """{产物目录: {节点: {"topics": [子主题的完整目录…], "families": [直接挂的族…]}}}；节点 "" 是产物根。"""
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: {"topics": [], "families": []}))
    for f in fams:
        pd = f.get("product_dir") or prod_dir_of(f["product"])
        segs = f["topic"].split("/")
        out[pd][f["topic"]]["families"].append(f)
        for k in range(1, len(segs) + 1):
            par, ch = "/".join(segs[:k - 1]), "/".join(segs[:k])
            if ch not in out[pd][par]["topics"]:
                out[pd][par]["topics"].append(ch)
    return out


def find_oversize(fams, rules, max_rules, max_children):
    big_f = [(f, n_rules(f, rules)) for f in fams if n_rules(f, rules) > max_rules]
    big_t = []
    for pd, nodes in sorted(tree_children(fams).items()):
        for node, ch in sorted(nodes.items()):
            n = len(ch["topics"]) + len(ch["families"])
            if n > max_children:
                big_t.append((pd, node, n))
    return big_f, big_t


def topic_label(topics_pd, t):
    segs = t.split("/") if t else []
    return " / ".join(tname(topics_pd.get("/".join(segs[:k]))) or segs[k - 1] for k in range(1, len(segs) + 1))


def cmd_oversize(a):
    """列出超限的节点：规矩超过 --max-rules 条的族；直接子项（子主题加直接挂的族）超过 --max-children 个的主题节点（含产物根）。"""
    fams = L.jload(os.path.join(a.out, "families.json"))
    topics = L.jload(os.path.join(a.out, "topics.json"), {})
    rules = L.load_rules(a.rules)
    big_f, big_t = find_oversize(fams, rules, a.max_rules, a.max_children)
    rep = {"max_rules": a.max_rules, "max_children": a.max_children,
           "families": [{"family": f["key"], "short": f.get("short"), "product": f["product"], "topic": f["topic"], "dir": f["dir"],
                         "name": f["name"], "rules": n} for f, n in big_f],
           "topics": [{"product_dir": pd, "node": node, "name": topic_label(topics.get(pd, {}), node) or "（产物根）", "children": n}
                      for pd, node, n in big_t]}
    L.jsave(os.path.join(a.out, "oversize.json"), rep)
    print(f"规矩超过 {a.max_rules} 条的族 {len(big_f)} 个；直接子项超过 {a.max_children} 个的主题节点 {len(big_t)} 个")
    for x in rep["families"]:
        print(f"  族 {x['short']} {x['name']}（{x['rules']} 条）  {L.PRODUCT_DIRS.get(x['product'], x['product'])}/{x['topic']}/{x['dir']}  {x['family']}")
    for x in rep["topics"]:
        print(f"  主题 {x['product_dir']}/{x['node'] or '（产物根）'} {x['name']}：直接子项 {x['children']} 个")
    sys.exit(1 if big_f or big_t else 0)


def pending_proposals(out):
    pdir, ddir = os.path.join(out, "proposals"), os.path.join(out, "decisions")
    return [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(pdir, "fam-*.json")))
            if not os.path.isfile(os.path.join(ddir, os.path.basename(p)))]


def write_batches(out, props, per_batch, prefix="family"):
    bdir = os.path.join(out, "batches")
    os.makedirs(bdir, exist_ok=True)
    batches, cur, n = [], [], 0
    for p in props:
        m = len(p["rules"])
        if cur and n + m > per_batch:
            batches.append(cur)
            cur, n = [], 0
        cur.append(L.relpath(os.path.join(out, "proposals", p["proposal"] + ".json")))
        n += m
    if cur:
        batches.append(cur)
    first = max_num(glob.glob(os.path.join(bdir, f"{prefix}-*.txt")), prefix + r"-(\d+)\.txt") + 1
    names = []
    for k, b in enumerate(batches, first):
        names.append(f"{prefix}-{k:03d}.txt")
        with open(os.path.join(bdir, names[-1]), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(x + "\n" for x in b))
    return names


def cmd_split_families(a):
    """给每个超限的族出一个拆分提案（就是它的全部规矩，带 split_of、原来的主题、原族的通用查法、同主题下别的族的目录名），
    编号接在已有提案后面、作为新的一轮；子代理照 family-brief.md「拆一个超限的族」写决定，apply（不加 --fresh）落盘时原族被替换。"""
    pend = pending_proposals(a.out)
    if pend:
        raise SystemExit(f"已有 {len(pend)} 个提案还没有决定（{', '.join(pend[:8])}…）：先写完决定、apply 之后再拆")
    fams = L.jload(os.path.join(a.out, "families.json"))
    topics = L.jload(os.path.join(a.out, "topics.json"), {})
    rules = L.load_rules(a.rules)
    big_f, _ = find_oversize(fams, rules, a.max_rules, a.max_children)
    if not big_f:
        print(f"没有规矩超过 {a.max_rules} 条的族")
        return
    old_props = glob.glob(os.path.join(a.out, "proposals", "fam-*.json"))
    nxt = max_num(old_props, r"fam-(\d+)\.json") + 1
    rnd = max([L.jload(p).get("round") or 1 for p in old_props] or [0]) + 1
    props = []
    for k, (f, n) in enumerate(big_f, nxt):
        pd = f.get("product_dir") or prod_dir_of(f["product"])
        gens = [x for x in dedupe([f.get("general")] + [r for r in f["rules"] if (rules.get(r) or {}).get("general")]) if x and x in rules]
        o = {"proposal": f"fam-{k:04d}", "round": rnd, "product": f["product"], "split_of": f["key"],
             "split_reason": f"族里有 {n} 条规矩，超过 {a.max_rules} 条",
             "family": {"short": f.get("short"), "name": f["name"], "line": f["line"], "dir": f["dir"]},
             "topic": {"dir": f["topic"], "name": tname(topics.get(pd, {}).get(f["topic"]))},
             "generals": [{"id": g, "title": rules[g].get("title")} for g in gens],
             "sibling_dirs": sorted({x["dir"] for x in fams if x is not f and x["product"] == f["product"] and x["topic"] == f["topic"]} |
                                    {t.split("/")[-1] for t in topics.get(pd, {}) if t.rsplit("/", 1)[0] == f["topic"] and "/" in t}),
             "avg_similarity": None,
             "rules": [{"id": r, "title": rules[r].get("title"), "product": f["product"], "triggers": rules[r].get("triggers"),
                        "keys": rules[r].get("keys")} for r in f["rules"] if r in rules and not rules[r].get("general")]}
        L.jsave(os.path.join(a.out, "proposals", o["proposal"] + ".json"), o)
        props.append(o)
    names = write_batches(a.out, props, a.per_batch)
    print(f"第 {rnd} 轮（拆族）：提案 {props[0]['proposal']}–{props[-1]['proposal']} 共 {len(props)} 个，批次 {', '.join(names)}")


def check_topic_split(lst, d, fams, topics, max_children):
    """一份「拆超限主题节点」的决定对当前的族和主题。返回错误列表。"""
    errs = []
    pd, node = lst["product_dir"], lst["node"]
    cur = tree_children(fams)[pd][node]
    byk = {f["key"]: f for f in fams}
    cur_items = {("topic", t) for t in cur["topics"]} | {("family", f["key"]) for f in cur["families"]}
    lst_items = {("topic", x["dir"]) if x["kind"] == "topic" else ("family", x["family"]) for x in lst["children"]}
    if cur_items != lst_items:
        errs.append("清单过时了：这个节点现在的直接子项和清单对不上，要重出清单")
    if d.get("split") != lst["split"]:
        errs.append(f"split 应为 {lst['split']}")
    new = {}
    for k, t in enumerate(d.get("topics") or [], 1):
        seg = (t.get("dir") or "").strip()
        if not seg or "/" in seg or not L.DIR_RX.match(seg):
            errs.append(f"新主题 {k}：dir「{seg}」要是一级目录名（小写英文、数字和短横线，不带 /）")
        for x in ("name", "line"):
            if not (t.get(x) or "").strip():
                errs.append(f"新主题 {k}（{seg}）：{x} 不能为空")
        if seg in new:
            errs.append(f"新主题 {seg} 列了两次")
        new[seg] = t
    if not new:
        errs.append("至少要新起一个下一级主题")
    assign = {}
    for k, x in enumerate(d.get("assign") or [], 1):
        item = ("family", x["family"]) if x.get("family") else ("topic", x.get("topic_dir"))
        if item not in lst_items:
            errs.append(f"assign {k}：{item[1]} 不是这个节点的直接子项")
        if item in assign:
            errs.append(f"assign {k}：{item[1]} 出现了两次")
        dest = x.get("topic") or ""
        if dest and dest not in new:
            errs.append(f"assign {k}：{item[1]} 要去的主题 {dest} 没有在 topics 里列出")
        assign[item] = dest
    for it in sorted(lst_items - set(assign)):
        errs.append(f"{it[1]} 没有在 assign 里")

    def nm(it):        # 子项在目录树里的名字：族的目录名、子主题的最后一级
        return (byk[it[1]]["dir"] if it[1] in byk else it[1]) if it[0] == "family" else it[1].split("/")[-1]
    stay = [it for it, dest in assign.items() if not dest and it in lst_items]
    if len(new) + len(stay) > max_children:
        errs.append(f"拆完之后这个节点的直接子项还有 {len(new) + len(stay)} 个，超过 {max_children}")
    stay_names = {nm(it) for it in stay}
    for seg, t in new.items():
        mem = [it for it, dest in assign.items() if dest == seg and it in lst_items]
        if not mem:
            errs.append(f"新主题 {seg} 下面什么都没有")
        if len(mem) > max_children:
            errs.append(f"新主题 {seg} 的直接子项有 {len(mem)} 个，超过 {max_children}")
        for n_, c in collections.Counter(nm(it) for it in mem).items():
            if c > 1:
                errs.append(f"新主题 {seg} 下有 {c} 个子项都叫 {n_}")
        if seg in stay_names:
            errs.append(f"新主题的目录名 {seg} 和留在这个节点下的子项同名")
    tp = topics.get(pd, {})
    names = [t.get("name") for t in new.values()] + [tname(tp.get(it[1])) for it in stay if it[0] == "topic"]
    for n_, c in collections.Counter(names).items():
        if n_ and c > 1:
            errs.append(f"拆完之后同一层里有 {c} 个主题都叫「{n_}」")
    return errs


def apply_topic_split(fams, topics_pd, lst, d):
    node = lst["node"]
    pre = node + "/" if node else ""
    pd = lst["product_dir"]
    mine = [f for f in fams if (f.get("product_dir") or prod_dir_of(f["product"])) == pd]
    byk = {f["key"]: f for f in mine}
    for x in d.get("assign") or []:
        dest = x.get("topic") or ""
        if not dest:
            continue
        if x.get("family"):
            byk[x["family"]]["topic"] = pre + dest
            continue
        D = x["topic_dir"]
        nd = pre + dest + "/" + D.split("/")[-1]
        for f in mine:
            if f["topic"] == D or f["topic"].startswith(D + "/"):
                f["topic"] = nd + f["topic"][len(D):]
        for k in [k for k in topics_pd if k == D or k.startswith(D + "/")]:
            topics_pd[nd + k[len(D):]] = topics_pd.pop(k)
    for t in d.get("topics") or []:
        topics_pd[pre + t["dir"]] = {"name": t["name"], "line": t["line"]}


def cmd_topic_split_lists(a):
    """给每个超限的主题节点出一份清单 topic_splits/lists/ts-NNNN.json（它的直接子项：子主题和族），批次清单
    batches/topic-split-NNN.txt；子代理照 topic-brief.md「拆一个超限的主题节点」写 topic_splits/decisions/ts-NNNN.json。
    还有没落盘的清单的节点不重出。"""
    fams = L.jload(os.path.join(a.out, "families.json"))
    topics = L.jload(os.path.join(a.out, "topics.json"), {})
    rules = L.load_rules(a.rules)
    applied = set(load_state(a.out).get("topic_splits_applied") or [])
    ldir, ddir = os.path.join(a.out, "topic_splits", "lists"), os.path.join(a.out, "topic_splits", "decisions")
    os.makedirs(ldir, exist_ok=True)
    os.makedirs(ddir, exist_ok=True)
    pending = {}
    for p in glob.glob(os.path.join(ldir, "ts-*.json")):
        x = L.jload(p)
        if x["split"] not in applied:
            pending[(x["product_dir"], x["node"])] = x["split"]
    _, big_t = find_oversize(fams, rules, a.max_rules, a.max_children)
    tc = tree_children(fams)
    nxt = max_num(glob.glob(os.path.join(ldir, "ts-*.json")), r"ts-(\d+)\.json") + 1
    made = []
    for pd, node, n in big_t:
        if (pd, node) in pending:
            print(f"  {pd}/{node or '（产物根）'}：已有没落盘的清单 {pending[(pd, node)]}，不重出")
            continue
        ch, tp = tc[pd][node], topics.get(pd, {})

        def under(t):
            return [f for f in fams if (f.get("product_dir") or prod_dir_of(f["product"])) == pd and (f["topic"] == t or f["topic"].startswith(t + "/"))]
        items = [{"kind": "topic", "dir": t, "seg": t.split("/")[-1], "name": tname(tp.get(t)), "line": tline(tp.get(t)),
                  "children": len(tc[pd][t]["topics"]) + len(tc[pd][t]["families"]), "families": len(under(t)),
                  "rules": sum(n_rules(f, rules) for f in under(t))} for t in ch["topics"]]
        items += [{"kind": "family", "family": f["key"], "short": f.get("short"), "name": f["name"], "line": f["line"], "dir": f["dir"],
                   "rules": n_rules(f, rules), "general": has_general(f, rules)} for f in ch["families"]]
        lst = {"split": f"ts-{nxt:04d}", "product": PRODUCT_OF_DIR.get(pd, pd), "product_dir": pd, "node": node,
               "node_name": topic_label(tp, node) or "（产物根）", "node_line": tline(tp.get(node)) if node else "",
               "max_children": a.max_children, "children_count": n, "children": items}
        L.jsave(os.path.join(ldir, lst["split"] + ".json"), lst)
        made.append(lst["split"])
        nxt += 1
    bdir = os.path.join(a.out, "batches")
    os.makedirs(bdir, exist_ok=True)
    nb = max_num(glob.glob(os.path.join(bdir, "topic-split-*.txt")), r"topic-split-(\d+)\.txt") + 1
    names = []
    for k in range(0, len(made), a.lists_per_batch):
        names.append(f"topic-split-{nb:03d}.txt")
        with open(os.path.join(bdir, names[-1]), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(L.relpath(os.path.join(ldir, s + ".json")) + "\n" for s in made[k:k + a.lists_per_batch]))
        nb += 1
    print(f"超限的主题节点 {len(big_t)} 个；新出清单 {len(made)} 份" + (f"（{made[0]}–{made[-1]}），批次 {', '.join(names)}" if made else ""))


def cmd_topic_split_check(a):
    lst = L.jload(os.path.join(a.out, "topic_splits", "lists", a.split + ".json"))
    dp = os.path.join(a.out, "topic_splits", "decisions", a.split + ".json")
    if not os.path.isfile(dp):
        raise SystemExit(f"没有 {dp}")
    errs = check_topic_split(lst, L.jload(dp), L.jload(os.path.join(a.out, "families.json")),
                             L.jload(os.path.join(a.out, "topics.json"), {}), lst.get("max_children") or a.max_children)
    for e in errs[:60]:
        print("  - " + e)
    print(f"{a.split}（{lst['product_dir']}/{lst['node'] or '（产物根）'}）：违反 {len(errs)} 处")
    sys.exit(1 if errs else 0)


def cmd_topic_split_apply(a):
    """按顺序落盘 topic_splits/decisions/ 里还没落过的决定：族挪进新的下一级主题，子主题整棵挪下去，topics.json 加上新主题。
    每份先对当前状态再查一遍，有一处不对就都不落。"""
    st = load_state(a.out)
    applied = list(st.get("topic_splits_applied") or [])
    fams = L.jload(os.path.join(a.out, "families.json"))
    topics = L.jload(os.path.join(a.out, "topics.json"), {})
    todo = [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(a.out, "topic_splits", "decisions", "ts-*.json")))]
    todo = [s for s in todo if s not in applied]
    for s in todo:
        lst = L.jload(os.path.join(a.out, "topic_splits", "lists", s + ".json"))
        d = L.jload(os.path.join(a.out, "topic_splits", "decisions", s + ".json"))
        errs = check_topic_split(lst, d, fams, topics, lst.get("max_children") or a.max_children)
        if errs:
            print(f"{s} 有 {len(errs)} 处不对，都没有落盘：")
            for e in errs[:40]:
                print("  - " + e)
            sys.exit(1)
        apply_topic_split(fams, topics.setdefault(lst["product_dir"], {}), lst, d)
        print(f"  {s}：{lst['product_dir']}/{lst['node'] or '（产物根）'} 下新起 {len(d.get('topics') or [])} 个主题")
    if not todo:
        print("没有要落盘的拆主题决定")
        return
    L.jsave(os.path.join(a.out, "families.json"), fams)
    L.jsave(os.path.join(a.out, "topics.json"), topics)
    st["topic_splits_applied"] = applied + todo
    L.jsave(os.path.join(a.out, "apply_state.json"), st)
    _, big_t = find_oversize(fams, L.load_rules(a.rules), a.max_rules, a.max_children)
    print(f"落盘 {len(todo)} 份；还超限的主题节点 {len(big_t)} 个" + ("（再跑 topic-split-lists）" if big_t else ""))


# ---------------------------------------------------------------- apply

def join_same_key(fams, into=None):
    """同一产物、同一主题、同一目录名的族并成一个，并进排在前面的那个（into 是已有的族，先放进去）：同一批里子代理有意写成
    同名的、下一轮归进已有族的都这样并。规矩接在后面，same 合起来；两边都带通用查法时，后一条作为族里的另一条通用查法放进
    rules（导出时同样呈现为通用查法），不丢。返回 (并完的族, 并了几个, [(留下的族, 并进来的族)]（两边都带通用查法的）)。"""
    out = list(into or [])
    by_key = {(f["product"], f["topic"], f["dir"]): f for f in out}
    joined, both_gen = 0, []
    for f in fams:
        k = (f["product"], f["topic"], f["dir"])
        o = by_key.get(k)
        if o is None:
            out.append(f)
            by_key[k] = f
            continue
        o["rules"] += [r for r in f["rules"] if r not in o["rules"]]
        if f.get("general") and o.get("general") and f["general"] != o["general"]:
            if f["general"] not in o["rules"]:
                o["rules"].append(f["general"])
            both_gen.append((o.get("key"), f.get("key")))
        else:
            o["general"] = o.get("general") or f.get("general")
        o["same"] = (o.get("same") or []) + (f.get("same") or [])
        if f.get("key"):
            o.setdefault("joined_from", []).append(f["key"])
        joined += 1
    return out, joined, both_gen


def load_state(out):
    return L.jload(os.path.join(out, "apply_state.json"), {})


def rounds_in(fams, allprops):
    """families.json 里的族出自哪几轮提案（族的 proposal、key，并进来的 joined_from、理主题并掉的 merged_from）。"""
    pids = set()
    for f in fams:
        pids |= {f.get("proposal") or ""} | {x.split("#")[0] for x in [f.get("key") or ""] + (f.get("joined_from") or [])
                                              + (f.get("merged_from") or [])}
    return {allprops[p].get("round") or 1 for p in pids if p in allprops}


def cmd_apply(a):
    rules = L.load_rules(a.rules)
    alias = load_alias(a.merge)
    allprops = {os.path.basename(p)[:-5]: L.jload(p) for p in sorted(glob.glob(os.path.join(a.out, "proposals", "fam-*.json")))}
    first = a.fresh or not os.path.isfile(os.path.join(a.out, "families.json"))
    state = load_state(a.out)
    if a.fresh and not a.check and (state.get("incremental_rounds") or state.get("topic_splits_applied")):
        raise SystemExit(f"基础库建成之后已经加过增量（第 {state.get('incremental_rounds')} 轮）或拆过主题节点"
                         f"（{state.get('topic_splits_applied')}）；--fresh 会把这些冲掉。增量用不加 --fresh 的 apply")
    props = allprops
    done_rounds = set()
    if a.proposals:
        want = set(a.proposals.split(","))
        props = {k: v for k, v in props.items() if k in want}
    elif not first:                    # 增量：只落还没落过的轮（已经落过的在 families.json 里，主题可能已经理过、拆过）
        done_rounds = set(state.get("rounds_applied") or rounds_in(L.jload(os.path.join(a.out, "families.json")), allprops))
        props = {k: v for k, v in props.items() if (v.get("round") or 1) not in done_rounds}
        print(f"增量：已经落过的轮 {sorted(done_rounds)}；这次落 {len(props)} 个提案（第 {sorted({v.get('round') or 1 for v in props.values()})} 轮）")
    for p in props.values():           # 补并落盘之后：提案里被并掉的规矩号换成留下的那条（去重）
        ids = dedupe([alias.get(r["id"], r["id"]) for r in p["rules"]])
        byid = {alias.get(r["id"], r["id"]): r for r in p["rules"]}
        p["rules"] = [dict(byid[i], id=i) for i in ids]
    old_topics = {} if a.fresh else L.jload(os.path.join(a.out, "topics.json"), {})
    bad, notes, fams, unplaced, gen_written = [], [], [], [], []
    topics = {k: dict(v) for k, v in old_topics.items()}
    in_props = {r["id"]: pid for pid, p in props.items() for r in p["rules"]}
    for pid, p in props.items():
        dp = os.path.join(a.out, "decisions", pid + ".json")
        if not os.path.isfile(dp):
            bad.append(f"{pid}：没有决定文件 decisions/{pid}.json")
            continue
        d = L.jload(dp)
        mine = {r["id"] for r in p["rules"]}
        seen = collections.Counter()
        for k, f in enumerate(d.get("families") or [], 1):
            w = f"{pid} 第 {k} 族"
            for x in ("name", "line", "dir"):
                if not (f.get(x) or "").strip():
                    bad.append(f"{w}：{x} 不能为空")
            if f.get("dir") and not L.DIR_RX.match(f["dir"]):
                bad.append(f"{w}：目录名「{f['dir']}」要是小写英文、数字和短横线")
            prod_dir = L.PRODUCT_DIRS.get(p["product"], "")
            tp = topics.setdefault(prod_dir, {})
            if p.get("split_of"):      # 拆超限的族：新族都留在原来的主题下
                t = {"dir": p["topic"]["dir"], "name": tname(tp.get(p["topic"]["dir"])) or p["topic"].get("name")}
            else:
                t = f.get("topic") or {}
            segs = (t.get("dir") or "").split("/")
            if not t.get("dir") or not all(L.DIR_RX.match(s) for s in segs):
                bad.append(f"{w}：主题目录「{t.get('dir')}」每级要是小写英文、数字和短横线（用 / 分级）")
            if not (t.get("name") or "").strip():
                bad.append(f"{w}：主题要有中文名")
            if t.get("dir") and t.get("name"):
                if t["dir"] in tp and tname(tp[t["dir"]]) != t["name"]:
                    (notes if first else bad).append(f"{w}：主题 {t['dir']} 的中文名前后不一致（{tname(tp[t['dir']])} / {t['name']}）")
                if t["dir"] not in tp and not first:
                    notes.append(f"{w}：新起的主题 {t['dir']}（{t['name']}）" + ("" if t.get("line") else "，没写主题的一行"))
                tp.setdefault(t["dir"], {"name": t["name"], "line": t.get("line") or ""})
            rs = dedupe([alias.get(r, r) for r in f.get("rules") or []])
            if not rs:
                bad.append(f"{w}：一条规矩都没有")
            for rid in rs:
                seen[rid] += 1
                if rid not in mine:
                    bad.append(f"{w}：{rid} 不在这个提案里" + (f"（在 {in_props[rid]}）" if rid in in_props else ""))
            same = [{"rules": dedupe([alias.get(r, r) for r in s.get("rules") or []]), "reason": s.get("reason")}
                    if isinstance(s, dict) else s for s in f.get("same") or []]
            check_same(f, f.get("rules") or [], w, bad)       # 按子代理写的原样查（补并之前的规矩号）
            same = [s for s in same if isinstance(s, dict) and len(s["rules"]) > 1]   # 补并之后已经并成一条的组不再留
            gid = None
            g = f.get("general")
            offered = [x["id"] for x in p.get("generals") or []]
            if isinstance(g, str):     # 拆族时沿用原族的通用查法：写它的规矩号
                if g in offered:
                    gid = g
                else:
                    bad.append(f"{w}：general 写规矩号时只能是原族的通用查法（{offered}）")
            elif g:
                if g.get("general") is not True or g.get("product") != p["product"]:
                    bad.append(f"{w}：通用查法要带 \"general\": true，product 和提案一样")
                else:
                    gid = L.rule_id(g["product"], g.get("title") or "")
                    src = sorted({m.group(1) for s in [x for st in (g.get("how") or []) for x in (st.get("support") or [])]
                                  if (m := CLAIM_CASE.match(s))}) or sorted({c for rid in rs if rid in rules for c in rules[rid].get("sources") or []})
                    gen_written.append(dict({"id": gid}, **{k_: v for k_, v in g.items() if k_ not in ("id", "sources", "status", "general")},
                                            sources=src, status="active", general=True))
            fams.append({"key": f"{pid}#{k}", "product": p["product"], "product_dir": prod_dir, "topic": t.get("dir"), "dir": f.get("dir"),
                         "name": f.get("name"), "line": f.get("line"), "rules": rs, "general": gid, "proposal": pid, "same": same,
                         **({"split_of": p["split_of"]} if p.get("split_of") else {})})
        for x in d.get("move_out") or []:
            rid = alias.get(x.get("rule"), x.get("rule"))
            seen[rid] += 1
            unplaced.append({"rule": rid, "proposal": pid, "reason": x.get("reason")})
        for rid in mine:
            if seen[rid] == 0:
                bad.append(f"{pid}：{rid} 没有归到任何族，也没有列进 move_out")
            elif seen[rid] > 1:
                bad.append(f"{pid}：{rid} 出现了 {seen[rid]} 次")
    # 同名的族先并好（理主题的清单就是并完之后的族），再用理主题的决定
    fams, joined_new, both_gen = join_same_key(fams)
    # 第一次建库：有理主题的决定就用它（每个产物一份），覆盖主题、合并族
    applied = []
    if first and not a.no_topic_decisions and not bad:
        gen_ids = {g["id"]: g for g in gen_written}
        all_rules = dict(rules, **gen_ids)
        for pd in sorted({f["product_dir"] for f in fams}):
            dp = os.path.join(a.out, "topic_decisions", pd + ".json")
            if not os.path.isfile(dp):
                continue
            d = L.jload(dp)
            mine = [f for f in fams if f["product_dir"] == pd]
            errs = check_topic_decision(mine, d, all_rules, pd)
            if errs:
                bad += [f"理主题 {pd}：{e}" for e in errs]
                continue
            new, tmap = apply_topic_decision(mine, d)
            fams = [f for f in fams if f["product_dir"] != pd] + new
            topics[pd] = tmap
            applied.append(pd)
    names = collections.Counter((f["product"], f["topic"], f["dir"]) for f in fams)
    for k, c in names.items():
        if c > 1:
            msg = f"同一产物同一主题下族目录重名：{k}"
            (notes if first and k[0] and L.PRODUCT_DIRS.get(k[0]) not in applied else bad).append(msg)
    old_fams = existing_families(a)
    split_new = collections.defaultdict(list)
    for f in fams:
        if f.get("split_of"):
            split_new[f["split_of"]].append(f)
    for k, fl in split_new.items():
        o = next((f for f in old_fams if f.get("key") == k), None)
        if o is None:
            bad.append(f"拆族的提案指的族 {k} 在 families.json 里已经没有了（清单过时，要重出）")
            continue
        pd = o.get("product_dir") or prod_dir_of(o["product"])
        taken = {f["dir"] for f in old_fams if f is not o and f["product"] == o["product"] and f["topic"] == o["topic"]} | \
            {t.split("/")[-1] for t in topics.get(pd, {}) if "/" in t and t.rsplit("/", 1)[0] == o["topic"]}
        for f in fl:
            if f["dir"] in taken:
                bad.append(f"拆出来的族 {f['key']} 的目录名 {f['dir']} 和同一主题下别的族或子主题重名")
    if bad:
        print(f"归族输出有 {len(bad)} 处不对，没有落盘：")
        for b in bad[:60]:
            print("  - " + b)
        sys.exit(1)
    if notes:
        print(("提示（第一次建库时主题只当建议，理主题之后再定）" if first else "提示") + f" {len(notes)} 项：")
        for b in notes[:20]:
            print("  · " + b)
    # 增量：拆开的族在原位置换成拆出来的几个族；其余和已有的族同产物、同主题、同目录名的，规矩接在已有族的后面
    base_list, offered = [], set()
    for f in old_fams:
        if f.get("key") in split_new:
            base_list += split_new[f["key"]]
            offered |= {f.get("general")} | {r for r in f["rules"] if (rules.get(r) or {}).get("general")}
        else:
            base_list.append(f)
    fams, joined, bg = join_same_key([f for f in fams if not f.get("split_of")], into=base_list)
    both_gen += bg
    owner, dropped = {}, 0
    for f in fams:                     # 已有族里被并掉的规矩号也换掉；换完一条规矩只留在第一个族里
        keep = []
        for r in dedupe([alias.get(x, x) for x in f["rules"]]):
            if r in owner:
                dropped += 1
                continue
            owner[r] = f
            keep.append(r)
        f["rules"] = keep
    empty = [f.get("key") for f in fams if not f["rules"] and not f.get("general")]
    fams = [f for f in fams if f["rules"] or f.get("general")]
    used_gens = {f.get("general") for f in fams} | {r for f in fams for r in f["rules"] if (rules.get(r) or {}).get("general")}
    orphan = sorted(x for x in offered - used_gens if x)       # 拆族时没有沿用的原通用查法：落盘时删掉
    width = max(3, len(str(len(fams))))
    for k, f in enumerate(fams, 1):
        f["family"] = f"family-{k:04d}"
        f["short"] = f"f{k:0{width}d}"                       # 给审的 agent 用的短号，一次导出里唯一
    if split_new:
        print(f"拆开的族 {len(split_new)} 个 → 新族 {sum(len(v) for v in split_new.values())} 个；没有沿用、要删的原通用查法 {orphan}")
    if empty:
        print(f"规矩都被并走、空了的族 {len(empty)} 个，去掉：{empty[:10]}")
    # move_out 的规矩：后来（下一轮）放进了族的不算待挪；同一条挪了几次的只留最后一次；增量时以前没挪完的接着算
    if not first:
        unplaced = L.jload(os.path.join(a.out, "unplaced.json"), []) + unplaced
    last = {}
    for x in unplaced:
        if x["rule"] not in owner:
            last[x["rule"]] = x
    placed_later = len({x["rule"] for x in unplaced} & set(owner))
    unplaced = list(last.values())
    if joined_new:
        print(f"同产物、同主题、同目录名的族并进排在前面的那个：{joined_new} 个" +
              (f"（两边都带通用查法、后一条作为族里另一条通用查法留着的 {len(both_gen)} 处：{both_gen[:5]}）" if both_gen else ""))
    if joined:
        print(f"并进已有族的 {joined} 个")
    if placed_later:
        print(f"前一轮 move_out、后一轮放进了族的 {placed_later} 条")
    if dropped:
        print(f"补并之后同一条规矩出现在两个族里、从后面的族里去掉的 {dropped} 处")
    gen_bad = 0
    if gen_written:
        os.makedirs(L.WORK, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="general_check-", dir=L.WORK)     # 每次调用一个，几批并行自检时互不相踩
        try:
            for g in gen_written:
                L.jsave(os.path.join(tmp, g["id"] + ".json"), g)
            cmd = [sys.executable, "-X", "utf8", os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_rules.py"), "--dir", tmp]
            if a.format_only:
                cmd.append("--format-only")
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        lines = r.stdout.strip().splitlines() or [r.stderr[-300:]]
        print("通用查法的检查：", lines[-1])
        if r.returncode:
            gen_bad = 1
            print("\n".join(x for x in lines if x.startswith(("[", "  - "))))
    if a.check:
        print(f"（只检查，没有落盘）族 {len(fams)} 个，通用查法 {len(gen_written)} 条，待挪的 {len(unplaced)} 条")
        sys.exit(gen_bad)
    if gen_bad:
        print("通用查法没过检查，没有落盘")
        sys.exit(1)
    for g in gen_written:             # 内容没变的不重写
        p = os.path.join(a.rules, g["id"] + ".json")
        if not os.path.isfile(p) or L.jload(p) != g:
            L.jsave(p, g)
    for x in orphan:
        p = os.path.join(a.rules, x + ".json")
        if os.path.isfile(p):
            os.remove(p)
    L.jsave(os.path.join(a.out, "families.json"), fams)
    L.jsave(os.path.join(a.out, "topics.json"), topics)
    L.jsave(os.path.join(a.out, "unplaced.json"), unplaced)
    now = sorted({v.get("round") or 1 for v in props.values()})
    if first:
        st = {"rounds_applied": now, "incremental_rounds": [], "topic_splits_applied": []}
    else:
        if not done_rounds:
            done_rounds = set(state.get("rounds_applied") or rounds_in(old_fams, allprops))
        st = dict(state, rounds_applied=sorted(done_rounds | set(now)),
                  incremental_rounds=sorted(set(state.get("incremental_rounds") or []) | set(now)))
        st.setdefault("topic_splits_applied", [])
    L.jsave(os.path.join(a.out, "apply_state.json"), st)
    print(f"族 {len(fams)} 个，主题 {sum(len(v) for v in topics.values())} 个，归进族的规矩 {sum(len(f['rules']) for f in fams)} 条，"
          f"新写的通用查法 {len(gen_written)} 条，待挪的 {len(unplaced)} 条" + (f"；用了理主题的决定：{applied}" if applied else ""))
    sys.exit(1 if unplaced else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["propose", "apply", "topics-list", "topics-check", "same-groups", "oversize", "split-families",
                                    "topic-split-lists", "topic-split-check", "topic-split-apply"])
    ap.add_argument("--rules", default=os.path.join(L.STORE, "rules"))
    ap.add_argument("--out", default=os.path.join(L.STORE, "families"))
    ap.add_argument("--merge", default=os.path.join(L.STORE, "merge"),
                    help="合并目录：apply 从 merge_map.json 取补并后的规矩号映射；same-groups 往 groups/、batches/ 里写补并组")
    ap.add_argument("--merge-per-batch", type=int, default=40, help="same-groups：每批补并组的规矩合计不超过几条")
    ap.add_argument("--threshold", type=float, default=0.3)
    ap.add_argument("--max-size", type=int, default=20)
    ap.add_argument("--attach-min", type=float, default=0.05)
    ap.add_argument("--per-batch", type=int, default=80)
    ap.add_argument("--format-only", action="store_true")
    ap.add_argument("--new-only", action="store_true", help="propose：只给还没归族的规矩出提案，并附上同一产物下最相近的已有族")
    ap.add_argument("--existing-top", type=int, default=8, help="propose --new-only：每个提案附几个最相近的已有族")
    ap.add_argument("--fresh", action="store_true", help="apply：不读已有的 families.json，从头建（第一次建库）")
    ap.add_argument("--no-topic-decisions", action="store_true", help="apply：第一次建库时也不用 topic_decisions/（理主题之前那一遍）")
    ap.add_argument("--check", action="store_true", help="apply：只检查决定（给归族的子代理自检用），不落盘")
    ap.add_argument("--proposals", help="apply：只看这些提案（逗号分隔的提案号）；--check 时常用")
    ap.add_argument("--product", help="topics-check：产物（规格 / 计划与派工 / 代码 / 资源）或产物目录（spec / plan / code / resource）")
    ap.add_argument("--max-rules", type=int, default=MAX_RULES, help="oversize / split-families：族里规矩超过几条算超限")
    ap.add_argument("--max-children", type=int, default=MAX_CHILDREN, help="oversize / topic-split-*：主题节点直接子项超过几个算超限")
    ap.add_argument("--lists-per-batch", type=int, default=4, help="topic-split-lists：每批几份清单")
    ap.add_argument("--split", help="topic-split-check：清单号（ts-NNNN）")
    a = ap.parse_args()
    {"propose": cmd_propose, "apply": cmd_apply, "topics-list": cmd_topics_list, "topics-check": cmd_topics_check,
     "same-groups": cmd_same_groups, "oversize": cmd_oversize, "split-families": cmd_split_families,
     "topic-split-lists": cmd_topic_split_lists, "topic-split-check": cmd_topic_split_check,
     "topic-split-apply": cmd_topic_split_apply}[a.cmd](a)


if __name__ == "__main__":
    main()
