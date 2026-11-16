# -*- coding: utf-8 -*-
"""第 2b 步「复核」的统计：读 store/reviews/<卡号>.json（复核记录，格式见 references/review-brief.md），报
  复核了多少张卡；规矩从几条到几条；按记录里的 check 各改了多少处（check 照记录原样计数，不预设有几类；CHECKS 只给现在已知的
  编号配个名字，任务书改了编号也不影响计数）；拆了多少次、多出多少条；挪进 left_out 多少条；unsure 多少项；
  有改动的卡几张；复核记录里的 rules_after 和候选文件里现在的规矩条数对不上的卡；读不了的记录；
  以及没有复核记录的卡：有候选文件、没有复核记录的（列出卡号），和还没有候选文件的（只报个数）。
只读 store/reviews/、store/candidates/、work/cards_index.json。
用法（在分支根目录下）： py -3 -X utf8 skills/memory-rules/scripts/review_stats.py [--reviews DIR] [--candidates DIR] [--json] [--all]
  --all：没有复核记录的卡全部列出（默认列前 30 个）；--json：把统计写成 JSON 打印出来。"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, json, os  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rulelib as L  # noqa: E402

CHECKS = {1: "做法和例外出自卡", 2: "一条一个做法", 3: "范围不超出卡", 4: "触发字面看得见", 5: "取值出处标得对",
          6: "不带出事应用的东西", 7: "几张清单记得对"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--reviews", default=os.path.join(L.STORE, "reviews"))
    ap.add_argument("--candidates", default=os.path.join(L.STORE, "candidates"))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    revs, bad = {}, []
    for p in sorted(glob.glob(os.path.join(a.reviews, "case-*.json"))):
        try:
            revs[os.path.basename(p)[:-5]] = json.load(io.open(p, encoding="utf-8"))
        except (ValueError, OSError) as e:
            bad.append({"file": os.path.basename(p), "error": str(e)[:120]})
    cands = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(a.candidates, "case-*.json"))}
    all_cards = {x["case"] for x in L.jload(L.INDEX, {"index": []})["index"]}
    by_check, before, after, splits, extra, moved, unsure, touched, mismatch = collections.Counter(), 0, 0, 0, 0, 0, 0, 0, []
    for cid, r in revs.items():
        before += int(r.get("rules_before") or 0)
        after += int(r.get("rules_after") or 0)
        ch = r.get("changes") or []
        for c in ch:
            by_check[c.get("check")] += 1
        sp = r.get("splits") or []
        splits += len(sp)
        extra += sum(max(0, len(s.get("into") or []) - 1) for s in sp)
        mv = r.get("moved_to_left_out") or []
        moved += len(mv)
        unsure += len(r.get("unsure") or [])
        touched += bool(ch or sp or mv)
        cp = os.path.join(a.candidates, cid + ".json")
        if os.path.isfile(cp):
            try:
                n = len(json.load(io.open(cp, encoding="utf-8")).get("rules") or [])
                if r.get("rules_after") is not None and n != int(r["rules_after"]):
                    mismatch.append({"case": cid, "rules_after": r["rules_after"], "candidates_now": n})
            except ValueError:
                pass
    no_review = sorted(cands - set(revs))
    no_cand = sorted(all_cards - cands)
    rep = {"reviewed": len(revs), "rules_before": before, "rules_after": after, "cards_changed": touched,
           "changes_by_check": {(f"{k} {CHECKS[k]}" if k in CHECKS else str(k)): v for k, v in sorted(by_check.items(), key=lambda kv: (str(kv[0])))},
           "changes_total": sum(by_check.values()), "splits": splits, "rules_added_by_splits": extra, "moved_to_left_out": moved,
           "unsure": unsure, "rules_after_mismatch": mismatch, "unreadable": bad,
           "candidates_without_review": len(no_review), "cards_without_candidates": len(no_cand),
           "candidates_without_review_list": no_review}
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
        return
    print(f"复核了 {len(revs)} 张卡（有改动的 {touched} 张）；规矩 {before} 条 → {after} 条")
    print(f"按 check 分的改动处数（共 {rep['changes_total']} 处）：" + "；".join(f"{k}：{v}" for k, v in rep["changes_by_check"].items()))
    print(f"拆分 {splits} 次（多出 {extra} 条）；挪进 left_out {moved} 条；unsure {unsure} 项")
    if mismatch:
        print(f"复核记录的 rules_after 和候选文件现在的条数对不上的 {len(mismatch)} 张：" + "，".join(f"{m['case']}（{m['rules_after']}/{m['candidates_now']}）" for m in mismatch[:10]))
    if bad:
        print(f"读不了的复核记录 {len(bad)} 个：" + "，".join(b["file"] for b in bad[:10]))
    print(f"有候选、没有复核记录的卡 {len(no_review)} 张；还没有候选文件的卡 {len(no_cand)} 张")
    for c in (no_review if a.all else no_review[:30]):
        print("  " + c)
    if not a.all and len(no_review) > 30:
        print(f"  ……另有 {len(no_review) - 30} 张（加 --all 全部列出）")


if __name__ == "__main__":
    main()
