# -*- coding: utf-8 -*-
"""把知识文件渲染成交给模型的那段文字（不调模型，只读；只往 --out 指定的目录写）。

  - 知识段（知识文件有条目时才有）：
      已核实的平台事实（核实时用的是 <sdk.harmony>；安卓 <sdk.android>。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
      - 〔<step>〕<fact>
      - …
    不带出处（source）和链接，不带 code。sdk 缺键时用「鸿蒙 SDK」「平台资源和源码」。
    新格式的文件（sdk 里有 docs_date / docs_commit）段头在鸿蒙 SDK 后面多一句
    「；OpenHarmony 文档 master <docs_date>（提交 <docs_commit 前 8 位>）」；旧格式的文件段头不变。
    新格式文件的输出和经验库仓库里 knowledge/render.py 对同一文件、同一正文的输出逐字节相同。
  - 经验块（给了 --memory 时）：经验正文 = memory/<主题>/<经验号>.lesson.md 去掉「ID：…」一行和「[本主题](index.md)」一行，
    截到「## 来源」（或「## 同源经验」）之前；把知识文件的 changes 依次套上（已发布进正文的不再套；原句在当前文本里
    逐字出现一次就替换；否则按「空白可有可无」对上恰好一处再替换；都不是就报错、不套）；正文末尾去空白后空一行接知识段。
可选：--with-source 每条后面接「（出处：<source>）」（给人核对用）；--kinds=卡里验证,… 只留这几类条目。

用法：
  py -3.12 -B -X utf8 render.py <知识文件或目录> [--memory <memory 目录>] [--out <目录>] [--with-source] [--kinds=…]
不给 --out 时打印到标准输出（多条之间用一行「===== 经验号」隔开）；给了 --out 时每条写 <经验号>.md。
有改句套不上时退出码 1。只用标准库。"""
import sys

sys.dont_write_bytecode = True
import argparse, glob, io, json, os, re  # noqa: E401,E402

HEAD = "已核实的平台事实（核实时用的是 {h}；安卓 {a}。{tail}）："
TAIL = ("和具体应用无关，直接用，不用再查"
        "；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看")
SRC_RX = re.compile(r"\n## (?:来源|同源经验)")


def block(d, with_source=False, kinds=None):
    ent = d.get("entries") or []
    if kinds is not None:
        ent = [e for e in ent if e.get("kind") in kinds]
    if not ent:
        return ""
    sdk = d.get("sdk") or {}
    h = sdk.get("harmony", "鸿蒙 SDK")
    if sdk.get("docs_date") or sdk.get("docs_commit"):          # 新格式：段头多写文档用的是 master 哪一天的提交
        when = sdk.get("docs_date") or ""
        commit = (sdk.get("docs_commit") or "")[:8]
        h += "；OpenHarmony 文档 master " + when + (f"（提交 {commit}）" if commit else "")
    lines = [HEAD.format(h=h, a=sdk.get("android", "平台资源和源码"), tail=TAIL)]
    for e in ent:
        src = f"（出处：{(e.get('source') or '').strip()}）" if with_source else ""
        lines.append(f"- 〔{(e.get('step') or '').strip()}〕{(e.get('fact') or '').strip()}{src}")
    return "\n".join(lines)


def body(path):
    t = SRC_RX.split(io.open(path, encoding="utf-8").read(), maxsplit=1)[0]
    t = re.sub(r"(?m)^\[本主题\]\(index\.md\)\n\n?", "", t)
    t = re.sub(r"(?m)^ID：`lesson-[0-9a-f]+`.*\n\n?", "", t)
    return t.strip() + "\n"


def loose(s):
    parts = [re.escape(x) for x in re.split(r"\s+", s.strip()) if x]
    return re.compile(r"\s*".join(parts))


def published(text, before, after):
    """这处改句是不是已经发布进正文了：新句在正文里，而原句不在新句之外出现。
    并进经验库以后正文里就是新句，这时不再套、也不报错；渲染结果和「对着发布前的正文当场套」逐字节相同。"""
    if after not in text:
        return False
    if before not in text:
        return not list(loose(before).finditer(text))
    # 原句还在：只有它每一次出现都落在新句里面（新句 = 原句加了条件的那种）才算已发布
    return before in after and text.count(before) == text.count(after) * after.count(before)


def apply_changes(text, changes, lid):
    """依次套，逐字一处 → 替换；否则空白可有可无恰好一处 → 替换；否则报出来。
    已经发布进正文的改句（见 published）算套上、正文不动。"""
    problems, n = [], 0
    for c in changes:
        before, after = (c.get("before") or "").strip(), (c.get("after") or "").strip()
        if not before or not after:
            problems.append(f"{lid[7:15]} 有一处改动缺原句或新句")
            continue
        if published(text, before, after):
            n += 1
            continue
        if text.count(before) == 1:
            text = text.replace(before, after)
            n += 1
            continue
        m = list(loose(before).finditer(text))
        if len(m) == 1:
            text = text[:m[0].start()] + after + text[m[0].end():]
            n += 1
        else:
            problems.append(f"{lid[7:15]}〔{c.get('where')}〕原句在正文里对上 {len(m)} 处：{before[:50]}…")
    return text, n, problems


def render_one(d, lesson_path=None, with_source=False, kinds=None):
    """-> (文字, 套上的改句数, 问题列表)。没有 lesson_path 时只出知识段。"""
    b = block(d, with_source, kinds)
    if not lesson_path:
        return b, 0, []
    lid = d.get("id") or os.path.basename(lesson_path).split(".")[0]
    text, n, problems = apply_changes(body(lesson_path), d.get("changes") or [], lid)
    text = text.rstrip()
    return (text + "\n\n" + b if b else text), n, problems


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--memory")
    ap.add_argument("--out")
    ap.add_argument("--with-source", action="store_true")
    ap.add_argument("--kinds")
    a = ap.parse_args(argv)
    kinds = set(x for x in a.kinds.split(",") if x) if a.kinds else None
    files = sorted(glob.glob(os.path.join(a.path, "lesson-*.json"))) if os.path.isdir(a.path) else [a.path]
    lib = {}
    if a.memory:
        for p in glob.glob(os.path.join(a.memory, "**", "lesson-*.lesson.md"), recursive=True):
            lib[os.path.basename(p).split(".")[0]] = p
    if a.out:
        os.makedirs(a.out, exist_ok=True)
    all_problems, n_all = [], 0
    for f in files:
        d = json.load(io.open(f, encoding="utf-8"))
        lid = d.get("id") or d.get("lesson") or os.path.basename(f)[:-5]
        lp = lib.get(lid) if a.memory else None
        if a.memory and not lp:
            all_problems.append(f"{lid[7:15]} 在 memory 里没有")
            continue
        text, n, problems = render_one(d, lp, a.with_source, kinds)
        n_all += n
        all_problems += problems
        if a.out:
            io.open(os.path.join(a.out, lid + ".md"), "w", encoding="utf-8", newline="\n").write(text + "\n")
        else:
            print("=====", lid)
            print(text)
    if a.memory:
        print(f"套上改句 {n_all} 处", file=sys.stderr)
    for x in all_problems:
        print("问题：" + x, file=sys.stderr)
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
