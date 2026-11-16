# -*- coding: utf-8 -*-
"""检查脚本和渲染脚本的自测。只写 work/selftest/basic/。
  1. references/examples/ 下的两个样例过 check_rules.py，应当 0 处违反；
  2. 拿代码类样例故意改坏，每种一个目录 work/selftest/basic/<名字>/，分别跑检查，看是否查出、是否只报预期那一类：
     本机路径（how 里加一个盘符路径）、缺 keys、probe 正则不合法、support 不存在（recommendation:99）、引文改一个字；
     另拿规格类样例把 wrong 栏清空（规格类的触发要写 wrong）；
     再做几个变体：触发只写固定记号和反引号字面量（应当通过）、取值 9 项（只出提示 P4）、触发里有占位写法（只出提示 P5）、
     conflicts 栏（接受并计数；不是列表应当查出）、left_out 的「针对经验库本身的建议」（应当通过）、文档本地副本的引文
     （副本在时测：原文应当通过，改一个字应当查出）；
  3. 合并后的规矩（store/rules/ 的样子）：代码类样例补上 id、sources、general、status 应当通过，去掉 sources 应当查出；
  4. 两个样例用 render.py 渲染，过可移植检查（check_rules 的 nonportable_hits，另加用户目录名），写 work/selftest/basic/rendered.txt；
     并核对 references/format.md 里两个例子的 JSON、呈现和索引行与样例文件、渲染结果一致；refs 的 where 写本机绝对路径应当被拒。
用法（在分支根目录下）： py -3 -X utf8 skills/memory-rules/scripts/selftest.py"""
import sys

sys.dont_write_bytecode = True
import copy, importlib.util, io, json, os, re, shutil, subprocess  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EX = os.path.join(HERE, "..", "references", "examples")
OUT = os.path.join(ROOT, "work", "selftest", "basic")
CODE, SPEC = "case-4f627840679361f165a3", "case-caa0a4c6289286b0e6ba"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_selftest", os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(d, *args):
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "check_rules.py"), "--dir", d, *args],
                       capture_output=True, text=True, encoding="utf-8")
    lines = r.stdout.strip().splitlines()
    if r.returncode not in (0, 1) or not lines:
        raise SystemExit(f"check_rules.py 出错：{r.stdout[-400:]} {r.stderr[-800:]}")
    return r.returncode, [x.strip()[2:] for x in lines if x.strip().startswith("- ")], lines[-1]


def ex(case):
    return json.load(io.open(os.path.join(EX, case + ".json"), encoding="utf-8"))


def broken(name, case, fn, expect):
    o = copy.deepcopy(ex(case))
    fn(o["rules"][0])
    d = os.path.join(OUT, name)
    os.makedirs(d)
    json.dump(o, io.open(os.path.join(d, case + ".json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    code, viol, last = run(d)
    hit = [v for v in viol if expect in v]
    return {"name": name, "exit": code, "caught": bool(hit), "only_expected": len(hit) == len(viol), "violations": viol}


def b_path(r):
    r["how"][0]["text"] += "（见 C:\\Users\\someone\\AppData\\Local\\Android\\Sdk\\sources\\android-36.1\\android\\widget\\TextView.java）"


def b_keys(r):
    del r["keys"]


def b_probe(r):
    r["probe"]["pattern"] = "\\.shadow\\(\\s*\\{["


def b_support(r):
    r["how"][0]["support"] = [CODE + "#recommendation:99"]


def b_quote(r):
    r["refs"][0]["quote"] = r["refs"][0]["quote"].replace("ShadowOptions |", "ShadowOption |", 1)


def b_abs_where(r):
    r["refs"][0]["where"] = "C:/Program Files/Huawei/DevEco Studio/sdk/default/" + r["refs"][0]["where"]


def b_spec_wrong(r):
    r["triggers"][0]["wrong"] = ""


def variant(name, case, fn, want_exit, expect=None, in_last=None):
    """整个文件改一处，看退出码、违反或提示里有没有 expect、最后一行里有没有 in_last。"""
    o = copy.deepcopy(ex(case))
    fn(o)
    d = os.path.join(OUT, name)
    os.makedirs(d)
    json.dump(o, io.open(os.path.join(d, case + ".json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "check_rules.py"), "--dir", d], capture_output=True, text=True, encoding="utf-8")
    out = r.stdout
    ok = r.returncode == want_exit and (expect is None or expect in out) and (in_last is None or in_last in out.strip().splitlines()[-1])
    return {"name": name, "exit": r.returncode, "ok": ok, "last": out.strip().splitlines()[-1] if out.strip() else r.stderr[-200:]}


sys.path.insert(0, HERE)
import sources as S  # noqa: E402
DOCS_REL = "zh-cn/application-dev/Readme-CN.md"
DOCS = os.path.join(S.roots()["oh-docs"] or os.path.join(ROOT, "work", "ohdocs"), *DOCS_REL.split("/"))


def v_marker(o):
    o["rules"][0]["triggers"] = [{"read": "代码注释里有 `FWD-REF` 登记的占位", "wrong": "注释里写了 FWD-REF，登记表里却没有这一行"}]


def v_values9(o):
    o["rules"][0]["values"] += o["rules"][0]["values"][:2]


def v_placeholder(o):
    o["rules"][0]["triggers"][0]["wrong"] = "对应的 Text 上写的是 <Class>.<method>(...)"


def v_conflicts(o):
    o["conflicts"] = ["测试：卡里的做法和声明的说法冲突"]


def v_conflicts_bad(o):
    o["conflicts"] = "不是列表"


def v_library_reason(o):
    o["left_out"].append({"text": "测试：修订某条经验", "reason": "针对经验库本身的建议"})


def v_docs_ref(o, bad=False):
    o["rules"][0]["refs"].append({"what": "测试：文档本地副本的引文", "kind": "oh-docs", "where": DOCS_REL + " 应用开发导读",
                                  "quote": "[应用开发导读](application-dev-guide.md)" if not bad else "[应用开发指南](application-dev-guide.md)",
                                  "version": "docs f41b9345"})


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if os.path.exists(OUT):
        shutil.rmtree(OUT)                 # 只删 work/ 下本脚本自己写的目录
    os.makedirs(OUT)
    code, viol, last = run(os.path.abspath(EX))
    res = {"examples": {"exit": code, "violations": viol, "last": last}, "broken": [
        broken("local-path", CODE, b_path, "出现本机路径或行号"),
        broken("no-keys", CODE, b_keys, "keys 必须是"),
        broken("bad-probe", CODE, b_probe, "probe 的正则不能编译"),
        broken("no-such-support", CODE, b_support, "这张卡没有这条结论"),
        broken("quote-changed", CODE, b_quote, "quote 没有逐字出现"),
        broken("spec-no-wrong", SPEC, b_spec_wrong, "wrong 栏要写"),
        broken("abs-where", CODE, b_abs_where, "要写来源里的相对路径"),
    ]}
    res["variants"] = [
        variant("marker-trigger", CODE, v_marker, 0),                                  # 固定记号、反引号字面量算标识符
        variant("values-9", CODE, v_values9, 0, "P4"),                                  # 取值超过 8 项：只出提示
        variant("placeholder", CODE, v_placeholder, 0, "P5"),                           # 占位写法：只出提示
        variant("conflicts", CODE, v_conflicts, 0, None, "conflicts 1"),                # conflicts 栏接受并计数
        variant("conflicts-not-list", CODE, v_conflicts_bad, 1, "conflicts 必须是列表"),
        variant("left-out-library", CODE, v_library_reason, 0),                         # 新的 left_out 原因
    ]
    if os.path.isfile(DOCS):                                                            # 文档本地副本在才测
        res["variants"] += [variant("docs-ref", CODE, v_docs_ref, 0),
                            variant("docs-ref-changed", CODE, lambda o: v_docs_ref(o, True), 1, "quote 没有逐字出现在 Readme-CN.md 里")]
    for v in res["variants"]:
        print(f"变体 {v['name']}：{'通过' if v['ok'] else '没通过'}（exit {v['exit']}）")
    # 合并后的规矩（store/rules/ 的样子）：代码类样例补上 id、sources、general、status，应当 0 处违反；去掉 sources 应当查出
    d = os.path.join(OUT, "merged")
    os.makedirs(d)
    m = dict(ex(CODE)["rules"][0], id="rule-0123456789ab", sources=[CODE], general=False, status="active")
    json.dump(m, io.open(os.path.join(d, "rule-0123456789ab.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    mc, mv, ml = run(d)
    d2 = os.path.join(OUT, "merged-no-sources")
    os.makedirs(d2)
    json.dump(dict(m, sources=[]), io.open(os.path.join(d2, "rule-0123456789ab.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    nc, nv, nl = run(d2)
    res["merged"] = {"exit": mc, "violations": mv, "no_sources_violations": nv}
    print("合并后的规矩：exit", mc, mv, "| 去掉 sources：", nv)
    R, C = load("render"), load("check_rules")
    api = R.api_version()
    texts = []
    for case in (CODE, SPEC):
        texts.append(R.render_file(os.path.join(EX, case + ".json"), api))
        texts.append(R.render_file(os.path.join(EX, case + ".json"), api, index=True))
    text = "\n\n".join(texts)
    user = os.path.basename(os.path.expanduser("~"))
    hits = C.nonportable_hits(text) + ([("用户目录名", user)] if user and re.search(re.escape(user), text, re.I) else [])
    io.open(os.path.join(OUT, "rendered.txt"), "w", encoding="utf-8", newline="\n").write(text + "\n")
    fmt = io.open(os.path.join(EX, "..", "format.md"), encoding="utf-8").read()
    in_fmt = {case: json.dumps(ex(case), ensure_ascii=False, indent=2) in fmt
              and R.render_file(os.path.join(EX, case + ".json"), api) in fmt
              and R.render_file(os.path.join(EX, case + ".json"), api, index=True) in fmt for case in (CODE, SPEC)}
    res["render"] = {"api": api, "portable_hits": hits, "format_md_in_sync": in_fmt}
    print("format.md 里的两个例子和样例文件、渲染结果一致：", in_fmt)
    json.dump(res, io.open(os.path.join(OUT, "selftest.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print("两个样例：exit", code, "|", last)
    for b in res["broken"]:
        print(f"改坏 {b['name']}：查出 {b['caught']}，只报预期那一类 {b['only_expected']}，exit {b['exit']}；{b['violations']}")
    print("渲染：API", api, "，可移植检查命中", len(hits))
    ok = code == 0 and all(b["caught"] and b["only_expected"] for b in res["broken"]) and all(v["ok"] for v in res["variants"]) and not hits and mc == 0 and \
        any("sources 至少列一张卡" in v for v in nv) and all(in_fmt.values())
    print("自测", "通过" if ok else "没通过")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
