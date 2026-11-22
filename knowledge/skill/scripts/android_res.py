# -*- coding: utf-8 -*-
"""查安卓平台资源和依赖库资源，默认「读全」（只读，只用标准库）。

为什么有它：核过的条目有出入的，多半是只看了 values/ 里那一份 style、没看 values-v21 等限定目录里的重定义
和 parent 链上的覆写，或者只看了库的一个版本。这个脚本把「所有 values* 目录、整条 parent 链、最旧和最新两个库版本」
变成默认输出。

用法（py -3.12 -B -X utf8 android_res.py …）：
  style <名字> [--item <属性>]        style / 主题：每个限定目录里的定义、顺着 parent（显式的 parent= 和名字里点号的
                                      隐式父）一路查到底，每层打印 parent 和 <属性> 的原值；小结按 API 级别（和夜间）
                                      解析到字面值
  color|dimen|bool|integer|fraction <名字>   每个限定目录里的定义（res/color*/ 下的颜色状态列表也查），解析到字面值
  attr <名字> [--theme <主题>]…       attr 的声明（format、enum），和它在主题里的取值（不给 --theme 用常见的亮、暗两个主题）
选项：
  --api N [N …]       平台资源用哪几个 API 级别并排比（默认本机装的最新一个，会提示还有哪些）
  --lib 组:库 [--lib …]   查依赖库（Gradle 缓存 modules-2 里的 aar）；默认对缓存里最旧、最新两个正式版各查一遍
  --version V [V …]   指定库版本：写 V 给第一个 --lib，写 组:库=V 给那个库（可给几个）；
                      给了 --version 时，没指定版本的库只取最新的正式版
  --theme 主题        解析 ?attr 用哪个主题（style 查的是主题时默认用它自己；查控件 style 时要给）
  --sdk 目录          Android SDK 目录；不给时取环境变量 ANDROID_SDK_ROOT，再取 ANDROID_HOME，都没有就报错
  --gradle 目录       Gradle 的 caches 目录；不给时取环境变量 GRADLE_USER_HOME 下的 caches，再取 Gradle 自己的
                      默认位置（用户主目录下 .gradle/caches）
  --phone 规格        「常见手机」参考配置，默认 sw=360-412,h=660-915,dpi=xxhdpi（h 是竖屏时的可用高 screenHeightDp、
                      即长边：targetSdk 35 以下不含状态栏和导航栏，物理高 760–915dp 的手机约 660–870dp；targetSdk 35
                      起含系统栏。竖屏时宽=sw、高=h，横屏时宽=h、高=sw）；同时用于「手机横屏」那一行（下限取 660：
                      h720dp 这类阈值正落在常见手机的可用高范围里，要分两种情形写）
  --tablet 规格       「平板」参考配置，默认 sw=600-800,h=960-1280,dpi=xhdpi，竖屏、横屏都算
名字：平台资源直接写（Theme.Material.Light、darker_gray）；查库时平台的写 android:前缀。--item 不带 android: 前缀时，
库的 style 里 <属性> 和 android:<属性> 两个都查（库自己声明了同名 attr 时，两者是不同的属性）。

小结分四段，都要看：
  1. 参考配置下实际命中：★常见手机竖屏、手机横屏、平板三行，各写按这个配置命中的是哪一份、值是多少；配置是一个
     范围，范围里不同机型命中不同的，按条件分行列出（如「sw 360–371dp：…；sw 372–412dp：…」）。写事实以
     ★常见手机竖屏那一行为主，同时写出别的配置下的取值。
  2. 各限定变体：每个带屏幕宽高（sw/w/h<N>dp）、横竖屏、密度、屏幕尺寸、长屏、圆屏、界面模式（watch、television
     等）、布局方向、触屏限定的目录（含它们和 night、vNN 的组合）各一行：条件、只满足这个条件时的取值，并标出
     参考配置会不会命中它。
  3. 只按 API 级别和日夜（values/、values-vNN、values-night 这几种目录之间怎么选）。
  4. 另有以下变体，要逐个看：语言、地区、运营商（mcc/mnc）、语法性别、广色域、HDR、键盘、导航键这些限定，工具不
     归纳，逐个列出目录名。
命中的判法照安卓资源匹配（frameworks/base 的 ResTable_config::match 和 isBetterThan）：先去掉和配置矛盾的目录（密度
不淘汰），剩下的按限定条件的优先级逐个比——布局方向 > sw > w、h（按「配置值减目录值」之和，小的胜）> 屏幕尺寸 >
长屏 > 圆屏 > 横竖屏 > 界面模式 > 日夜 > 密度（不带密度按 mdpi 算；都比配置高时取低的、都低时取高的，否则缩小优先）
> 触屏 > vNN（取不超过配置的最大值）。没实现的：上面第 4 段那些限定（含这类限定的目录一律当作不命中）；两份目录在
所有已实现的限定上都打平时（如有效密度相同）取带限定的那份，安卓那时取遍历中靠后的。参考配置里横屏的高直接取 sw、
没扣状态栏和导航栏；长屏按 长边×3/5 ≥ 短边−1 算；屏幕尺寸按短边、长边的 320/470、480/640、720/960 分档。
参考配置的宽、高指 Configuration 的 screenWidthDp / screenHeightDp（资源匹配用的可用尺寸；按旧 targetSdk 跑时不含
状态栏和导航栏，物理高 800dp 的手机约 730dp），用 --phone / --tablet 改时照这个口径写。
其余口径：默认语言、未按下的可用状态。查库时 android: 开头的父主题和资源按 --api 的平台资源解析，真机用的是它自己
那一版的框架资源。"""
import sys

sys.dont_write_bytecode = True
import argparse, itertools, os, re, zipfile  # noqa: E401,E402
import xml.etree.ElementTree as ET  # noqa: E402

A_NS = "{http://schemas.android.com/apk/res/android}"
AUTO_NS = "{http://schemas.android.com/apk/res-auto}"
VALUE_TYPES = ("color", "dimen", "bool", "integer", "fraction", "drawable")
DEF_TAGS = ("style", "attr") + VALUE_TYPES
PREFILTER = re.compile(rb"<(?:style|color|dimen|bool|integer|fraction|drawable|attr|declare-styleable)[\s>/]"
                       rb"|<item\s[^>]*\btype=")
REF = re.compile(r"^([@?])(\+)?(\*)?(?:([\w.]+):)?(?:([\w-]+)/)?([\w.]+)$")
HEX = re.compile(r"^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


# ---------------------------------------------------------------- 限定符和配置

DENS = {"ldpi": 120, "mdpi": 160, "tvdpi": 213, "hdpi": 240, "xhdpi": 320, "xxhdpi": 480, "xxxhdpi": 640,
        "anydpi": 0xfffe, "nodpi": 0xffff}
DENS_NAME = {v: k for k, v in DENS.items()}
UIMODES = ("car", "desk", "television", "appliance", "watch", "vrheadset")
SIZES = {"small": 1, "normal": 2, "large": 3, "xlarge": 4}
SIZE_NAME = {v: k for k, v in SIZES.items()}
UI_WORDS = {"car": "车机", "desk": "底座", "television": "电视", "appliance": "家电", "watch": "手表",
            "vrheadset": "VR 头显"}


class Q:
    """一个限定目录名解析出来的限定条件。unk = 工具不归纳的限定（语言、运营商、键盘等）。"""
    __slots__ = ("name", "v", "night", "sw", "w", "h", "orient", "uimode", "dens", "size", "long", "round",
                 "ldir", "touch", "unk")


_QCACHE = {}


def pq(dirname):
    q = _QCACHE.get(dirname)
    if q is not None:
        return q
    q = Q()
    q.name, q.v, q.night, q.sw, q.w, q.h = dirname, 0, None, 0, 0, 0
    q.orient = q.uimode = q.long = q.round = q.ldir = q.touch = None
    q.dens, q.size, q.unk = 0, 0, []
    for t in dirname.split("-")[1:]:
        m = re.fullmatch(r"(sw|w|h)(\d+)dp", t)
        if re.fullmatch(r"v\d+", t):
            q.v = int(t[1:])
        elif t in ("night", "notnight"):
            q.night = t == "night"
        elif m:
            setattr(q, m.group(1), int(m.group(2)))
        elif t in ("port", "land"):
            q.orient = t
        elif t in UIMODES:
            q.uimode = t
        elif t in DENS:
            q.dens = DENS[t]
        elif re.fullmatch(r"\d+dpi", t):
            q.dens = int(t[:-3])
        elif t in SIZES:
            q.size = SIZES[t]
        elif t in ("long", "notlong"):
            q.long = t == "long"
        elif t in ("round", "notround"):
            q.round = t == "round"
        elif t in ("ldrtl", "ldltr"):
            q.ldir = t[2:]
        elif t in ("finger", "notouch", "stylus"):
            q.touch = t
        else:
            q.unk.append(t)
    _QCACHE[dirname] = q
    return q


def screen_quals(q):
    """除 vNN、night 以外、工具归纳的限定有没有。"""
    return bool(q.sw or q.w or q.h or q.orient or q.uimode or q.dens or q.size or q.long is not None
                or q.round is not None or q.ldir or q.touch)


def qual_order(e):
    q = pq(e.qual if hasattr(e, "qual") else e[0])
    return (2 if q.unk else (1 if screen_quals(q) else 0), q.night is not None, q.v, q.name)


def q_words(q):
    """限定条件的中文说法。"""
    out = []
    if q.ldir:
        out.append("从右到左布局" if q.ldir == "rtl" else "从左到右布局")
    if q.sw:
        out.append(f"最短边 ≥{q.sw}dp")
    if q.w:
        out.append(f"可用宽度 ≥{q.w}dp")
    if q.h:
        out.append(f"可用高度 ≥{q.h}dp")
    if q.size:
        out.append(f"屏幕尺寸 {SIZE_NAME[q.size]} 及以上")
    if q.long is not None:
        out.append("长屏" if q.long else "非长屏")
    if q.round is not None:
        out.append("圆屏" if q.round else "非圆屏")
    if q.orient:
        out.append("竖屏" if q.orient == "port" else "横屏")
    if q.uimode:
        out.append(UI_WORDS[q.uimode])
    if q.night is not None:
        out.append("夜间" if q.night else "日间")
    if q.dens:
        out.append(f"密度 {DENS_NAME.get(q.dens, str(q.dens) + 'dpi')}" + ("" if q.dens in (0xfffe, 0xffff) else
                                                                        f"（{q.dens}dpi，按缩放就近选）"))
    if q.touch:
        out.append({"finger": "手指触屏", "notouch": "无触屏", "stylus": "触控笔"}[q.touch])
    if q.v:
        out.append(f"API ≥{q.v}")
    return "、".join(out)


class Cfg:
    """一台设备的配置。0 / None = 没有这一项（这时带这一项限定的目录不命中）；uimode 恒为 normal（手机、平板）。"""
    __slots__ = ("api", "night", "sw", "w", "h", "orient", "uimode", "dens", "size", "long", "round", "ldir",
                 "touch")

    def __init__(self, api, night=False, **kw):
        self.api, self.night = api, night
        self.sw = self.w = self.h = self.dens = self.size = 0
        self.orient = self.long = self.round = self.ldir = self.touch = None
        self.uimode = "normal"
        for k, v in kw.items():
            setattr(self, k, v)


def matches(q, c):
    """ResTable_config::match 的对应部分：和配置矛盾的目录不命中（密度不淘汰）。"""
    if q.unk:
        return False
    if q.v > c.api or (q.night is not None and q.night != c.night):
        return False
    if q.sw > c.sw or q.w > c.w or q.h > c.h:
        return False
    if (q.orient and q.orient != c.orient) or (q.uimode and q.uimode != c.uimode):
        return False
    if q.size and q.size > c.size:
        return False
    if (q.long is not None and q.long != c.long) or (q.round is not None and q.round != c.round):
        return False
    if (q.ldir and q.ldir != c.ldir) or (q.touch and q.touch != c.touch):
        return False
    return True


def dens_better(a, b, req):
    ta, tb = a or 160, b or 160
    if ta == tb:
        return a != 0  # 有效密度相同：取带密度限定的（安卓此时取遍历中靠后的那份）
    if ta == 0xfffe:
        return True
    if tb == 0xfffe:
        return False
    r = req if req and req != 0xfffe else 160
    h, l, big = ta, tb, True
    if l > h:
        h, l, big = l, h, False
    if r >= h:
        return big
    if l >= r:
        return not big
    return (not big) if ((2 * l - r) * h > r * r) else big


def better(a, b, c):
    """ResTable_config::isBetterThan 的对应部分；a、b 都已命中。"""
    if a.ldir != b.ldir and c.ldir:
        return bool(a.ldir)
    if a.sw != b.sw:
        return a.sw > b.sw
    if a.w or a.h or b.w or b.h:
        da = db = 0
        if c.w:
            da, db = da + c.w - a.w, db + c.w - b.w
        if c.h:
            da, db = da + c.h - a.h, db + c.h - b.h
        if da != db:
            return da < db
    if a.size != b.size:
        fa, fb = a.size, b.size
        if c.size >= 2:
            fa, fb = fa or 2, fb or 2
        return (a.size != 0) if fa == fb else fa > fb
    if a.long != b.long and c.long is not None:
        return a.long is not None
    if a.round != b.round and c.round is not None:
        return a.round is not None
    if a.orient != b.orient and c.orient:
        return bool(a.orient)
    if a.uimode != b.uimode:
        return bool(a.uimode)
    if a.night != b.night:
        return a.night is not None
    if a.dens != b.dens:
        return dens_better(a.dens, b.dens, c.dens)
    if a.touch != b.touch and c.touch:
        return bool(a.touch)
    if a.v != b.v:
        return a.v > b.v
    return False


# ---------------------------------------------------------------- 资源索引

class Entry:
    __slots__ = ("type", "name", "qual", "file", "value", "attrs", "parent", "items", "extra")

    def __init__(self, typ, name, qual, file):
        self.type, self.name, self.qual, self.file = typ, name, qual, file
        self.value, self.attrs, self.parent, self.items, self.extra = "", {}, None, [], ""


class Source:
    """一份资源：平台 android-N 的 data/res，或一个 aar 的 res/。ns='android' 或 'app'。"""

    def __init__(self, label, ns, level=None):
        self.label, self.ns, self.level = label, ns, level
        self.idx, self.colorfiles, self.notes, self.min_sdk = {}, {}, [], None

    def add_values(self, qual, rel, data):
        if not PREFILTER.search(data):
            return
        try:
            root = ET.fromstring(data)
        except ET.ParseError as e:
            self.notes.append(f"{rel} 解析失败：{e}")
            return
        for el in root:
            tag = el.tag if isinstance(el.tag, str) else ""
            if tag == "declare-styleable":
                for a in el:
                    if a.tag == "attr" and (a.get("format") or len(a)):
                        self._attr(a, qual, rel, "declare-styleable " + (el.get("name") or ""))
                continue
            if tag == "item":
                typ = el.get("type")
                if typ not in VALUE_TYPES:
                    continue
            elif tag in DEF_TAGS:
                typ = tag
            else:
                continue
            name = el.get("name")
            if not name:
                continue
            if typ == "attr":
                self._attr(el, qual, rel, "")
                continue
            e = Entry(typ, name, qual, rel)
            if typ == "style":
                e.parent = el.get("parent")
                for it in el:
                    if it.tag != "item" or not it.get("name"):
                        continue
                    raw = it.get("name")
                    if raw.startswith("android:"):
                        ns, an = "android", raw[8:]
                    else:
                        ns, an = self.ns, raw
                    e.items.append((ns, an, raw, "".join(it.itertext()).strip()))
            else:
                e.value = "".join(el.itertext()).strip()
                e.attrs = {k: v for k, v in el.attrib.items() if k != "name"}
                e.extra = tag
            self.idx.setdefault((typ, name), []).append(e)

    def _attr(self, el, qual, rel, where):
        name = el.get("name")
        if not name or (self.ns == "app" and name.startswith("android:")):
            return
        e = Entry("attr", name, qual, rel)
        e.value = el.get("format") or ""
        kids = [f"{k.tag} {k.get('name')}={k.get('value')}" for k in el if isinstance(k.tag, str)]
        e.extra = where + ("；" if where and kids else "") + ("、".join(kids[:12]) + ("…" if len(kids) > 12 else ""))
        self.idx.setdefault(("attr", name), []).append(e)


class PlatformSource(Source):
    def __init__(self, res, label, level):
        super().__init__(label, "android", level)
        self.res = res
        for d in sorted(os.listdir(res)):
            p = os.path.join(res, d)
            if not os.path.isdir(p):
                continue
            if d == "values" or d.startswith("values-"):
                for f in sorted(os.listdir(p)):
                    if f.endswith(".xml"):
                        with open(os.path.join(p, f), "rb") as fh:
                            self.add_values(d, f"{d}/{f}", fh.read())
            elif d == "color" or d.startswith("color-"):
                for f in os.listdir(p):
                    if f.endswith(".xml"):
                        self.colorfiles.setdefault(f[:-4], []).append((d, f"{d}/{f}"))

    def read(self, rel):
        with open(os.path.join(self.res, rel), "rb") as fh:
            return fh.read()


class AarSource(Source):
    def __init__(self, path, label):
        super().__init__(label, "app")
        self.zip = zipfile.ZipFile(path)
        for n in sorted(self.zip.namelist()):
            parts = n.split("/")
            if len(parts) != 3 or parts[0] != "res" or not parts[2].endswith(".xml"):
                continue
            d, f = parts[1], parts[2]
            if d == "values" or d.startswith("values-"):
                self.add_values(d, f"{d}/{f}", self.zip.read(n))
            elif d == "color" or d.startswith("color-"):
                self.colorfiles.setdefault(f[:-4], []).append((d, f"{d}/{f}"))
        try:
            m = re.search(rb'minSdkVersion="(\d+)"', self.zip.read("AndroidManifest.xml"))
            self.min_sdk = int(m.group(1)) if m else None
        except KeyError:
            pass

    def read(self, rel):
        return self.zip.read("res/" + rel)


# ---------------------------------------------------------------- 一组资源（若干库 + 一个平台）

def node_label(node, lib_mode):
    ns, name = node
    return ("android:" + name) if (ns == "android" and lib_mode) else name


class World:
    def __init__(self, libs, platform):
        self.libs, self.platform = libs, platform
        self.lib_mode = bool(libs)
        self.seen, self.picked, self.refs = set(), set(), []
        self.label = " ＋ ".join([s.label for s in libs] + [f"平台 {platform.label}"]) if libs else platform.label

    def lookup(self, typ, ns, name):
        for s in (self.libs if ns == "app" else [self.platform]):
            ents = s.idx.get((typ, name))
            if ents:
                return s, ents
        return None, []

    def select(self, ents, cfg, key=lambda e: e.qual):
        """照安卓的资源匹配选一份：去掉矛盾的，剩下的里最具体（最接近配置）的胜。"""
        best, bq = None, None
        for e in ents:
            name = key(e)
            self.seen.add(name)
            q = pq(name)
            if matches(q, cfg) and (best is None or better(q, bq, cfg)):
                best, bq = e, q
        if bq is not None:
            self.picked.add(bq.name)
        return best

    @staticmethod
    def parent_of(e, ns):
        if e.parent is None:
            return (ns, e.name.rsplit(".", 1)[0]) if "." in e.name else None
        p = e.parent.strip().lstrip("@").replace("*", "")
        if not p:
            return None
        if p.startswith("android:"):
            ns, p = "android", p[8:]
        if p.startswith("style/"):
            p = p[6:]
        return (ns, p)

    # -- 主题里某个属性的取值
    def resolve_item(self, theme, key, cfg):
        node, hops = theme, 0
        while node and hops < 80:
            hops += 1
            src, ents = self.lookup("style", *node)
            if not ents:
                return None, None, f"{node_label(node, self.lib_mode)} 没找到定义"
            e = self.select(ents, cfg)
            if e is None:
                return None, None, f"{node_label(node, self.lib_mode)} 在这个配置下没有适用的变体"
            for ns, an, raw, val in e.items:
                if (ns, an) == key:
                    return val, src.ns, f"{node_label(node, self.lib_mode)} [{e.qual}]"
            node = self.parent_of(e, node[0])
        return None, None, "链上都没设"

    # -- 把一个值解析到字面值；返回 (字面值或 None, 经过的各步)
    def resolve_value(self, val, ns, cfg, theme, depth=0):
        v = (val or "").strip()
        if depth > 30:
            return None, ["引用太深，停"]
        m = REF.match(v)
        if not m or v in ("@null", "@empty"):
            return v, []
        sigil, _, _, pkg, typ, name = m.groups()
        rns = "android" if pkg == "android" else ("app" if pkg else ns)
        if sigil == "?":
            if theme is None:
                return None, [f"停在 {v}（要看用它的主题，加 --theme）"]
            v2, ns2, where = self.resolve_item(theme, (rns, name), cfg)
            if v2 is None:
                return None, [f"停在 {v}：{where}"]
            fin, st = self.resolve_value(v2, ns2, cfg, theme, depth + 1)
            return fin, [f"{v2}〔{where}〕"] + st
        if typ in VALUE_TYPES:
            src, ents = self.lookup(typ, rns, name)
            if ents:
                e = self.select(ents, cfg)
                if e is None:
                    return None, [f"停在 {v}：这个配置下没有适用的定义"]
                fin, st = self.resolve_value(e.value, src.ns, cfg, theme, depth + 1)
                tag = "" if (e.qual == "values" and len(ents) == 1) else f"〔{e.qual}〕"
                return fin, ([f"{e.value}{tag}"] if REF.match(e.value) or tag else []) + st
            if typ in ("color", "drawable"):
                for s in (self.libs if rns == "app" else [self.platform]):
                    if name in s.colorfiles:
                        return self.resolve_csl(s, name, cfg, theme, depth)
            return None, [f"停在 {v}：没找到"]
        return None, [f"停在 {v}（{typ} 不是取值，不再解析）"]

    def resolve_csl(self, src, name, cfg, theme, depth):
        files = src.colorfiles[name]
        f = self.select(files, cfg, key=lambda x: x[0])
        if f is None:
            return None, [f"停在 color/{name}：这个配置下没有适用的状态列表"]
        try:
            root = ET.fromstring(src.read(f[1]))
        except ET.ParseError as e:
            return None, [f"停在 {f[1]}：解析失败 {e}"]
        items = [it for it in root if it.tag == "item"]
        normal = {"state_enabled": True, "state_window_focused": True}
        pick = None
        for it in items:
            ok = True
            for k, val in it.attrib.items():
                if k.startswith(A_NS + "state_") or k.startswith(AUTO_NS + "state_"):
                    st = k.split("}", 1)[1]
                    if (val == "true") != normal.get(st, False):
                        ok = False
            if ok:
                pick = it
                break
        others = len(items) - 1
        if pick is None:
            return None, [f"状态列表 {src.label} {f[1]}：没有匹配默认状态的项"]
        color = pick.get(A_NS + "color")
        alpha = pick.get(A_NS + "alpha") or pick.get(AUTO_NS + "alpha")
        lstar = pick.get(A_NS + "lStar") or pick.get(AUTO_NS + "lStar")
        head = f"状态列表 {f[1]}（默认项 color={color}" + (f" alpha={alpha}" if alpha else "") + \
               (f" lStar={lstar}" if lstar else "") + f"；另有 {others} 个状态项）"
        fc, sc = self.resolve_value(color, src.ns, cfg, theme, depth + 1)
        steps = [head] + ([f"color: {' → '.join(sc)}"] if sc else [])
        if not alpha:
            return fc, steps + (["lStar 没有计算"] if lstar else [])
        fa, sa = self.resolve_value(alpha, src.ns, cfg, theme, depth + 1)
        steps += [f"alpha: {' → '.join(sa) if sa else fa}"]
        if fc is None or fa is None:
            return None, steps
        mixed = apply_alpha(fc, fa)
        return (f"{mixed}（{fc} × alpha {fa}）" if mixed else f"{fc} × alpha {fa}"), steps + (
            ["lStar 没有计算"] if lstar else [])


def norm_hex(c):
    m = HEX.match(c or "")
    if not m:
        return None
    h = m.group(1)
    if len(h) in (3, 4):
        h = "".join(ch * 2 for ch in h)
    if len(h) == 6:
        h = "ff" + h
    return h.lower()


def apply_alpha(color, alpha):
    h = norm_hex(color)
    try:
        a = float(alpha)
    except (TypeError, ValueError):
        return None
    if not h:
        return None
    na = int(int(h[:2], 16) * a + 0.5)  # 同 ColorStateList.modulateColorAlpha 的取整
    return "#%02x%s" % (max(0, min(255, na)), h[2:])


def show_final(fin):
    if fin is None:
        return "（没解析到字面值）"
    h = norm_hex(fin)
    return f"{fin}（= #{h}）" if h and fin.lower() != "#" + h else fin


# ---------------------------------------------------------------- 按配置汇总

def configs_for(world):
    """返回要算的 API 级别。平台模式：就是这个平台的级别；库模式：库的 minSdk 加上遇到过的 vNN。"""
    if not world.lib_mode:
        return [world.platform.level]
    base = max((s.min_sdk or 14) for s in world.libs)  # 应用的 minSdk 不会低于任何一个库的
    vs = {pq(q).v for q in world.seen}
    return sorted({base} | {v for v in vs if v > base})


# 参考配置：(名字, 是否主参考, 规格选项名, 方向)
REF_DEFS = [("常见手机竖屏", True, "phone", ("port",)), ("手机横屏", False, "phone", ("land",)),
            ("平板", False, "tablet", ("port", "land"))]
REF_SPECS = {"phone": "sw=360-412,h=660-915,dpi=xxhdpi", "tablet": "sw=600-800,h=960-1280,dpi=xhdpi"}


def parse_spec(s):
    """'sw=360-412,h=760-915,dpi=xxhdpi' -> (sw 范围, 长边范围, 密度)。"""
    d = {}
    for part in s.split(","):
        k, _, v = part.strip().partition("=")
        d[k.strip()] = v.strip()
    try:
        def rng(x):
            lo, _, hi = x.partition("-")
            return int(lo), int(hi or lo)
        dens = d.get("dpi", "xxhdpi")
        dens = DENS[dens] if dens in DENS else int(dens.replace("dpi", ""))
        return rng(d["sw"]), rng(d["h"]), dens
    except (KeyError, ValueError):
        raise SystemExit(f"参考配置写法不对：{s}（例：sw=360-412,h=760-915,dpi=xxhdpi）")


def size_class(short, long_):
    if long_ >= 960 and short >= 720:
        return 4
    if long_ >= 640 and short >= 480:
        return 3
    if long_ >= 470 and short >= 320:
        return 2
    return 1


def intervals(lo, hi, ths):
    """把 [lo, hi] 按阈值切成段；段内所有限定的命中情况相同，取段首代表这一段。"""
    pts = sorted({lo} | {t for t in ths if lo < t <= hi})
    return [(p, pts[i + 1] - 1 if i + 1 < len(pts) else hi) for i, p in enumerate(pts)]


def fmt_iv(label, ivs):
    def f(lo, hi):
        if lo == 0 and hi == len(ivs) - 1:
            return None
        a, b = ivs[lo][0], ivs[hi][1]
        return f"{label} {a}dp" if a == b else f"{label} {a}–{b}dp"
    return f


def fmt_api(apis, lib_mode):
    def f(lo, hi):
        if lo == 0 and hi == len(apis) - 1:
            return None
        a, b = apis[lo], (apis[hi + 1] - 1 if hi + 1 < len(apis) else None)
        return (f"API {a}–{b}" if b != a else f"API {a}") if b else f"API {a} 起"
    return f


def fmt_night(lo, hi):
    return None if lo != hi else ("夜间" if lo else "日间")


def run_grid(world, fn, dims, make_cfg):
    """dims = [(名, [取值…], 格式化)]；对每个取值组合算一遍。返回 {下标元组: (键, 文字, 走到的目录)}。"""
    pts = {}
    for idx in itertools.product(*[range(len(d[1])) for d in dims]):
        world.picked = set()
        k, txt = fn(make_cfg({d[0]: d[1][i] for d, i in zip(dims, idx)}))
        pts[idx] = (k, txt, frozenset(world.picked))
    return pts


def describe(pts, dims, fixed=frozenset()):
    """把结果按条件分组：每次挑最能分开结果的一维切开，相邻且结果相同的段合并。返回 [([条件…], 文字, 键)]。"""
    first = next(iter(pts.values()))
    if len({v[0] for v in pts.values()}) == 1:
        return [([], first[1], first[0])]
    free = [d for d in range(len(dims)) if d not in fixed and len(dims[d][1]) > 1]

    def cost(d):
        return sum(len({v[0] for i, v in pts.items() if i[d] == j}) for j in range(len(dims[d][1])))
    d = min(free, key=cost)
    runs = []
    for j in range(len(dims[d][1])):
        sub = {i: v for i, v in pts.items() if i[d] == j}
        sig = tuple((i[:d] + i[d + 1:], v[0]) for i, v in sorted(sub.items(), key=lambda x: x[0]))
        if runs and runs[-1][2] == sig:
            runs[-1][1] = j
        else:
            runs.append([j, j, sig, sub])
    out = []
    for lo, hi, _, sub in runs:
        cond = dims[d][2](lo, hi)
        for conds, txt, k in describe(sub, dims, fixed | {d}):
            out.append(([cond] + conds if cond else conds, txt, k))
    return out


def grid_lines(head, leaves, indent="  "):
    if len(leaves) == 1 and not leaves[0][0]:
        return [f"{indent}{head}：{leaves[0][1]}"]
    return [f"{indent}{head}：因配置而异——"] + [f"{indent}    {'，'.join(c) or '其余'}：{t}" for c, t, _ in leaves]


def summarize(world, fn):
    """fn(cfg) -> (结果键, 展示文字)。返回 (小结各行, 结构)。四段：参考配置、各限定变体、只按 API 和日夜、不归纳的变体。"""
    world.seen.clear()
    fn(Cfg(world.platform.level if not world.lib_mode else 99))
    for _ in range(6):
        before = set(world.seen)
        apis = configs_for(world)
        res, var_pts, ref_pts = summarize_pass(world, fn, apis)
        if world.seen == before and configs_for(world) == apis:
            break
    out, struct = [], []
    ref_hits = {}
    out.append(" ・参考配置下实际命中（写事实以 ★ 那一行为主，同时写出其他配置下的取值）：")
    for name, star, desc, per in ref_pts:
        leaves_all, picked_all = [], []
        lvs = [(o, describe(pts, dims)) for o, dims, pts in per]
        for o, dims, pts in per:
            picked_all += [v[2] for v in pts.values()]
        sig = [[(c, k) for c, _, k in lv] for _, lv in lvs]
        if all(s == sig[0] for s in sig):  # 竖屏、横屏分法和结果都一样：不分方向
            leaves_all = lvs[0][1]
        else:
            for o, lv in lvs:
                leaves_all += [([("竖屏" if o == "port" else "横屏")] + c, t, k) for c, t, k in lv]
        if len({k for _, _, k in leaves_all}) == 1:
            leaves_all = [([], leaves_all[0][1], leaves_all[0][2])]
        out += grid_lines(f"{'★' if star else ''}{name}（{desc}）", leaves_all)
        for c, _, k in leaves_all:
            struct.append(("ref", name, tuple(c), k))
        ref_hits[name] = (frozenset.union(*picked_all), frozenset.intersection(*picked_all))
    if var_pts:
        out.append(" ・各限定变体（每个一行：目录、条件、只满足这个条件时的取值；实际设备上谁胜看上面的参考配置）：")
    for qn, (dims, pts) in var_pts.items():
        tags = []
        for name, (anyp, allp) in ref_hits.items():
            if qn in allp:
                tags.append(f"{name}会命中")
            elif qn in anyp:
                tags.append(f"{name}部分配置命中（看上面分行）")
        if not any(qn in v[2] for v in pts.values()):
            tags.append("只满足这个条件时没走到它")
        head = f"[{qn}] {q_words(pq(qn))}" + (f"（{'；'.join(tags)}）" if tags else "")
        if tags and tags[0].startswith("常见手机竖屏"):
            head = "★" + head
        lv = describe(pts, dims)
        out += grid_lines(head, lv, "    ")
        for c, _, k in lv:
            struct.append(("var", qn, tuple(c), k))
    has_night = any(pq(q).night is not None and not pq(q).unk for q in world.seen)
    nights = (False, True) if has_night and any(res[(a, False)][0] != res[(a, True)][0] for a in apis) else (False,)
    out.append(" ・只按 API 级别和日夜（values/、values-vNN、values-night 之间怎么选；不满足任何屏幕、方向、密度限定时）：")
    for n in nights:
        rows, cur = [], None
        for i, a in enumerate(apis):
            k, txt = res[(a, n)]
            if cur and cur[2] == k:
                cur[1] = a
            else:
                cur = [a, a, k, txt]
                rows.append(cur)
        for j, (lo, hi, k, txt) in enumerate(rows):
            nxt = rows[j + 1][0] - 1 if j + 1 < len(rows) else None
            if not world.lib_mode:
                rng = f"android-{world.platform.label.split('-')[-1]}"
            else:
                rng = f"API {lo}–{nxt}" if nxt and nxt != lo else (f"API {lo}" if nxt else f"API {lo} 起")
            pre = ("夜间 " if n else ("日间 " if len(nights) == 2 else ""))
            out.append(f"    {pre}{rng}：{txt}")
            struct.append((n, lo if world.lib_mode else 0, nxt if world.lib_mode else 0, k))
    if has_night and len(nights) == 1:
        out.append("    （遇到了夜间限定的变体，日间、夜间结果相同）")
    unk = sorted({q for q in world.seen if pq(q).unk}, key=lambda q: (pq(q).unk, q))
    if unk:
        shown = unk if len(unk) <= 60 else unk[:60]
        out.append(f" ・另有以下变体，要逐个看（语言、地区、运营商、语法性别、键盘导航等限定，工具不归纳，共 {len(unk)} 个"
                   + ("；只列前 60 个，全部见上面逐层列出的部分" if len(unk) > 60 else "") + "）：")
        out.append("    " + "、".join(shown))
    return out, struct


def summarize_pass(world, fn, apis):
    """按当前见过的目录算一遍：只按 API 和日夜、各限定变体、各参考配置。"""
    toks = [pq(q) for q in list(world.seen) if not pq(q).unk]
    night_seen = any(q.night is not None for q in toks)
    res = {(a, n): fn(Cfg(a, n)) for a in apis for n in (False, True)}
    base_dims = []
    if len(apis) > 1:
        base_dims.append(("api", apis, fmt_api(apis, world.lib_mode)))
    # 各限定变体：只满足这个目录的限定（其余都没有）时的取值
    var_pts = {}
    for q in sorted({q for q in toks if screen_quals(q)}, key=lambda q: qual_order((q.name,))):
        dims = list(base_dims)
        if night_seen and q.night is None:
            dims.append(("night", [False, True], fmt_night))

        def mk(v, q=q):
            return Cfg(v.get("api", apis[0]),
                       q.night if q.night is not None else v.get("night", False),
                       sw=q.sw, w=q.w, h=q.h, orient=q.orient, uimode=q.uimode or "normal", dens=q.dens,
                       size=q.size, long=q.long, round=q.round, ldir=q.ldir, touch=q.touch)
        var_pts[q.name] = (dims, run_grid(world, fn, dims, mk))
    # 参考配置
    sws = {q.sw for q in toks if q.sw}
    ws = {q.w for q in toks if q.w}
    hs = {q.h for q in toks if q.h}
    size_seen = any(q.size for q in toks)
    ref_pts = []
    for name, star, spec, orients in REF_DEFS:
        (swlo, swhi), (llo, lhi), dens = world.refs[spec]
        per = []
        for o in orients:
            sth, lth = (sws | ws, hs) if o == "port" else (sws | hs, ws)
            if size_seen:
                sth, lth = sth | {320, 480, 720}, lth | {470, 640, 960}
            dims = list(base_dims)
            if night_seen:
                dims.append(("night", [False, True], fmt_night))
            siv, liv = intervals(swlo, swhi, sth), intervals(llo, lhi, lth)
            dims.append(("sw", siv, fmt_iv("sw", siv)))
            dims.append(("long", liv, fmt_iv("高" if o == "port" else "宽", liv)))

            def mk(v, o=o):
                s, L = v["sw"][0], v["long"][0]
                return Cfg(v.get("api", apis[0]), v.get("night", False), sw=s, w=s if o == "port" else L,
                           h=L if o == "port" else s, orient=o, dens=dens, size=size_class(s, L),
                           long=(L * 3 // 5) >= (s - 1), round=False, ldir="ltr", touch="finger")
            per.append((o, dims, run_grid(world, fn, dims, mk)))
        dn = DENS_NAME.get(dens, f"{dens}dpi")
        if orients == ("port",):
            desc = f"sw {swlo}–{swhi}dp，宽=sw，高 {llo}–{lhi}dp，{dn}"
        elif orients == ("land",):
            desc = f"宽 {llo}–{lhi}dp，高≈sw {swlo}–{swhi}dp，{dn}"
        else:
            desc = f"sw {swlo}–{swhi}dp，长边 {llo}–{lhi}dp，竖屏和横屏，{dn}"
        if len(apis) == 1 and world.lib_mode:
            desc += f"，API {apis[0]}"
        ref_pts.append((name, star, desc, per))
    return res, var_pts, ref_pts


# ---------------------------------------------------------------- 命令

def wanted_keys(world, item):
    if item.startswith("android:"):
        return [("android", item[8:])]
    if world.lib_mode and any(s.idx.get(("attr", item)) for s in world.libs):
        return [("app", item), ("android", item)]
    return [("android", item)]


def key_label(k, world):
    return ("android:" + k[1]) if (k[0] == "android" and world.lib_mode) else k[1]


def start_node(world, name):
    if name.startswith("android:"):
        return ("android", name[8:])
    if world.lib_mode:
        s, ents = world.lookup("style", "app", name)
        if ents:
            return ("app", name)
    return ("android", name)


def is_theme_like(name):
    return "Theme" in name or name.split(":")[-1].startswith("Platform.")


def style_chain(world, start, keys):
    """BFS 顺着所有变体的 parent；返回 [(层名, [行…])]。"""
    out, seen, queue = [], set(), [(start, 0)]
    while queue:
        node, d = queue.pop(0)
        if node in seen or d > 60:
            continue
        seen.add(node)
        label = node_label(node, world.lib_mode)
        src, ents = world.lookup("style", *node)
        if not ents:
            out.append((label, [f"{'  ' * min(d, 1)}{label}：没找到定义（链停在这里）"]))
            continue
        lines = []
        for e in sorted(ents, key=qual_order):
            par = world.parent_of(e, node[0])
            if e.parent is None:
                ptxt = f"parent=（隐式）{par[1]}" if par else "parent=（无）"
            elif not e.parent.strip():
                ptxt = 'parent=""（无）'
            else:
                ptxt = "parent=" + e.parent
            vals = []
            for k in keys:
                hit = [val for ns, an, raw, val in e.items if (ns, an) == k]
                vals.append(f"{key_label(k, world)}={hit[-1]}" if hit else f"{key_label(k, world)} 未设")
            tail = ("；" + "，".join(vals)) if keys else f"；{len(e.items)} 项"
            lines.append(f"  {label}  [{e.qual}] {e.file.split('/')[-1]}：{ptxt}{tail}")
            if par and par not in seen:
                queue.append((par, d + 1))
        out.append((label, lines))
    return out


def print_worlds(worlds, blocks):
    """blocks[i] = [(层名, [行…])]；第一组全打，后面的只打和第一组不同的层。"""
    base = dict(blocks[0])
    for i, (w, bl) in enumerate(zip(worlds, blocks)):
        print(f"== {w.label} ==")
        if i == 0:
            for _, lines in bl:
                print("\n".join(lines))
            continue
        same = 0
        for name, lines in bl:
            if base.get(name) == lines:
                same += 1
            else:
                tag = "新出现的层" if name not in base else "和第一组不同"
                print(f"  ※ {name}（{tag}）：")
                print("\n".join(lines))
        gone = [n for n in base if n not in dict(bl)]
        if gone:
            print(f"  这一组没有的层：{'、'.join(gone)}")
        print(f"  （其余 {same} 层（项）与「{worlds[0].label}」相同，略）")


def cmd_style(worlds, a):
    blocks, sums = [], []
    for w in worlds:
        start = start_node(w, a.name)
        keys = wanted_keys(w, a.item) if a.item else []
        blocks.append(style_chain(w, start, keys))
        theme = None
        if a.theme:
            theme = start_node(w, a.theme[0])
        elif is_theme_like(a.name):
            theme = start
        lines, structs = [], []
        for k in keys:
            def fn(cfg, k=k):
                val, ns, where = w.resolve_item(start, k, cfg)
                if val is None:
                    return ("none", where), f"没设（{where}）"
                fin, st = w.resolve_value(val, ns, cfg, theme)
                chain = " → ".join([val] + st)
                return (fin, where, chain), f"{show_final(fin)}；设在 {where}：{chain}"
            out, st = summarize(w, fn)
            lines.append(f" {key_label(k, w)}：")
            lines += out
            structs.append((k, st))
        if not keys:
            def fn(cfg):
                path, node = [], start
                while node and len(path) < 60:
                    src, ents = w.lookup("style", *node)
                    e = w.select(ents, cfg) if ents else None
                    if e is None:
                        path.append(node_label(node, w.lib_mode) + ("（没找到）" if not ents else "（无适用变体）"))
                        break
                    path.append(node_label(node, w.lib_mode) + ("" if e.qual == "values" else f"[{e.qual}]"))
                    node = w.parent_of(e, node[0])
                return tuple(path), " → ".join(path)
            out, st = summarize(w, fn)
            lines.append(" 生效的链：")
            lines += out
            structs.append(("chain", st))
        if theme is None and keys:
            lines.append("  （这个 style 不像主题，?attr 没有解析；要解析加 --theme <主题>）")
        sums.append((lines, structs))
    print_worlds(worlds, blocks)
    print_summary(worlds, sums, f"{a.name}" + (f" 的 {a.item}" if a.item else ""))


def cmd_value(worlds, a):
    blocks, sums = [], []
    for w in worlds:
        name = a.name
        ns = "android" if (name.startswith("android:") or not w.lib_mode) else "app"
        name = name.split(":", 1)[-1]
        src, ents = w.lookup(a.cmd, ns, name)
        if not ents and ns == "app" and not (a.cmd == "color" and any(name in s.colorfiles for s in w.libs)):
            ns = "android"
            src, ents = w.lookup(a.cmd, ns, name)
        lines = []
        for e in sorted(ents or [], key=qual_order):
            attrs = "".join(f' {k}="{v}"' for k, v in e.attrs.items())
            lines.append(f"  [{e.qual}] {e.file}：<{e.extra} name=\"{e.name}\"{attrs}>{e.value}</{e.extra}>")
        csl_src = [s for s in (w.libs if ns == "app" else [w.platform]) if name in s.colorfiles] if a.cmd == "color" else []
        for s in csl_src:
            for q, rel in sorted(s.colorfiles[name], key=qual_order):
                try:
                    its = [" ".join(f"{k.split('}')[-1]}={v}" for k, v in it.attrib.items())
                           for it in ET.fromstring(s.read(rel)) if it.tag == "item"]
                except ET.ParseError:
                    its = ["（解析失败）"]
                lines.append(f"  [{q}] {rel}：颜色状态列表（{'平台' if s.ns == 'android' else s.label.split(' ')[0]}）"
                             f"：{' | '.join(its)}")
        if not lines:
            lines.append(f"  {name}：{'库和平台' if w.lib_mode else '平台'}资源里都没找到")
        lab = f"{'android:' if ns == 'android' and w.lib_mode else ''}{name}"
        blocks.append([(lab, lines)])
        theme = start_node(w, a.theme[0]) if a.theme else None
        prefix = "@android:" if ns == "android" and w.lib_mode else "@"

        def fn(cfg):
            fin, st = w.resolve_value(f"{prefix}{a.cmd}/{name}", "app" if w.lib_mode else "android", cfg, theme)
            if len(st) == 1 and fin and st[0].startswith(fin + "〔"):
                return (fin, tuple(st)), show_final(fin) + st[0][len(fin):]  # 直接取值：只补上是哪个目录
            return (fin, tuple(st)), f"{show_final(fin)}" + (f"：{' → '.join(st)}" if st else "")
        out, st = summarize(w, fn)
        sums.append(([f" {lab}："] + out, [(lab, st)]))
    print_worlds(worlds, blocks)
    print_summary(worlds, sums, a.name)


DEFAULT_THEMES = [("Theme.Material3.Light", "Theme.Material3.Dark"),
                  ("Theme.MaterialComponents.Light", "Theme.MaterialComponents"),
                  ("Theme.AppCompat.Light", "Theme.AppCompat")]


def cmd_attr(worlds, a):
    blocks, sums = [], []
    for w in worlds:
        name = a.name
        lines = []
        for ns in (["app", "android"] if w.lib_mode and not name.startswith("android:") else ["android"]):
            src, ents = w.lookup("attr", ns, name.split(":", 1)[-1])
            for e in ents:
                lines.append(f"  {('android:' if ns == 'android' and w.lib_mode else '')}{e.name} [{e.qual}] "
                             f"{e.file}（{'平台' if src.ns == 'android' else src.label.split(' ')[0]}）：format={e.value or '—'}" + (f"；{e.extra}" if e.extra else ""))
        if not lines:
            lines.append(f"  {name}：没找到 attr 声明")
        blocks.append([(name, lines)])
        if a.theme:
            themes = a.theme
        elif w.lib_mode:
            themes = []
            for pair in DEFAULT_THEMES:
                if any(s.idx.get(("style", pair[0])) for s in w.libs):
                    themes = list(pair)
                    break
        else:
            themes = ["Theme.Material.Light", "Theme.Material"]
        out_all, structs = [], []
        for t in themes:
            start = start_node(w, t)
            for k in wanted_keys(w, name):
                def fn(cfg, k=k, start=start):
                    val, ns, where = w.resolve_item(start, k, cfg)
                    if val is None:
                        return ("none", where), f"没设（{where}）"
                    fin, st = w.resolve_value(val, ns, cfg, start)
                    chain = " → ".join([val] + st)
                    return (fin, where, chain), f"{show_final(fin)}；设在 {where}：{chain}"
                out, st = summarize(w, fn)
                out_all.append(f" {t} 的 {key_label(k, w)}：")
                out_all += out
                structs.append((t, k, st))
        if not themes:
            out_all.append("  （没有可用的默认主题，用 --theme 指定）")
        sums.append((out_all, structs))
    print_worlds(worlds, blocks)
    print_summary(worlds, sums, name)


def print_summary(worlds, sums, what):
    print(f"\n小结（{what}；四段都要看：参考配置、各限定变体、按 API 和日夜、要逐个看的变体；判法和口径见 --help）：")
    for w, (lines, _) in zip(worlds, sums):
        mins = [f"{s.label} minSdk {s.min_sdk}" for s in w.libs if s.min_sdk]
        print(f"【{w.label}】" + (f"（{'，'.join(mins)}）" if mins else ""))
        print("\n".join(lines))
    if len(worlds) > 1:
        diff = [w.label for w, (_, st) in zip(worlds[1:], sums[1:]) if st != sums[0][1]]
        vals = lambda st: [[r[3][0] for r in x[-1]] for x in st]  # noqa: E731
        only_range = [w.label for w, (_, st) in zip(worlds[1:], sums[1:])
                      if st != sums[0][1] and vals(st) == vals(sums[0][1])]
        if not diff:
            print(f"各组比较：和「{worlds[0].label}」完全相同。")
        else:
            print(f"各组比较：{'、'.join(diff)} 和「{worlds[0].label}」不同" +
                  (f"（其中 {'、'.join(only_range)} 只是 API 分段或出处不同，字面值一样）" if only_range else "") +
                  "；取值随版本变的要分别写进事实。")
    if worlds[0].lib_mode:
        print(f"（android: 开头的父主题和资源按平台 {worlds[0].platform.label} 解析；真机用自己那一版的框架资源。）")


# ---------------------------------------------------------------- 找文件

def vkey(v):
    m = re.match(r"(\d+(?:\.\d+)*)(.*)", v)
    if not m:
        return ((), 0, v)
    return (tuple(int(x) for x in m.group(1).split(".")), 1 if not m.group(2) else 0, m.group(2))


def lib_versions(gradle, coord):
    g, art = coord.split(":")[:2]
    base = os.path.join(gradle, "modules-2", "files-2.1", g, art)
    out = {}
    if os.path.isdir(base):
        for ver in os.listdir(base):
            vd = os.path.join(base, ver)
            for h in (os.listdir(vd) if os.path.isdir(vd) else []):
                f = os.path.join(vd, h, f"{art}-{ver}.aar")
                if os.path.isfile(f):
                    out[ver] = f
    return out


def platform_levels(sdk):
    pd = os.path.join(sdk, "platforms")
    out = []
    for d in os.listdir(pd) if os.path.isdir(pd) else []:
        if d.startswith("android-") and os.path.isdir(os.path.join(pd, d, "data", "res")):
            out.append(d[8:])
    return sorted(out, key=vkey)


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("style", "attr") + VALUE_TYPES)
    ap.add_argument("name")
    ap.add_argument("--item")
    ap.add_argument("--api", nargs="+")
    ap.add_argument("--lib", action="append", default=[])
    ap.add_argument("--version", nargs="+")
    ap.add_argument("--theme", action="append")
    ap.add_argument("--sdk")
    ap.add_argument("--gradle")
    ap.add_argument("--phone", default=REF_SPECS["phone"])
    ap.add_argument("--tablet", default=REF_SPECS["tablet"])
    a = ap.parse_args(argv)
    refs = {"phone": parse_spec(a.phone), "tablet": parse_spec(a.tablet)}
    sdk = a.sdk or os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    if not sdk:
        raise SystemExit("没给 Android SDK 目录：用 --sdk 指定，或设环境变量 ANDROID_SDK_ROOT / ANDROID_HOME")
    gradle = a.gradle or (os.path.join(os.environ["GRADLE_USER_HOME"], "caches") if os.environ.get("GRADLE_USER_HOME")
                          else os.path.join(os.path.expanduser("~"), ".gradle", "caches"))
    levels = platform_levels(sdk)
    if not levels:
        raise SystemExit(f"Android SDK 里没有 platforms/android-*/data/res：{sdk}（用 --sdk 指定）")
    apis = a.api or [levels[-1]]
    apis = [x[8:] if x.startswith("android-") else x for x in apis]
    bad = [x for x in apis if x not in levels]
    if bad:
        raise SystemExit(f"本机没有 android-{bad[0]} 的平台资源；有：{', '.join(levels)}")
    print(f"平台资源：用 {', '.join('android-' + x for x in apis)}"
          + ("（默认取最新）" if not a.api else "") + f"；本机有 {', '.join(levels)}，--api 可给一个或几个并排比")
    plats = [PlatformSource(os.path.join(sdk, "platforms", "android-" + x, "data", "res"), "android-" + x,
                            int(vkey(x)[0][0])) for x in apis]
    worlds = []
    if a.lib:
        sets, pinned = [], {}
        for x in a.version or []:
            c, _, v = x.rpartition("=")
            pinned.setdefault(c or a.lib[0], []).append(v)
        for coord in a.lib:
            vers = lib_versions(gradle, coord)
            if not vers:
                raise SystemExit(f"Gradle 缓存里没有 {coord} 的 aar（{gradle}；用 --gradle 指定）")
            order = sorted(vers, key=vkey)
            stable = [v for v in order if vkey(v)[1] == 1] or order
            if coord in pinned:
                miss = [v for v in pinned[coord] if v not in vers]
                if miss:
                    raise SystemExit(f"{coord} 缓存里没有 {miss[0]}；有：{', '.join(order)}")
                pick, why = pinned[coord], "--version 指定"
            elif pinned:
                pick, why = stable[-1:], "别的库指定了版本，这个取最新的正式版"
            else:
                pick = [stable[0], stable[-1]] if len(stable) > 1 else stable[:1]
                why = "最旧、最新的正式版"
            print(f"库 {coord}：缓存里有 aar 的版本 {', '.join(order)}；这次查 {', '.join(pick)}（{why}）")
            sets.append([(coord, v, vers[v]) for v in pick])
        n = max(len(s) for s in sets)
        for p in plats:
            for j in range(n):
                libs = []
                for s in sets:
                    coord, v, path = s[min(j, len(s) - 1)]
                    src = AarSource(path, f"{coord.split(':')[1]} {v}")
                    libs.append(src)
                worlds.append(World(libs, p))
    else:
        worlds = [World([], p) for p in plats]
    for w in worlds:
        w.refs = refs
        for s in w.libs + [w.platform]:
            for n in s.notes[:3]:
                print(f"（注意：{s.label} {n}）")
    print()
    if a.cmd == "style":
        cmd_style(worlds, a)
    elif a.cmd == "attr":
        cmd_attr(worlds, a)
    else:
        cmd_value(worlds, a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
