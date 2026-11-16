# -*- coding: utf-8 -*-
"""第 3 步「合并」的聚类：把相近的候选规矩连成组，交给子代理判断是否同一个触发、同一个做法。

读 store/candidates/<卡号>.json（--candidates 可换目录），每条候选给一个临时号「卡号#序号」（序号从 1 起，按文件里 rules 的顺序）。
只在同一 product 内比较。每条候选的文档 = keys.read ∪ keys.product ∪ 标题（标识符的整体词和部分词，加中文两字 bigram；
见 rulelib.py），IDF 在同一 product 的候选上算，两两算余弦。同一张卡的候选彼此不连边（提炼时已经在卡内并过）。
相似度不低于 --threshold 的连边，取连通分量成组；
超过 --max-size（默认 10）条的组，阈值每次加 --step 再拆，直到都不超过。

写（--out，默认 store/merge/）。每一期用自己的前缀（--phase，基础库是 group，增量每期起一个名字，如 p2），互不覆盖：
  groups/<前缀>-NNNN.json   多条候选的组：组号、product、拆出它时的阈值、组内两两相似度、每条候选的临时号和全文
  singles.json（基础库）/ singles-<前缀>.json（增量）   单独成组的候选（不交给子代理，apply_merge.py 直接转成规矩）
  batches/merge-NNN.txt（基础库）/ batches/<前缀>-NNN.txt（增量）   分批清单：每批若干个组文件的路径（相对分支根目录，用 /），每批候选合计
                       不超过 --per-batch 条（默认 40；一个组本身更大的自成一批）
  cluster_report.json（基础库）/ cluster_report-<前缀>.json（增量）   参数、各 product 的条数、相似度分布、组大小分布
重跑同一期时先清掉这一期以前写的组、批次、singles 和报告；这一期已经有合并决定（decisions/<前缀>-*.json）时拒绝。
别的期的组、补并组（same-*，families.py same-groups 写的）和 decisions/ 都不动。
按卡的清单取候选：--only-file <文件>（每行一个卡号，# 开头的行和空行不算）、--only 卡号,…（两者都给时取并集）。
  分两期建库时：基础库用 --only-file work/lists/in-e613047f.txt；
  增量用 --only-file work/lists/not-in-e613047f.txt --existing store/rules --phase p2。
增量归并：--existing store/rules 把库里已有的规矩（不含通用查法）一起聚；已有规矩的临时号就是规矩号，组里标 existing: true。
  只算「新候选之间」和「新候选和已有规矩之间」的相似度，已有规矩彼此之间不连边（它们已经合并过，不再拿来串组）；
  只含已有规矩的组不出。--existing 时必须用 --phase 给这一期起名（不能是 group 或 same）。
用法： py -3 -X utf8 skills/memory-rules/scripts/cluster.py [--candidates DIR] [--out DIR] [--existing DIR --phase 名字] [--only-file 文件]
                [--only 卡号,…] [--threshold 0.35] [--max-size 10] [--step 0.05] [--per-batch 40]
阈值默认 0.35（2026-11-15 的试跑：0.35 多出来的组约一半该并；漏并的多在相似度 0.25 以下，阈值管不到）。"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, os, re, time  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rulelib as L  # noqa: E402


def doc_terms(r):
    keys = r.get("keys") or {}
    k = " ".join(list(keys.get("read") or []) + list(keys.get("product") or []))
    return L.merge_terms(L.ident_terms(k), L.ident_terms(r.get("title") or ""), L.cjk_terms(r.get("title") or ""),
                         L.cjk_terms(k))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", default=os.path.join(L.STORE, "candidates"))
    ap.add_argument("--out", default=os.path.join(L.STORE, "merge"))
    ap.add_argument("--existing", help="增量归并：已有规矩的目录（如 store/rules）。已有规矩以规矩号当临时号参与聚类；"
                                        "只含已有规矩、没有新候选的组不出；只差已有规矩、没有新候选的单条也不列进 singles")
    ap.add_argument("--only", help="只聚这些卡的候选（逗号分隔的卡号）")
    ap.add_argument("--only-file", help="只聚这个清单里的卡的候选（每行一个卡号）")
    ap.add_argument("--threshold", type=float, default=0.35)
    ap.add_argument("--max-size", type=int, default=10)
    ap.add_argument("--step", type=float, default=0.05)
    ap.add_argument("--per-batch", type=int, default=40)
    ap.add_argument("--phase", default="group", help="这一期的前缀：基础库 group（默认）；增量每期一个名字，如 p2")
    a = ap.parse_args()
    t0 = time.time()
    px = a.phase
    if not re.fullmatch(r"[a-z][a-z0-9]*", px) or px == "same":
        raise SystemExit(f"--phase {px}：要是小写英文开头的字母数字，不能是 same")
    if a.existing and px == "group":
        raise SystemExit("增量（--existing）要用 --phase 给这一期起个名字（如 p2），免得覆盖基础库的组和批次")
    base = px == "group"
    f_singles = "singles.json" if base else f"singles-{px}.json"
    f_report = "cluster_report.json" if base else f"cluster_report-{px}.json"
    b_pat = "merge-*.txt" if base else f"{px}-*.txt"
    done = glob.glob(os.path.join(a.out, "decisions", f"{px}-*.json"))
    if done:
        raise SystemExit(f"这一期（{px}）已经有 {len(done)} 个合并决定，重新聚类会和它们对不上；换一个 --phase，或先把这些决定挪走")
    cands = L.load_candidates(a.candidates)
    keep = set()
    if a.only:
        keep |= set(a.only.split(","))
    if a.only_file:
        keep |= {x.strip() for x in io.open(a.only_file, encoding="utf-8") if x.strip() and not x.startswith("#")}
    if a.only or a.only_file:
        cands = [c for c in cands if c[1] in keep]
    n_new = len(cands)
    if a.existing:
        cands += [(rid, None, None, r) for rid, r in L.load_rules(a.existing).items() if not r.get("general")]
    by_prod = collections.defaultdict(list)
    for c in cands:
        by_prod[c[3].get("product") or "（未写）"].append(c)
    for sub, pat in (("groups", f"{px}-*.json"), ("batches", b_pat)):   # 只清这一期以前写的；别的期、补并组（same-*）不动
        p = os.path.join(a.out, sub)
        os.makedirs(p, exist_ok=True)
        for f in glob.glob(os.path.join(p, pat)):
            os.remove(f)
    groups, singles, all_sims, nearest, sizes = [], [], [], [], collections.Counter()
    for prod in sorted(by_prod):
        items = by_prod[prod]
        terms = [doc_terms(c[3]) for c in items]
        idf, _ = L.idf_table(terms)
        vecs = [L.vector(t, idf) for t in terms]
        active = {i for i, c in enumerate(items) if c[1] is not None} if a.existing else None
        sims = L.pair_sims(vecs, active=active)
        # 同一张卡的几条候选在提炼时已经按「同一个触发、同一个做法」并过，彼此不连边
        same = [k for k in sims if items[k[0]][1] is not None and items[k[0]][1] == items[k[1]][1]]
        for k in same:
            del sims[k]
        all_sims += list(sims.values())
        best = collections.defaultdict(float)
        for (i, j), s in sims.items():
            best[i], best[j] = max(best[i], s), max(best[j], s)
        nearest += [best[i] for i in range(len(items))]
        for members, th in L.split_by_threshold(list(range(len(items))), sims, a.threshold, a.max_size, a.step):
            if all(items[i][1] is None for i in members):
                continue                                     # 全是已有规矩：没有新东西要判断
            sizes[len(members)] += 1
            if len(members) == 1:
                tmp, case, idx, r = items[members[0]]
                singles.append({"tmp": tmp, "case": case, "index": idx, "product": prod, "nearest_similarity": round(best[members[0]], 3), "rule": r})
                continue
            members.sort()
            pairs = [{"a": items[i][0], "b": items[j][0], "similarity": round(sims.get((i, j), 0.0), 3)}
                     for x, i in enumerate(members) for j in members[x + 1:]]
            groups.append({"product": prod, "threshold": th, "pairs": pairs,
                           "members": [{"tmp": items[i][0], "case": items[i][1], "index": items[i][2], "existing": items[i][1] is None,
                                        "rule": items[i][3]} for i in members]})
    for k, g in enumerate(groups, 1):
        g["group"] = f"{px}-{k:04d}"
        L.jsave(os.path.join(a.out, "groups", g["group"] + ".json"), {"group": g["group"], **{x: g[x] for x in ("product", "threshold", "pairs", "members")}})
    L.jsave(os.path.join(a.out, f_singles), singles)
    batches, cur, n = [], [], 0
    for g in groups:
        m = len(g["members"])
        if cur and n + m > a.per_batch:
            batches.append(cur)
            cur, n = [], 0
        cur.append(L.relpath(os.path.join(a.out, "groups", g["group"] + ".json")))
        n += m
    if cur:
        batches.append(cur)
    bnames = []
    for k, b in enumerate(batches, 1):
        bnames.append(f"merge-{k:03d}.txt" if base else f"{px}-{k:03d}.txt")
        with open(os.path.join(a.out, "batches", bnames[-1]), "w", encoding="utf-8", newline="\n") as f:
            f.write("".join(x + "\n" for x in b))
    rep = {"params": L.rel_params(a), "candidates": len(cands), "new_candidates": n_new, "existing_rules": len(cands) - n_new,
           "seconds": round(time.time() - t0, 1), "by_product": {p: len(v) for p, v in by_prod.items()},
           "existing_in_groups": sum(1 for g in groups for m in g["members"] if m["existing"]),
           "pair_similarity_quantiles": L.quantiles(all_sims), "nearest_neighbor_quantiles": L.quantiles(nearest),
           "nearest_at_least_threshold": sum(1 for x in nearest if x >= a.threshold),
           "group_sizes": dict(sorted(sizes.items())), "groups": len(groups), "singles": len(singles), "batches": len(batches),
           "batch_files": bnames, "singles_file": f_singles, "candidates_in_groups": sum(len(g["members"]) for g in groups)}
    L.jsave(os.path.join(a.out, f_report), rep)
    print(f"候选 {n_new} 条" + (f"，已有规矩 {len(cands) - n_new} 条" if a.existing else "") +
          f"（{rep['by_product']}）；阈值 {a.threshold}，组上限 {a.max_size}；用时 {rep['seconds']} 秒")
    print(f"多条的组 {len(groups)} 个（共 {rep['candidates_in_groups']} 条），单独成组 {len(singles)} 条；分 {len(batches)} 批" +
          (f"（{bnames[0]}–{bnames[-1]}，组号 {px}-0001 起）" if bnames else ""))
    print("组大小分布：", rep["group_sizes"])
    print("所有正相似度对的分位数：", rep["pair_similarity_quantiles"])
    print("每条候选最近邻相似度的分位数：", rep["nearest_neighbor_quantiles"], f"；最近邻不低于阈值的 {rep['nearest_at_least_threshold']} 条")


if __name__ == "__main__":
    main()
