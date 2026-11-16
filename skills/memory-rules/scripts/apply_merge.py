# -*- coding: utf-8 -*-
"""第 3 步「合并」的落盘：检查子代理的合并输出，把每组的结果和单独成组的候选写成规矩（store/rules/<规矩号>.json），最后跑检查。

读（--merge，默认 store/merge/）：groups/<组号>.json、singles.json（cluster.py 写的），decisions/<组号>.json（子代理写的，格式见
references/merge-brief.md）：
  {"group": "group-0001",
   "merged": [{"members": ["case-a#1", "case-b#2"], "reason": "一句理由", "rule": {候选格式的一条规矩，可带 "status"}}],
   "kept":   [{"member": "case-c#1", "reason": "一句理由"}]}
检查：每个组都有决定；组里每条候选恰好被处理一次（进了某个 merged 的 members，或在 kept 里），不多不少；merged 至少两条、
有理由，规矩的 product 和组的一样，status 只能是 active 或 disputed。有任何一处不对就停，不写规矩。
写成规矩：
  - 单独成组的、kept 的：候选原样（去掉 x_ 开头的语料栏），sources = 这张卡（语料带了 x_sources 的用它），general = false
    （语料带了 x_general 的用它），status = active；
  - merged 的：用子代理写的规矩，sources = 各成员来源的并集，general = false，status 取它写的（默认 active）；
  - 规矩号 = rule- 加 sha1(product + 换行 + title) 的前 12 位；两条不同的规矩撞号时，撞的那条把 sources 也算进哈希，并报出来；
  - 组里的已有规矩（增量归并时 cluster.py --existing 带进来的，或补并组 same-* 的全部成员）：kept 的不动；并进 merged 的，
    新规矩沿用其中按组文件顺序排在前面的那条已有规矩的规矩号，其余被并掉的已有规矩文件删除。
另写 merge_map.json（临时号 → 规矩号；被并掉的已有规矩号也作为临时号指向留下的那条）和 origins.json（规矩号 → 出自哪些临时号、
哪个组、理由）。全量（--fresh）时从头写；否则在已有的上面更新：原来指向被并掉的规矩的都改指留下的那条，被并掉的规矩的来历并进
留下的那条。最后对规矩目录跑 check_rules.py --dir <规矩目录>（--format-only 时只查格式）。
组的选择：默认只看基础库的组（group-*）和 singles.json，必须加 --fresh（不加 --fresh 重落基础库会和已有规矩全部撞号）；
--prefix <期名>（cluster.py --phase 起的名字，如 p2）只看这一期的组（<期名>-*）和 singles-<期名>.json，在已有规矩上改、不删别的；
--prefix same 只看归族时标出的补并组（same-*，families.py same-groups 写的），不碰 singles；--groups 直接点名。
增量和补并重跑同一期时结果不变：这一期以前落过的候选（merge_map 里已经指向某个规矩号的）不算撞号。
用法： py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --fresh [--merge DIR] [--rules-out DIR] [--format-only]   基础库
       py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --prefix p2            落盘增量这一期（在已有规矩上改）
       py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --prefix same          落盘补并组（在已有规矩上改）
       py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --check --groups <组号,…>     合并的子代理自检用
  --fresh：先删掉规矩目录里已有的 rule-*.json（全量重建时用；只能和基础库的组一起用）。
  --check：只检查这些组的决定，合并出的规矩写到 work/ 下这次调用自己的临时目录（merge_check-*，退出时删掉）跑 check_rules.py，
           不写规矩目录、merge_map 和 origins。"""
import sys

sys.dont_write_bytecode = True
import argparse, atexit, glob, os, shutil, subprocess, tempfile  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rulelib as L  # noqa: E402

DROP = ("id", "general", "status", "sources")


def clean(r):
    return {k: v for k, v in r.items() if not k.startswith("x_") and k not in DROP}


def sources_of(m):
    r = m["rule"]
    if m.get("existing"):
        return list(r.get("sources") or [])
    return list(r.get("x_sources") or [m["case"]])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--merge", default=os.path.join(L.STORE, "merge"))
    ap.add_argument("--rules-out", default=os.path.join(L.STORE, "rules"))
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--format-only", action="store_true")
    ap.add_argument("--check", action="store_true", help="只检查决定（给合并的子代理自检用）：不写规矩目录和映射，合并出的规矩写到 work/ 下临时目录跑检查")
    ap.add_argument("--groups", help="只看这些组（逗号分隔的组号）；--check 时常用")
    ap.add_argument("--prefix", default="group", help="只看组号以它开头的组：group（基础库，连同 singles.json，默认）、"
                                                     "增量的期名（如 p2，连同 singles-p2.json）或 same（归族时标出的补并组）")
    a = ap.parse_args()
    if not a.check and not a.groups:
        if a.prefix == "group" and not a.fresh:
            raise SystemExit("基础库的组（group-*）只能连同 --fresh 落盘；增量用 --prefix <期名>，补并用 --prefix same")
        if a.prefix != "group" and a.fresh:
            raise SystemExit(f"--prefix {a.prefix} 是在已有规矩上改，不能加 --fresh（会删掉全部已有规矩）")
    groups = {os.path.basename(p)[:-5]: L.jload(p) for p in sorted(glob.glob(os.path.join(a.merge, "groups", "*.json")))}
    f_singles = None if a.prefix == "same" else ("singles.json" if a.prefix == "group" else f"singles-{a.prefix}.json")
    singles = L.jload(os.path.join(a.merge, f_singles), []) if f_singles else []
    if a.groups:
        want = set(a.groups.split(","))
        groups = {k: v for k, v in groups.items() if k in want}
        singles = []
    else:
        groups = {k: v for k, v in groups.items() if k.startswith(a.prefix + "-")}
    if a.check:                # 每次调用一个临时目录（几批并行自检时互不相踩），退出时删掉
        os.makedirs(L.WORK, exist_ok=True)
        a.rules_out = tempfile.mkdtemp(prefix="merge_check-", dir=L.WORK)
        atexit.register(shutil.rmtree, a.rules_out, True)
        a.fresh = True
        singles = []
    bad, out = [], []          # out: (规矩, 来源临时号, 组号, 理由, 已有规矩号列表)
    for gid, g in groups.items():
        mem = {m["tmp"]: m for m in g["members"]}
        dp = os.path.join(a.merge, "decisions", gid + ".json")
        if not os.path.isfile(dp):
            bad.append(f"{gid}：没有决定文件 decisions/{gid}.json")
            continue
        d = L.jload(dp)
        seen = {}
        for k, x in enumerate(d.get("merged") or [], 1):
            ms = x.get("members") or []
            if len(ms) < 2:
                bad.append(f"{gid} merged 第 {k} 项：至少要两条候选")
            if not (x.get("reason") or "").strip():
                bad.append(f"{gid} merged 第 {k} 项：要写理由")
            r = x.get("rule")
            if not isinstance(r, dict):
                bad.append(f"{gid} merged 第 {k} 项：缺 rule")
                continue
            if r.get("product") != g["product"]:
                bad.append(f"{gid} merged 第 {k} 项：product 应为 {g['product']}")
            if r.get("status", "active") not in ("active", "disputed"):
                bad.append(f"{gid} merged 第 {k} 项：status 只能是 active 或 disputed")
            for t in ms:
                seen.setdefault(t, []).append(f"merged {k}")
            if all(t in mem for t in ms):
                src = sorted({s for t in ms for s in sources_of(mem[t])})
                old = [m["tmp"] for m in g["members"] if m.get("existing") and m["tmp"] in ms]   # 按组文件里的顺序：排在前面的留号
                out.append((dict(clean(r), sources=src, general=False, status=r.get("status", "active")), ms, gid, x.get("reason"), old))
        for k, x in enumerate(d.get("kept") or [], 1):
            t = x.get("member")
            seen.setdefault(t, []).append(f"kept {k}")
            if not (x.get("reason") or "").strip():
                bad.append(f"{gid} kept 第 {k} 项：要写理由")
            if t in mem and not mem[t].get("existing"):
                m = mem[t]
                out.append((dict(clean(m["rule"]), sources=sources_of(m), general=bool(m["rule"].get("x_general")), status="active"),
                            [t], gid, x.get("reason"), []))
        for t, where in seen.items():
            if t not in mem:
                bad.append(f"{gid}：{t} 不是这个组的成员")
            elif len(where) > 1:
                bad.append(f"{gid}：{t} 被处理了 {len(where)} 次（{'、'.join(where)}）")
        for t in mem:
            if t not in seen:
                bad.append(f"{gid}：{t} 没有被处理（要么并进某条，要么单独保留）")
    for s in singles:
        out.append((dict(clean(s["rule"]), sources=list(s["rule"].get("x_sources") or [s["case"]]),
                         general=bool(s["rule"].get("x_general")), status="active"), [s["tmp"]], None, "单独成组", []))
    if bad:
        print(f"合并输出有 {len(bad)} 处不对，没有写规矩：")
        for b in bad[:60]:
            print("  - " + b)
        sys.exit(1)
    os.makedirs(a.rules_out, exist_ok=True)
    if a.fresh:
        for p in glob.glob(os.path.join(a.rules_out, "rule-*.json")):
            os.remove(p)
    # 不是全量重建时，映射和来历在已有的上面更新（增量、补并）
    keep_maps = not a.fresh and not a.check
    mp = L.jload(os.path.join(a.merge, "merge_map.json"), {}) if keep_maps else {}
    origins = L.jload(os.path.join(a.merge, "origins.json"), {}) if keep_maps else {}
    ids, collisions, removed, alias = {}, [], [], {}
    taken = set() if a.fresh else {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(a.rules_out, "rule-*.json"))}
    for r, ms, gid, why, old in out:
        rid = old[0] if old else L.rule_id(r["product"], r["title"])
        mine_before = all(mp.get(t) == rid for t in ms)       # 重跑同一期：这些候选上次就落成了这条，不算撞号
        if not old and (rid in ids or (rid in taken and not mine_before)):   # 和这次写的或库里已有的撞号
            collisions.append({"title": r["title"], "first": ids.get(rid) or rid, "second": ms})
            rid = L.rule_id(r["product"], r["title"] + "\n" + ",".join(r["sources"]))
        ids[rid] = ms
        r = dict({"id": rid}, **r)
        L.jsave(os.path.join(a.rules_out, rid + ".json"), r)
        prev = [origins.pop(o, None) for o in old]            # 并进来的已有规矩原来的来历
        members = list(dict.fromkeys([t for p in prev if p for t in p.get("members") or []] + [t for t in ms if t not in old]))
        for t in ms:
            mp[t] = rid
        origins[rid] = {"members": members or ms, "group": gid, "reason": why,
                        **({"merged_rules": old} if len(old) > 1 else {})}
        for o in old[1:]:
            alias[o] = rid
            p = os.path.join(a.rules_out, o + ".json")
            if os.path.isfile(p):
                os.remove(p)
                removed.append(o)
    if alias:                                                 # 原来指向被并掉的规矩的临时号，改指留下的那条
        for t, v in list(mp.items()):
            if v in alias:
                mp[t] = alias[v]
    if not a.check:
        L.jsave(os.path.join(a.merge, "merge_map.json"), mp)
        L.jsave(os.path.join(a.merge, "origins.json"), origins)
    n_merged = sum(1 for _, ms, _, _, _ in out if len(ms) > 1)
    print(f"组 {len(groups)} 个、单独成组 {len(singles)} 条 → 规矩 {len(out)} 条（其中合并出的 {n_merged} 条）写进 {a.rules_out}；"
          f"撞号改哈希的 {len(collisions)} 条；删掉被并掉的已有规矩 {len(removed)} 条")
    for c in collisions[:10]:
        print("  撞号：", c)
    cmd = [sys.executable, "-X", "utf8", os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_rules.py"), "--dir", a.rules_out]
    if a.format_only:
        cmd.append("--format-only")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    lines = r.stdout.strip().splitlines()
    print("检查：", lines[-1] if lines else r.stderr[-300:])
    if r.returncode:
        print("\n".join(x for x in lines if x.startswith(("[", "  - ")))[:3000])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
