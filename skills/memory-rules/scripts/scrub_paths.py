# -*- coding: utf-8 -*-
"""一次性的清理：过程记录（合并的组和决定、归族的决定、批次清单、报告）里的本机路径。
  - JSON 文件：嵌在任何位置的出处（带 kind、where 的对象，如组成员的全文、merged[].rule、通用查法 general）照 migrate_refs.py
    的办法改成可移植写法；其余字符串里在分支根目录下的绝对路径改成相对分支根目录的路径（用 /）。
  - 文本文件（批次清单）：每行在分支根目录下的绝对路径改成相对路径。
  改完再扫一遍，仍带本机路径的列出来（不硬改）。只改给的文件，不碰 store/rules/ 和 families.json。
用法： py -3 -X utf8 skills/memory-rules/scripts/scrub_paths.py <文件或目录…> [--dry-run]
  目录里的 *.json、*.txt 都处理。"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, json, os, re  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_refs as M  # noqa: E402
import rulelib as L  # noqa: E402
import sources as S  # noqa: E402

LOCAL = re.compile(r"(?i)Users[\\/]+[^\\/\s\"]+[\\/]|(?<![A-Za-z0-9])[A-Za-z]:[\\/]")


def rel(s):
    """分支根目录下的绝对路径 → 相对路径（用 /）；别的原样。"""
    if not isinstance(s, str) or not re.match(r"[A-Za-z]:[\\/]", s):
        return s
    a, r = os.path.normcase(os.path.abspath(s)), os.path.normcase(os.path.abspath(L.ROOT))
    if a == r:
        return "."
    if a.startswith(r + os.sep):
        return os.path.abspath(s)[len(os.path.abspath(L.ROOT)) + 1:].replace("\\", "/")
    return s


def walk(o, stats, bad, where):
    """改 o（原地）：出处对象走 migrate_ref，其余字符串走 rel。返回改没改。"""
    ch = False
    if isinstance(o, dict):
        if isinstance(o.get("kind"), str) and o.get("kind") in S.KIND_ROOT and isinstance(o.get("where"), str):
            stats["refs"] += 1
            ch |= M.migrate_ref(o, stats, bad, where)
        for k, v in list(o.items()):
            if isinstance(v, str):
                nv = rel(v)
                if nv != v and not (k == "where" and o.get("kind") in S.KIND_ROOT):
                    o[k] = nv
                    stats["paths"] += 1
                    ch = True
            else:
                ch |= walk(v, stats, bad, where)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str):
                nv = rel(v)
                if nv != v:
                    o[i] = nv
                    stats["paths"] += 1
                    ch = True
            else:
                ch |= walk(v, stats, bad, where)
    return ch


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    files = []
    for x in a.paths:
        files += sorted(glob.glob(os.path.join(x, "*.json")) + glob.glob(os.path.join(x, "*.txt"))) if os.path.isdir(x) else [x]
    stats, bad, changed, left = collections.Counter(), [], collections.Counter(), []
    for p in files:
        raw = io.open(p, encoding="utf-8").read()
        if p.endswith(".json"):
            o = json.loads(raw)
            if not walk(o, stats, bad, os.path.basename(p)):
                new = raw
            else:
                new = json.dumps(o, ensure_ascii=False, indent=1) + "\n"
        else:
            lines = raw.splitlines()
            out = [rel(x.strip()) if x.strip() else x for x in lines]
            stats["paths"] += sum(1 for x, y in zip(lines, out) if x.strip() != y)
            new = "\n".join(out) + ("\n" if raw.endswith("\n") else "")
        if new != raw:
            changed[os.path.basename(os.path.dirname(p)) + "/" + ("*.txt" if p.endswith(".txt") else "*.json")] += 1
            if not a.dry_run:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
        if LOCAL.search(new):
            left.append(os.path.relpath(p, L.ROOT).replace("\\", "/"))
    print(f"文件 {len(files)} 个，改了 {sum(changed.values())} 个：{dict(changed)}")
    print(f"出处 {stats['refs']} 条：改写 {sum(stats[k] for k in S.KIND_ROOT)}（{ {k: stats[k] for k in S.KIND_ROOT if stats[k]} }），"
          f"已是可移植写法 {stats['already']}，几个版本一样取最低的 {stats['lowest_version_chosen']}，没改的 {len(bad)}；其余路径改成相对的 {stats['paths']} 处"
          + ("（--dry-run，没写文件）" if a.dry_run else ""))
    for b in bad[:10]:
        print("  没改：", b)
    print(f"改完仍带本机路径的文件 {len(left)} 个：{left[:10]}")


if __name__ == "__main__":
    main()
