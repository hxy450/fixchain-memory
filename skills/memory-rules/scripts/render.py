# -*- coding: utf-8 -*-
"""规矩 JSON → 呈现给 agent 的样子（docs/rules-v2-design.md 第 4 节），以及第三层索引里的那一行。

one(rule, n_cards, n_apps, api)  一条规矩的正文（第四层 <规矩号>.md 的内容），格式固定，没有内容的段整段不出：
    # <title>
    （空行）
    审的是：<product>
    触发（任一种）：
    - 读到：<read>；写错的样子：<wrong>          （空的那一栏不写）
    适用范围：<scope>
    不适用的情形：<exceptions 的 text，用分号连>
    做法：
    - <how 的 text>
    已核实的写法和取值（核实时用的是鸿蒙 SDK API <N>）：
    - <value>：<meaning>（出处：<source>）
    针对本应用要查的：
    - <what>：<where>；<how>
    未核实：<unverified，用分号连>
    来源：<N> 张卡，<M> 个应用
  refs、keys、probe、siblings_checked、alternatives_unverified 不呈现。
index_line(rule, rid)  第三层索引的一行：- <规矩号>｜<title>｜读到：<第一个触发的 read>；写错：<第一个触发的 wrong>
  （read 或 wrong 为空时那一半不写）。
来源的张数和应用数：合并后的规矩按 sources 数，应用名取 work/cards_index.json；候选规矩只出自一张卡（文件的 case）。
API 版本：--api 给了就用它；没给就读本机 DevEco 的 sdk/default/sdk-pkg.json 的 apiVersion，读不到用 23。

用法： py -3 -X utf8 skills/memory-rules/scripts/render.py <规矩文件.json> [--index] [--api N]
  候选文件（case-*.json）里的每条规矩依次输出，规矩号写成「<卡号>#<序号>」；合并后的规矩文件（rule-*.json）输出一条。
只读。"""
import sys

sys.dont_write_bytecode = True
import io, json, os, re  # noqa: E401,E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
INDEX = os.path.join(ROOT, "work", "cards_index.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources as S  # noqa: E402


def _s(x):
    return x.strip() if isinstance(x, str) else ""


def api_version(default="23"):
    """本机鸿蒙 SDK（work/sources.local.json 的 harmony-sdk，没配按惯例找）的 sdk-pkg.json 里的 apiVersion，读不到用 default。"""
    try:
        return str(json.load(io.open(os.path.join(S.roots()["harmony-sdk"] or "", "sdk-pkg.json"), encoding="utf-8"))["data"]["apiVersion"])
    except (OSError, ValueError, KeyError, TypeError):
        return default


CLAIM_LABEL = re.compile(r"^(case-[0-9A-Za-z]+)#(diagnosis|recommendation:(\d+))$")


def claim_label(claim):
    m = CLAIM_LABEL.match(claim or "")
    if not m:
        return None, None
    return m.group(1), ("诊断" if m.group(2) == "diagnosis" else f"建议 {m.group(3)}")


def provenance(r, sources):
    """来源一节的逐张列表：每张卡一行「- 卡号（应用）：做法第 1 步 ← 建议 2、诊断；例外 1 ← 建议 3；取值 2 ← 建议 1」。
    出自 support（做法、例外、取值里各项引的卡的结论）；只列为来源、正文各项没有直接引它的，注明。"""
    uses = {}
    parts = [(f"做法第 {i} 步", x) for i, x in enumerate(r.get("how") or [], 1)] + \
        [(f"例外 {i}", x) for i, x in enumerate(r.get("exceptions") or [], 1)] + \
        [(f"取值 {i}", x) for i, x in enumerate(r.get("values") or [], 1)]
    for where, x in parts:
        if not isinstance(x, dict):
            continue
        per = {}
        for s in x.get("support") or []:
            c, lab = claim_label(s)
            if c and lab not in per.setdefault(c, []):
                per[c].append(lab)
        for c, labs in per.items():
            uses.setdefault(c, []).append(f"{where} ← {'、'.join(labs)}")
    out = []
    for c in list(sources) + [c for c in uses if c not in sources]:
        app = app_of(c) or "未记录应用"
        out.append(f"- {c}（{app}）：" + ("；".join(uses[c]) if c in uses else "列为来源，正文各项没有直接引它"))
    return out


_app_of = None


def app_of(case):
    global _app_of
    if _app_of is None:
        _app_of = {}
        if os.path.isfile(INDEX):
            _app_of = {x["case"]: x.get("app") or "" for x in json.load(io.open(INDEX, encoding="utf-8"))["index"]}
    return _app_of.get(case, "")


def counts(sources):
    apps = {app_of(c) or f"（未记录：{c}）" for c in sources}
    return len(sources), len(apps)


def one(r, n_cards=1, n_apps=1, api="23", sources=None):
    """sources 给了（卡号列表）时，来源那一行下面逐张列出卡号、应用和各项出自哪条结论（见 provenance）。"""
    out = [f"# {_s(r.get('title'))}", ""]
    if _s(r.get("product")):
        out.append(f"审的是：{_s(r['product'])}")
    trig = []
    for t in r.get("triggers") or []:
        parts = []
        if _s(t.get("read")):
            parts.append(f"读到：{_s(t['read'])}")
        if _s(t.get("wrong")):
            parts.append(f"写错的样子：{_s(t['wrong'])}")
        if parts:
            trig.append("- " + "；".join(parts))
    if trig:
        out += ["触发（任一种）："] + trig
    if _s(r.get("scope")):
        out.append(f"适用范围：{_s(r['scope'])}")
    exc = [_s(x.get("text")) for x in r.get("exceptions") or [] if _s(x.get("text"))]
    if exc:
        out.append("不适用的情形：" + "；".join(exc))
    how = [_s(x.get("text")) for x in r.get("how") or [] if _s(x.get("text"))]
    if how:
        out += ["做法："] + [f"- {x}" for x in how]
    vals = [f"- {_s(v['value'])}" + (f"：{_s(v.get('meaning'))}" if _s(v.get("meaning")) else "")
            + (f"（出处：{_s(v.get('source'))}）" if _s(v.get("source")) else "")
            for v in r.get("values") or [] if _s(v.get("value"))]
    if vals:
        out += [f"已核实的写法和取值（核实时用的是鸿蒙 SDK API {api}）："] + vals
    lk = [f"- {_s(x['what'])}" + (f"：{_s(x.get('where'))}" if _s(x.get("where")) else "") + (f"；{_s(x.get('how'))}" if _s(x.get("how")) else "")
          for x in r.get("lookups") or [] if _s(x.get("what"))]
    if lk:
        out += ["针对本应用要查的："] + lk
    unv = [_s(x) for x in r.get("unverified") or [] if _s(x)]
    if unv:
        out.append("未核实：" + "；".join(unv))
    if n_cards:
        out.append(f"来源：{n_cards} 张卡，{n_apps} 个应用")
        if sources:
            out += provenance(r, sources)
    return "\n".join(out)


def index_line(r, rid):
    t = (r.get("triggers") or [{}])[0] or {}
    parts = []
    if _s(t.get("read")):
        parts.append(f"读到：{_s(t['read'])}")
    if _s(t.get("wrong")):
        parts.append(f"写错：{_s(t['wrong'])}")
    return f"- {rid}｜{_s(r.get('title'))}｜" + "；".join(parts)


def render_file(path, api, index=False):
    o = json.load(io.open(path, encoding="utf-8"))
    name = os.path.basename(path)[:-5]
    if name.startswith("case-"):
        items = [(f"{name}#{i}", r, [name]) for i, r in enumerate(o.get("rules") or [], 1)]
    else:
        items = [(o.get("id") or name, o, o.get("sources") or [])]
    out = []
    for rid, r, src in items:
        n, m = counts(src)
        out.append(index_line(r, rid) if index else one(r, n, m, api))
    return ("\n" if index else "\n\n").join(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    api = a[a.index("--api") + 1] if "--api" in a else api_version()
    files = [x for x in a if x.endswith(".json")]
    for f in files:
        print(render_file(f, api, index="--index" in a))


if __name__ == "__main__":
    main()
