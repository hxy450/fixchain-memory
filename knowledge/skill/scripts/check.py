# -*- coding: utf-8 -*-
r"""检查知识文件（不调模型，只读，不写任何文件）。写知识和复核的人用；可选核对本机的 SDK、文档同步目录等出处。
经验库仓库里的 knowledge/check.py 是仓库一侧的检查（同一套格式规则，不核本机出处），并入仓库时跑那一个。

报错（有一处就退出码 1）：
  格式  json 能解析；顶层键 id（= 文件名）、sdk（含 harmony、android 两个字符串）、changes（列表）、entries（列表）、
        device_todo（字符串列表）、dropped_notes（非负整数），可有 note（字符串）；不许再有 unverified、doubts（统一时要清掉）。
        entries 为空时 note 必须写明为什么没有条目。
  条目  step、fact、source、kind、origin 都是非空字符串；kind 是 鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证；origin 是 沿用并复核 / 新查；
        step 是正文的部分名（标题、何时使用、适用情境、例外与边界、原因、做法第 N 步、做法第 N、M 步），几个部分用「 / 」连。
  改句  where、before、after、basis、type 都是非空字符串；type 是 改错 / 加条件 / 写成明确做法 / 改措辞；where 同 step 的写法。
        给了 --memory（经验库的 memory 目录，按 <经验号>.lesson.md 递归找）或 --bodies（平铺的正文目录，<经验号>.md）时：
        经验文件要在；改句按渲染时的办法依次套（原句在当前文本里逐字出现一次，或空白可有可无地对上恰好一处），
        套不上的报错。原句在原经验文件里不是恰好出现一次、但落在前一处改句的新句里能套上的，只列出。
  路径  fact、source、after、basis、note、device_todo 里不许有本机路径（盘符、用户目录、应用数据目录）和「文件:行号」「第 N 行」。
  应用名 fact、after、note 里不许有 --app-name 给的应用名（不区分大小写）。留作评测的应用名不写进这个脚本，用参数传。
  卡里验证 kind=卡里验证 的 fact 不许出现「改为|改成|后一致|不再|修好|返修」（它只写什么条件下平台怎么表现，不写某次返修怎么改的）。
  尾巴  所有 fact 不许出现「改成…后|后一致|修好|撤回|还原|不靠|适合|：用于|仍要|再作|后再」（返修经过和做法建议的尾巴要去掉）。
  链接  source、basis 里的网址只许是一手来源（见 FIRST_HAND）：OpenHarmony 文档仓库 master 的 blob 链接、AOSP 源码站、
        安卓官方参考文档、依赖库的官方仓库或源码包；别的网址（博客、问答、教程）报错。文档写 raw 链接也报错（出处写 blob 链接）。
  新格式 sdk 里有 verified_on、docs_commit、docs_date 任一个，或加了 --require-new 时，按新格式的写法查：
        三个键都要有（核实日期、文档 master 的提交号、提交日期，日期写 YYYY-MM-DD），harmony 里写明 API 几；
        文档出处要写成链接（https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/<路径>.md，小节名），
        旧写法「文档 xxx.md，小节名」报错。没有这几个键的旧格式文件两种写法都认。

只列出、不算错（给人逐条看）：
  - 改句的新句里提到 设备 / 上机 / 截图 / 核对 / 登记 / 实测 的（拿经验去做事的模型没有设备，要看它能不能照做）；
  - 安卓平台、依赖库条目里写「默认」却没有「另设 / 没设 / 未设 / 没写 / 未写 / 不设 …」这类限定的；
  - fact 里提到的 API 版本比 sdk.harmony 写的本机 SDK 高、却没注明超出本机 SDK 的；
  - 给了 --docs 时，文件的 docs_commit 和同步目录现在的提交不同的；
  - 给了 --sources 时，出处核对不上的（见下）。

--sources：把出处拿到本机来源里对一遍。根目录用参数给，脚本里不写本机路径：
  --oh-ets  鸿蒙 SDK 的 openharmony/ets 目录      --hms-ets  鸿蒙 SDK 的 hms/ets 目录
  --docs    sync_ohdocs.py 建的 OpenHarmony 文档同步目录（最新 master）
  --android-platforms  Android SDK 的 platforms 目录   --android-src  Android SDK 的 sources/android-<N> 目录
  鸿蒙声明：文件在、点到的成员名在文件里；平台资源：文件在、资源名在文件里；安卓源码：类文件在、成员名在；
  文档：链接写法按仓库内路径找文件，旧写法按文件名找，再看小节名在不在。
  卡里验证、依赖库、AOSP 和官方参考文档的网址不核；认不出的出处写法列出来。

用法：
  py -3.12 -B -X utf8 check.py <知识文件目录或文件 …> [--memory <memory 目录> | --bodies <正文目录>] [--app-name 名字 …] [--require-new]
                               [--docs <文档同步目录>] [--sources --oh-ets … --hms-ets … --android-platforms … --android-src …]
只用标准库（--docs 时用 git 读同步目录的提交号，只读）。"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, json, os, re  # noqa: E401,E402

KINDS = ("鸿蒙接口", "安卓平台", "依赖库", "卡里验证")
ORIGINS = ("沿用并复核", "新查")
TYPES = ("改错", "加条件", "写成明确做法", "改措辞")
TOP = ("id", "sdk", "changes", "entries", "device_todo", "dropped_notes")
PART_RX = re.compile(r"^(标题|何时使用|适用情境|例外与边界|原因|做法第 \d+(?:、\d+)* 步)$")
MACHINE_RX = [("盘符路径", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")),
              ("Users 目录", re.compile(r"(?i)(?<![A-Za-z0-9])users[\\/]")),
              ("App" "Data", re.compile(r"(?i)app" r"data"))]   # 分两段写：本文件自己过仓库的提交前扫描
FILE_EXT = "java|kt|kts|xml|ets|ts|js|mjs|json5?|md|py|gradle|properties|txt|c|cc|cpp|h|hpp|aidl|smali|ya?ml|html?|css"
LINE_RX = re.compile(rf"(?i)[\w$-]+\.(?:{FILE_EXT})\s*(?:[:：]\s*\d+(?![\w.])|#L\d+|;l=\d+)|第\s*\d+\s*行")
URL_RX = re.compile(r"https?://[^\s，,；;）)」]+")
DOC_LINK_RX = re.compile(r"https://(gitcode\.com/openharmony/docs/blob|raw\.gitcode\.com/openharmony/docs/raw)/master/"
                         r"(zh-cn/application-dev/[^\s，,；;）)]+?\.md)")
OLD_DOC_RX = re.compile(r"(?<![/\w.-])[\w.-]+\.md(?![\w/])")
# 一手来源：OpenHarmony 文档仓库（master 的 blob 链接）；AOSP 源码站；安卓官方参考文档；依赖库的官方仓库和源码包（Maven 仓库里的 sources jar）
FIRST_HAND = ("https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/",
              "https://android.googlesource.com/", "https://cs.android.com/",
              "https://developer.android.com/reference/", "https://developer.android.google.cn/reference/",
              "https://github.com/androidx/androidx/", "https://github.com/material-components/material-components-android/",
              "https://maven.google.com/", "https://dl.google.com/android/maven2/", "https://repo1.maven.org/maven2/")
NEW_SDK_KEYS = ("verified_on", "docs_commit", "docs_date")
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
API_RX = re.compile(r"API(?:\s*version)?\s*(\d{1,2})(?!\d)", re.I)
BEYOND = re.compile("超出本机|本机 SDK|本机SDK|SDK 里没有|SDK 中没有|声明里没有|本机声明没有|本机没有")
CARD_BAD = re.compile("改为|改成|后一致|不再|修好|返修")                      # rules.md T3
TAIL_BAD = re.compile("改成.{0,12}后|后一致|修好|撤回|还原|不靠|适合|：用于|仍要|再作|后再")   # rules.md T5
DEVICE = re.compile(r"设备|上机|截图|核对|登记|实测")                          # rules.md U6
QUALIFIER = re.compile("另设|没设|未设|没写|未写|不设|不写|未调用|没有改|没改|缺省|未声明|没声明|不传|省略|未覆写|没有覆写")
SRC_RX = re.compile(r"\n## (?:来源|同源经验)")


# ---------------------------------------------------------------- 正文
def body(path):
    t = SRC_RX.split(io.open(path, encoding="utf-8").read(), maxsplit=1)[0]
    t = re.sub(r"(?m)^\[本主题\]\(index\.md\)\n\n?", "", t)
    t = re.sub(r"(?m)^ID：`lesson-[0-9a-f]+`.*\n\n?", "", t)
    return t.strip() + "\n"


def loose(s):
    parts = [re.escape(x) for x in re.split(r"\s+", s.strip()) if x]
    return re.compile(r"\s*".join(parts))


# ---------------------------------------------------------------- 出处（根目录用参数给）
class Sources:
    def __init__(self, a):
        self.oh, self.hms, self.res, self.src = a.oh_ets, a.hms_ets, a.android_platforms, a.android_src
        self.docs = a.docs
        self.cache = {}
        self.doc_index = collections.defaultdict(list)
        if a.docs:
            for p in glob.glob(os.path.join(a.docs, "zh-cn", "application-dev", "**", "*.md"), recursive=True) or \
                    glob.glob(os.path.join(a.docs, "**", "*.md"), recursive=True):
                self.doc_index[os.path.basename(p).lower()].append(p)

    def doc_sections(self, part, texts, tail):
        sec = [y.strip() for y in re.split(r"[、,，]", tail) if y.strip()]
        t = "\n".join(x or "" for x in texts)
        miss = [x for x in sec if x and x not in t and not re.search(r"起始版本|since", x)]
        return "对得上" if not miss else "文档里没有：" + "、".join(miss[:3])

    def text(self, path):
        if path not in self.cache:
            try:
                self.cache[path] = io.open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                self.cache[path] = None
        return self.cache[path]

    def find_oh(self, rel):
        rel = re.sub(r"^ets/", "", rel.strip().replace("\\", "/"))
        roots = [r for r in (self.oh, self.hms) if r]
        cands = [os.path.join(r, rel) for r in roots]
        if rel.startswith("component/") and self.oh:
            cands.append(os.path.join(self.oh, "build-tools", "ets-loader", "declarations", rel[len("component/"):]))
        for c in cands:
            if os.path.exists(c):
                return c
        for r in roots:
            hits = glob.glob(os.path.join(r, "**", os.path.basename(rel)), recursive=True)
            if hits:
                return hits[0]
        return None

    @staticmethod
    def last_ident(member):
        m = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", member)
        return m[-1] if m else None

    def check(self, src):
        out = []
        for part in re.split(r"[；;]", src):
            part = part.strip()
            if not part:
                continue
            m = DOC_LINK_RX.search(part)
            if m:                                   # 新写法：文档仓库 master 的链接，后接「，小节名」
                if m.group(1).startswith("raw."):
                    out.append(("文档", part, "出处要写 blob 链接，不写 raw 链接"))
                    continue
                if not self.docs:
                    out.append(("文档", part, "不核（没给 --docs）"))
                    continue
                f = os.path.join(self.docs, *m.group(2).split("/"))
                if not os.path.exists(f):
                    out.append(("文档", part, "同步目录里没有这个文件（文档改名或挪了位置？）"))
                    continue
                tail = re.sub(r"^[\s，,（(]+", "", part[m.end():]).rstrip("）)")
                out.append(("文档", part, self.doc_sections(part, [self.text(f)], tail)))
                continue
            if URL_RX.search(part):
                out.append(("联网来源", part, "不核（网址）"))
                continue
            m = re.search(r"((?:ets/)?[\w@./-]+\.d\.e?ts)\s*[，,]?\s*(.*)$", part)
            if m and ("鸿蒙" in part or "SDK" in part or part.startswith("ets/")):
                if not (self.oh or self.hms):
                    out.append(("鸿蒙声明", part, "不核（没给 --oh-ets / --hms-ets）"))
                    continue
                f = self.find_oh(m.group(1))
                if not f:
                    out.append(("鸿蒙声明", part, "文件没找到"))
                    continue
                t = self.text(f) or ""
                miss = [x for x in (self.last_ident(y) for y in re.split(r"[、,，]", m.group(2)) if y.strip()) if x and x not in t]
                out.append(("鸿蒙声明", part, "对得上" if not miss else "文件里没有：" + "、".join(miss)))
                continue
            m = re.search(r"(data/res/[\w./-]+\.xml)\s*[，,]?\s*(.*)$", part)
            if m and not self.res:
                out.append(("安卓平台资源", part, "不核（没给 --android-platforms）"))
                continue
            if m:
                ok = None
                for plat in ("android-34", "android-35", "android-36", "android-33", "android-30"):
                    f = os.path.join(self.res, plat, m.group(1).replace("/", os.sep))
                    if os.path.exists(f):
                        t = self.text(f) or ""
                        names = [y.strip() for y in re.split(r"[、,，]", re.sub(r"（.*?）", "", m.group(2))) if y.strip()]
                        idents = [n2 for n2 in (re.findall(r"[A-Za-z_][\w.]*", n1) for n1 in names) for n2 in n2[:1]]
                        miss = [x for x in idents if x not in t and x.split(".")[-1] not in t]
                        ok = ("安卓平台资源", part, "对得上" if not miss else f"{plat} 里没有：" + "、".join(miss))
                        if not miss:
                            break
                out.append(ok or ("安卓平台资源", part, "文件没找到"))
                continue
            rx = r"(?<![\w/])((?:values[\w-]*|drawable[\w*-]*|color|layout|anim|animator|xml)/[\w.*-]+\.(?:xml|png))"
            m = re.search(rx, part)
            if m and self.res and "包内" not in part and "androidx" not in part and "com.google" not in part:
                rels = re.findall(rx, part)
                tail = part.split("，", 1)[1] if "，" in part else ""
                names = [x for x in re.findall(r"[A-Za-z_][\w.]*", re.sub(r"（.*?）", "", tail)) if len(x) > 3 and not x.endswith(".xml")]
                bad = []
                for rel in rels:
                    found = None
                    for plat in ("android-34", "android-35", "android-36", "android-33", "android-30"):
                        if "*" in rel:
                            hits = glob.glob(os.path.join(self.res, plat, "data", "res", *rel.split("/")))
                            if hits:
                                found = hits[0]
                                break
                        else:
                            f = os.path.join(self.res, plat, "data", "res", *rel.split("/"))
                            if os.path.exists(f):
                                found = f
                                break
                    if not found:
                        bad.append(rel + " 没找到")
                    elif len(rels) == 1 and found.endswith(".xml"):
                        t = self.text(found) or ""
                        miss = [x for x in names if x not in t and x.split(".")[-1] not in t]
                        if miss:
                            bad.append(rel + " 里没有：" + "、".join(miss[:4]))
                out.append(("安卓平台资源", part, "对得上" if not bad else "；".join(bad)))
                continue
            if "包内" in part or re.search(r"\b(appcompat|material|androidx)\b", part):
                out.append(("依赖库", part, "不核（依赖库包）"))
                continue
            m = re.search(r"\b((?:android|java|javax|androidx|com\.android)\.[\w.]+?)(?:#([\w<>]+))?(?=[\s，,、（(]|$)", part)
            if m and m.group(1).startswith(("android.", "java.", "com.android.")):
                if not self.src:
                    out.append(("安卓源码", part, "不核（没给 --android-src）"))
                    continue
                parts = m.group(1).split(".")
                i = next((k for k, x in enumerate(parts) if x[:1].isupper()), len(parts) - 1)
                f = os.path.join(self.src, *parts[:i], parts[i] + ".java")
                if not os.path.exists(f):
                    out.append(("安卓源码", part, "源码文件没找到"))
                    continue
                t = self.text(f) or ""
                names = [x for x in [m.group(2)] + parts[i + 1:] if x] + re.findall(r"#([\w]+)", part)
                miss = [x for x in dict.fromkeys(names) if x and x not in t]
                out.append(("安卓源码", part, "对得上" if not miss else "类里没有：" + "、".join(miss)))
                continue
            m = re.search(r"([\w.-]+\.md)\s*[，,（(]?\s*([^）)]*)", part)
            if m and not self.doc_index:
                out.append(("文档", part, "不核（没给 --docs）"))
                continue
            if m:
                hits = self.doc_index.get(m.group(1).lower())
                if not hits:
                    out.append(("文档", part, "文档没找到"))
                    continue
                out.append(("文档", part, self.doc_sections(part, [self.text(h) for h in hits], m.group(2))))
                continue
            if "卡里" in part:
                out.append(("卡里验证", part, "不核"))
            elif re.search(r"androidx\.|字节码|compose", part, re.I):
                out.append(("依赖库", part, "不核（依赖库包）"))
            else:
                out.append(("其它", part, "认不出的出处写法"))
        return out


# ---------------------------------------------------------------- 检查
def nonempty(x):
    return isinstance(x, str) and x.strip() != ""


def parts_ok(s):
    return all(PART_RX.match(p.strip()) for p in s.split(" / "))


def check_file(path, lib, app_rx, srcs, err, note, src_tally, require_new=False, docs_head=None):
    lid = os.path.basename(path)[:-5]
    try:
        d = json.load(io.open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        err.append(f"{lid}：json 读不了：{e}")
        return
    tag = lid[7:15]
    for k in TOP:
        if k not in d:
            err.append(f"{tag}：缺顶层键 {k}")
    for k in ("unverified", "doubts"):
        if k in d:
            err.append(f"{tag}：还留着 {k}（统一时要清掉：转成条目、写进正文、记 device_todo 或删掉）")
    extra = set(d) - set(TOP) - {"note", "unverified", "doubts"}
    if extra:
        note.append(f"{tag}：有不认识的顶层键 {sorted(extra)}")
    if d.get("id") != lid:
        err.append(f"{tag}：id 和文件名不一致：{d.get('id')}")
    sdk = d.get("sdk")
    if not isinstance(sdk, dict) or not nonempty(sdk.get("harmony")) or not nonempty(sdk.get("android")):
        err.append(f"{tag}：sdk 要有 harmony、android 两个非空字符串（没用到就写「不涉及」「未用」）")
        sdk = sdk if isinstance(sdk, dict) else {}
    new = require_new or any(k in sdk for k in NEW_SDK_KEYS)
    if new:
        for k in ("verified_on", "docs_date"):
            if not (isinstance(sdk.get(k), str) and DATE_RX.match(sdk[k])):
                err.append(f"{tag}：新格式的 sdk.{k} 要写 YYYY-MM-DD")
        if not (isinstance(sdk.get("docs_commit"), str) and re.fullmatch(r"[0-9a-f]{7,40}", sdk["docs_commit"])):
            err.append(f"{tag}：新格式的 sdk.docs_commit 要写文档仓库 master 的提交号（sync_ohdocs.py 打印的）")
        if sdk.get("harmony") not in ("未用",) and not API_RX.search(sdk.get("harmony") or ""):
            err.append(f"{tag}：新格式的 sdk.harmony 要写明本机鸿蒙 SDK 是 API 几")
        if docs_head and isinstance(sdk.get("docs_commit"), str) and not docs_head.startswith(sdk["docs_commit"][:7]):
            note.append(f"{tag}：sdk.docs_commit {sdk['docs_commit'][:8]} 和同步目录现在的提交 {docs_head[:8]} 不同（文档 master 后来更新过，要不要重核看改动）")
    local_api = int(API_RX.search(sdk.get("harmony") or "").group(1)) if API_RX.search(sdk.get("harmony") or "") else None
    if not isinstance(d.get("dropped_notes"), int) or d.get("dropped_notes", 0) < 0:
        err.append(f"{tag}：dropped_notes 要是非负整数")
    dt = d.get("device_todo")
    if not isinstance(dt, list) or not all(nonempty(x) for x in dt):
        err.append(f"{tag}：device_todo 要是字符串列表")
    ents = d.get("entries")
    if not isinstance(ents, list):
        err.append(f"{tag}：entries 不是列表")
        ents = []
    if not ents and not nonempty(d.get("note")):
        err.append(f"{tag}：没有条目时 note 要写明为什么（例：流程类经验，做法不依赖平台事实）")
    texts = []
    for k, e in enumerate(ents, 1):
        w = f"{tag} 第 {k} 条"
        if not isinstance(e, dict):
            err.append(f"{w}：不是对象")
            continue
        for key in ("step", "fact", "source", "kind", "origin"):
            if not nonempty(e.get(key)):
                err.append(f"{w}：缺 {key}")
        if e.get("kind") not in KINDS:
            err.append(f"{w}：kind 不是 {'/'.join(KINDS)}：{e.get('kind')}")
        if e.get("origin") not in ORIGINS:
            err.append(f"{w}：origin 不是 {'/'.join(ORIGINS)}：{e.get('origin')}")
        if nonempty(e.get("step")) and not parts_ok(e["step"]):
            err.append(f"{w}：step 不是正文的部分名：{e['step']}")
        fact = e.get("fact") or ""
        if e.get("kind") == "卡里验证" and CARD_BAD.search(fact):
            err.append(f"{w}：卡里验证的条目写了返修怎么改的（「{CARD_BAD.search(fact).group(0)}」）：{fact[:60]}")
        if TAIL_BAD.search(fact):
            err.append(f"{w}：fact 带了返修经过或做法建议的尾巴（「{TAIL_BAD.search(fact).group(0)}」）：{fact[:60]}")
        if "默认" in fact and e.get("kind") in ("安卓平台", "依赖库") and not QUALIFIER.search(fact):
            note.append(f"{w}：默认值没写「应用没有另设时」一类的限定（看是不是应用可另设的值）：{fact[:70]}")
        if local_api and e.get("kind") == "鸿蒙接口":
            hi = [int(x) for x in API_RX.findall(fact) if int(x) > local_api]
            if hi and not BEYOND.search(fact):
                note.append(f"{w}：提到 API {max(hi)}，高于本机 SDK 的 API {local_api}，没注明超出本机 SDK：{fact[:70]}")
        if new:
            for part in re.split(r"[；;]", e.get("source") or ""):
                if OLD_DOC_RX.search(part) and not DOC_LINK_RX.search(part):
                    err.append(f"{w}：新格式文件的文档出处要写成链接（ohdocs_link.py 换）：{part.strip()[:80]}")
        texts += [(w + " fact", fact, True), (w + " source", e.get("source") or "", False)]
        if srcs:
            for cat, part, verdict in srcs.check(e.get("source") or ""):
                v = "对得上" if verdict == "对得上" else ("不核" if verdict.startswith("不核") else "有问题")
                src_tally[(cat, v)] += 1
                if v == "有问题":
                    note.append(f"{w}：出处｜{verdict}｜{part[:120]}")
    chs = d.get("changes")
    if not isinstance(chs, list):
        err.append(f"{tag}：changes 不是列表")
        chs = []
    for k, c in enumerate(chs, 1):
        w = f"{tag} 改句 {k}"
        if not isinstance(c, dict):
            err.append(f"{w}：不是对象")
            continue
        for key in ("where", "before", "after", "basis", "type"):
            if not nonempty(c.get(key)):
                err.append(f"{w}：缺 {key}")
        if c.get("type") not in TYPES:
            err.append(f"{w}：type 不是 {'/'.join(TYPES)}：{c.get('type')}")
        if nonempty(c.get("where")) and not parts_ok(c["where"]):
            err.append(f"{w}：where 不是正文的部分名：{c['where']}")
        if DEVICE.search(c.get("after") or ""):
            note.append(f"{w}：新句提到「{DEVICE.search(c['after']).group(0)}」：{c['after'][:100]}")
        texts += [(w + " after", c.get("after") or "", True), (w + " basis", c.get("basis") or "", False)]
    texts += [(f"{tag} note", d.get("note") or "", True)] + [(f"{tag} device_todo", x, False) for x in dt or [] if isinstance(x, str)]
    for where, t, names in texts:
        for url in URL_RX.findall(t):
            if names:                          # fact、after、note 交给模型（或给人看），不放链接
                err.append(f"{where}：这一栏不放链接（链接只写在 source、basis 里）：{url[:80]}")
            elif DOC_LINK_RX.match(url) and url.startswith("https://raw."):
                err.append(f"{where}：文档出处写 blob 链接，不写 raw 链接：{url[:80]}")
            elif not url.startswith(FIRST_HAND):
                err.append(f"{where}：不是一手来源的网址（只认 OpenHarmony 文档仓库 master、AOSP、安卓官方参考文档、依赖库官方仓库和源码包）：{url[:80]}")
        for lab, rx in MACHINE_RX:
            if rx.search(t):
                err.append(f"{where}：有本机路径（{lab}）")
        if LINE_RX.search(t):
            err.append(f"{where}：有行号写法「{LINE_RX.search(t).group(0)}」")
        if names:
            for rx in app_rx:
                if rx.search(t):
                    err.append(f"{where}：有应用名「{rx.search(t).group(0)}」")
    if lib is not None:
        p = lib.get(lid)
        if not p:
            err.append(f"{tag}：正文目录里没有这条经验")
            return
        raw = io.open(p, encoding="utf-8").read()
        text = body(p)
        for k, c in enumerate(chs, 1):
            b, a = (c.get("before") or "").strip(), (c.get("after") or "").strip()
            if not b or not a:
                continue
            n_raw = raw.count(b)
            # 已经发布进正文的改句（并进经验库以后）：新句在、原句不在新句之外出现 → 算对上，和 render.py 的 published 同一条规则
            if a in text and ((b not in text and not list(loose(b).finditer(text)))
                              or (b in text and b in a and text.count(b) == text.count(a) * a.count(b))):
                continue
            if text.count(b) == 1:
                text = text.replace(b, a)
            else:
                m = list(loose(b).finditer(text))
                if len(m) == 1:
                    text = text[:m[0].start()] + a + text[m[0].end():]
                else:
                    err.append(f"{tag} 改句 {k}：原句在（套过前面改句的）正文里对上 {len(m)} 处，套不上：{b[:50]}…")
                    continue
            if n_raw != 1:
                note.append(f"{tag} 改句 {k}：原句在经验文件里出现 {n_raw} 次（按空白可有可无或落在前一处新句里才套上）：{b[:50]}…")


def docs_commit(d):
    """同步目录现在的提交号（git rev-parse HEAD，只读）；读不到返回 None。"""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    except OSError:
        return None


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="+")
    ap.add_argument("--memory")
    ap.add_argument("--bodies")
    ap.add_argument("--app-name", action="append", default=[])
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--require-new", action="store_true")
    for k in ("--oh-ets", "--hms-ets", "--docs", "--android-platforms", "--android-src"):
        ap.add_argument(k)
    a = ap.parse_args(argv)
    files = []
    for p in a.path:                       # 可以给目录（查其中全部 lesson-*.json），也可以给一个或几个文件
        files += sorted(glob.glob(os.path.join(p, "lesson-*.json"))) if os.path.isdir(p) else [p]
    lib = None
    if a.memory and a.bodies:
        ap.error("--memory 和 --bodies 只给一个")
    if a.memory:
        lib = {os.path.basename(p).split(".")[0]: p for p in glob.glob(os.path.join(a.memory, "**", "lesson-*.lesson.md"), recursive=True)}
    elif a.bodies:
        lib = {os.path.basename(p)[:-3]: p for p in glob.glob(os.path.join(a.bodies, "lesson-*.md"))}
    app_rx = [re.compile(re.escape(n), re.I) for n in a.app_name if n.strip()]
    srcs = Sources(a) if a.sources else None
    docs_head = docs_commit(a.docs) if a.docs else None
    err, note, src_tally = [], [], collections.Counter()
    n_ent = n_ch = 0
    for f in files:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
            n_ent += len(d.get("entries") or [])
            n_ch += len(d.get("changes") or [])
        except (OSError, ValueError):
            pass
        check_file(f, lib, app_rx, srcs, err, note, src_tally, a.require_new, docs_head)
    print(f"{len(files)} 个知识文件，条目 {n_ent} 条，改句 {n_ch} 处" + ("；改句按正文核过" if lib is not None else "；没给 --memory / --bodies，改句没对正文"))
    if srcs:
        print("出处核对：" + "；".join(f"{c} {v} {n}" for (c, v), n in sorted(src_tally.items())))
    print(f"错误 {len(err)} 处" + ("：" if err else ""))
    for x in err:
        print("  " + x)
    print(f"要人看的 {len(note)} 处" + ("：" if note else ""))
    for x in note:
        print("  " + x)
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
