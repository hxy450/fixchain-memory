# -*- coding: utf-8 -*-
"""把一条经验（memory/ 里的正文）和它的知识文件（knowledge/lessons/<id>.json）渲染成交给模型的那一段文字。

写法和影子提示词里的经验块一致：
  - 正文：memory/<主题>/<id>.lesson.md 去掉 ID 行和「[本主题](index.md)」一行，截到「## 来源」（或「## 同源经验」）之前；
    「来源支持：…」一行留在正文末尾。
  - 知识文件有条目时，空一行接一段「已核实的平台事实（核实时用的是 …；安卓 …。…）：」，每条一行「- 〔step〕fact」，
    条目有非空 scope 的在后面加「〔成立范围：scope〕」。不带出处（source）、不带写法（code）、不带 device_todo。
  - 知识文件里的 changes（对正文某句的改动）：本分支已经经 store 提案把它们发布进正文，这时只核对（改后的句子在，原句在
    改后的句子之外不再出现）。某处改动还没发布进正文（新句不在、原句恰好对上一处，按原样或忽略空白）时，照提示词生成器的
    做法当场套上，并在汇总里报出套了几处。两样都不是就报错。
  - 经验在 memory/ 里没有：store 里已退役的只列出、不渲染；别的报错。

用法（在仓库根目录）：
  python knowledge/render.py                 渲染全部，写到 knowledge/rendered/<主题>/<id>.md（每次重写，多余的旧文件删掉）
  python knowledge/render.py lesson-<id>     把一条打印到标准输出（id 可写前 8 位以上）
  python knowledge/render.py --check         只核对，不写文件
有问题时退出码 1。只用标准库，路径都相对仓库根。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / "memory"
KN = ROOT / "knowledge" / "lessons"
OUT = ROOT / "knowledge" / "rendered"
STORE = ROOT / "store"

KN_HEAD = "已核实的平台事实（核实时用的是 {h}；安卓 {a}。{tail}）："
KN_TAIL = "和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看"
SRC_RX = re.compile(r"\n## (?:来源|同源经验)")


def lib_paths():
    out = {}
    for p in MEM.rglob("lesson-*.lesson.md"):
        lid = p.name[:-len(".lesson.md")]
        if lid in out:
            raise SystemExit(f"{lid} 在 memory/ 里出现两次")
        out[lid] = p
    return out


def store_status():
    """store 快照里每条经验的状态（只用来说明 memory/ 里为什么没有某条）。"""
    try:
        head = json.loads((STORE / "HEAD.json").read_text(encoding="utf-8"))["revision"]
        snap = json.loads((STORE / "snapshots" / f"{head}.json").read_text(encoding="utf-8"))
        return {k: v.get("status") for k, v in snap["lessons"].items()}
    except (OSError, KeyError, ValueError):
        return {}


def body(path):
    """经验正文：不含来源列表、ID 行和主题回链。"""
    t = SRC_RX.split(Path(path).read_text(encoding="utf-8"), maxsplit=1)[0]
    t = re.sub(r"(?m)^\[本主题\]\(index\.md\)\n\n?", "", t)
    t = re.sub(r"(?m)^ID：`lesson-[0-9a-f]+`.*\n\n?", "", t)
    return t.strip() + "\n"


def loose(s):
    """原句按「空白可有可无」去对。"""
    parts = [re.escape(x) for x in re.split(r"\s+", s.strip()) if x]
    return re.compile(r"\s*".join(parts))


def found(text, s):
    n = text.count(s)
    return n if n else len(list(loose(s).finditer(text)))


def effective_afters(changes):
    """每处改动最后留在正文里的样子：后一处改动的原句落在前一处的新句里时，前一处的新句按后一处改过。"""
    pairs = [((c.get("before") or "").strip(), (c.get("after") or "").strip()) for c in changes]
    out = []
    for k, (_, a) in enumerate(pairs):
        for b2, a2 in pairs[k + 1:]:
            if b2 and b2 in a:
                a = a.replace(b2, a2, 1)
        out.append(a)
    return pairs, out


def apply_or_check(text, changes, lid):
    """-> (正文, 问题列表, 当场套上的处数)。已发布的改动只核对；未发布的（新句不在、原句恰好一处）当场套上。"""
    problems, n_now = [], 0
    pairs, eff = effective_afters(changes)
    for k, ((b, a), e) in enumerate(zip(pairs, eff), 1):
        if not b or not a:
            problems.append(f"{lid[7:15]} 第 {k} 处改动缺原句或新句")
            continue
        if found(text, e):
            masked = text
            for x in sorted((y for y in eff if y), key=len, reverse=True):
                masked = loose(x).sub("\u0000", masked)
            if found(masked, b):
                problems.append(f"{lid[7:15]} 第 {k} 处改动的新句已在正文里，原句却也还在：{b[:40]}…")
            continue
        if text.count(b) == 1:
            text = text.replace(b, a)
            n_now += 1
            continue
        m = list(loose(b).finditer(text))
        if len(m) == 1:
            text = text[:m[0].start()] + a + text[m[0].end():]
            n_now += 1
        else:
            problems.append(f"{lid[7:15]} 第 {k} 处改动：新句不在正文里，原句对上 {len(m)} 处：{b[:40]}…")
    return text, problems, n_now


def knowledge(d):
    ent = d.get("entries") or []
    if not ent:
        return ""
    sdk = d.get("sdk") or {}
    lines = [KN_HEAD.format(h=sdk.get("harmony", "鸿蒙 SDK"), a=sdk.get("android", "平台资源和源码"), tail=KN_TAIL)]
    for e in ent:
        line = f"- 〔{(e.get('step') or '').strip()}〕{(e.get('fact') or '').strip()}"
        scope = (e.get("scope") or "").strip()
        if scope:
            line += f"〔成立范围：{scope}〕"
        lines.append(line)
    att = d.get("attachment")
    if att:
        lines += ["", "附：" + att.get("title", ""), "```js"] + (att.get("text") or "").rstrip("\n").split("\n") + ["```"]
    return "\n".join(lines)


def render(lid, path, d, counter=None):
    """-> (交给模型的那一段文字，不带末尾换行；问题列表)。d 是知识文件内容，没有知识文件时为 None。"""
    inner = "\n" + body(path).strip() + "\n"
    problems = []
    if d:
        inner, problems, n_now = apply_or_check(inner, d.get("changes") or [], lid)
        if counter is not None and n_now:
            counter[lid] = n_now
    text = inner.strip()
    kb = knowledge(d) if d else ""
    return (text + "\n\n" + kb if kb else text), problems


def resolve(raw, LP):
    raw = raw.strip()
    if raw in LP:
        return raw
    k = raw.replace("lesson-", "")
    hits = [x for x in LP if x[7:].startswith(k)] if len(k) >= 8 else []
    if len(hits) != 1:
        raise SystemExit(f"{raw}：memory/ 里对上 {len(hits)} 条经验")
    return hits[0]


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    LP = lib_paths()
    args = [a for a in argv if not a.startswith("--")]
    if args:
        lid = resolve(args[0], LP)
        f = KN / f"{lid}.json"
        d = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else None
        text, problems = render(lid, LP[lid], d)
        print(text)
        for x in problems:
            print("问题：" + x, file=sys.stderr)
        return 1 if problems else 0
    only_check = "--check" in argv
    status = store_status()
    problems, skipped, written, applied_now = [], [], set(), {}
    for f in sorted(KN.glob("lesson-*.json")):
        lid = f.stem
        d = json.loads(f.read_text(encoding="utf-8"))
        if lid not in LP:
            if status.get(lid) == "retired":
                skipped.append(lid)
            else:
                problems.append(f"{lid[7:15]} 在 memory/ 里没有（store 里的状态：{status.get(lid)}）")
            continue
        text, pr = render(lid, LP[lid], d, applied_now)
        problems += pr
        if not only_check:
            out = OUT / LP[lid].parent.relative_to(MEM) / f"{lid}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text + "\n", encoding="utf-8", newline="\n")
            written.add(out.resolve())
    if not only_check and OUT.is_dir():
        for p in sorted(OUT.rglob("*.md")):
            if p.resolve() not in written:
                p.unlink()
        for p in sorted((x for x in OUT.rglob("*") if x.is_dir()), key=lambda x: len(x.parts), reverse=True):
            if not any(p.iterdir()):
                p.rmdir()
    print(f"{'核对' if only_check else '渲染'} {len(written) if not only_check else len(list(KN.glob('lesson-*.json'))) - len(skipped)} 条；"
          f"store 里已退役、不渲染 {len(skipped)} 条" + (f"：{'、'.join(x[7:15] for x in skipped)}" if skipped else "")
          + f"；正文里还没有、当场套上的改句 {sum(applied_now.values())} 处"
          + (f"（{'、'.join(f'{k[7:15]} {v}' for k, v in applied_now.items())}）" if applied_now else ""))
    if problems:
        print("问题：")
        for x in problems:
            print("  " + x)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
