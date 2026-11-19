# 把 knowledge/lessons/*.json 渲染成带知识的经验文件，写到 knowledge/memory/ 下和 memory/ 相同的相对路径。
#   正文：按 json 里的 changes 把原句换成新句（每处必须正好对上一次，否则报错退出）。
#   后面：接一节「已核实的平台事实」（json 里的 entries；条目有 code 字段时带「写法」）。
#   来源和证据卡不复制，留一行指回 memory/ 里的原文件。
# 用法（在仓库根目录）：python knowledge/render.py
import os, io, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "memory")
KN = os.path.join(ROOT, "knowledge", "lessons")
OUT = os.path.join(ROOT, "knowledge", "memory")


def loose(s):
    """原句按「空白可有可无」去对。"""
    return re.compile(r"\s*".join(re.escape(x) for x in re.split(r"\s+", s.strip()) if x))


def apply_changes(body, changes, lid, problems):
    n = 0
    for c in changes:
        before, after = (c.get("before") or "").strip(), (c.get("after") or "").strip()
        if not before or not after:
            problems.append(f"{lid}：有一处改动缺原句或新句")
            continue
        if body.count(before) == 1:
            body = body.replace(before, after)
            n += 1
            continue
        m = list(loose(before).finditer(body))
        if len(m) == 1:
            body = body[:m[0].start()] + after + body[m[0].end():]
            n += 1
        else:
            problems.append(f"{lid}〔{c.get('where')}〕原句对上 {len(m)} 处：{before[:40]}…")
    return body, n


def block(d):
    sdk = d.get("sdk") or {}
    tail = "和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看"
    if any((e.get("code") or "").strip() for e in d.get("entries") or []):
        tail += "；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄"
    lines = ["## 已核实的平台事实", "",
             f"核实时用的是 {sdk.get('harmony', '鸿蒙 SDK')}；安卓 {sdk.get('android', '平台资源和源码')}。" + tail + "。", ""]
    for e in d.get("entries") or []:
        lines.append(f"- 〔{(e.get('step') or '').strip()}〕{(e.get('fact') or '').strip()}（出处：{(e.get('source') or '').strip()}）")
        code = (e.get("code") or "").strip()
        for i, ln in enumerate(x.strip() for x in code.split("\n") if x.strip()):
            lines.append(("  写法：" if i == 0 else "        ") + ln)
    return "\n".join(lines)


problems, done = [], 0
for p in sorted(glob.glob(os.path.join(KN, "lesson-*.json"))):
    d = json.load(io.open(p, encoding="utf-8"))
    lid = os.path.basename(p)[:-5]
    hits = glob.glob(os.path.join(SRC, "**", lid + ".lesson.md"), recursive=True)
    if len(hits) != 1:
        problems.append(f"{lid}：memory/ 里找到 {len(hits)} 个原文件")
        continue
    rel = os.path.relpath(hits[0], SRC)
    text = io.open(hits[0], encoding="utf-8").read().replace("\r\n", "\n")
    cut = re.search(r"(?m)^(来源支持：|## 来源)", text)          # 来源和证据卡不复制
    body = (text[:cut.start()] if cut else text).rstrip() + "\n"
    body, n = apply_changes(body, d.get("changes") or [], lid, problems)
    out = os.path.join(OUT, rel)
    back = os.path.relpath(hits[0], os.path.dirname(out)).replace(os.sep, "/")
    note = (f"> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/{lid}.json` 改了 {n} 句，"
            f"后面接了 {len(d.get('entries') or [])} 条已核实的平台事实。原文、来源和证据卡见 [{'memory/' + rel.replace(os.sep, '/')}]({back})。")
    body = body.replace("[本主题](index.md)", note, 1) if "[本主题](index.md)" in body else body.rstrip() + "\n\n" + note + "\n"
    parts = [body.rstrip()]
    if d.get("entries"):
        parts.append(block(d))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n\n".join(parts) + "\n")
    done += 1
print(f"渲染 {done} 条")
if problems:
    print("问题：")
    for x in problems:
        print("  " + x)
    sys.exit(1)
