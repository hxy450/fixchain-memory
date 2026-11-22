# -*- coding: utf-8 -*-
r"""Check knowledge files against knowledge/RULES.md (read only, no model call, writes nothing).

  python knowledge/check.py knowledge/lessons [--only <id 8 chars,…>] [--legacy-ok] [--app-name NAME …]

Per lesson-<id>.json in the dir (not recursive; _*.json skipped):
  - json parses; "lesson" equals the file name's id; the lesson is in this repository's memory/ (a lesson that the store
    has retired is listed, not an error, and its changes are not checked).
  - entries: a list; each entry has step, fact, scope, source, kind, origin as non-empty strings; kind is one of KINDS;
    at most MAX_ENTRIES entries.
  - source, fact, scope, code: no machine path (drive letter, a users directory, the local app-data directory) and no
    「file:line」 reference (x.ext:12, x.ext#L12, x.ext 第 12 行).
  - fact, scope: no migrated app's name (APP_NAMES plus every --app-name, case-insensitive). The names of held-out
    evaluation apps are not kept in this repository: pass them with --app-name.
  - changes: a list; each has where, before, after, basis, type (non-empty). Checked against this lesson's text (the text
    the shadow sees: cut at 「## 来源」/「## 同源经验」, no ID line, no topic link), exactly or with whitespace optional.
    In this repository the changes are published into the lessons (memory/ is exported from a store that carries them):
    a published change has its after in the text (when a later change's before lies inside it, the after as the later
    change left it) and its before nowhere outside the afters. A change not published yet (a new knowledge file) is
    listed, not an error, when its before is found exactly once (the prompt generator / render.py stop otherwise).
A file is old-format when it has no "lesson" key (the third version's files use "id") and none of its entries has a scope
key (a file with "lesson", or with some scopes, is checked as a new file). With --legacy-ok, in an old-format file these
are listed, not errors: the "id" key (it must still equal the file name), entries without scope,
more than MAX_ENTRIES entries, kind 「卡里验证」 (a kind of the third version). Everything else stays an error.

2026-11-21 format (no "lesson" key, and sdk has one of verified_on / docs_commit / docs_date): checked by check_dated() with
the rules of the knowledge-writing skill's check script (not by the rules above; --legacy-ok does not apply to it):
  - top keys id (= file name), sdk (harmony, android non-empty strings), changes, entries, device_todo (list of
    strings), dropped_notes (int >= 0), note when there are no entries; no unverified / doubts left. sdk: verified_on and
    docs_date YYYY-MM-DD, docs_commit hex (7-40), harmony names the API level.
  - entries: step, fact, source, kind, origin non-empty; kind 鸿蒙接口 / 安卓平台 / 依赖库 / 卡里验证; origin 沿用并复核 /
    新查; step is a part name of the lesson text; no entry limit, no scope. 卡里验证 facts have no repair wording; no fact
    has a repair or advice tail. A document source is a link to the OpenHarmony docs repository's master (blob).
  - changes: where, before, after, basis, type non-empty; type 改错 / 加条件 / 写成明确做法 / 改措辞; where is a part name.
  - fact / after / note: no link, no app name; source / basis: links only to first-hand sources; all of fact, source,
    after, basis, note, device_todo: no machine path, no line reference.
  - against this lesson's text, change by change in order, as render.py (and the skill's render script) does: published
    (the after is in the text and the before nowhere outside it) is fine; else, when the after and the before are both
    there (and the after is not part of the before), an error; else it must go on (exactly once, else whitespace
    optional exactly once, in the text with the earlier changes on) and is listed as not published yet.
  Listed, not errors (the skill's 「要人看的」): changes whose after mentions device / screenshot work, 安卓平台 / 依赖库
  facts with 「默认」 but no 「应用没有另设」-like qualifier, 鸿蒙接口 facts naming an API above the local SDK's without
  saying so, unknown top keys, a before found other than once in the lesson file. Source verification against local SDK
  and docs trees (the skill's --sources / --docs) is not done here.
Exit 1 when there is any error (or an --only id has no file), else 0. Standard library only."""
import sys

sys.dont_write_bytecode = True
import argparse, json, re  # noqa: E401,E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "memory"                 # read only
STORE = ROOT / "store"                # read only: only to tell a retired lesson from a missing one
KINDS = ("鸿蒙接口", "安卓平台", "依赖库")
LEGACY_KINDS = ("卡里验证",)
MAX_ENTRIES = 6
ENTRY_KEYS = ("step", "fact", "scope", "source", "kind", "origin")
CHANGE_KEYS = ("where", "before", "after", "basis", "type")
TEXT_FIELDS = ("source", "fact", "scope", "code")
NAME_FIELDS = ("fact", "scope")
# migrated apps (add here, or pass --app-name). Short names are matched as whole words; the rest as substrings, case-insensitive.
APP_NAMES = ["cofi", "gameoflife", "game of life", "antennapod"]
MACHINE_RX = [("盘符路径", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]")),
              ("Users 目录", re.compile(r"(?i)(?<![A-Za-z0-9])users[\\/]")),
              ("AppData", re.compile(r"(?i)appdata"))]
FILE_EXT = "java|kt|kts|xml|ets|ts|js|mjs|json5?|md|py|gradle|properties|txt|c|cc|cpp|h|hpp|aidl|smali|ya?ml|html?|css"
LINE_RX = re.compile(rf"(?i)[\w$-]+\.(?:{FILE_EXT})\s*(?:[:：]\s*\d+(?![\w.])|#L\d+|[（(]?\s*第\s*\d+\s*行)")
SRC_RX = re.compile(r"\n## (?:来源|同源经验)")
ID_RX = re.compile(r"^lesson-[0-9a-f]{20}$")


def app_rx(name):
    e = re.escape(name)
    return re.compile(rf"(?i)(?<![a-z0-9]){e}(?![a-z0-9])" if len(name) < 6 else rf"(?i){e}")


def lib_text(path):
    """The lesson text as the prompt generator / knowledge/render.py takes it."""
    t = SRC_RX.split(path.read_text(encoding="utf-8"), maxsplit=1)[0]
    t = re.sub(r"(?m)^\[本主题\]\(index\.md\)\n\n?", "", t)
    t = re.sub(r"(?m)^ID：`lesson-[0-9a-f]+`.*\n\n?", "", t)
    return "\n" + t.strip() + "\n"


def store_status():
    try:
        head = json.loads((STORE / "HEAD.json").read_text(encoding="utf-8"))["revision"]
        snap = json.loads((STORE / "snapshots" / f"{head}.json").read_text(encoding="utf-8"))
        return {k: v.get("status") for k, v in snap["lessons"].items()}
    except (OSError, KeyError, ValueError):
        return {}


def loose(s):
    parts = [re.escape(x) for x in re.split(r"\s+", s.strip()) if x]
    return re.compile(r"\s*".join(parts))


def found(text, before):
    """-> number of places the sentence is found (exactly, else with whitespace optional)."""
    n = text.count(before)
    return n if n else len(list(loose(before).finditer(text)))


def nonempty(v):
    return isinstance(v, str) and v.strip() != ""


def check_file(f, lib, legacy_ok, app_rx_list, status):
    """-> (errors, legacy notes, info)."""
    err, leg = [], []
    stem = f.stem
    if not ID_RX.match(stem):
        return [f"文件名不是 lesson-<20 位十六进制>.json"], [], {}
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return [f"json 解析不了：{e}"], [], {}
    if not isinstance(d, dict):
        return ["顶层不是对象"], [], {}
    if is_dated(d):
        return check_dated(stem, d, lib, app_rx_list, status)
    entries, changes = d.get("entries"), d.get("changes")
    if not isinstance(entries, list):
        err.append("entries 不是列表（或缺）")
        entries = []
    if changes is None:
        changes = []
    elif not isinstance(changes, list):
        err.append("changes 不是列表")
        changes = []
    old = "lesson" not in d and not any(isinstance(e, dict) and "scope" in e for e in entries)

    def soft(msg):
        (leg if (legacy_ok and old) else err).append(msg)
    if "lesson" in d:
        if d["lesson"] != stem:
            err.append(f"lesson 「{d['lesson']}」和文件名不一致")
    elif d.get("id") == stem:
        soft("用的是 id 键，不是 lesson")
    else:
        err.append("缺 lesson 键（id 也和文件名不一致）")
    retired = stem not in lib and status.get(stem) == "retired"
    if retired:
        leg.append("store 里已退役：memory/ 里没有，改句不核")
    elif stem not in lib:
        err.append("memory/ 里没有这条经验")
    if len(entries) > MAX_ENTRIES:
        soft(f"entries {len(entries)} 条，超过 {MAX_ENTRIES} 条")
    no_scope = 0
    for k, e in enumerate(entries, 1):
        if not isinstance(e, dict):
            err.append(f"第 {k} 条不是对象")
            continue
        for key in ENTRY_KEYS:
            if key == "scope" and "scope" not in e and legacy_ok and old:
                no_scope += 1                    # listed once per file below
                continue
            if not nonempty(e.get(key)):
                err.append(f"第 {k} 条 {key} 缺或为空")
        kind = e.get("kind")
        if nonempty(kind) and kind not in KINDS:
            if kind in LEGACY_KINDS:
                soft(f"第 {k} 条 kind 「{kind}」（第三版的类别）")
            else:
                err.append(f"第 {k} 条 kind 「{kind}」不是 {' / '.join(KINDS)} 之一")
        for fld in TEXT_FIELDS:
            v = e.get(fld)
            if not isinstance(v, str):
                continue
            for what, rx in MACHINE_RX:
                m = rx.search(v)
                if m:
                    err.append(f"第 {k} 条 {fld} 有本机路径（{what}）：…{v[max(0, m.start() - 15):m.end() + 25]}…")
            refs = [m.group(0) for m in LINE_RX.finditer(v)]
            if refs:
                err.append(f"第 {k} 条 {fld} 有「文件:行号」引用：{'、'.join(refs)}")
        for fld in NAME_FIELDS:
            v = e.get(fld)
            if isinstance(v, str):
                hits = [n for n, rx in app_rx_list if rx.search(v)]
                if hits:
                    err.append(f"第 {k} 条 {fld} 有被迁移应用的名字：{'、'.join(hits)}")
    if no_scope:
        leg.append(f"{no_scope} / {len(entries)} 条没有 scope")
    text = lib_text(lib[stem]) if stem in lib else None
    pairs = [((c.get("before") or "").strip(), (c.get("after") or "").strip()) if isinstance(c, dict) else ("", "") for c in changes]
    eff = []
    for k, (_, a) in enumerate(pairs):
        for b2, a2 in pairs[k + 1:]:
            if b2 and b2 in a:
                a = a.replace(b2, a2, 1)
        eff.append(a)
    masked = text
    if text is not None:
        for a in sorted((x for x in eff if x), key=len, reverse=True):
            masked = loose(a).sub("\u0000", masked)
    for k, c in enumerate(changes, 1):
        if not isinstance(c, dict):
            err.append(f"改句第 {k} 处不是对象")
            continue
        miss = [key for key in CHANGE_KEYS if not nonempty(c.get(key))]
        if miss:
            err.append(f"改句第 {k} 处〔{c.get('where')}〕缺 {'、'.join(miss)}")
        b, a = pairs[k - 1]
        if b and a and text is not None:
            if found(text, eff[k - 1]):                  # published: the after is there, the before is gone
                n = found(masked, b)
                if n:
                    err.append(f"改句第 {k} 处〔{c.get('where')}〕after 已在正文里，before 在 after 之外却还出现 {n} 处：{b[:50]}…")
                continue
            n = found(text, b)                           # not published yet: the before must be found exactly once
            if n == 1:
                leg.append(f"改句第 {k} 处〔{c.get('where')}〕还没发布进正文（before 唯一可定位）")
            elif n == 0:
                err.append(f"改句第 {k} 处〔{c.get('where')}〕after 不在正文里，before 也找不到：{b[:50]}…")
            else:
                err.append(f"改句第 {k} 处〔{c.get('where')}〕after 不在正文里，before 出现 {n} 处（要能唯一定位）：{b[:50]}…")
    return err, leg, {"entries": len(entries), "changes": len(changes), "old_format": old}


# ---------------------------------------------------------------- 2026-11-21 format (the knowledge-writing skill's rules)
D_KINDS = ("鸿蒙接口", "安卓平台", "依赖库", "卡里验证")
D_ORIGINS = ("沿用并复核", "新查")
D_TYPES = ("改错", "加条件", "写成明确做法", "改措辞")
D_TOP = ("id", "sdk", "changes", "entries", "device_todo", "dropped_notes")
D_SDK_KEYS = ("verified_on", "docs_commit", "docs_date")
D_PART_RX = re.compile(r"^(标题|何时使用|适用情境|例外与边界|原因|做法第 \d+(?:、\d+)* 步)$")
D_LINE_RX = re.compile(rf"(?i)[\w$-]+\.(?:{FILE_EXT})\s*(?:[:：]\s*\d+(?![\w.])|#L\d+|;l=\d+)|第\s*\d+\s*行")
D_URL_RX = re.compile(r"https?://[^\s，,；;）)」]+")
D_DOC_LINK_RX = re.compile(r"https://(gitcode\.com/openharmony/docs/blob|raw\.gitcode\.com/openharmony/docs/raw)/master/"
                           r"(zh-cn/application-dev/[^\s，,；;）)]+?\.md)")
D_OLD_DOC_RX = re.compile(r"(?<![/\w.-])[\w.-]+\.md(?![\w/])")
D_FIRST_HAND = ("https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/",
                "https://android.googlesource.com/", "https://cs.android.com/",
                "https://developer.android.com/reference/", "https://developer.android.google.cn/reference/",
                "https://github.com/androidx/androidx/", "https://github.com/material-components/material-components-android/",
                "https://maven.google.com/", "https://dl.google.com/android/maven2/", "https://repo1.maven.org/maven2/")
D_DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
D_API_RX = re.compile(r"API(?:\s*version)?\s*(\d{1,2})(?!\d)", re.I)
D_BEYOND = re.compile("超出本机|本机 SDK|本机SDK|SDK 里没有|SDK 中没有|声明里没有|本机声明没有|本机没有")
D_CARD_BAD = re.compile("改为|改成|后一致|不再|修好|返修")
D_TAIL_BAD = re.compile("改成.{0,12}后|后一致|修好|撤回|还原|不靠|适合|：用于|仍要|再作|后再")
D_DEVICE = re.compile(r"设备|上机|截图|核对|登记|实测")
D_QUALIFIER = re.compile("另设|没设|未设|没写|未写|不设|不写|未调用|没有改|没改|缺省|未声明|没声明|不传|省略|未覆写|没有覆写")


def is_dated(d):
    """The 2026-11-21 format: no "lesson" key, and sdk records the check date or the docs master commit."""
    sdk = d.get("sdk")
    return "lesson" not in d and isinstance(sdk, dict) and any(k in sdk for k in D_SDK_KEYS)


def d_published(text, before, after):
    """Same as render.py published(): the after is in the text and the before nowhere outside it."""
    if after not in text:
        return False
    if before not in text:
        return not list(loose(before).finditer(text))
    return before in after and text.count(before) == text.count(after) * after.count(before)


def d_parts_ok(s):
    return all(D_PART_RX.match(p.strip()) for p in s.split(" / "))


def check_dated(stem, d, lib, app_rx_list, status):
    """-> (errors, listed, info) for a 2026-11-21 format file."""
    err, leg = [], []
    for k in D_TOP:
        if k not in d:
            err.append(f"缺顶层键 {k}")
    for k in ("unverified", "doubts"):
        if k in d:
            err.append(f"还留着 {k}（统一时要清掉：转成条目、写进正文、记 device_todo 或删掉）")
    extra = set(d) - set(D_TOP) - {"note", "unverified", "doubts"}
    if extra:
        leg.append(f"有不认识的顶层键 {sorted(extra)}")
    if d.get("id") != stem:
        err.append(f"id 和文件名不一致：{d.get('id')}")
    retired = stem not in lib and status.get(stem) == "retired"
    if retired:
        leg.append("store 里已退役：memory/ 里没有，改句不核")
    elif stem not in lib:
        err.append("memory/ 里没有这条经验")
    sdk = d.get("sdk")
    if not isinstance(sdk, dict) or not nonempty(sdk.get("harmony")) or not nonempty(sdk.get("android")):
        err.append("sdk 要有 harmony、android 两个非空字符串（没用到就写「不涉及」「未用」）")
        sdk = sdk if isinstance(sdk, dict) else {}
    for k in ("verified_on", "docs_date"):
        if not (isinstance(sdk.get(k), str) and D_DATE_RX.match(sdk[k])):
            err.append(f"新格式的 sdk.{k} 要写 YYYY-MM-DD")
    if not (isinstance(sdk.get("docs_commit"), str) and re.fullmatch(r"[0-9a-f]{7,40}", sdk["docs_commit"])):
        err.append("新格式的 sdk.docs_commit 要写文档仓库 master 的提交号")
    if sdk.get("harmony") not in ("未用",) and not D_API_RX.search(sdk.get("harmony") or ""):
        err.append("新格式的 sdk.harmony 要写明本机鸿蒙 SDK 是 API 几")
    m_api = D_API_RX.search(sdk.get("harmony") or "")
    local_api = int(m_api.group(1)) if m_api else None
    if not isinstance(d.get("dropped_notes"), int) or d.get("dropped_notes", 0) < 0:
        err.append("dropped_notes 要是非负整数")
    dt = d.get("device_todo")
    if not isinstance(dt, list) or not all(nonempty(x) for x in dt):
        err.append("device_todo 要是字符串列表")
    ents = d.get("entries")
    if not isinstance(ents, list):
        err.append("entries 不是列表")
        ents = []
    if not ents and not nonempty(d.get("note")):
        err.append("没有条目时 note 要写明为什么（例：流程类经验，做法不依赖平台事实）")
    texts = []
    for k, e in enumerate(ents, 1):
        w = f"第 {k} 条"
        if not isinstance(e, dict):
            err.append(f"{w}：不是对象")
            continue
        for key in ("step", "fact", "source", "kind", "origin"):
            if not nonempty(e.get(key)):
                err.append(f"{w}：缺 {key}")
        if e.get("kind") not in D_KINDS:
            err.append(f"{w}：kind 不是 {'/'.join(D_KINDS)}：{e.get('kind')}")
        if e.get("origin") not in D_ORIGINS:
            err.append(f"{w}：origin 不是 {'/'.join(D_ORIGINS)}：{e.get('origin')}")
        if nonempty(e.get("step")) and not d_parts_ok(e["step"]):
            err.append(f"{w}：step 不是正文的部分名：{e['step']}")
        fact = e.get("fact") or ""
        if e.get("kind") == "卡里验证" and D_CARD_BAD.search(fact):
            err.append(f"{w}：卡里验证的条目写了返修怎么改的（「{D_CARD_BAD.search(fact).group(0)}」）：{fact[:60]}")
        if D_TAIL_BAD.search(fact):
            err.append(f"{w}：fact 带了返修经过或做法建议的尾巴（「{D_TAIL_BAD.search(fact).group(0)}」）：{fact[:60]}")
        if "默认" in fact and e.get("kind") in ("安卓平台", "依赖库") and not D_QUALIFIER.search(fact):
            leg.append(f"{w}：默认值没写「应用没有另设时」一类的限定（看是不是应用可另设的值）：{fact[:70]}")
        if local_api and e.get("kind") == "鸿蒙接口":
            hi = [int(x) for x in D_API_RX.findall(fact) if int(x) > local_api]
            if hi and not D_BEYOND.search(fact):
                leg.append(f"{w}：提到 API {max(hi)}，高于本机 SDK 的 API {local_api}，没注明超出本机 SDK：{fact[:70]}")
        for part in re.split(r"[；;]", e.get("source") or ""):
            if D_OLD_DOC_RX.search(part) and not D_DOC_LINK_RX.search(part):
                err.append(f"{w}：新格式文件的文档出处要写成链接：{part.strip()[:80]}")
        texts += [(w + " fact", fact, True), (w + " source", e.get("source") or "", False)]
    chs = d.get("changes")
    if not isinstance(chs, list):
        err.append("changes 不是列表")
        chs = []
    for k, c in enumerate(chs, 1):
        w = f"改句第 {k} 处"
        if not isinstance(c, dict):
            err.append(f"{w}：不是对象")
            continue
        for key in CHANGE_KEYS:
            if not nonempty(c.get(key)):
                err.append(f"{w}：缺 {key}")
        if c.get("type") not in D_TYPES:
            err.append(f"{w}：type 不是 {'/'.join(D_TYPES)}：{c.get('type')}")
        if nonempty(c.get("where")) and not d_parts_ok(c["where"]):
            err.append(f"{w}：where 不是正文的部分名：{c['where']}")
        if D_DEVICE.search(c.get("after") or ""):
            leg.append(f"{w}：新句提到「{D_DEVICE.search(c['after']).group(0)}」：{c['after'][:100]}")
        texts += [(w + " after", c.get("after") or "", True), (w + " basis", c.get("basis") or "", False)]
    texts += [("note", d.get("note") or "", True)] + [("device_todo", x, False) for x in dt or [] if isinstance(x, str)]
    for where, t, names in texts:
        for url in D_URL_RX.findall(t):
            if names:
                err.append(f"{where}：这一栏不放链接（链接只写在 source、basis 里）：{url[:80]}")
            elif D_DOC_LINK_RX.match(url) and url.startswith("https://raw."):
                err.append(f"{where}：文档出处写 blob 链接，不写 raw 链接：{url[:80]}")
            elif not url.startswith(D_FIRST_HAND):
                err.append(f"{where}：不是一手来源的网址（只认 OpenHarmony 文档仓库 master、AOSP、安卓官方参考文档、依赖库官方仓库和源码包）：{url[:80]}")
        for lab, rx in MACHINE_RX:
            if rx.search(t):
                err.append(f"{where}：有本机路径（{lab}）")
        if D_LINE_RX.search(t):
            err.append(f"{where}：有行号写法「{D_LINE_RX.search(t).group(0)}」")
        if names:
            hits = [n for n, rx in app_rx_list if rx.search(t)]
            if hits:
                err.append(f"{where}：有被迁移应用的名字：{'、'.join(hits)}")
    if stem in lib:
        raw = lib[stem].read_text(encoding="utf-8")
        seq = lib_text(lib[stem])                     # the text with the changes not published yet put on in order
        pairs = [((c.get("before") or "").strip(), (c.get("after") or "").strip()) if isinstance(c, dict) else ("", "") for c in chs]
        for k, (b, a) in enumerate(pairs, 1):
            if not b or not a:
                continue
            w = f"改句第 {k} 处〔{chs[k - 1].get('where')}〕"
            if d_published(seq, b, a):                # published: the after is there, the before nowhere outside it
                continue
            if a in seq and b in seq and a not in b:  # both there: published or not cannot be told
                err.append(f"{w}after 已在正文里，before 在 after 之外却还出现：{b[:50]}…")
                continue
            if seq.count(b) == 1:
                seq = seq.replace(b, a)
            else:
                m = list(loose(b).finditer(seq))
                if len(m) != 1:
                    err.append(f"{w}after 不在正文里，before 在（套过前面改句的）正文里对上 {len(m)} 处，套不上：{b[:50]}…")
                    continue
                seq = seq[:m[0].start()] + a + seq[m[0].end():]
            leg.append(f"{w}还没发布进正文（before 唯一可定位）")
            if raw.count(b) != 1:
                leg.append(f"{w}原句在经验文件里出现 {raw.count(b)} 次（按空白可有可无或落在前一处新句里才套上）：{b[:50]}…")
    return err, leg, {"entries": len(ents), "changes": len(chs), "old_format": False, "dated": True}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="the knowledge dir (lesson-<id>.json files), e.g. knowledge/lessons")
    ap.add_argument("--only", default="", help="comma-separated 8-character id prefixes")
    ap.add_argument("--legacy-ok", action="store_true", help="old-format files: list their old-format items, not as errors")
    ap.add_argument("--app-name", action="append", default=[], help="one more app name to keep out of fact / scope (repeatable)")
    a = ap.parse_args()
    d = Path(a.dir)
    if not d.is_dir():
        print(f"不是目录：{d}")
        return 2
    app_rx_list = [(n, app_rx(n)) for n in APP_NAMES + [x.strip() for x in a.app_name if x.strip()]]
    only = [x.strip().replace("lesson-", "")[:8] for x in a.only.split(",") if x.strip()]
    files = sorted(f for f in d.glob("lesson-*.json"))
    if only:
        files = [f for f in files if f.stem[7:15] in only]
    lib = {p.name[:-len(".lesson.md")]: p for p in LIB.rglob("lesson-*.lesson.md")}
    status = store_status()
    n_err, n_leg, n_old, n_dated = 0, 0, 0, 0
    print(f"目录 {d}；{len(files)} 个文件" + (f"（--only {','.join(only)}）" if only else "") + ("；--legacy-ok" if a.legacy_ok else "")
          + f"；应用名 {len(app_rx_list)} 个")
    for x in only:
        if not any(f.stem[7:15] == x for f in files):
            print(f"  {x}｜错误｜目录里没有这条经验的文件")
            n_err += 1
    for f in files:
        err, leg, info = check_file(f, lib, a.legacy_ok, app_rx_list, status)
        n_err += len(err)
        n_leg += len(leg)
        n_old += bool(info.get("old_format"))
        n_dated += bool(info.get("dated"))
        status_word = "有错" if err else ("只列出" if leg else "通过")
        print(f"{f.stem[7:15]}｜{status_word}｜条目 {info.get('entries', '?')}、改句 {info.get('changes', '?')}")
        for x in err:
            print(f"    错误：{x}")
        for x in leg:
            print(f"    列出：{x}")
    print(f"\n合计：{len(files)} 个文件，错误 {n_err} 处，只列出 {n_leg} 处（旧格式文件 {n_old} 个"
          + (f"，2026-11-21 起的新格式文件 {n_dated} 个" if n_dated else "") + "）。" +("通过" if not n_err else "不通过"))
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
