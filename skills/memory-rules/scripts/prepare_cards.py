# -*- coding: utf-8 -*-
"""第 1 步「准备」：把本分支 store/ 里 HEAD 指的那一版卡库渲染成提炼用的工作包，并分批。

读：store/HEAD.json → store/snapshots/<revision>.json → store/cases/<卡号>/<revision>.json（只读，不改 store/）。
写（都在分支根目录的 work/ 下，work/ 不进版本库）：
  work/cards/<卡号>.md        一张卡一个文件：情境（title / when / description / 环境版本）、诊断全文、每条建议原文、
                              卡里记的没核到的点（unknown）、调查图里各产物的节点内容（每个节点的说明，标出出问题的节点）。
                              结论前的方括号是它在 support 里的写法，例如 [case-…#recommendation:2]。撤回的结论标明不能引。
  work/cards_index.json       每张卡：卡号、所属应用、在快照 e613047f 里有没有、建议条数、卡的 revision；另有应用清单
                              （check_rules.py 用它生成出事应用的名单）。所属应用取卡的 metadata.migration.project；没记的
                              从卡里路径的 …/harmony/<目录名> 认（app_basis = path），都没有的记「未记录」。
  work/batches/extract-NNN.txt  提炼分批：全部卡号排序后 random.Random(1115).shuffle，按顺序切成每批不超过 12 张
                              （批数 = ceil(总数 / 12)，各批张数相差不超过 1）；每行一个卡文件的绝对路径。
  work/batches/pilot.txt      试跑小样：全部卡号排序后 random.Random(1115).sample(…, 12)，每行一个卡文件的绝对路径
                              （这 12 张也照常在 extract 批次里）。
  work/lists/in-e613047f.txt、not-in-e613047f.txt  按卡是否在快照 e613047f 里分开的卡号清单（分两期建库用）。
用法： py -3 -X utf8 skills/memory-rules/scripts/prepare_cards.py [--per-batch 12] [--pilot 12] [--seed 1115]
       py -3 -X utf8 skills/memory-rules/scripts/prepare_cards.py --lists-only     只写 work/lists/ 的两个清单（不动卡文件和批次）"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, io, json, math, os, random, re, shutil  # noqa: E401,E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
STORE = os.path.join(ROOT, "store")
WORK = os.path.join(ROOT, "work")
E613 = "e613047f1f1074bea5aff8ac27e372ca643918ade9ded233caba6b941a542eb2"


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def quote(text):
    return "\n".join("> " + x if x.strip() else ">" for x in (text or "").strip().split("\n"))


def base(key):
    k = str(key or "").replace("\\", "/").rstrip("/")
    return k.rsplit("/", 1)[-1] or k


def env_line(c):
    seen = []
    for e in (c.get("metadata") or {}).get("environment") or []:
        s = f"{e.get('name')}={e.get('value')}"
        if s not in seen:
            seen.append(s)
    return "；".join(seen)


HARMONY_DIR = re.compile(r"/harmony/([^/]+)")


def infer_app(c):
    """卡里没记 metadata.migration.project 时，从调查图的产物和节点路径、环境记录的工作目录里取 …/harmony/<目录名>；
    只在恰好一个名字时采用（app_basis 记为 path），否则留空（未记录）。"""
    keys = [(g.get("target") or {}).get("key") or "" for g in c.get("graphs") or []]
    keys += [n.get("key") or "" for g in c.get("graphs") or [] for n in g.get("nodes") or []]
    keys += [e.get("cwd") or "" for e in (c.get("metadata") or {}).get("environment") or []]
    names = {m.group(1) for k in keys for m in HARMONY_DIR.finditer(str(k).replace("\\", "/"))}
    return names.pop() if len(names) == 1 else ""


def render(cid, c, meta, head):
    recs = c.get("recommendations") or []
    wd = set(meta.get("withdrawn_claims") or [])
    out = [f"# 卡 {cid}", "",
           f"- 库版本 {head[:8]}，这张卡的 revision {meta['revision'][:12]}；共 {len(recs)} 条建议。",
           f"- 结论前方括号里的内容就是它在 `support` 里的写法（`{cid}#diagnosis` 或 `{cid}#recommendation:N`）。"
           + (f"已撤回、不能引的：{'、'.join(sorted(wd))}。" if wd else ""),
           "- 卡是对某一次具体迁移的调查记录，里面的文件名、类名、资源名、控件 id、取值和文案属于出事的应用，不要带进规矩。",
           "", "## 情境", "",
           f"- title：{c.get('title')}", f"- when：{c.get('when')}", f"- description：{c.get('description')}"]
    env = env_line(c)
    if env:
        out.append(f"- 环境：{env}")
    out += ["", "## 诊断", "", f"[{cid}#diagnosis]" + ("（已撤回，不能引）" if "diagnosis" in wd else ""), "", quote(c.get("summary"))]
    out += ["", "## 建议"]
    for i, r in enumerate(recs, 1):
        k = f"recommendation:{i}"
        out += ["", f"[{cid}#{k}]" + ("（已撤回，不能引）" if k in wd else ""), "", quote(r)]
    unk = c.get("unknown") or []
    if unk:
        out += ["", "## 卡里记的没核到的点", ""] + [f"- {x}" for x in unk]
    gs = c.get("graphs") or []
    if gs:
        out += ["", "## 调查图里的节点（只供理解情境，不能作 support）", "",
                "每个产物一节：先是这个产物上的诊断（有的话），再按时间列出调查涉及的文件和子代理，「出问题」标的是偏差形成的地方。"]
        for gi, g in enumerate(gs, 1):
            out += ["", f"### 产物 {gi}：{base((g.get('target') or {}).get('key'))}"]
            if (g.get("summary") or "").strip():
                out += ["", quote(g["summary"])]
            out.append("")
            for n in g.get("nodes") or []:
                tag = "【出问题】" if n.get("problem") else ""
                out.append(f"- {tag}{base(n.get('key'))}：{(n.get('reason') or '').strip()}")
    return "\n".join(out) + "\n"


def write_lists(index):
    """work/lists/in-e613047f.txt、not-in-e613047f.txt：按卡是否在快照 e613047f 里分开的卡号清单（每行一个，按卡号排序）。
    分两期建库用：基础库只用前一个清单里的卡，第二期把后一个清单的卡按增量归并加进去。"""
    d = os.path.join(WORK, "lists")
    os.makedirs(d, exist_ok=True)
    out = {}
    for name, want in (("in-e613047f.txt", True), ("not-in-e613047f.txt", False)):
        ids = sorted(x["case"] for x in index if bool(x["in_e613047f"]) == want)
        io.open(os.path.join(d, name), "w", encoding="utf-8", newline="\n").write("".join(x + "\n" for x in ids))
        out[name] = len(ids)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-batch", type=int, default=12)
    ap.add_argument("--pilot", type=int, default=12)
    ap.add_argument("--seed", type=int, default=1115)
    ap.add_argument("--lists-only", action="store_true", help="只按已有的 work/cards_index.json 写 work/lists/ 的两个清单，不动卡文件和批次")
    a = ap.parse_args()
    if a.lists_only:
        print("清单：", write_lists(jload(os.path.join(WORK, "cards_index.json"))["index"]))
        return
    head = jload(os.path.join(STORE, "HEAD.json"))["revision"]
    snap = jload(os.path.join(STORE, "snapshots", head + ".json"))
    e613 = set(jload(os.path.join(STORE, "snapshots", E613 + ".json"))["cases"])
    cards_dir, batch_dir = os.path.join(WORK, "cards"), os.path.join(WORK, "batches")
    for d in (cards_dir, batch_dir):
        if os.path.exists(d):
            shutil.rmtree(d)          # 只删 work/ 下本脚本自己写的目录
        os.makedirs(d)
    index, apps, chars = [], collections.Counter(), []
    for cid in sorted(snap["cases"]):
        meta = snap["cases"][cid]
        if meta.get("status") != "available":
            continue
        c = jload(os.path.join(STORE, "cases", cid, meta["revision"] + ".json"))
        recorded = ((c.get("metadata") or {}).get("migration") or {}).get("project") or ""
        inferred = "" if recorded else infer_app(c)
        app = recorded or inferred
        text = render(cid, c, meta, head)
        io.open(os.path.join(cards_dir, cid + ".md"), "w", encoding="utf-8", newline="\n").write(text)
        chars.append(len(text))
        apps[app or "（未记录）"] += 1
        index.append({"case": cid, "app": app, "app_basis": "metadata" if recorded else ("path" if inferred else "未记录"),
                      "in_e613047f": cid in e613, "recommendations": len(c.get("recommendations") or []),
                      "withdrawn_claims": meta.get("withdrawn_claims") or [], "revision": meta["revision"], "title": c.get("title")})
    ids = [x["case"] for x in index]
    order = list(ids)
    random.Random(a.seed).shuffle(order)
    k = max(1, math.ceil(len(order) / a.per_batch))
    batches = [order[j::k] for j in range(k)]               # 轮流发牌：各批张数相差不超过 1，批内保持打乱后的顺序
    for j, b in enumerate(batches, 1):
        io.open(os.path.join(batch_dir, f"extract-{j:03d}.txt"), "w", encoding="utf-8", newline="\n").write(
            "".join(os.path.join(cards_dir, x + ".md") + "\n" for x in b))
    pilot = random.Random(a.seed).sample(ids, a.pilot)
    io.open(os.path.join(batch_dir, "pilot.txt"), "w", encoding="utf-8", newline="\n").write(
        "".join(os.path.join(cards_dir, x + ".md") + "\n" for x in pilot))
    json.dump({"library_revision": head, "e613047f": E613, "cards": len(index), "apps": len(apps),
               "in_e613047f": sum(x["in_e613047f"] for x in index),
               "app_list": [{"app": k_, "cards": v} for k_, v in sorted(apps.items(), key=lambda kv: (-kv[1], kv[0]))],
               "batches": {"seed": a.seed, "per_batch": a.per_batch, "count": k, "sizes": [len(b) for b in batches]},
               "pilot": pilot, "index": index},
              io.open(os.path.join(WORK, "cards_index.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    lists = write_lists(index)
    chars.sort()
    print(f"库版本 {head[:8]}：卡 {len(index)} 张，应用 {len(apps)} 个，其中在 e613047f 里的卡 {sum(x['in_e613047f'] for x in index)} 张；清单 {lists}")
    print(f"提炼分批 {k} 批（每批 {min(len(b) for b in batches)}–{max(len(b) for b in batches)} 张，种子 {a.seed}）；试跑小样 {len(pilot)} 张")
    print(f"卡文件字数：中位 {chars[len(chars) // 2]}，90% {chars[int(len(chars) * .9)]}，最大 {chars[-1]}")


if __name__ == "__main__":
    main()
