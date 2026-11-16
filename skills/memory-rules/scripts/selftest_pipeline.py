# -*- coding: utf-8 -*-
"""合并、归族、理主题、导出、召回各脚本的自测：用 references/examples/ 的两张卡（代码类那张再多写一条讲偏移的候选），再加一张讲
同一件事的卡（文字阴影，引另一张真卡的建议），在 work/selftest/pipeline/ 下走一遍全流程，并故意做错几处。
  1. cluster：三条文字阴影的候选聚成一组，规格那条单独成组；--only-file 只取清单里的卡；增量（--existing）时新候选和已有规矩
     聚在一组、已有的标 existing；
  2. apply_merge：漏处理一条候选的决定应当被拒；正确的决定（两条并一条、一条单独保留）落盘后，合并出的规矩 sources 有两张卡，
     过检查（不只查格式）；--check 也走一遍；
  3. families：族目录名不合法的决定应当被拒；带一条通用查法的正确决定先 --check（不落盘），再落盘（代码产物拆成两个族）；
  4. 理主题：topics-list 出清单；漏了族的决定 topics-check 应当查出；正确的决定（两级主题、把两个代码族并成一个）过检查，
     apply --fresh 用它覆盖主题、合并族，topics.json 带上主题的一行；
  4b. 补并（在复制出来的目录里）：same 里写了不在族里的规矩应当被拒；正确的 same 过 --check，same-groups 做出 same-0001（成员是两条
     已有规矩、带全文、标 existing）和批次清单；合并决定 --check 通过，apply_merge --prefix same 落盘后留下排在前面那条的规矩号、
     另一条的文件删掉，merge_map 把它和它原来的临时号都指向留下的那条，origins 记 merged_rules；apply --fresh 把族里被并掉的
     规矩号换成留下的那条、same 组不再留，短号从 f001 连续编；
  4c. 第一次建库的两轮归族（在复制出来的目录里，多加两条文字阴影规矩）：通用查法不进提案；第一轮挪出两条、标一组 same，
     apply --fresh 退出码 1；有决定时从头 propose 被拒、什么都不动；propose --new-only 出第二轮（提案号、批次号接着排，round 2，
     附已有族，已有的提案、批次、决定一字不动）；第二轮归进已有族，--check 通过，apply --fresh 两轮一起落：待挪的清空、
     四条在同一个族里、same 两组；same-groups 重跑时 same-0001 和它的批次不动，第二轮的组是 same-0002、进新批次；
  5. propose --new-only：附的已有族不超过 --existing-top 个，带相似度；
  6. build_index：rules/ 树、keys.jsonl、manifest.json 都写出来，四层的文件都在，族的 index.md 里有通用查法，顶层和主题层有主题的一行；
     每个产物有 map.md（「短号 族名（条数）」、不带链接），manifest 的 family_short 指到族的路径；
  7. recall：读过的文件里有 android:shadowColor、交回的文件里有 .shadow({ 时，文字阴影的规矩排第一且 probe 命中；--level family
     排第一的是文字阴影的族、带短号；--exclude-apps 去掉唯一的应用后合并出的规矩不在视图里；lines、body 能取出；show 一次取顶层（只列代码）、
     族和规矩正文；show map 只列代码的地图；show <短号> <规矩号> 取出族（族名、族的一行、通用查法、每条规矩一行）和正文；
     coarse --as-tree --products 代码,规格 --k 1 合在一起只取一个族（文字阴影），排成小树、不带得分；--with-lines --k 2 两个产物的
     族都在，每个族下面带族的一行和规矩的行，通用查法只有标题一行。
只写 work/selftest/pipeline/。用法（在分支根目录下）： py -3 -X utf8 skills/memory-rules/scripts/selftest_pipeline.py"""
import sys

sys.dont_write_bytecode = True
import copy, glob, io, json, os, shutil, subprocess  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rulelib as L  # noqa: E402

EX = os.path.join(HERE, "..", "references", "examples")
OUT = os.path.join(L.WORK, "selftest", "pipeline")
CODE, SPEC, OTHER = "case-4f627840679361f165a3", "case-caa0a4c6289286b0e6ba", "case-9058ac868b6feb3a04e0"


def run(script, *args):
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, script), *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    cands, merge, rules, fam, tree = (os.path.join(OUT, x) for x in ("candidates", "merge", "rules", "families", "rules_tree"))
    os.makedirs(cands)
    shutil.copy2(os.path.join(EX, SPEC + ".json"), os.path.join(cands, SPEC + ".json"))
    o = L.jload(os.path.join(EX, CODE + ".json"))
    r2 = copy.deepcopy(o["rules"][0])
    r2["title"] = "shadowDx / shadowDy 照搬成 textShadow 的 offsetX / offsetY"
    o2 = dict(o, rules=[o["rules"][0], r2])
    L.jsave(os.path.join(cands, CODE + ".json"), o2)
    r = copy.deepcopy(o["rules"][0])
    r["title"] = "TextView 的 shadowRadius / shadowColor 转成 Text.textShadow，不用 .shadow"
    r["how"][0]["support"] = [OTHER + "#recommendation:4"]
    L.jsave(os.path.join(cands, OTHER + ".json"), {"case": OTHER, "rules": [r], "left_out": [], "corrections": [], "gaps": [], "conflicts": []})
    res = {}
    # 1 cluster
    code, out = run("cluster.py", "--candidates", cands, "--out", merge)
    groups = sorted(glob.glob(os.path.join(merge, "groups", "*.json")))
    g = L.jload(groups[0]) if groups else {"members": []}
    singles = L.jload(os.path.join(merge, "singles.json"), [])
    res["cluster"] = len(groups) == 1 and {m["tmp"] for m in g["members"]} == {CODE + "#1", CODE + "#2", OTHER + "#1"} and \
        [s["tmp"] for s in singles] == [SPEC + "#1"]
    lst = os.path.join(OUT, "only.txt")
    io.open(lst, "w", encoding="utf-8").write(SPEC + "\n")
    code, out = run("cluster.py", "--candidates", cands, "--out", os.path.join(OUT, "merge_only"), "--only-file", lst)
    rep = L.jload(os.path.join(OUT, "merge_only", "cluster_report.json"), {})
    res["cluster_only_file"] = code == 0 and rep.get("new_candidates") == 1 and rep.get("singles") == 1 and rep.get("groups") == 0
    # 2 apply_merge
    dec = os.path.join(merge, "decisions", g.get("group", "x") + ".json")
    L.jsave(dec, {"group": g.get("group"), "merged": [], "kept": [{"member": CODE + "#1", "reason": "测试：故意漏掉两条"}]})
    code, out = run("apply_merge.py", "--merge", merge, "--rules-out", rules, "--fresh")
    res["merge_rejects_missing"] = code == 1 and "没有被处理" in out
    mr = copy.deepcopy(o["rules"][0])
    mr["how"][0]["support"] = [CODE + "#recommendation:3", OTHER + "#recommendation:4"]
    L.jsave(dec, {"group": g.get("group"), "merged": [{"members": [CODE + "#1", OTHER + "#1"], "reason": "测试：同一个触发（TextView 的 shadow* 属性）、同一个做法（Text.textShadow）",
                                                         "rule": mr}], "kept": [{"member": CODE + "#2", "reason": "测试：讲的是偏移的对应，另成一条"}]})
    code, out = run("apply_merge.py", "--merge", merge, "--check", "--groups", g.get("group", "x"))
    res["merge_check_mode"] = code == 0 and "硬规则违反合计 0 处" in out
    code, out = run("apply_merge.py", "--merge", merge, "--rules-out", rules, "--fresh")
    rs = L.load_rules(rules) if os.path.isdir(rules) else {}
    merged = [x for x in rs.values() if len(x.get("sources") or []) == 2]
    res["merge_applies"] = code == 0 and len(rs) == 3 and len(merged) == 1 and "硬规则违反合计 0 处" in out
    shadow = merged[0]["id"] if merged else None
    # 1b 增量聚类：一条新候选对已有规矩
    c2 = os.path.join(OUT, "candidates_new")
    os.makedirs(c2)
    L.jsave(os.path.join(c2, "case-test00000000000001.json"), {"case": "case-test00000000000001", "rules": [r]})
    code0, _ = run("cluster.py", "--candidates", c2, "--out", os.path.join(OUT, "merge_inc"), "--existing", rules)   # 没给 --phase：拒绝
    code, out = run("cluster.py", "--candidates", c2, "--out", os.path.join(OUT, "merge_inc"), "--existing", rules, "--phase", "p2")
    ig = [L.jload(p) for p in glob.glob(os.path.join(OUT, "merge_inc", "groups", "p2-*.json"))]
    res["cluster_incremental"] = code0 != 0 and code == 0 and len(ig) == 1 and any(m["existing"] for m in ig[0]["members"]) and \
        any(not m["existing"] for m in ig[0]["members"]) and shadow in {m["tmp"] for m in ig[0]["members"]} and \
        os.path.isfile(os.path.join(OUT, "merge_inc", "batches", "p2-001.txt"))
    # 3 families
    code, out = run("families.py", "propose", "--rules", rules, "--out", fam, "--threshold", "0.3")
    props = [L.jload(p) for p in sorted(glob.glob(os.path.join(fam, "proposals", "*.json")))]
    gen = dict(copy.deepcopy(mr), title="测试用通用查法：TextView 的文字阴影属性去哪查、怎么写", general=True)

    def decide(bad_dir=False):
        for pr in props:
            ids = [x["id"] for x in pr["rules"]]
            if pr["product"] == "代码":
                fs = [{"name": "TextView 的文字阴影属性", "dir": "Text Shadow" if bad_dir else "text-shadow", "line": "源端 TextView 带 shadow* 属性",
                       "topic": {"dir": "ui/text", "name": "文本"}, "rules": [i for i in ids if i == shadow], "general": gen},
                      {"name": "文字阴影的偏移", "dir": "text-shadow-offset", "line": "源端 TextView 带 shadowDx / shadowDy",
                       "topic": {"dir": "ui/text", "name": "文字"}, "rules": [i for i in ids if i != shadow], "general": None}]
            else:
                fs = [{"name": "自绘画布的单位", "dir": "canvas-unit", "line": "规格里写画布单位的那一节",
                       "topic": {"dir": "canvas", "name": "画布"}, "rules": ids, "general": None}]
            L.jsave(os.path.join(fam, "decisions", pr["proposal"] + ".json"), {"proposal": pr["proposal"], "families": fs, "move_out": []})
    decide(bad_dir=True)
    code, out = run("families.py", "apply", "--rules", rules, "--out", fam, "--merge", merge, "--fresh")
    res["families_rejects_bad_dir"] = code == 1 and "目录名" in out
    decide()
    code, out = run("families.py", "apply", "--rules", rules, "--out", fam, "--merge", merge, "--fresh", "--check")
    res["families_check_mode"] = code == 0 and not os.path.exists(os.path.join(fam, "families.json"))
    code, out = run("families.py", "apply", "--rules", rules, "--out", fam, "--merge", merge, "--fresh")
    fl = L.jload(os.path.join(fam, "families.json"), [])
    res["families_applies"] = code == 0 and len(fl) == 3 and sum(1 for f in fl if f.get("general")) == 1 and "中文名前后不一致" in out
    # 4 理主题
    code, out = run("families.py", "topics-list", "--rules", rules, "--out", fam)
    tl = L.jload(os.path.join(fam, "topic_lists", "code.json"), {})
    res["topics_list"] = code == 0 and len(tl.get("families") or []) == 2 and os.path.isfile(os.path.join(fam, "topic_lists", "spec.json"))
    keys = {x["dir"]: x["family"] for x in tl.get("families") or []}
    td = {"product": "代码",
          "topics": [{"dir": "ui", "name": "界面", "line": "源端是 View 和布局 XML、目标是 ArkUI 组件时"},
                     {"dir": "ui/text", "name": "文本", "line": "手里有 TextView、Text 一类显示文字的控件时"}],
          "families": [{"family": keys.get("text-shadow"), "topic": "ui/text"}],
          "merge": [{"into": keys.get("text-shadow"), "from": [keys.get("text-shadow-offset")], "reason": "测试：说的都是 TextView 的文字阴影属性"}],
          "review": []}
    L.jsave(os.path.join(fam, "topic_decisions", "code.json"), td)
    code, out = run("families.py", "topics-check", "--product", "代码", "--out", fam)
    res["topics_check_rejects_missing"] = code == 1 and "没有归到主题" in out
    td["families"].append({"family": keys.get("text-shadow-offset"), "topic": "ui/text"})
    L.jsave(os.path.join(fam, "topic_decisions", "code.json"), td)
    L.jsave(os.path.join(fam, "topic_decisions", "spec.json"),
            {"product": "规格", "topics": [{"dir": "canvas", "name": "画布", "line": "规格里写自绘画布的那几节"}],
             "families": [{"family": x["family"], "topic": "canvas"} for x in L.jload(os.path.join(fam, "topic_lists", "spec.json"))["families"]],
             "merge": [], "review": []})
    code, out = run("families.py", "topics-check", "--product", "code", "--out", fam)
    res["topics_check_passes"] = code == 0
    code, out = run("families.py", "apply", "--rules", rules, "--out", fam, "--merge", merge, "--fresh")
    fl = L.jload(os.path.join(fam, "families.json"), [])
    tj = L.jload(os.path.join(fam, "topics.json"), {})
    cf = [f for f in fl if f["product"] == "代码"]
    res["topics_applied"] = code == 0 and len(cf) == 1 and len(cf[0]["rules"]) == 2 and cf[0]["topic"] == "ui/text" and \
        (tj.get("code", {}).get("ui/text") or {}).get("line", "").startswith("手里有") and \
        sorted(f.get("short", "") for f in fl) == [f"f{k:03d}" for k in range(1, len(fl) + 1)]
    # 4b 补并：在复制出来的目录里做，不影响后面几步
    rs_, fs_, ms_ = (os.path.join(OUT, x) for x in ("rules_same", "families_same", "merge_same"))
    shutil.copytree(rules, rs_)
    shutil.copytree(fam, fs_)
    shutil.copytree(merge, ms_)
    os.remove(os.path.join(fs_, "topic_decisions", "code.json"))     # 代码这边改成一个族，原来的理主题决定对不上了
    offset = L.jload(os.path.join(merge, "merge_map.json"), {}).get(CODE + "#2")
    cps = [pr["proposal"] for pr in props if pr["product"] == "代码"]
    cpid = cps[0] if len(cps) == 1 else "x"

    def same_dec(same):
        L.jsave(os.path.join(fs_, "decisions", cpid + ".json"), {"proposal": cpid, "move_out": [], "families": [
            {"name": "TextView 的文字阴影属性", "dir": "text-shadow", "line": "源端 TextView 带 shadow* 属性",
             "topic": {"dir": "ui/text", "name": "文本"}, "rules": [shadow, offset], "general": gen, "same": same}]})
    same_dec([{"rules": [shadow, "rule-000000000bad"], "reason": "测试：故意写一条不在族里的"}])
    code, out = run("families.py", "apply", "--rules", rs_, "--out", fs_, "--merge", ms_, "--fresh", "--check", "--proposals", cpid)
    res["same_rejects_bad"] = code == 1 and "不在这个族的 rules 里" in out
    same_dec([{"rules": [shadow, offset], "reason": "测试：从标题和触发看都是 TextView 的文字阴影属性"}])
    code, out = run("families.py", "apply", "--rules", rs_, "--out", fs_, "--merge", ms_, "--fresh", "--check", "--proposals", cpid)
    ok = code == 0
    code, out = run("families.py", "same-groups", "--rules", rs_, "--out", fs_, "--merge", ms_)
    sg = L.jload(os.path.join(ms_, "groups", "same-0001.json"), {})
    res["same_groups"] = ok and code == 0 and [m["tmp"] for m in sg.get("members") or []] == [shadow, offset] and \
        all(m["existing"] and m["rule"].get("title") for m in sg["members"]) and sg.get("product") == "代码" and \
        os.path.isfile(os.path.join(ms_, "batches", "same-001.txt")) and os.path.isfile(os.path.join(ms_, "groups", g.get("group", "x") + ".json"))
    L.jsave(os.path.join(ms_, "decisions", "same-0001.json"), {"group": "same-0001", "kept": [], "merged": [
        {"members": [shadow, offset], "reason": "测试：同一个触发、同一个做法", "rule": copy.deepcopy(mr)}]})
    code, out = run("apply_merge.py", "--merge", ms_, "--check", "--groups", "same-0001")
    ok = code == 0 and "硬规则违反合计 0 处" in out
    code, out = run("apply_merge.py", "--merge", ms_, "--rules-out", rs_, "--prefix", "same")
    mm2 = L.jload(os.path.join(ms_, "merge_map.json"), {})
    org = L.jload(os.path.join(ms_, "origins.json"), {})
    kept = L.jload(os.path.join(rs_, (shadow or "x") + ".json"), {})
    res["same_merge_applies"] = ok and code == 0 and "硬规则违反合计 0 处" in out and kept.get("sources") == sorted([CODE, OTHER]) and \
        not os.path.exists(os.path.join(rs_, (offset or "x") + ".json")) and mm2.get(offset) == shadow and mm2.get(CODE + "#2") == shadow and \
        (org.get(shadow) or {}).get("merged_rules") == [shadow, offset] and offset not in org and \
        sorted((org.get(shadow) or {}).get("members") or []) == sorted([CODE + "#1", CODE + "#2", OTHER + "#1"])
    code, out = run("families.py", "apply", "--rules", rs_, "--out", fs_, "--merge", ms_, "--fresh")
    fl2 = L.jload(os.path.join(fs_, "families.json"), [])
    cf2 = [f for f in fl2 if f["product"] == "代码"]
    res["same_alias_in_apply"] = code == 0 and len(cf2) == 1 and cf2[0]["rules"] == [shadow] and cf2[0]["same"] == [] and \
        sorted(f.get("short", "") for f in fl2) == [f"f{k:03d}" for k in range(1, len(fl2) + 1)]
    # 4c 第一次建库的两轮归族
    r4, f4, m4 = (os.path.join(OUT, x) for x in ("rules_2r", "families_2r", "merge_2r"))
    shutil.copytree(rules, r4)
    os.makedirs(m4)
    extra = []
    for t in ("测试：第三条文字阴影规矩", "测试：第四条文字阴影规矩"):
        x = dict(L.jload(os.path.join(rules, shadow + ".json")), title=t, id=L.rule_id("代码", t))
        L.jsave(os.path.join(r4, x["id"] + ".json"), x)
        extra.append(x["id"])
    gid = L.rule_id(gen["product"], gen["title"])
    code, out = run("families.py", "propose", "--rules", r4, "--out", f4, "--merge", m4)
    p1 = {pr["proposal"]: pr for pr in (L.jload(p) for p in sorted(glob.glob(os.path.join(f4, "proposals", "*.json"))))}
    cp1 = [k for k, v in p1.items() if v["product"] == "代码"]
    ok1 = code == 0 and len(cp1) == 1 and {x["id"] for x in p1[cp1[0]]["rules"]} == {shadow, offset, *extra} and \
        os.path.isfile(os.path.join(r4, gid + ".json")) and not any(x["id"] == gid for v in p1.values() for x in v["rules"])
    for pid, pr in p1.items():
        if pr["product"] == "代码":
            d = {"proposal": pid, "move_out": [{"rule": e, "reason": "测试：先挪出去"} for e in extra], "families": [
                {"name": "TextView 的文字阴影属性", "dir": "text-shadow", "line": "源端 TextView 带 shadow* 属性", "topic": {"dir": "ui/text", "name": "文本"},
                 "rules": [shadow, offset], "general": gen, "same": [{"rules": [shadow, offset], "reason": "测试：第一轮标的"}]}]}
        else:
            d = {"proposal": pid, "move_out": [], "families": [{"name": "自绘画布的单位", "dir": "canvas-unit", "line": "规格里写画布单位的那一节",
                                                                "topic": {"dir": "canvas", "name": "画布"}, "rules": [x["id"] for x in pr["rules"]], "general": None}]}
        L.jsave(os.path.join(f4, "decisions", pid + ".json"), d)
    code, out = run("families.py", "apply", "--rules", r4, "--out", f4, "--merge", m4, "--fresh", "--no-topic-decisions")
    ok1 = ok1 and code == 1 and {u["rule"] for u in L.jload(os.path.join(f4, "unplaced.json"), [])} == set(extra)
    code, out = run("families.py", "same-groups", "--rules", r4, "--out", f4, "--merge", m4)
    s1 = io.open(os.path.join(m4, "groups", "same-0001.json"), encoding="utf-8").read() if code == 0 else ""
    ok1 = ok1 and [m["tmp"] for m in json.loads(s1 or "{}").get("members") or []] == [shadow, offset]

    def snap():
        return {p: io.open(p, encoding="utf-8").read() for sub in ("proposals", "batches", "decisions") for p in glob.glob(os.path.join(f4, sub, "*"))}
    before = snap()
    code, out = run("families.py", "propose", "--rules", r4, "--out", f4, "--merge", m4)      # 从头出：已有决定，应当拒绝、什么都不动
    res["two_rounds_round1"] = ok1 and code != 0 and "已有决定" in out and snap() == before
    code, out = run("families.py", "propose", "--rules", r4, "--out", f4, "--merge", m4, "--new-only")
    after = snap()
    pid2 = f"fam-{len(p1) + 1:04d}"
    p2 = L.jload(os.path.join(f4, "proposals", pid2 + ".json"), {})
    res["two_rounds_propose"] = code == 0 and all(after.get(p) == v for p, v in before.items()) and p2.get("round") == 2 and \
        {x["id"] for x in p2.get("rules") or []} == set(extra) and len(after) == len(before) + 2 and \
        os.path.isfile(os.path.join(f4, "batches", "family-002.txt")) and \
        any(x["dir"] == "text-shadow" for x in p2.get("existing_families") or [])
    L.jsave(os.path.join(f4, "decisions", pid2 + ".json"), {"proposal": pid2, "move_out": [], "families": [
        {"name": "TextView 的文字阴影属性", "dir": "text-shadow", "line": "源端 TextView 带 shadow* 属性", "topic": {"dir": "ui/text", "name": "文本"},
         "rules": extra, "general": None, "same": [{"rules": extra, "reason": "测试：第二轮标的"}]}]})
    code, out = run("families.py", "apply", "--rules", r4, "--out", f4, "--merge", m4, "--check", "--proposals", pid2)
    ok2 = code == 0
    code, out = run("families.py", "apply", "--rules", r4, "--out", f4, "--merge", m4, "--fresh", "--no-topic-decisions")
    fl4 = L.jload(os.path.join(f4, "families.json"), [])
    cf4 = [f for f in fl4 if f["product"] == "代码"]
    res["two_rounds_apply"] = ok2 and code == 0 and L.jload(os.path.join(f4, "unplaced.json"), [1]) == [] and len(fl4) == 2 and \
        len(cf4) == 1 and cf4[0]["rules"] == [shadow, offset, *extra] and cf4[0]["general"] == gid and len(cf4[0]["same"]) == 2 and \
        "后一轮放进了族的 2 条" in out
    code, out = run("families.py", "same-groups", "--rules", r4, "--out", f4, "--merge", m4)
    s2 = L.jload(os.path.join(m4, "groups", "same-0002.json"), {})
    b2 = io.open(os.path.join(m4, "batches", "same-002.txt"), encoding="utf-8").read() if os.path.isfile(os.path.join(m4, "batches", "same-002.txt")) else ""
    res["two_rounds_same_stable"] = code == 0 and io.open(os.path.join(m4, "groups", "same-0001.json"), encoding="utf-8").read() == s1 and \
        [m["tmp"] for m in s2.get("members") or []] == extra and "same-0002.json" in b2 and "same-0001.json" not in b2 and \
        "same-0001.json" in io.open(os.path.join(m4, "batches", "same-001.txt"), encoding="utf-8").read()
    # 5 propose --new-only
    r3 = os.path.join(OUT, "rules_new")
    shutil.copytree(rules, r3)
    nr = dict(L.jload(os.path.join(rules, shadow + ".json")), id="rule-00000000000f", title="测试：新来的一条文字阴影规矩")
    L.jsave(os.path.join(r3, "rule-00000000000f.json"), nr)
    f3 = os.path.join(OUT, "families_new")
    shutil.copytree(fam, f3)
    code, out = run("families.py", "propose", "--rules", r3, "--out", f3, "--new-only", "--existing-top", "1")
    np_ = [x for x in (L.jload(p) for p in glob.glob(os.path.join(f3, "proposals", "*.json"))) if x.get("round") == 2]
    res["propose_new_only"] = code == 0 and len(np_) == 1 and len(np_[0].get("existing_families") or []) == 1 and \
        "similarity" in np_[0]["existing_families"][0] and np_[0]["existing_families"][0]["dir"] == "text-shadow"
    # 6 build_index
    code, out = run("build_index.py", "--rules", rules, "--families", fam, "--out", tree)
    keys_ = [json.loads(x) for x in io.open(os.path.join(tree, "keys.jsonl"), encoding="utf-8")] if code == 0 else []
    top = io.open(os.path.join(tree, "index.md"), encoding="utf-8").read() if code == 0 else ""
    tui = io.open(os.path.join(tree, "code", "ui", "index.md"), encoding="utf-8").read() if code == 0 else ""
    res["build_index"] = code == 0 and len(keys_) == 4 and all(os.path.isfile(os.path.join(tree, *k["path"].split("/"))) for k in keys_) and \
        os.path.isfile(os.path.join(tree, "manifest.json")) and "源端是 View 和布局 XML" in top and "手里有 TextView" in tui and \
        any("## 通用查法" in io.open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(tree, "code", "**", "index.md"), recursive=True))
    cmap = io.open(os.path.join(tree, "code", "map.md"), encoding="utf-8").read() if code == 0 else ""
    man = L.jload(os.path.join(tree, "manifest.json"), {})
    cshort = next((k["family_short"] for k in keys_ if k["product"] == "代码"), "")
    res["build_index_map"] = bool(cshort) and f"{cshort} TextView 的文字阴影属性（3）" in cmap and "文本（3 条）：手里有" in cmap and \
        "](" not in cmap and (man.get("family_short") or {}).get(cshort) == "code/ui/text/text-shadow" and \
        os.path.isfile(os.path.join(tree, "spec", "map.md"))
    # 7 recall
    rd, wr = os.path.join(OUT, "read.xml"), os.path.join(OUT, "Page.ets")
    io.open(rd, "w", encoding="utf-8").write('<TextView android:shadowColor="#80000000" android:shadowRadius="2" />\n')
    io.open(wr, "w", encoding="utf-8").write("Text(this.title)\n  .shadow({ radius: 2, color: '#80000000' })\n")
    code, out = run("recall.py", "coarse", "--rules", tree, "--product", "代码", "--read", rd, "--wrote", wr, "--json")
    topr = json.loads(out[out.index("["):]) if code == 0 else []
    code_rules = {k["id"] for k in keys_ if k["product"] == "代码"}
    res["recall_top_and_probe"] = bool(topr) and topr[0]["id"] in code_rules and bool(topr[0]["probe"])
    code, out = run("recall.py", "coarse", "--rules", tree, "--product", "代码", "--read", rd, "--wrote", wr, "--level", "family", "--json")
    topf = json.loads(out[out.index("["):]) if code == 0 else []
    res["recall_family_level"] = bool(topf) and topf[0]["family_dir"].endswith("/text-shadow") and topf[0]["rules"] == 3 and \
        topf[0].get("short") == cshort
    code, out = run("recall.py", "lines", shadow or "x", "--rules", tree, "--exclude-apps", "AntennaPod")
    res["recall_exclude_apps"] = code == 0 and "视图里没有这条" in out
    code, out = run("recall.py", "body", shadow or "x", "--rules", tree)
    res["recall_body"] = code == 0 and out.startswith("# TextView")
    code, out = run("recall.py", "show", "index", "code/ui/text/text-shadow", shadow or "x", "spec/canvas", "--rules", tree, "--products", "代码")
    res["recall_show"] = code == 0 and out.count("==== ") == 4 and "代码（code）" in out and "规格（spec）" not in out and \
        "agent 会看到什么" in out and "# TextView" in out and "跳过" in out
    code, out = run("recall.py", "show", "map", "--rules", tree, "--products", "代码")
    res["recall_show_map"] = code == 0 and f"{cshort} TextView 的文字阴影属性（3）" in out and "规格：" not in out and "](" not in out
    code, out = run("recall.py", "show", cshort or "f999", shadow or "x", "--rules", tree)
    blk = out.split("==== ")[1] if out.count("==== ") == 2 else ""
    res["recall_show_short"] = code == 0 and blk.splitlines()[1:2] == [f"{cshort} TextView 的文字阴影属性（3 条）"] and \
        "agent 会看到什么：源端 TextView" in blk and "通用查法：" in blk and \
        sum(1 for x in blk.splitlines() if x.startswith("rule-") and "｜" in x) == 2 and "# TextView" in out.split("==== ")[2]
    code, out = run("recall.py", "coarse", "--rules", tree, "--products", "代码,规格", "--read", rd, "--wrote", wr, "--level", "family",
                    "--k", "1", "--as-tree")
    tl_ = out.splitlines()
    res["recall_as_tree"] = code == 0 and tl_[0].startswith("粗筛出的一部分") and "show map" in tl_[0] and "入选 1 个" in tl_[0] and \
        "界面 / 文本：手里有 TextView" in out and f"  {cshort} TextView 的文字阴影属性（3）" in tl_ and "画布" not in out and \
        "0." not in out and "［" not in out
    code, out = run("recall.py", "coarse", "--rules", tree, "--products", "代码,规格", "--read", rd, "--wrote", wr, "--k", "2", "--with-lines")
    tl_ = out.splitlines()
    res["recall_as_tree_lines"] = code == 0 and "入选 2 个" in tl_[0] and "代码：入选 1 个族" in tl_ and "规格：入选 1 个族" in tl_ and \
        "    agent 会看到什么：源端 TextView 带 shadow* 属性" in tl_ and \
        sum(1 for x in tl_ if x.startswith("    通用查法：rule-") and "测试用通用查法" in x) == 1 and \
        sum(1 for x in tl_ if x.startswith("    rule-") and "｜" in x) == 3 and "已核实的写法" not in out
    # 7b 来源明细、对照表、产物目录的 index.md；recall 默认不带来源明细；部署包
    page = io.open(os.path.join(tree, *next(k["path"] for k in keys_ if k["id"] == shadow).split("/")), encoding="utf-8").read()
    cards_md = io.open(os.path.join(tree, "cards.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(tree, "cards.md")) else ""
    pidx = io.open(os.path.join(tree, "code", "index.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(tree, "code", "index.md")) else ""
    code, out = run("recall.py", "show", shadow, "--rules", tree)
    code2, out2 = run("recall.py", "show", shadow, "--rules", tree, "--with-sources")
    res["export_sources"] = "来源：2 张卡" in page and f"- {CODE}（" in page and "做法第 1 步 ← 建议 3" in page and \
        f"- {OTHER}（" in page and f"- {CODE}（" not in out and "来源：2 张卡" in out and f"- {CODE}（" in out2 and \
        f"{CODE}｜" in cards_md and shadow in cards_md and "](map.md)" in pidx and "](ui/index.md)" in pidx
    dep = os.path.join(OUT, "deploy")
    code, out = run("build_index.py", "--rules", rules, "--families", fam, "--out", os.path.join(OUT, "rules_tree_again"),
                    "--deploy-out", dep, "--products", "代码")
    dkeys = [json.loads(x) for x in io.open(os.path.join(dep, "keys.jsonl"), encoding="utf-8")] if code == 0 else []
    r3 = subprocess.run([sys.executable, "-X", "utf8", os.path.join(dep, "scripts", "recall.py"), "show", "map"], capture_output=True, text=True,
                        encoding="utf-8", cwd=dep)
    dpage = io.open(os.path.join(dep, *dkeys[0]["path"].split("/")), encoding="utf-8").read() if dkeys else ""
    res["export_deploy"] = code == 0 and bool(dkeys) and all(k["product"] == "代码" for k in dkeys) and \
        not any("sources" in k or "apps" in k for k in dkeys) and not os.path.exists(os.path.join(dep, "manifest.json")) and \
        not os.path.exists(os.path.join(dep, "cards.md")) and not os.path.exists(os.path.join(dep, "spec")) and "- case-" not in dpage and \
        "来源：" in dpage and r3.returncode == 0 and "代码：" in r3.stdout and "规格：" not in r3.stdout
    # 8 基础库建完之后的一期增量：合并（p2）→ 归族（不加 --fresh）→ 超限拆分（族、主题节点）→ 导出
    r8, f8, m8, c8, t8 = (os.path.join(OUT, x) for x in ("inc_rules", "inc_families", "inc_merge", "inc_candidates", "inc_tree"))
    for s_, d_ in ((rules, r8), (fam, f8), (merge, m8)):
        shutil.copytree(s_, d_)
    os.makedirs(c8)
    NEW = "case-test00000000000002"
    inc = []
    for t in ("测试：第二期讲文字阴影颜色的候选", "测试：第二期讲文字阴影半径的候选"):
        x = dict(copy.deepcopy(o["rules"][0]), title=t, x_sources=[OTHER])
        x["how"][0]["support"] = [OTHER + "#recommendation:4"]
        inc.append(x)
    L.jsave(os.path.join(c8, NEW + ".json"), {"case": NEW, "rules": inc, "left_out": [], "corrections": [], "gaps": [], "conflicts": []})
    base_files = {p: io.open(p, encoding="utf-8").read() for sub in ("groups", "batches", "decisions") for p in glob.glob(os.path.join(m8, sub, "*"))}
    code, out = run("cluster.py", "--candidates", c8, "--out", m8, "--existing", r8, "--phase", "p2")
    g8 = L.jload(os.path.join(m8, "groups", "p2-0001.json"), {"members": []})
    res["inc_cluster"] = code == 0 and {m["tmp"] for m in g8["members"]} == {NEW + "#1", NEW + "#2", shadow, offset} and \
        all(io.open(p, encoding="utf-8").read() == v for p, v in base_files.items() if os.path.isfile(p)) and \
        all(os.path.isfile(p) for p in base_files) and os.path.isfile(os.path.join(m8, "batches", "p2-001.txt")) and \
        os.path.isfile(os.path.join(m8, "singles-p2.json"))
    L.jsave(os.path.join(m8, "decisions", "p2-0001.json"), {"group": "p2-0001", "merged": [
        {"members": [shadow, NEW + "#1"], "reason": "测试：同一个触发、同一个做法", "rule": copy.deepcopy(mr)}],
        "kept": [{"member": offset, "reason": "测试：讲偏移"}, {"member": NEW + "#2", "reason": "测试：另成一条"}]})
    rb = L.rule_id("代码", inc[1]["title"])
    code0, _ = run("apply_merge.py", "--merge", m8, "--rules-out", r8)                    # 不加 --fresh 落基础库的组：拒绝
    code, out = run("apply_merge.py", "--merge", m8, "--rules-out", r8, "--prefix", "p2")
    files1 = sorted(os.listdir(r8))
    code2, out2 = run("apply_merge.py", "--merge", m8, "--rules-out", r8, "--prefix", "p2")   # 重跑同一期：结果不变
    mm8 = L.jload(os.path.join(m8, "merge_map.json"), {})
    res["inc_merge"] = code0 != 0 and code == 0 and code2 == 0 and sorted(os.listdir(r8)) == files1 and "撞号改哈希的 0 条" in out2 and \
        mm8.get(NEW + "#1") == shadow and mm8.get(NEW + "#2") == rb and mm8.get(CODE + "#2") == offset and \
        os.path.isfile(os.path.join(r8, rb + ".json")) and os.path.isfile(os.path.join(r8, offset + ".json"))
    code, out = run("families.py", "propose", "--rules", r8, "--out", f8, "--merge", m8, "--new-only")
    p8 = [x for x in (L.jload(p) for p in glob.glob(os.path.join(f8, "proposals", "*.json"))) if x.get("round") == 2]
    ok8 = code == 0 and len(p8) == 1 and [x["id"] for x in p8[0]["rules"]] == [rb] and \
        any(x["dir"] == "text-shadow" and x["topic_name"] == "文本" for x in p8[0]["existing_families"])
    pid8 = p8[0]["proposal"] if p8 else "x"
    L.jsave(os.path.join(f8, "decisions", pid8 + ".json"), {"proposal": pid8, "move_out": [], "families": [
        {"name": "TextView 的文字阴影属性", "dir": "text-shadow", "line": "源端 TextView 带 shadow* 属性", "topic": {"dir": "ui/text", "name": "文本"},
         "rules": [rb], "general": None, "same": []}]})
    code, out = run("families.py", "apply", "--rules", r8, "--out", f8, "--merge", m8)
    fl8 = L.jload(os.path.join(f8, "families.json"), [])
    cf8 = [f for f in fl8 if f["product"] == "代码"]
    tj8 = L.jload(os.path.join(f8, "topics.json"), {})
    st8 = L.jload(os.path.join(f8, "apply_state.json"), {})
    before8 = io.open(os.path.join(f8, "families.json"), encoding="utf-8").read()
    code0, out0 = run("families.py", "apply", "--rules", r8, "--out", f8, "--merge", m8, "--fresh")          # 有增量之后 --fresh：拒绝
    res["inc_families"] = ok8 and code == 0 and len(fl8) == 2 and len(cf8) == 1 and cf8[0]["rules"] == [shadow, offset, rb] and \
        cf8[0]["topic"] == "ui/text" and (tj8.get("code", {}).get("ui/text") or {}).get("line", "").startswith("手里有") and \
        st8.get("incremental_rounds") == [2] and code0 != 0 and "冲掉" in out0 and \
        io.open(os.path.join(f8, "families.json"), encoding="utf-8").read() == before8
    # 超限的族：按 --max-rules 2 拆
    lim = ["--max-rules", "2", "--max-children", "2"]
    code1, out1 = run("families.py", "oversize", "--rules", r8, "--out", f8, *lim)
    code, out = run("families.py", "split-families", "--rules", r8, "--out", f8, *lim)
    sp = [x for x in (L.jload(p) for p in glob.glob(os.path.join(f8, "proposals", "*.json"))) if x.get("split_of")]
    pid9 = sp[0]["proposal"] if sp else "x"
    ok9 = code1 == 1 and "TextView 的文字阴影属性（3 条）" in out1 and code == 0 and len(sp) == 1 and sp[0]["split_of"] == cf8[0]["key"] and \
        sp[0]["round"] == 3 and [x["id"] for x in sp[0]["generals"]] == [gid] and {x["id"] for x in sp[0]["rules"]} == {shadow, offset, rb}

    def split_dec(g0):
        L.jsave(os.path.join(f8, "decisions", pid9 + ".json"), {"proposal": pid9, "move_out": [], "families": [
            {"name": "文字阴影的颜色和半径", "dir": "shadow-color", "line": "源端 TextView 带 shadowColor / shadowRadius", "topic": {"dir": "x", "name": "x"},
             "rules": [shadow], "general": g0, "same": []},
            {"name": "文字阴影的偏移", "dir": "shadow-offset", "line": "源端 TextView 带 shadowDx / shadowDy", "topic": {"dir": "x", "name": "x"},
             "rules": [offset], "general": None, "same": []},
            {"name": "第二期的文字阴影", "dir": "shadow-extra", "line": "源端 TextView 带 shadow* 属性（第二期）", "topic": {"dir": "x", "name": "x"},
             "rules": [rb], "general": None, "same": []}]})
    split_dec("rule-000000000bad")
    code, out = run("families.py", "apply", "--rules", r8, "--out", f8, "--merge", m8, "--check", "--proposals", pid9)
    ok9 = ok9 and code == 1 and "只能是原族的通用查法" in out
    split_dec(gid)
    code, out = run("families.py", "apply", "--rules", r8, "--out", f8, "--merge", m8, "--check", "--proposals", pid9)
    ok9 = ok9 and code == 0
    code, out = run("families.py", "apply", "--rules", r8, "--out", f8, "--merge", m8)
    fl9 = L.jload(os.path.join(f8, "families.json"), [])
    cf9 = [f for f in fl9 if f["product"] == "代码"]
    res["inc_split_family"] = ok9 and code == 0 and [f["dir"] for f in cf9] == ["shadow-color", "shadow-offset", "shadow-extra"] and \
        all(f["topic"] == "ui/text" for f in cf9) and cf9[0]["general"] == gid and os.path.isfile(os.path.join(r8, gid + ".json"))
    # 超限的主题节点：ui/text 下 3 个族 > 2，加一层
    code1, out1 = run("families.py", "oversize", "--rules", r8, "--out", f8, *lim)
    code, out = run("families.py", "topic-split-lists", "--rules", r8, "--out", f8, *lim)
    tl8 = L.jload(os.path.join(f8, "topic_splits", "lists", "ts-0001.json"), {})
    keys9 = {f["dir"]: f["key"] for f in cf9}
    ok10 = code1 == 1 and "code/ui/text" in out1 and code == 0 and tl8.get("node") == "ui/text" and len(tl8.get("children") or []) == 3 and \
        os.path.isfile(os.path.join(f8, "batches", "topic-split-001.txt"))
    tsd = {"split": "ts-0001", "node": "ui/text", "topics": [{"dir": "shadow", "name": "文字阴影", "line": "源端 TextView 带 shadow* 属性时"}],
           "assign": [{"family": keys9.get("shadow-color"), "topic": "shadow"}, {"family": keys9.get("shadow-offset"), "topic": "shadow"}]}
    L.jsave(os.path.join(f8, "topic_splits", "decisions", "ts-0001.json"), tsd)
    code, out = run("families.py", "topic-split-check", "--split", "ts-0001", "--out", f8)
    ok10 = ok10 and code == 1 and "没有在 assign 里" in out
    tsd["assign"].append({"family": keys9.get("shadow-extra"), "topic": ""})
    L.jsave(os.path.join(f8, "topic_splits", "decisions", "ts-0001.json"), tsd)
    code, out = run("families.py", "topic-split-check", "--split", "ts-0001", "--out", f8)
    ok10 = ok10 and code == 0
    code, out = run("families.py", "topic-split-apply", "--rules", r8, "--out", f8, *lim)
    fl10 = L.jload(os.path.join(f8, "families.json"), [])
    tj10 = L.jload(os.path.join(f8, "topics.json"), {})
    code1, out1 = run("families.py", "oversize", "--rules", r8, "--out", f8, *lim)
    res["inc_split_topic"] = ok10 and code == 0 and code1 == 0 and \
        sorted(f["topic"] for f in fl10 if f["product"] == "代码") == ["ui/text", "ui/text/shadow", "ui/text/shadow"] and \
        (tj10.get("code", {}).get("ui/text/shadow") or {}).get("name") == "文字阴影" and \
        L.jload(os.path.join(f8, "apply_state.json"), {}).get("topic_splits_applied") == ["ts-0001"]
    code, out = run("build_index.py", "--rules", r8, "--families", f8, "--out", t8)
    m8txt = io.open(os.path.join(t8, "code", "map.md"), encoding="utf-8").read() if code == 0 else ""
    code2, out2 = run("recall.py", "show", "code/ui/text/shadow", "--rules", t8)
    code3, out3 = run("recall.py", "coarse", "--rules", t8, "--product", "代码", "--read", rd, "--wrote", wr, "--as-tree", "--k", "3")
    res["inc_export_deep"] = code == 0 and os.path.isfile(os.path.join(t8, "code", "ui", "text", "shadow", "shadow-color", "index.md")) and \
        "界面 / 文本 / 文字阴影（" in m8txt and code2 == 0 and "文字阴影的偏移" in out2 and \
        code3 == 0 and "界面 / 文本 / 文字阴影：源端 TextView" in out3 and "第二期的文字阴影" in out3
    L.jsave(os.path.join(OUT, "selftest_pipeline.json"), res)
    for k, v in res.items():
        print(f"{k}: {'通过' if v else '没通过'}")
    print("流程自测", "通过" if all(res.values()) else "没通过")
    sys.exit(0 if all(res.values()) else 1)


if __name__ == "__main__":
    main()
