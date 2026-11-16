# -*- coding: utf-8 -*-
"""检查规矩文件是否满足 docs/rules-v2-design.md 第 4、7 节和 references/format.md 的硬规则。
只读 store/（HEAD 那一版的快照，用来核对 support 引的卡和结论）、work/cards_index.json（出事应用的名单）、work/sources.local.json
（知识库来源在本机的根目录）和 refs 解析出的来源文件。

用法（在分支根目录下）：
  py -3 skills/memory-rules/scripts/check_rules.py [卡号前 8 位 …]            查 store/candidates/ 下的候选规矩（不带参数查全部）
  py -3 skills/memory-rules/scripts/check_rules.py --rules [规矩号前缀 …]     查 store/rules/ 下合并后的规矩
  py -3 skills/memory-rules/scripts/check_rules.py --dir <目录> [前缀 …]      查另一个目录里的 case-*.json / rule-*.json
  加 --format-only：只查格式，不核对 support 引的卡和结论在不在库里、不核对 refs 的来源文件和引文（用于试跑的语料）
  --roots：打印各来源在本机的根目录（子代理打开来源文件时用根目录接上 where 里的相对路径）
文件名决定类型：case-<卡号>.json 是一张卡的候选规矩，rule-<12 位十六进制>.json 是一条合并后的规矩。

硬规则（每处违反计 1）：
  文件  UTF-8 不带 BOM 的合法 JSON。
    候选：case 与文件名一致；rules 是 0–8 条的列表；left_out / corrections / gaps 是列表，conflicts 可以没有、有就是列表；
          rules 为空时 left_out 不能为空；left_out 每项有 text 和 reason（reason 是「没有产物里看得到的触发」「要上机或截图才能做」
          「只对出事应用成立」「针对经验库本身的建议」之一，或「其他：…」）；corrections 每项有 was / now / ref；gaps、conflicts
          每项是非空字符串；规矩里不能有 id、general、status、sources（这几栏由后面的脚本补）。
    合并后：id 与文件名一致且是 rule-<12 位十六进制>；sources 非空且都是库里的卡；general 是 true / false；
          status 是 active 或 disputed。
  必填栏  title、scope、why、siblings_checked 是非空字符串；title 不超过 60 字；product 是「规格」「计划与派工」「代码」「资源」之一；
          triggers 至少一个；how 1–3 步，每步有 text 和非空 support；exceptions 每项有 text 和非空 support；values 每项有
          value、meaning、source，support 是列表；lookups 每项有 what、where、how；unverified、alternatives_unverified 是字符串列表；
          refs 每项 kind 合法、what / where / quote / version 非空、quote 不超过 200 字。
  长度  正文（title、triggers、scope、exceptions、why、how 合计，不算换行）不超过 800 字；general 为 true 的不超过 600 字。
  support  写成「卡号#结论」；卡在库里（store/HEAD.json 指的快照），结论是这张卡确有的 diagnosis 或 recommendation:N，且没有撤回；
          候选文件里只能引这张卡自己；合并后的规矩里引到的卡要列在 sources 里；values 里 support 为空（来自知识库）的，refs 不能为空。
  refs  where 写来源里的相对路径加符号名（不许本机绝对路径；鸿蒙 SDK、Android SDK 写相对根目录的路径，依赖库写
          「group:artifact:version 包内路径」，文档写文档库里的相对路径，见 knowledge-sources.md 和 sources.py）；按
          work/sources.local.json 配的根目录（没配的按惯例找）解析成本机文件，quote 去掉空白后逐字出现在文件里（文件也去掉空白）；
          oh-docs 写的是 http(s) 地址的不核对原文（旧写法，仍接受）。本机没有这个来源的根目录、或 Gradle 缓存里没有这个库的，
          不算违反，记作「没能核对」单列；根目录在、文件找不到的算违反。where、what、version 里不能有盘符路径、用户目录、
          AppData、Program Files、.gradle、%LOCALAPPDATA%、%USERPROFILE%。
  可移植  呈现和召回用的各栏（规矩里除 refs、probe 以外的所有栏，含 keys）不能有：盘符路径、Users\\ 或 Users/、AppData、
          Program Files、.gradle、%LOCALAPPDATA%、%USERPROFILE%，以及「文件名:行号」（带扩展名的文件名后接 : ： # 或括号再接可带 L 的
          数字）；也不能出现「本例」「本应用」「该应用」「此应用」「.jsonl」「转录」。
  触发  每个触发有 read、wrong 两栏（字符串，没有写空字符串），至少一栏非空。
          代码、资源类：非空的每一栏里至少有一个代码标识符（认定见 is_code_ident 和 code_idents：另算流水线里的固定记号，
          即大写字母、数字、连字符、下划线组成的记号，以及反引号括起来的字面量）。
          规格、计划与派工类：wrong 栏非空（写文档里看得到的说法或缺的那一项），不强求代码标识符。
  keys  是 {"read": [...], "product": [...]}，每栏 3–12 个非空字符串。
  probe  null，或 {"pattern": 非空字符串, "note": 非空字符串}，pattern 用 Python re 能编译。
  应用名  上面「可移植」那些栏和 probe 里不能出现出事应用的名字：名单取 work/cards_index.json 的应用清单，每个名字连同去掉
          常见前后缀（app_、-hmos、-ohos、_android、_live_android、-vestN、com.xxx. 前缀）的变体，比的时候都去掉空白、
          连字符、下划线并转小写；比较形不到 4 个字符的、纯数字的、和平台词重名的（GENERIC_APP_NAMES）不比。
提示（不算硬规则，汇总里单列）：
  P1  values 的 source 里既没有文件名也没有类名或符号名、又不是「卡里修好并验证过」的条目数；
  P2  support 为空的取值，在 refs 里找不到对应出处的条目数（对应的认定见 value_has_ref）；
  P3  probe 的正则能匹配空字符串（搜什么都会命中）；
  P4  一条规矩的取值超过 8 项；
  P5  触发里有占位写法（<…>.<…>、Xxx、stopXxx 这类），多半是为了过检查编出来的标识符。
汇总：每张卡（每个文件）一行：规矩数、left_out、corrections、gaps、conflicts、违反数、提示数；最后一行是合计。"""
import sys

sys.dont_write_bytecode = True
import glob, io, json, os, re  # noqa: E401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources as S  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
STORE = os.path.join(ROOT, "store")
INDEX = os.path.join(ROOT, "work", "cards_index.json")
PRODUCTS = ("规格", "计划与派工", "代码", "资源")
CODE_PRODUCTS = ("代码", "资源")
KINDS = {"harmony-dts", "android-sdk", "android-lib", "oh-docs"}
REASONS = ("没有产物里看得到的触发", "要上机或截图才能做", "只对出事应用成立", "针对经验库本身的建议")
MAX_VALUES = 8
CANDIDATE_ONLY_ABSENT = ("id", "general", "status", "sources")
MAX_RULES = 8
BAN = re.compile(r"本例|本应用|该应用|此应用|\.jsonl|转录")
CLAIM = re.compile(r"^(case-[0-9A-Za-z]+)#(diagnosis|recommendation:\d+)$")
RULE_ID = re.compile(r"^rule-[0-9a-f]{12}$")
FILE_EXT = r"(?:java|kt|kts|xml|ets|ts|js|mjs|json5?|jsonl|md|gradle|properties|py|txt|cpp|cc|c|h|hpp|yaml|yml|toml|html|css|aidl|smali)"
NONPORTABLE = [
    ("盘符路径", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")),
    ("Users\\", re.compile(r"(?i)Users[\\/]")),
    ("AppData", re.compile(r"(?i)AppData")),
    ("Program Files", re.compile(r"(?i)Program Files")),
    (".gradle", re.compile(r"(?i)\.gradle(?![A-Za-z0-9])")),
    ("%LOCALAPPDATA%", re.compile(r"(?i)%LOCALAPPDATA%")),
    ("%USERPROFILE%", re.compile(r"(?i)%USERPROFILE%")),
    ("文件名:行号", re.compile(r"[\w\-.]+\." + FILE_EXT + r"(?![A-Za-z0-9])\s*[:：#(（]\s*L?\d+")),
]
FILE_NAME = re.compile(r"[\w\-.]+\." + FILE_EXT + r"(?![A-Za-z0-9])")
PRODUCT_WORDS = {"Android", "ArkUI", "ArkTS", "HarmonyOS", "OpenHarmony", "Harmony", "Java", "Kotlin", "Compose", "Material",
                 "Gradle", "DevEco", "Jetpack", "Google", "Huawei"}
GENERIC_APP_NAMES = {"nfc"}       # 应用名同时是平台词的，不当作出事应用的名字来比
TOKEN = re.compile(r"[A-Za-z_$@?][A-Za-z0-9_$]*(?:[.:/#][A-Za-z_$][A-Za-z0-9_$]*)*")
FROM_CARD = "卡里修好并验证过"
FORMAT_ONLY = False     # --format-only：不核对 support 引的卡和结论是否在库里、不核对 refs 的本机文件和引文（只查格式）


def norm(s):
    return re.sub(r"\s+", "", s or "")


def is_code_ident(tok, before, after):
    """代码标识符的认定（ASCII 记号，按 [A-Za-z_$@?][A-Za-z0-9_$]* 并允许用 . : / # 连成限定名切出来），满足任一条就算：
    a. 限定名：含 . : / # 连接的两段以上（Text.textShadow、android:shadowColor、@dimen/x、TextView#setShadowLayer）；
    b. 含下划线（wrap_content、FLAG_FULLSCREEN）；
    c. 驼峰：小写字母后紧跟大写字母（setShadowLayer、textShadow）；
    d. 大写开头、含小写、至少 3 个字母（TextView、Text、Canvas）；
    e. 紧跟着左括号（shadow(、padding(），或紧跟在 < . @ ? 后面（<TextView、.shadow、@color、?attr）。
    产品或平台的名字本身（PRODUCT_WORDS）、全大写又不带下划线和点的缩写（XML、SDK、DP）、纯小写的普通单词都不算。"""
    core = tok.lstrip("@?$")
    if core in PRODUCT_WORDS:
        return False
    if re.search(r"[A-Za-z0-9_$][.:/#][A-Za-z_$]", tok):
        return True
    if "_" in core.strip("_"):
        return True
    if re.search(r"[a-z][A-Z]", core):
        return True
    if re.match(r"[A-Z]", core) and re.search(r"[a-z]", core) and len(re.findall(r"[A-Za-z]", core)) >= 3:
        return True
    if tok[:1] in "@?" and len(core) >= 2:
        return True
    if after == "(" or (before and before in "<.@?"):
        return re.search(r"[A-Za-z]", core) is not None and not (core.isupper() and len(core) <= 4 and after != "(")
    return False


MARKER = re.compile(r"(?<![A-Za-z0-9_\-])(?=[A-Z0-9_\-]*[A-Z])[A-Z0-9][A-Z0-9_\-]*[A-Z0-9](?![A-Za-z0-9_\-])")
GENERIC_ACRONYMS = {"XML", "SDK", "API", "UI", "ID", "DP", "SP", "PX", "VP", "FP", "OS", "JSON", "HTTP", "HTTPS", "URL", "URI", "CPU",
                    "GPU", "IDE", "APP", "UX", "RGB", "ARGB", "RGBA", "HTML", "CSS", "JS", "TS", "PNG", "SVG", "AAR", "JAR", "AGP"}
BACKTICK = re.compile(r"`[^`\n]+`")


def code_idents(text):
    """代码标识符（见 is_code_ident），另加两种：
    f. 流水线里的固定记号：大写字母、数字、连字符、下划线组成、至少两个字符、至少含一个大写字母（如 FWD-REF、P-S2-UNC、TODO）；
       常见的通用缩写（GENERIC_ACRONYMS：XML、SDK、API、UI、DP…）不算；
    g. 反引号括起来的字面量（`…`）。"""
    text = text or ""
    out = []
    for m in TOKEN.finditer(text):
        b = text[m.start() - 1] if m.start() > 0 else ""
        a = text[m.end()] if m.end() < len(text) else ""
        if is_code_ident(m.group(0), b, a):
            out.append(m.group(0))
    out += [m.group(0) for m in MARKER.finditer(text) if m.group(0) not in GENERIC_ACRONYMS and m.group(0) not in out]
    out += [m.group(0) for m in BACKTICK.finditer(text)]
    return out


PLACEHOLDER = re.compile(r"<[^<>\s]{1,40}>\.<[^<>\s]{1,40}>|[A-Za-z]*Xxx[A-Za-z]*|\b[a-z]+xxx\b")


_cache = {}


def file_text_of(f, text):
    """解析到的来源文件全文去掉空白（按 kind 和定位缓存）。"""
    k = id(text)                      # sources.py 按文件缓存了全文，同一个文件是同一个对象
    if k not in _cache:
        _cache[k] = norm(text)
    return _cache[k]


def nonportable_hits(text):
    return [(name, m.group(0)) for name, rx in NONPORTABLE for m in rx.finditer(text or "")]


_resolved = {}


def resolved(f):
    """refs 的一条 → sources.resolve 的结果（按 kind 和 where 缓存）。"""
    k = (f.get("kind"), (f.get("where") or "").strip())
    if k not in _resolved:
        _resolved[k] = S.resolve(*k)
    return _resolved[k]


def ref_file_and_symbol(f):
    _, _, name, sym = resolved(f)
    sym = re.sub(r"[（(][^（()）]*[)）]\s*$", "", sym or "").strip().lstrip("，,、;；:：# ").strip()
    return name, sym


def value_has_ref(v, refs):
    """P2 的「对应」：满足任一条就算 a. ref 的文件名（在线文档取 URL 最后一段）出现在取值的 source 里；b. ref 的 where 里
    路径后面的符号名出现在取值的 value 或 source 里；c. 取值 value 里有一个 4 个字符以上的代码标识符逐字出现在 ref 的 quote 里。"""
    src, val = v.get("source") or "", v.get("value") or ""
    for f in refs:
        if not isinstance(f, dict):
            continue
        name, sym = ref_file_and_symbol(f)
        if name and name in src:
            return True
        if sym and (sym in val or sym in src):
            return True
        q = norm(f.get("quote"))
        if any(len(x) >= 4 and norm(x) in q for x in code_idents(val)):
            return True
    return False


# ---------------------------------------------------------------- 卡库和应用名

_lib = {}


def library():
    if not _lib:
        head = json.load(io.open(os.path.join(STORE, "HEAD.json"), encoding="utf-8"))["revision"]
        snap = json.load(io.open(os.path.join(STORE, "snapshots", head + ".json"), encoding="utf-8"))
        _lib.update(head=head, cases=snap["cases"])
    return _lib


def claim_ok(case, claim):
    meta = library()["cases"].get(case)
    if not meta or meta.get("status") != "available":
        return "卡不在库里"
    if claim not in (meta.get("claims") or []):
        return "这张卡没有这条结论"
    if claim in (meta.get("withdrawn_claims") or []):
        return "这条结论已撤回"
    return None


def cmp_form(s):
    return re.sub(r"[\s\-_]+", "", s or "").lower()


def name_variants(app):
    out = {app}
    s = app
    m = re.match(r"^(?:com|org|net|io)\.[\w.]+\.(\w+)$", s)
    if m:
        out.add(m.group(1))
    for rx in (r"^app[_\-]", r"[_\-](?:hmos|ohos)$", r"_live_android$", r"_android$", r"[_\-]vest\d+$", r"^android[_\-]"):
        s2 = re.sub(rx, "", s)
        if s2 != s:
            out.add(s2)
            s = s2
    return out


_apps = None


def app_names():
    """[(比较形, 原名)]：出事应用的名单（见文件头「应用名」）。"""
    global _apps
    if _apps is None:
        if not os.path.isfile(INDEX):
            raise SystemExit(f"没有 {INDEX}：先跑 skills/memory-rules/scripts/prepare_cards.py")
        idx = json.load(io.open(INDEX, encoding="utf-8"))
        forms = {}
        for a in idx.get("app_list") or []:
            name = a.get("app") or ""
            if not name or name.startswith("（"):
                continue
            for v in name_variants(name):
                f = cmp_form(v)
                if len(f) >= 4 and not f.isdigit() and f not in GENERIC_APP_NAMES:
                    forms.setdefault(f, name)
        _apps = sorted(forms.items(), key=lambda kv: -len(kv[0]))
    return _apps


# ---------------------------------------------------------------- 一条规矩

def nonempty(x):
    return isinstance(x, str) and bool(x.strip())


def visible_fields(r):
    """[(栏名, 文本)]：除 refs、probe 以外的所有栏里的字符串（含 keys）。"""
    out = []

    def walk(k, v):
        if isinstance(v, str):
            out.append((k, v))
        elif isinstance(v, list):
            for j, x in enumerate(v, 1):
                walk(f"{k}[{j}]", x)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                walk(f"{k}.{kk}", vv)
    for k, v in r.items():
        if k not in ("refs", "probe"):
            walk(k, v)
    return out


def body_len(r):
    parts = [r.get("title"), r.get("scope"), r.get("why")]
    for t in r.get("triggers") or []:
        if isinstance(t, dict):
            parts += [t.get("read"), t.get("wrong")]
    for k in ("exceptions", "how"):
        parts += [s.get("text") for s in r.get(k) or [] if isinstance(s, dict)]
    t = "\n".join(p for p in parts if isinstance(p, str))
    return len(t) - t.count("\n")


def check_rule(r, w, ctx, bad, st):
    """ctx: {"kind": "candidate"|"rule", "case": 候选文件的卡号}。"""
    if not isinstance(r, dict):
        bad.append(f"{w}：不是对象")
        return
    used = set()
    if ctx["kind"] == "candidate":
        for k in CANDIDATE_ONLY_ABSENT:
            if k in r:
                bad.append(f"{w}：候选规矩里不写 {k}（由后面的脚本补）")
    for k in ("title", "scope", "why", "siblings_checked"):
        if not nonempty(r.get(k)):
            bad.append(f"{w}：{k} 必须是非空字符串")
    if len(r.get("title") or "") > 60:
        bad.append(f"{w}：标题 {len(r['title'])} 字，超过 60")
    product = r.get("product")
    if product not in PRODUCTS:
        bad.append(f"{w}：product 必须是 {' | '.join(PRODUCTS)} 之一")

    def sup_ok(sup, where):
        if not isinstance(sup, list):
            bad.append(f"{where}：support 必须是列表")
            return
        for s in sup:
            m = CLAIM.match(s) if isinstance(s, str) else None
            if not m:
                bad.append(f"{where}：support「{s}」要写成「卡号#diagnosis」或「卡号#recommendation:N」")
                continue
            why = None if FORMAT_ONLY else claim_ok(m.group(1), m.group(2))
            if FORMAT_ONLY:
                used.add(m.group(1))
            elif why:
                bad.append(f"{where}：support「{s}」{why}")
            elif ctx["kind"] == "candidate" and m.group(1) != ctx["case"]:
                bad.append(f"{where}：support「{s}」不是这张卡的结论（候选规矩只引本卡）")
            else:
                used.add(m.group(1))

    trig = r.get("triggers")
    if not isinstance(trig, list) or not trig:
        bad.append(f"{w}：triggers 至少要有一个触发")
        trig = []
    for j, t in enumerate(trig, 1):
        if not isinstance(t, dict) or not isinstance(t.get("read"), str) or not isinstance(t.get("wrong"), str):
            bad.append(f"{w} 触发 {j}：要有 read 和 wrong 两栏（字符串，没有写空字符串）")
            continue
        filled = [k for k in ("read", "wrong") if t[k].strip()]
        if not filled:
            bad.append(f"{w} 触发 {j}：read、wrong 至少写一栏")
        for k in filled:
            m = PLACEHOLDER.search(t[k])
            if m:
                st["notes"].append(f"P5 {w} 触发 {j}：{k} 里有占位写法「{m.group(0)}」（不要为了过检查编造标识符）")
        if product in CODE_PRODUCTS:
            for k in filled:
                if not code_idents(t[k]):
                    bad.append(f"{w} 触发 {j}：{k} 里没有代码标识符（类名、方法名、属性、XML 标签、取值词等）")
        elif product in PRODUCTS and not t["wrong"].strip():
            bad.append(f"{w} 触发 {j}：规格、计划与派工类的规矩 wrong 栏要写（文档里看得到的说法或缺的那一项）")
    how = r.get("how")
    if not isinstance(how, list) or not 1 <= len(how) <= 3:
        bad.append(f"{w}：how 必须是 1–3 步")
        how = how if isinstance(how, list) else []
    for j, s in enumerate(how, 1):
        if not isinstance(s, dict) or not nonempty(s.get("text")) or not s.get("support"):
            bad.append(f"{w} 第 {j} 步：要有 text 和非空的 support")
        if isinstance(s, dict):
            sup_ok(s.get("support") or [], f"{w} 第 {j} 步")
    exc = r.get("exceptions")
    if not isinstance(exc, list):
        bad.append(f"{w}：exceptions 必须是列表（没有就写空列表）")
        exc = []
    for j, s in enumerate(exc, 1):
        if not isinstance(s, dict) or not nonempty(s.get("text")) or not s.get("support"):
            bad.append(f"{w} 例外 {j}：要有 text 和非空的 support（卡里没写的例外不要加）")
        if isinstance(s, dict):
            sup_ok(s.get("support") or [], f"{w} 例外 {j}")
    refs = r.get("refs")
    if not isinstance(refs, list):
        bad.append(f"{w}：refs 必须是列表（没有就写空列表）")
        refs = []
    vals = r.get("values")
    if not isinstance(vals, list):
        bad.append(f"{w}：values 必须是列表（没有就写空列表）")
        vals = []
    if len(vals) > MAX_VALUES:
        st["notes"].append(f"P4 {w}：取值 {len(vals)} 项，超过 {MAX_VALUES} 项（只留照做时用得上的，同族接口最多 3 个）")
    for j, v in enumerate(vals, 1):
        if not isinstance(v, dict) or not all(nonempty(v.get(k)) for k in ("value", "meaning", "source")):
            bad.append(f"{w} 取值 {j}：要有 value、meaning、source")
        if not isinstance(v, dict):
            continue
        sup_ok(v.get("support", []), f"{w} 取值 {j}")
        if not v.get("support") and not refs:
            bad.append(f"{w} 取值 {j}：support 为空（来自知识库）时 refs 里要有对应出处")
        src = v.get("source") if isinstance(v.get("source"), str) else ""
        if FROM_CARD not in src and not FILE_NAME.search(src) and not code_idents(src):
            st["notes"].append(f"P1 {w} 取值 {j}：source「{src[:40]}」里没有文件名，也没有类名或符号名")
        if not v.get("support") and refs and not value_has_ref(v, refs):
            st["notes"].append(f"P2 {w} 取值 {j}：support 为空，refs 里找不到对应的出处（{(v.get('value') or '')[:40]}）")
    lk = r.get("lookups")
    if not isinstance(lk, list):
        bad.append(f"{w}：lookups 必须是列表（没有就写空列表）")
        lk = []
    for j, x in enumerate(lk, 1):
        if not isinstance(x, dict) or not all(nonempty(x.get(k)) for k in ("what", "where", "how")):
            bad.append(f"{w} 要查 {j}：要有 what、where、how")
    for k in ("unverified", "alternatives_unverified"):
        v = r.get(k)
        if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
            bad.append(f"{w}：{k} 必须是字符串列表（没有就写空列表）")
    keys = r.get("keys")
    if not isinstance(keys, dict) or set(keys) != {"read", "product"}:
        bad.append(f"{w}：keys 必须是 {{\"read\": [...], \"product\": [...]}}")
    else:
        for k in ("read", "product"):
            col = keys[k]
            if not isinstance(col, list) or not all(nonempty(x) for x in col):
                bad.append(f"{w}：keys.{k} 必须是非空字符串的列表")
            elif not 3 <= len(col) <= 12:
                bad.append(f"{w}：keys.{k} 有 {len(col)} 个，要 3–12 个")
    probe = r.get("probe", "缺")
    if probe == "缺":
        bad.append(f"{w}：probe 要写（表达不了就写 null）")
    elif probe is not None:
        if not isinstance(probe, dict) or not nonempty(probe.get("pattern")) or not nonempty(probe.get("note")):
            bad.append(f"{w}：probe 要么是 null，要么是 {{\"pattern\": …, \"note\": …}}，两栏都非空")
        else:
            try:
                rx = re.compile(probe["pattern"])
                if rx.search(""):
                    st["notes"].append(f"P3 {w}：probe 的正则能匹配空字符串")
            except re.error as e:
                bad.append(f"{w}：probe 的正则不能编译（{e}）")
    if ctx["kind"] == "rule":
        src = r.get("sources")
        if not isinstance(src, list) or not src:
            bad.append(f"{w}：sources 至少列一张卡")
            src = []
        for s in src:
            if not FORMAT_ONLY and claim_ok(s, "diagnosis") == "卡不在库里":
                bad.append(f"{w}：sources 里的「{s}」不在库里")
        for s in sorted(used - set(src)):
            bad.append(f"{w}：support 用到了 {s}，sources 里要列上")
        if not isinstance(r.get("general"), bool):
            bad.append(f"{w}：general 必须是 true 或 false")
        if r.get("status") not in ("active", "disputed"):
            bad.append(f"{w}：status 必须是 active 或 disputed")
    n = body_len(r)
    cap = 600 if r.get("general") is True else 800
    if n > cap:
        bad.append(f"{w}：正文 {n} 字，超过 {cap}")
    for j, f in enumerate(refs, 1):
        if not isinstance(f, dict) or f.get("kind") not in KINDS:
            bad.append(f"{w} 出处 {j}：kind 必须是 {' | '.join(sorted(KINDS))} 之一")
            continue
        for k in ("what", "where", "quote", "version"):
            if not nonempty(f.get(k)):
                bad.append(f"{w} 出处 {j}：{k} 不能为空")
        if len(f.get("quote") or "") > 200:
            bad.append(f"{w} 出处 {j}：quote 超过 200 字")
        if S.is_absolute(f.get("where")):
            bad.append(f"{w} 出处 {j}：where 要写来源里的相对路径（见 knowledge-sources.md），不能写本机绝对路径")
            continue
        for k in ("where", "what", "version"):
            for name, hit in nonportable_hits(f.get(k) if isinstance(f.get(k), str) else ""):
                if name != "文件名:行号":
                    bad.append(f"{w} 出处 {j}：{k} 里出现本机路径（{name}：{hit}）")
        if f["kind"] == "android-lib" and not S.COORD.match((f.get("where") or "").strip()):
            bad.append(f"{w} 出处 {j}：依赖库的 where 要写「group:artifact:version 包内路径 资源名」")
            continue
        if FORMAT_ONLY:
            continue
        state, text, fname, _ = resolved(f)
        if state == "url":
            continue                 # 在线地址（文档的旧写法）：不核对原文
        if state in ("no-root", "no-lib"):
            st.setdefault("unchecked", []).append(f"{w} 出处 {j}：{text}")
            continue
        if state != "ok":
            bad.append(f"{w} 出处 {j}：{text}（{(f.get('where') or '')[:70]}）")
        elif norm(f.get("quote")) not in file_text_of(f, text):
            bad.append(f"{w} 出处 {j}：quote 没有逐字出现在 {fname} 里")
    texts = visible_fields(r)
    for k, t in texts:
        for name, hit in nonportable_hits(t):
            bad.append(f"{w} {k}：出现本机路径或行号（{name}：{hit}）")
        m = BAN.search(t)
        if m:
            bad.append(f"{w} {k}：出现「{m.group(0)}」")
    if isinstance(probe, dict) and isinstance(probe.get("pattern"), str):
        texts = texts + [("probe.pattern", probe["pattern"]), ("probe.note", probe.get("note") or "")]
    for k, t in texts:
        tf = cmp_form(t)
        for f, name in app_names():
            if f in tf:
                bad.append(f"{w} {k}：出现了出事应用的名字「{name}」")
                break


# ---------------------------------------------------------------- 文件

def load(path, bad):
    raw = io.open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        bad.append("文件带 BOM，要 UTF-8 不带 BOM")
        raw = raw[3:]
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        bad.append(f"不是合法的 UTF-8 JSON：{e}")
        return None


def check_candidate(path):
    cid = os.path.basename(path)[:-5]
    bad, st = [], {"rules": 0, "left_out": 0, "corrections": 0, "gaps": 0, "conflicts": 0, "notes": []}
    o = load(path, bad)
    if o is None:
        return bad, st
    if o.get("case") != cid:
        bad.append(f"case 应为 {cid}")
    if not FORMAT_ONLY and claim_ok(cid, "diagnosis") == "卡不在库里":
        bad.append(f"{cid} 不在库里（{library()['head'][:8]}）")
    for k in ("rules", "corrections", "left_out", "gaps"):
        if not isinstance(o.get(k), list):
            bad.append(f"{k} 必须是列表（没有就写空列表）")
    if not isinstance(o.get("conflicts", []), list):
        bad.append("conflicts 必须是列表（没有就写空列表）")
    rules = o.get("rules") if isinstance(o.get("rules"), list) else []
    lo = o.get("left_out") if isinstance(o.get("left_out"), list) else []
    co = o.get("corrections") if isinstance(o.get("corrections"), list) else []
    gp = o.get("gaps") if isinstance(o.get("gaps"), list) else []
    cf = o.get("conflicts") if isinstance(o.get("conflicts"), list) else []
    st.update(rules=len(rules), left_out=len(lo), corrections=len(co), gaps=len(gp), conflicts=len(cf))
    for j, x in enumerate(cf, 1):
        if not nonempty(x):
            bad.append(f"conflicts 第 {j} 项：要是非空字符串")
    if len(rules) > MAX_RULES:
        bad.append(f"一张卡最多 {MAX_RULES} 条规矩，这里有 {len(rules)} 条")
    if not rules and not lo:
        bad.append("rules 为空时要在 left_out 里写原因")
    for j, x in enumerate(lo, 1):
        if not isinstance(x, dict) or not nonempty(x.get("text")) or not nonempty(x.get("reason")):
            bad.append(f"left_out 第 {j} 项：要有 text 和 reason")
        elif not (x["reason"].strip() in REASONS or re.match(r"其他[：:]\s*\S", x["reason"].strip())):
            bad.append(f"left_out 第 {j} 项：reason 要是 {'、'.join(REASONS)} 之一或「其他：…」")
    for j, x in enumerate(co, 1):
        if not isinstance(x, dict) or not all(nonempty(x.get(k)) for k in ("was", "now", "ref")):
            bad.append(f"corrections 第 {j} 项：要有 was、now、ref")
    for j, x in enumerate(gp, 1):
        if not nonempty(x):
            bad.append(f"gaps 第 {j} 项：要是非空字符串")
    for i, r in enumerate(rules, 1):
        check_rule(r, f"第 {i} 条", {"kind": "candidate", "case": cid}, bad, st)
    return bad, st


def check_merged(path):
    rid = os.path.basename(path)[:-5]
    bad, st = [], {"rules": 0, "left_out": 0, "corrections": 0, "gaps": 0, "conflicts": 0, "notes": []}
    o = load(path, bad)
    if o is None:
        return bad, st
    if not RULE_ID.match(rid) or o.get("id") != rid:
        bad.append(f"id 应为文件名 {rid}，且是 rule-<12 位十六进制>")
    st["rules"] = 1
    check_rule(o, "规矩", {"kind": "rule", "case": None}, bad, st)
    return bad, st


def main():
    global FORMAT_ONLY
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--roots" in args:
        print(S.describe())
        return
    if "--format-only" in args:
        args.remove("--format-only")
        FORMAT_ONLY = True
    d = os.path.join(STORE, "candidates")
    if "--rules" in args:
        args.remove("--rules")
        d = os.path.join(STORE, "rules")
    if "--dir" in args:
        k = args.index("--dir")
        d = os.path.abspath(args[k + 1])
        args = args[:k] + args[k + 2:]
    files = sorted(glob.glob(os.path.join(d, "case-*.json")) + glob.glob(os.path.join(d, "rule-*.json")))
    if args:
        files = [f for f in files if any(os.path.basename(f).split("-", 1)[1].startswith(re.sub(r"^(case|rule)-", "", a)) for a in args)]
        if not files:
            print(f"在 {d} 下没有找到 {' '.join(args)} 的文件")
    allbad, nrules, notes, lines, T = 0, 0, 0, [], {"left_out": 0, "corrections": 0, "gaps": 0, "conflicts": 0}
    unchecked = []
    for f in files:
        bad, st = (check_candidate if os.path.basename(f).startswith("case-") else check_merged)(f)
        name = os.path.basename(f)[:-5]
        if bad:
            allbad += len(bad)
            print(f"\n[{name}] 硬规则违反 {len(bad)} 处：")
            for b in bad[:40]:
                print("  - " + b)
            if len(bad) > 40:
                print(f"  - ……另有 {len(bad) - 40} 处")
        if st["notes"]:
            print(f"\n[{name}] 提示（不算硬规则）{len(st['notes'])} 项：")
            for b in st["notes"][:20]:
                print("  · " + b)
        nrules += st["rules"]
        notes += len(st["notes"])
        unchecked += [f"[{name}] {x}" for x in st.get("unchecked") or []]
        for k in T:
            T[k] += st[k]
        lines.append(f"{name}：规矩 {st['rules']}，left_out {st['left_out']}，corrections {st['corrections']}，gaps {st['gaps']}，"
                     f"conflicts {st['conflicts']}，违反 {len(bad)}，提示 {len(st['notes'])}")
    print()
    for x in lines:
        print(x)
    if unchecked:
        print(f"没能核对的出处 {len(unchecked)} 条（本机没有这个来源或这个库，不算违反；配 work/sources.local.json 后再查）：")
        for x in unchecked[:20]:
            print("  ? " + x)
    print(f"查了 {len(files)} 个文件，{nrules} 条规矩；left_out {T['left_out']}，corrections {T['corrections']}，gaps {T['gaps']}，"
          f"conflicts {T['conflicts']}；提示 {notes} 项；硬规则违反合计 {allbad} 处")
    sys.exit(1 if allbad else 0)


if __name__ == "__main__":
    main()
