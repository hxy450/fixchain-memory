# -*- coding: utf-8 -*-
"""给一条经验收候选事实（不调模型，只读）。

四种来源。平常用 --from-case-files（直接从来源卡收）；另外三种读现成的候选表或重现旧候选表，留着兼容。

  --from-case-files PATH   直接从来源卡收：PATH 是一张卡的 JSON、放卡的目录（经验库 store 的 cases 目录、
                           一次归并的 run 目录等，递归找 migloop-case/* 的卡），或者写 links——按经验「## 来源」一节的链接
                           找卡（要 export --link-cards 导出的阅读包，且 store 还在链接指向的位置）。可以给几次。
                           收法见下面「直接从卡收」。
  --from-json  FILE   读现成的候选表（JSON：经验号 → {entries, unverified, rules, cards}，可以是 --all --out 写出的）。
  --from-rules DIR    按旧配法现配：DIR 是规矩库里放渲染好的规矩（rule-*.md，含「已核实的写法和取值」「来源：」两节）的目录。
  --from-cards DIR    按旧配法配卡一层的候选规矩：DIR 里是从卡写出的候选规矩文件（case-*.json）。

旧配法（--from-rules、--from-cards）：
  - 经验「## 来源」一节里每张卡记着「结论：diagnosis, recommendation:N …」；
  - 规矩的出处里每张卡记着它的做法、例外、取值引了这张卡的哪些结论（诊断 / 建议 N）；
  - 同一张卡、建议编号有交集的规矩配上；经验在这张卡上只引了诊断、没引建议时，才按诊断配。
  - 配上的规矩，「已核实的写法和取值」一节的每一行（含其后「针对本应用要查的：」下的各行）按出现顺序去重收进 entries；
    「未核实：」整行收进 unverified。规矩既没有取值也没有未核实时跳过。
  --from-rules、--from-cards 可以一起给（老卡的规矩在前、新卡的在后）。

直接从卡收（--from-case-files）：按经验「## 来源」引的「卡 + 结论 + 卡片版本」，只收这张卡上被引的那几条结论：
  - recommendation:N → 卡的 recommendations 第 N 条，按句切开，留下带平台标识符（接口名、带点的名字、@装饰器、常量、错误码、
    带单位的数）或平台行为词（渲染、回调、默认、缺省、抛、报错……）的句子；纯流程的句子（复核、截图、登记……）不收。
  - diagnosis → 卡的 summary，按句切开（卡里的硬换行不算句子边界），只留下讲上机或编译现象、修法用到的接口、声明或文档写明
    的行为的句子，而且要带平台标识符；讲生成过程里谁读了什么、写了什么的句子（Read、回执、生成者、派工……）不收，
    除非句子里有设备、日志、报错这类硬现象。整句（到句号为止，分号后的半句也算）里有引历史会话里模型思考的字样
    （思考、推理、以为、断言、假设……）的整句不收：候选只收平台事实，不摘抄、不转述当时模型怎么想。
  - 卡的 unknown（没核到的点）按句收进 unverified（同样跳过带思考字样的句子）；卡上有任何一条结论被引就收。
  - 卡的 metadata.environment 里的版本（鸿蒙 SDK、安卓 compileSdk、工具链）汇成一行「卡里记的环境」，不是候选。
  - 不收：调查图（graphs）的节点说明——那是谁读了什么、在哪里写错，不能当平台事实的出处；卡的 title、when、description。
  - 每行去掉转录行号（L123、agent-….jsonl:L…、repair L…、检查点 T…）、本机路径（换成文件名）和「文件:行号」。
  - 每行前面标出处：〔case-前 8 位·字段·类〕，字段是 建议N / 诊断 / 未核到N，类是 现象（上机、编译、日志）/ 修法 / 接口（声明、
    文档、默认、版本）。完全相同的行只留第一次出现的。判断「平台标识符」时去掉卡里调查图点名的应用文件名、包名和项目名；
    应用自己的变量名、类名脚本认不全，行里会留着，写知识时不带进去。
  卡上有的平台事实写在没有标识符的句子里、或和思考记录写在同一句里，脚本收不到，要写知识的人读卡另列（rules.md C6）。

经验从哪来：--memory DIR（经验库的 memory 目录，按 <经验号>.lesson.md 递归找）或 --lesson-file PATH（单个文件）。
--from-json 只要经验号。

--base-memory DIR（只配 --from-case-files）：归并前的阅读包。对照它列出这条经验改动了正文哪几部分、这次新引了哪几张卡，
  出自新卡的候选行多标「新卡」。--new-cards-only：只收这次新引的卡（加了句子、只补来源的经验用）。

输出：默认按编号打印（编号就是工作稿里「用到的候选」要记的下标）；--json 打印 JSON；--summary 每条经验一行计数。
--all --out FILE：对 --memory 下全部经验配一遍，写成 --from-json 读的那种结构（只写 --out 指定的文件）。
--compare FILE：把现配的结果和一份现成的候选表逐条经验比，报告逐字一致的条数（自检用）。

用法（Python 3.10+，只用标准库）：
  py -3.12 -B -X utf8 candidates.py --from-case-files links --memory <memory 目录> lesson-<id> [lesson-<id> …]
  py -3.12 -B -X utf8 candidates.py --from-case-files <store>/cases --memory <memory 目录> lesson-<id>
  py -3.12 -B -X utf8 candidates.py --from-case-files links --memory <memory> --base-memory <归并前的阅读包> --new-cards-only lesson-<id>
  py -3.12 -B -X utf8 candidates.py --from-json <候选表.json> lesson-<id> [lesson-<id> …]
  py -3.12 -B -X utf8 candidates.py --from-rules <rules 目录> --memory <memory 目录> lesson-<id>
  py -3.12 -B -X utf8 candidates.py --from-rules <rules 目录> --memory <memory 目录> --all --compare <候选表.json>
"""
import sys

sys.dont_write_bytecode = True
import argparse, collections, glob, io, json, os, re, urllib.parse  # noqa: E401,E402

CASE_RX = re.compile(r"(case-[0-9a-f]{20})")


# ---------------------------------------------------------------- 经验一侧
def lesson_wants(text):
    """经验「## 来源」一节：{卡号: {"d", "r1", …}}（旧配法用）。"""
    srcsec = text.split("## 来源")[1] if "## 来源" in text else ""
    want = {}
    for line in srcsec.splitlines():
        m = CASE_RX.search(line)
        if not m:
            continue
        concl = set()
        cm = re.search(r"结论[:：]\s*(.*)$", line)
        if cm:
            for tok in re.split(r"[,，、]\s*", cm.group(1)):
                tok = tok.strip(" `·")
                if tok.startswith("diagnosis"):
                    concl.add("d")
                else:
                    n = re.search(r"recommendation[:：]?\s*(\d+)", tok)
                    if n:
                        concl.add("r" + n.group(1))
        want[m.group(1)] = concl
    return want


def lesson_files(memory):
    out = {}
    for p in glob.glob(os.path.join(memory, "**", "lesson-*.lesson.md"), recursive=True):
        out[os.path.basename(p).split(".")[0]] = p
    return out


# ---------------------------------------------------------------- 规矩一侧
def rules_from_md(rules_dir):
    """渲染好的规矩（rule-*.md）→ {规矩号: {"src": {卡号: 结论集合}, "ver": [行], "unv": 行}}。"""
    rules = {}
    for p in glob.glob(os.path.join(rules_dir, "**", "rule-*.md"), recursive=True):
        t = io.open(p, encoding="utf-8").read()
        rid = os.path.basename(p)[:-3]
        parts = re.split(r"^来源：", t, flags=re.M)
        if len(parts) < 2:
            continue
        src = {}
        for line in parts[1].splitlines():
            m = CASE_RX.search(line)
            if not m:
                continue
            concl = set()
            for seg in re.findall(r"←\s*([^；;]+)", line):
                for tok in re.split(r"[,，、]\s*", seg.strip()):
                    tok = tok.strip()
                    if tok == "诊断":
                        concl.add("d")
                    else:
                        n = re.search(r"建议\s*(\d+)", tok)
                        if n:
                            concl.add("r" + n.group(1))
            src[m.group(1)] = concl
        m = re.search(r"^已核实的写法和取值[^\n]*\n(.*?)(?=^未核实|^来源：|\Z)", t, re.S | re.M)
        ver = [x.strip() for x in m.group(1).splitlines() if x.strip().startswith("-")] if m else []
        unv = re.search(r"^未核实：(.+)$", t, re.M)
        if not ver and not unv:
            continue
        rules[rid] = {"src": src, "ver": ver, "unv": unv.group(1).strip() if unv else ""}
    return rules


def _s(x):
    return x.strip() if isinstance(x, str) else ""


def _claims(items):
    out = collections.defaultdict(set)
    for x in items or []:
        if not isinstance(x, dict):
            continue
        for s in x.get("support") or []:
            m = re.match(r"^(case-[0-9a-f]{20})#(diagnosis|recommendation:(\d+))$", s or "")
            if m:
                out[m.group(1)].add("d" if m.group(2) == "diagnosis" else "r" + m.group(3))
    return out


def rules_from_cards(cards_dir):
    """卡一层的候选规矩（case-*.json，每个文件一张卡的候选规矩）→ 同上结构。规矩号写成「<卡号>#<序号>」。
    行的写法照规矩库的渲染脚本：取值「- value：meaning（出处：source）」，要查的「- what：where；how」；
    取值为空时整条规矩不出「已核实的写法和取值」一节，它的要查的行也就不会被收（和从 rule-*.md 收时一致）。"""
    rules = {}
    for p in sorted(glob.glob(os.path.join(cards_dir, "case-*.json"))):
        d = json.load(io.open(p, encoding="utf-8"))
        case = d.get("case") or os.path.basename(p)[:-5]
        for k, r in enumerate(d.get("rules") or [], 1):
            src = collections.defaultdict(set)
            for part in ("how", "exceptions", "values"):
                for c, s in _claims(r.get(part)).items():
                    src[c] |= s
            vals = [f"- {_s(v['value'])}" + (f"：{_s(v.get('meaning'))}" if _s(v.get("meaning")) else "")
                    + (f"（出处：{_s(v.get('source'))}）" if _s(v.get("source")) else "")
                    for v in r.get("values") or [] if isinstance(v, dict) and _s(v.get("value"))]
            lk = [f"- {_s(x['what'])}" + (f"：{_s(x.get('where'))}" if _s(x.get("where")) else "")
                  + (f"；{_s(x.get('how'))}" if _s(x.get("how")) else "")
                  for x in r.get("lookups") or [] if isinstance(x, dict) and _s(x.get("what"))]
            ver = vals + lk if vals else []
            unv = "；".join(_s(x) for x in r.get("unverified") or [] if _s(x))
            if not ver and not unv:
                continue
            rules[f"{case}#{k}"] = {"src": dict(src), "ver": ver, "unv": unv}
    return rules


# ---------------------------------------------------------------- 配
def match(want, rules):
    by_card = collections.defaultdict(list)
    for rid in rules:                  # 按读入顺序（rule-*.md 是 glob 的顺序）；顺序决定候选的编号
        for c in rules[rid]["src"]:
            by_card[c].append(rid)
    entries, unvs, used = [], [], []
    for c, concl in want.items():
        recs = {x for x in concl if x != "d"}
        for rid in by_card.get(c, ()):
            rc = rules[rid]["src"].get(c, set())
            rrecs = {x for x in rc if x != "d"}
            ok = bool(recs & rrecs) if recs else ("d" in rc and not rrecs or "d" in rc and "d" in concl)
            if not ok:
                continue
            used.append(rid)
            for e in rules[rid]["ver"]:
                if e not in entries:
                    entries.append(e)
            if rules[rid]["unv"] and rules[rid]["unv"] not in unvs:
                unvs.append(rules[rid]["unv"])
    return {"entries": entries, "unverified": unvs, "rules": sorted(set(used)), "cards": len(want)}


# ---------------------------------------------------------------- 直接从卡收（--from-case-files）
SRC_LINE = re.compile(r"^- (?:\[(case-[0-9a-f]{20})\]\(([^)]+)\)|`?(case-[0-9a-f]{20})`?) · 结论[:：]\s*(.*)$")
REV_LINE = re.compile(r"^\s+卡片版本[:：]\s*`?([0-9a-f]{64})`?")


def lesson_sources(path):
    """经验「## 来源」一节 → [(卡号, [结论…], 卡片版本或 None, 链接指向的本机文件或 None)]，按出现顺序。
    行的写法是作者导出脚本（publication.py 的 _lesson_text）写的：「- [卡号](相对链接) · 结论：a, b」下一行「  卡片版本：`…`」；
    不带 --link-cards 导出的部署包没有这一节。"""
    text = io.open(path, encoding="utf-8").read()
    if "## 来源" not in text:
        return []
    out = []
    for line in text.split("## 来源", 1)[1].splitlines():
        m = SRC_LINE.match(line)
        if m:
            link = m.group(2)
            target = os.path.normpath(os.path.join(os.path.dirname(path), urllib.parse.unquote(link))) if link else None
            claims = [c.strip(" `") for c in re.split(r"[,，、]\s*", m.group(4)) if c.strip(" `")]
            out.append([m.group(1) or m.group(3), claims, None, target])
            continue
        m = REV_LINE.match(line)
        if m and out and out[-1][2] is None:
            out[-1][2] = m.group(1)
    return [tuple(x) for x in out]


class CardIndex:
    """按「卡号 + 卡片版本」找卡文件。先看 links，再看 <目录>/<卡号>/<版本>.json（store 的 cases 目录的排法），
    最后递归扫目录里的 JSON（只认 schema 是 migloop-case/* 的）。"""

    def __init__(self, paths):
        self.links, self.dirs, self.by = False, [], {}
        self.scanned = False
        for p in paths:
            if p == "links":
                self.links = True
            elif os.path.isdir(p):
                self.dirs.append(p)
            elif os.path.isfile(p):
                self._add(p)
            else:
                print(f"--from-case-files：{p} 不存在", file=sys.stderr)

    def _add(self, p):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except (OSError, ValueError):
            return
        if isinstance(d, dict) and str(d.get("schema", "")).startswith("migloop-case/") and d.get("id"):
            self.by.setdefault((d["id"], d.get("revision")), p)
            self.by.setdefault((d["id"], None), p)

    def find(self, case, rev, link):
        """→ (文件, 版本对得上与否)；找不到 → (None, False)。"""
        if self.links and link and os.path.isfile(link):
            return link, True
        for d in self.dirs:
            for c in (os.path.join(d, case, f"{rev}.json"), os.path.join(d, "cases", case, f"{rev}.json")):
                if rev and os.path.isfile(c):
                    return c, True
        if self.dirs and not self.scanned:
            self.scanned = True
            for d in self.dirs:
                for p in glob.glob(os.path.join(d, "**", "*.json"), recursive=True):
                    b = os.path.basename(p)
                    if b.startswith("case-") or re.fullmatch(r"[0-9a-f]{64}\.json", b):
                        self._add(p)
        if (case, rev) in self.by:
            return self.by[(case, rev)], True
        if (case, None) in self.by:
            return self.by[(case, None)], False
        return None, False


# 句子里的引用：转录文件和行号、检查点、本机路径、文件:行号。都不是事实，去掉。
_REF = re.compile("|".join([
    r"(?:agent-[0-9a-f]{6,}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:\.jsonl)?"
    r"(?::?\s*L\d+(?:-L\d+)?(?:\s*[、,，]\s*L\d+(?:-L\d+)?)*)?",
    r"(?:repair|generation|materials)/[^\s，。；、）)]*?\.jsonl(?::L\d+(?:-L\d+)?)?",
    r"[\w.…-]*\.jsonl(?::?\s*L?\d+(?:-L?\d+)?)?:?",
    r"(?<![0-9A-Za-z-])[0-9a-f]{8}:\s*L\d+(?:-L\d+)?",
    r"(?:repair\s*(?:转录|日志)?|同转录|转录)\s*L\d+(?:-L\d+)?",
    r"(?:检查点|checkpoint)\s*(?:T\d+(?:-\d+)?)?(?:\s*L\d+(?:-L\d+)?)?",
    r"(?<![A-Za-z0-9_])L\d+(?:-L\d+)?(?:\s*[、,，]\s*L\d+(?:-L\d+)?)*",
    r"evidence/[\w./-]+",
]))
_PATH = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s，。；、）)”」'\"]+")   # 盘符路径；「memory://」这类不算
_FILELINE = re.compile(r"(\.(?:ets|java|kt|ts|xml|md|json5?|yaml|gradle))(?::\d+(?:-\d+)?(?:/\d+)*)")
# 历史模型思考的字样：整句不收（「as 断言」「类型断言」是 TS 的写法，先换掉再判）
_THINK_NARROW = re.compile(r"思考|推理|心想|thinking|reasoning", re.I)
_THINK = re.compile(r"思考|推理|推断|推导|以为|认为|断言|假设|自认|自称|心想|意识到|打算|想起|声称|判定|猜|凭记忆|记忆|印象|"
                    r"not 100% sure|thinking|reasoning|docs say|same formula|pattern from", re.I)
_TS_ASSERT = re.compile(r"as\s*断言|类型断言|非空断言")
_OBS = re.compile(r"设备|真机|上机|模拟器|实测|日志|hilog|报错|错误码|编译错误|\d+\s*个错误|异常|抛|崩溃|闪退|白屏|白板|编译|"
                  r"(?<![A-Za-z])(?:[Ee]rror|failed|[Ww]arn\w*)(?![A-Za-z])|does not exist|"
                  r"显示|看到|截图|不生效|无效|失败|拒绝|互换|透明|落盘|回送|吞")
# 讲生成过程里谁读了什么、写了什么的句子（调查经过，不是平台事实）；带硬现象（设备、日志、报错）的才留
_NARR = re.compile(r"Read|Write|回执|读到|读取|写前|写出|写成|写下|写入|派工|生成者|实现者|规格作者|转换者|子代理|主会话|"
                   r"Slice\s*\d|Stage\s*\d|编译门|自查|沿用|照抄|复制|先例")
_HARD = re.compile(r"设备|真机|上机|hilog|日志|报错|错误码|编译错误|\d+\s*个错误|抛|崩溃|闪退|白屏|白板|"
                   r"(?<![A-Za-z])(?:[Ee]rror|failed|code)(?![A-Za-z])|does not exist|不生效|无效")
_FIX = re.compile(r"返修|改为|改成|改用|换成|换用|补上|补全|修复|最终")
_API = re.compile(r"\.d\.ts|声明|文档|@since|@deprecated|@useinstead|deprecated|废弃|缺省|默认|签名|重载|枚举|API\s?\d+|since\s?\d+")
_BEHAVIOR = re.compile(r"渲染|回送|触发|回调|覆盖|异步|同步返回|默认|缺省|生效|返回|抛|报错|拒绝|忽略|透明|字节序|单位|换算|废弃|"
                       r"不接收|不支持|只接受|只描述|不代入|原样")
_PROCESS = re.compile(r"^(?:交付前|写前|写后|写完|动笔前|实现前|提交前)|复核|核对|核实|截图|回执|反馈|登记|上报")
# 针对经验库本身的建议（修订某条经验、召回漏了）：不是平台事实
_META = re.compile(r"lesson-[0-9a-f]{6,}|经验库|召回")
# re.ASCII：\w、\b 只认 ASCII，汉字和英文之间才算词边界（不加时「在onChange」里的 onChange 认不出）
_ID = re.compile(r"@[A-Za-z][\w.]+|[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+|\b[a-z]+[A-Z][\w$]*|\b[A-Z][a-z0-9]+[A-Z][\w$]*|"
                 r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b", re.ASCII)
_CODE = re.compile(r"\b\d{6,8}\b|code\W{0,4}\d{3,}|\b\d+(?:\.\d+)?\s?(?:vp|fp|dp|sp|px|ms)\b", re.ASCII)
_APP_FILE = re.compile(r"\.(?:ets|java|kt|md|xml|json5?|yaml|gradle|png|jpg)$", re.I)
_SKIP_SEG = {"src", "main", "java", "kotlin", "ets", "entry", "app", "res", "pages", "spec", "baseline", "features", "ui",
             "users", "projects", "work", "repair", "rounds"}


def _flat(text):
    """卡里的长字段按约 80 字硬换行；换行不是句子边界，空行才是段落边界。→ 段落列表。"""
    paras = []
    for para in re.split(r"\n\s*\n", text or ""):
        buf = ""
        for line in para.splitlines():
            line = line.strip()
            if not line:
                continue
            if buf and re.match(r"[A-Za-z0-9_)\]}\"'`]", buf[-1]) and re.match(r"[A-Za-z0-9_(\[{\"'`]", line[0]):
                buf += " "
            buf += line
        if buf:
            paras.append(buf)
    return paras


def _split(text, marks):
    """按 marks 切；引号、括号里面的不切。"""
    out, depth, cur = [], 0, ""
    for ch in text:
        cur += ch
        if ch in "“「『（(":
            depth += 1
        elif ch in "”」』）)":
            depth = max(0, depth - 1)
        elif ch in marks and depth == 0:
            out.append(cur)
            cur = ""
    out.append(cur)
    return [s.strip().rstrip(marks).strip() for s in out if s.strip(marks + " \t")]


def _sentences(text, drop=None):
    """先按 。！？ 切成整句；整句里有 drop 的字样（历史模型思考）就整句不要——分号后面的半句也算在这一句里；
    其余整句再按 ；切成分句。"""
    out = []
    for para in _flat(text):
        for sent in _split(para, "。！？"):
            if drop is not None and drop.search(_TS_ASSERT.sub("", sent)):
                continue
            out.extend(_split(sent, "；;"))
    return out


def _clean(s):
    s = _PATH.sub(lambda m: re.split(r"[\\/]", m.group(0).rstrip("\\/"))[-1], s)
    s = _FILELINE.sub(r"\1", s)
    s = _REF.sub("", s)
    for _ in range(3):
        # 引用拿掉后空下的括号；代码里的「()」不动
        s = re.sub(r"（[\s、,，;；:：]*）|\(\s*[、,，;；:：][\s、,，;；:：]*\)|\(\s+\)", "", s)
        s = re.sub(r"（[\s、,，;；]+", "（", s)
        s = re.sub(r"[\s、,，;；]+）", "）", s)
        s = re.sub(r"([、,，])\s*[、,，]+", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip(" ，,、；;：:")


def _app_tokens(card):
    """卡里点名的应用自己的名字（调查图里目标和节点的文件名、Java 包名、项目名），小写。"""
    toks = set()
    proj = ((card.get("metadata") or {}).get("migration") or {}).get("project")
    if isinstance(proj, str) and proj.strip():
        toks.add(proj.strip().lower())
    for g in card.get("graphs") or []:
        keys = [(g.get("target") or {}).get("key")] + [n.get("key") for n in g.get("nodes") or [] if isinstance(n, dict)]
        for k in keys:
            if not isinstance(k, str):
                continue
            segs = [x for x in re.split(r"[\\/]", k) if x]
            if not segs or ":" in segs[-1] or segs[-1].startswith("agent-"):
                continue
            stem = segs[-1].split(".")[0]
            if len(stem) >= 4:
                toks.add(stem.lower())
            if "java" in segs or "kotlin" in segs:
                i = max(j for j, x in enumerate(segs) if x in ("java", "kotlin"))
                pkg = [x for x in segs[i + 1:-1] if x.lower() not in _SKIP_SEG]
                if pkg:
                    toks.add(".".join(pkg).lower())
                    toks.update(x.lower() for x in pkg if len(x) >= 5)
    return toks


def _is_app(ident, toks):
    low = ident.lower().lstrip("@")
    if _APP_FILE.search(low) and not low.endswith(".d.ts"):
        return True
    first = low.split(".")[0]
    return first in toks or any(len(t) >= 6 and t in low for t in toks)


def platform_ids(s, toks):
    ids = [i for i in _ID.findall(s) if len(i) >= 4 and not _is_app(i, toks)]
    return ids + _CODE.findall(s)


def _kind(s):
    if _OBS.search(s):
        return "现象"
    if _API.search(s):
        return "接口"
    return "修法"


def harvest_card(card, claims):
    """一张卡上被引的结论 → (候选 [(字段, 类, 句)], 未核实 [(字段, 句)], 环境 {名: {值}}, 应用名集合)。"""
    toks = _app_tokens(card)
    rows, unv = [], []
    recs = card.get("recommendations") or []
    for c in claims:
        m = re.fullmatch(r"recommendation:(\d+)", c)
        if not m:
            continue
        n = int(m.group(1))
        if not 1 <= n <= len(recs) or not isinstance(recs[n - 1], str):
            continue
        if _META.search(recs[n - 1]):
            continue
        for s in _sentences(recs[n - 1], _THINK_NARROW):
            s = _clean(s)
            if not s:
                continue
            has_id = bool(platform_ids(s, toks))
            if has_id or (_BEHAVIOR.search(s) and not _PROCESS.search(s)):
                rows.append((f"建议{n}", "接口" if _API.search(s) else "修法", s))
    if "diagnosis" in claims and isinstance(card.get("summary"), str):
        for s in _sentences(card["summary"], _THINK):
            s = _clean(s)
            if not s or (_NARR.search(s) and not _HARD.search(s)):
                continue
            if (_OBS.search(s) or _FIX.search(s) or _API.search(s)) and platform_ids(s, toks):
                rows.append(("诊断", _kind(s), s))
    for k, u in enumerate(card.get("unknown") or [], 1):
        if not isinstance(u, str):
            continue
        for s in _sentences(u, _THINK):
            s = _clean(s)
            if s and (platform_ids(s, toks) or _API.search(s) or _OBS.search(s)):
                unv.append((f"未核到{k}", s))
    env = collections.defaultdict(set)
    for e in (card.get("metadata") or {}).get("environment") or []:
        if isinstance(e, dict) and isinstance(e.get("name"), str) and isinstance(e.get("value"), str):
            env[e["name"]].add(e["value"])
    return rows, unv, env, toks


LESSON_PART = re.compile(r"^## (何时使用|适用情境|例外与边界|原因|做法|可选检查)\s*$")


def lesson_parts(path):
    """经验正文 → {部分名: 文本}；做法按步拆成「做法第 N 步」。部分名和知识文件的 step 写法一致。"""
    parts, cur = {}, None
    for line in io.open(path, encoding="utf-8").read().split("## 来源", 1)[0].splitlines():
        if line.startswith("# ") and "标题" not in parts:
            parts["标题"] = line[2:].strip()
            continue
        m = LESSON_PART.match(line)
        if m:
            cur = m.group(1)
            continue
        if line.startswith("## ") or line.startswith("来源支持："):
            cur = None
            continue
        if cur is None or not line.strip():
            continue
        if cur == "做法":
            n = re.match(r"^(\d+)\.\s+(.*)$", line)
            if n:
                parts[f"做法第 {n.group(1)} 步"] = n.group(2).strip()
            continue
        parts[cur] = (parts.get(cur, "") + "\n" + line.strip()).strip()
    return parts


def from_case_files(lesson_path, index, base_path=None, new_only=False, has_base=False):
    """has_base：给了 --base-memory。这时 base_path 为 None 说明归并前没有这条经验（新增），它的卡全算新卡。"""
    srcs = lesson_sources(lesson_path)
    base_cards = {s[0] for s in lesson_sources(base_path)} if base_path else set()
    changed = ["整条（新增）"] if has_base and not base_path else []
    if base_path:
        a, b = lesson_parts(base_path), lesson_parts(lesson_path)
        for k in b:
            if k not in a:
                changed.append(k + "（新）")
            elif " ".join(a[k].split()) != " ".join(b[k].split()):
                changed.append(k)
        changed += [k + "（删）" for k in a if k not in b]
    new_cards = [s[0] for s in srcs if has_base and s[0] not in base_cards]
    entries, origins, unvs, seen = [], [], [], set()
    env = collections.defaultdict(set)
    missing, mismatch, found = [], [], 0
    for case, claims, rev, link in srcs:
        if new_only and case not in new_cards:
            continue
        path, exact = index.find(case, rev, link)
        if not path:
            missing.append(case)
            continue
        found += 1
        if not exact:
            mismatch.append(case)
        card = json.load(io.open(path, encoding="utf-8"))
        rows, unv, cenv, toks = harvest_card(card, claims)
        new_tag = "·新卡" if case in new_cards else ""
        for field, kind, s in rows:
            if s in seen:
                continue
            seen.add(s)
            entries.append(f"〔{case[:13]}·{field}·{kind}{new_tag}〕{s}")
            origins.append({"case": case, "field": field, "kind": kind, "new_card": bool(new_tag)})
        for field, s in unv:
            if s in seen:
                continue
            seen.add(s)
            unvs.append(f"〔{case[:13]}·{field}{new_tag}〕{s}")
        for k, v in cenv.items():
            env[k] |= v
    return {"entries": entries, "origins": origins, "unverified": unvs,
            "cards": len([s for s in srcs if not new_only or s[0] in new_cards]), "cards_found": found,
            "cards_missing": missing, "cards_other_revision": mismatch,
            "env": {k: sorted(v) for k, v in sorted(env.items())},
            "changed_parts": changed, "new_cards": new_cards}


def show(lid, v):
    print("=====", lid)
    if v is None:
        print("（没有这条经验的候选）")
        return
    if "cards_found" in v:
        print(f"来源卡 {v['cards']} 张（找到 {v['cards_found']} 张"
              + (f"，版本对不上 {len(v['cards_other_revision'])} 张：{', '.join(v['cards_other_revision'])}" if v["cards_other_revision"] else "")
              + (f"，没找到：{', '.join(v['cards_missing'])}" if v["cards_missing"] else "")
              + f"）；候选 {len(v['entries'])} 行；未核实 {len(v['unverified'])} 行")
        if v["env"]:
            print("卡里记的环境：" + "；".join(f"{k}={'/'.join(x)}" for k, x in v["env"].items()))
        if v["changed_parts"] or v["new_cards"]:
            print("对照归并前：改动的部分 " + ("、".join(v["changed_parts"]) or "无")
                  + "；新引的卡 " + (", ".join(v["new_cards"]) or "无"))
    else:
        print(f"来源卡 {v.get('cards')} 张；配上的规矩 {len(v.get('rules') or [])} 条；候选 {len(v.get('entries') or [])} 行；未核实 {len(v.get('unverified') or [])} 行")
    for i, e in enumerate(v.get("entries") or []):
        print(f"{i}\t{e}")
    for u in v.get("unverified") or []:
        print(f"未核实\t{u}")


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-case-files", action="append", default=[])
    ap.add_argument("--from-json")
    ap.add_argument("--from-rules")
    ap.add_argument("--from-cards")
    ap.add_argument("--memory")
    ap.add_argument("--lesson-file")
    ap.add_argument("--base-memory")
    ap.add_argument("--new-cards-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--compare")
    ap.add_argument("ids", nargs="*")
    a = ap.parse_args(argv)
    modes = [bool(a.from_case_files), bool(a.from_json), bool(a.from_rules or a.from_cards)]
    if sum(modes) != 1:
        ap.error("--from-case-files、--from-json 各自单独用；或者给 --from-rules、--from-cards 之一或两个")
    if (a.base_memory or a.new_cards_only) and not a.from_case_files:
        ap.error("--base-memory、--new-cards-only 只配 --from-case-files")
    if a.new_cards_only and not a.base_memory:
        ap.error("--new-cards-only 要和 --base-memory 一起给")

    if a.from_json:
        table = json.load(io.open(a.from_json, encoding="utf-8"))
        res = {i: table.get(i) for i in a.ids}
    else:
        files = {}
        if a.lesson_file:
            files[os.path.basename(a.lesson_file).split(".")[0]] = a.lesson_file
        if a.memory:
            allf = lesson_files(a.memory)
            if a.all:
                files.update(allf)
            for i in a.ids:
                if i in allf:
                    files[i] = allf[i]
                else:
                    print(f"{i}：memory 里没有这条经验", file=sys.stderr)
        if not files:
            ap.error("要给 --memory 加经验号（或 --all），或 --lesson-file")
        if a.from_case_files:
            index = CardIndex(a.from_case_files)
            basef = lesson_files(a.base_memory) if a.base_memory else {}
            res = {lid: from_case_files(p, index, basef.get(lid), a.new_cards_only, bool(a.base_memory))
                   for lid, p in sorted(files.items())}
        else:
            rules = {}
            if a.from_rules:
                rules.update(rules_from_md(a.from_rules))
            if a.from_cards:
                rules.update(rules_from_cards(a.from_cards))   # 规矩号是「卡号#序号」，和 rule-* 不会重名
            res = {lid: match(lesson_wants(io.open(p, encoding="utf-8").read()), rules) for lid, p in sorted(files.items())}

    if a.compare:
        ref = json.load(io.open(a.compare, encoding="utf-8"))
        same = diff = 0
        bad = []
        for lid, v in res.items():
            r = ref.get(lid)
            if r is not None and r.get("entries") == v["entries"] and r.get("unverified") == v["unverified"]:
                same += 1
            else:
                diff += 1
                bad.append(lid)
        only_ref = [x for x in ref if x not in res]
        print(f"现配 {len(res)} 条经验：和对照表 entries、unverified 逐字一致 {same} 条，不一致 {diff} 条；对照表里有、这次没配的 {len(only_ref)} 条")
        for lid in bad[:20]:
            r = ref.get(lid) or {}
            print(f"  不一致：{lid}（对照 {len(r.get('entries') or [])} 行 / 现配 {len(res[lid]['entries'])} 行）")
        return 0 if not diff else 1
    if a.out:
        io.open(a.out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
        print(f"写了 {len(res)} 条经验的候选：{a.out}")
        return 0
    if a.summary:
        for lid, v in res.items():
            if v is None:
                print(f"{lid}\t没有候选")
                continue
            extra = ""
            if "cards_found" in v:
                nn = sum(1 for o in v["origins"] if o["new_card"])
                extra = (f"\t找到 {v['cards_found']}\t出自新卡 {nn} 行" if a.base_memory else f"\t找到 {v['cards_found']}")
            print(f"{lid}\t来源卡 {v.get('cards')}{extra}\t候选 {len(v.get('entries') or [])}\t未核实 {len(v.get('unverified') or [])}")
        return 0
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for lid, v in res.items():
            show(lid, v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
