# -*- coding: utf-8 -*-
"""知识库来源在本机的根目录，以及 refs 的定位怎么解析成本机文件（check_rules.py、render.py、migrate_refs.py 共用）。

refs 的 where 写成可移植的样子，不带任何本机路径（见 references/knowledge-sources.md）：
  harmony-dts   鸿蒙 SDK 根目录（DevEco Studio 的 sdk/default）下的相对路径，加符号名
                  openharmony/ets/component/text.d.ts TextAttribute.textShadow
                  hms/ets/api/@hms.collaboration.systemShare.d.ts ShareController.show
  android-sdk   Android SDK 根目录下的相对路径（带平台版本），加资源名或「类#方法」
                  platforms/android-36/data/res/values/attrs.xml TextAppearance shadowRadius
                  sources/android-36.1/android/widget/TextView.java TextView#readTextAppearance
  android-lib   依赖库的坐标「group:artifact:version」，空一格写包内路径，再写资源名
                  androidx.appcompat:appcompat:1.7.1 res/values/values.xml Base.TextAppearance.AppCompat
  oh-docs       文档库里的相对路径（zh-cn/application-dev/…），加小节名；或完整的 http(s) 地址（旧写法，不核对原文）
路径一律用 /。

本机的根目录放在分支根目录下的 work/sources.local.json（不进版本库；样例见 skills/memory-rules/sources.example.json）：
  {"harmony-sdk": "…/DevEco Studio/sdk/default", "android-sdk": "…/Android/Sdk",
   "gradle-caches": ["…/.gradle/caches"], "oh-docs": "work/ohdocs"}
值可以是绝对路径，也可以是相对分支根目录的路径；gradle-caches 可以写一个或几个。没写的按惯例找：
  harmony-sdk   环境变量 DEVECO_SDK_HOME（下面的 default），再试 Program Files 下的 Huawei/DevEco Studio/sdk/default
  android-sdk   环境变量 ANDROID_HOME、ANDROID_SDK_ROOT，再试 %LOCALAPPDATA%/Android/Sdk、~/Library/Android/sdk、~/Android/Sdk
  gradle-caches 环境变量 GRADLE_USER_HOME 下的 caches，再试 ~/.gradle/caches
  oh-docs       分支根目录下的 work/ohdocs
依赖库按坐标找：先找 Gradle 缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 aar / jar 里的这个包内路径，
再找解包后的 transforms 目录（…/transformed/<artifact>-<version>/<包内路径>）。"""
import sys

sys.dont_write_bytecode = True
import glob, io, json, os, re, zipfile  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LOCAL = os.path.join(ROOT, "work", "sources.local.json")
KIND_ROOT = {"harmony-dts": "harmony-sdk", "android-sdk": "android-sdk", "android-lib": "gradle-caches", "oh-docs": "oh-docs"}
EXT = re.compile(r"\.(?:d\.ts|d\.ets|xml|ets|ts|json5?|md|java|kt|kts|gradle|properties|txt|js)")
COORD = re.compile(r"^([A-Za-z0-9_.\-]+):([A-Za-z0-9_.\-]+):([A-Za-z0-9_.\-]+)\s+(.*)$", re.S)
ABS = re.compile(r"^(?:[A-Za-z]:[\\/]|[\\/]|~)")

_roots = None


def _first_dir(*cands):
    for c in cands:
        if c and os.path.isdir(c):
            return os.path.abspath(c)
    return None


def roots():
    """{来源: 本机目录（gradle-caches 是目录的列表）}；找不到的值是 None（或空列表）。"""
    global _roots
    if _roots is not None:
        return _roots
    cfg = {}
    if os.path.isfile(LOCAL):
        cfg = json.load(io.open(LOCAL, encoding="utf-8"))

    def fix(p):
        return p if os.path.isabs(p) else os.path.join(ROOT, p)
    env = os.environ.get
    home = os.path.expanduser("~")
    pf = [env("ProgramFiles"), env("ProgramW6432"), r"C:\Program Files"]
    def conf(k):                # 配了就先用配的（不存在时再按惯例找）
        v = cfg.get(k)
        return [fix(v)] if isinstance(v, str) and v.strip() else []
    r = {}
    r["harmony-sdk"] = _first_dir(*(conf("harmony-sdk") + [os.path.join(env("DEVECO_SDK_HOME") or "", "default"), env("DEVECO_SDK_HOME")] +
                                    [os.path.join(x, "Huawei", "DevEco Studio", "sdk", "default") for x in pf if x]))
    r["android-sdk"] = _first_dir(*(conf("android-sdk") + [env("ANDROID_HOME"), env("ANDROID_SDK_ROOT"),
                                    os.path.join(env("LOCALAPPDATA") or "", "Android", "Sdk"),
                                    os.path.join(home, "Library", "Android", "sdk"), os.path.join(home, "Android", "Sdk")]))
    gc = cfg.get("gradle-caches")
    gc = [gc] if isinstance(gc, str) else (gc or [])
    gc = [fix(x) for x in gc if isinstance(x, str)]
    gc = [x for x in gc if os.path.isdir(x)] or [os.path.join(env("GRADLE_USER_HOME") or os.path.join(home, ".gradle"), "caches")]
    r["gradle-caches"] = [os.path.abspath(x) for x in gc if os.path.isdir(x)]
    r["oh-docs"] = _first_dir(*(conf("oh-docs") + [os.path.join(ROOT, "work", "ohdocs")]))
    _roots = r
    return r


def is_absolute(where):
    return bool(ABS.match((where or "").strip().lstrip('"')))


def split_path(where, exists):
    """where → (相对路径, 后面的符号名)。路径取以已知扩展名结尾、且 exists(路径) 为真的最长前缀；都不存在时取第一个。"""
    w = (where or "").strip().split("\n")[0]
    ends = [m.end() for m in EXT.finditer(w)]
    for e in reversed(ends):
        if exists(w[:e]):
            return w[:e], w[e:].strip()
    if ends:
        return w[:ends[0]], w[ends[0]:].strip()
    return w.split()[0] if w.split() else "", " ".join(w.split()[1:])


_zip_cache, _tr_cache, _lib_cache, _file_cache = {}, {}, {}, {}


def _read(p):
    if p not in _file_cache:
        _file_cache[p] = io.open(p, encoding="utf-8", errors="replace").read()
    return _file_cache[p]


def _lib_entry(coord, inner):
    """依赖库包内文件的内容（str），找不到时 None。"""
    inner = inner.replace("\\", "/")
    k = (coord, inner)
    if k not in _lib_cache:
        _lib_cache[k] = _lib_entry_uncached(coord, inner)
    return _lib_cache[k]


def _lib_entry_uncached(coord, inner):
    g, a, v = coord
    for c in roots()["gradle-caches"]:
        # 坐标目录下实际有的 aar / jar 都看（包的文件名不一定是「构件名-版本」，如 navigation-common-release.aar）
        for p in sorted(glob.glob(os.path.join(c, "modules-2", "files-2.1", g, a, v, "*", "*.aar")) +
                        glob.glob(os.path.join(c, "modules-2", "files-2.1", g, a, v, "*", "*.jar"))):
            try:
                if p not in _zip_cache:
                    _zip_cache[p] = zipfile.ZipFile(p)
                z = _zip_cache[p]
                if inner in z.namelist():
                    return z.read(inner).decode("utf-8", errors="replace")
            except (OSError, zipfile.BadZipFile):
                continue
        key = (c, f"{a}-{v}")
        if key not in _tr_cache:
            _tr_cache[key] = glob.glob(os.path.join(c, "*", "transforms", "*", "transformed", f"{a}-{v}")) + \
                glob.glob(os.path.join(c, "transforms-*", "*", "transformed", f"{a}-{v}"))
        for d in _tr_cache[key]:
            p = os.path.join(d, *inner.split("/"))
            if os.path.isfile(p):
                return _read(p)
    return None


def resolve(kind, where):
    """refs 的一条定位 → (状态, 内容或说明, 文件名, 符号名)。状态：
      ok        找到了，内容是文件全文（str）
      url       在线地址（oh-docs 的旧写法），不核对
      absolute  写的是本机绝对路径（不许）
      no-root   本机没有配这个来源的根目录（不算引文错）
      no-lib    本机的 Gradle 缓存里没有这个库（不算引文错）
      no-file   根目录在，但找不到这个文件（算错）
      bad       写法认不出"""
    w = (where or "").strip().lstrip('"')
    if kind == "oh-docs" and re.match(r"https?://", w):
        url = w.split()[0]
        return "url", None, url.rstrip("/").rsplit("/", 1)[-1], w[len(url):].strip()
    if is_absolute(w):
        return "absolute", "where 要写来源里的相对路径，不能写本机绝对路径", "", ""
    rk = KIND_ROOT.get(kind)
    if not rk:
        return "bad", f"kind {kind} 不认识", "", ""
    if kind == "android-lib":
        m = COORD.match(w)
        if not m:
            return "bad", "依赖库的 where 要写「group:artifact:version 包内路径 资源名」", "", ""
        coord, rest = (m.group(1), m.group(2), m.group(3)), m.group(4)
        if not roots()["gradle-caches"]:
            return "no-root", "本机没有 Gradle 缓存目录（work/sources.local.json 的 gradle-caches）", "", ""
        found = {}

        def ex(p):
            if p not in found:
                found[p] = _lib_entry(coord, p)
            return found[p] is not None
        inner, sym = split_path(rest, ex)
        if not ex(inner):
            have = any(glob.glob(os.path.join(c, "modules-2", "files-2.1", coord[0], coord[1], coord[2])) for c in roots()["gradle-caches"])
            if not have and not any(_tr_cache.get((c, f"{coord[1]}-{coord[2]}")) for c in roots()["gradle-caches"]):
                return "no-lib", f"本机没有这个库（{':'.join(coord)}）", os.path.basename(inner), sym
            return "no-file", f"{':'.join(coord)} 里没有 {inner}", os.path.basename(inner), sym
        return "ok", found[inner], os.path.basename(inner), sym
    base = roots()[rk]
    if not base:
        return "no-root", f"本机没有配 {rk} 的根目录（work/sources.local.json）", "", ""
    rel, sym = split_path(w, lambda p: os.path.isfile(os.path.join(base, *p.replace("\\", "/").split("/"))))
    p = os.path.join(base, *rel.replace("\\", "/").split("/"))
    if not os.path.isfile(p):
        return "no-file", f"{rk} 下没有 {rel}", os.path.basename(rel), sym
    try:
        return "ok", _read(p), os.path.basename(rel), sym
    except OSError as e:
        return "no-file", str(e), os.path.basename(rel), sym


def describe():
    """给子代理看的：本机各来源的根目录（它们要打开文件时用根目录接上相对路径）。"""
    r = roots()
    out = []
    for k in ("harmony-sdk", "android-sdk", "gradle-caches", "oh-docs"):
        v = r.get(k)
        out.append(f"{k}: " + ((" ; ".join(v) if v else "（没有）") if isinstance(v, list) else (v or "（没有）")))
    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(describe())
