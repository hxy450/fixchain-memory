# -*- coding: utf-8 -*-
"""把本机同步目录（sync_ohdocs.py 建的）里的文档路径换成出处用的链接，或反过来（只读，只用标准库）。

出处链接：https://gitcode.com/openharmony/docs/blob/master/zh-cn/application-dev/<路径>.md，后面接「，小节名」。
  to_link(path, root=None)  path 可以是同步目录里的绝对路径，或仓库内相对路径（zh-cn/application-dev/…），
                             或相对 application-dev 的路径（reference/apis-arkui/…）；给 raw=True 出原文链接
                             （https://raw.gitcode.com/openharmony/docs/raw/master/<仓库内路径>，取原文用，不写进出处）。
  from_link(url)            链接 → 仓库内相对路径（不是这个仓库 master 的 blob / raw 链接返回 None）。
  find(root, name)          按文件名在同步目录里找（把旧写法「文档 xxx.md，小节名」换成链接时用），返回仓库内相对路径列表。

用法：
  py -3.12 -B -X utf8 ohdocs_link.py <路径> […]               打印链接
  py -3.12 -B -X utf8 ohdocs_link.py --raw <路径> […]         打印原文链接
  py -3.12 -B -X utf8 ohdocs_link.py --root <同步目录> --find js-apis-http.md […]
  py -3.12 -B -X utf8 ohdocs_link.py --back <链接> […]        打印仓库内相对路径"""
import sys

sys.dont_write_bytecode = True
import os, re  # noqa: E401,E402

BLOB = "https://gitcode.com/openharmony/docs/blob/master/"
RAW = "https://raw.gitcode.com/openharmony/docs/raw/master/"
PREFIX = "zh-cn/application-dev/"
LINK_RX = re.compile(r"https://(?:gitcode\.com/openharmony/docs/blob|raw\.gitcode\.com/openharmony/docs/raw)/master/"
                     r"(zh-cn/application-dev/[^\s，,；;）)]+?\.md)")


def repo_path(path, root=None):
    p = path.replace("\\", "/").strip()
    if root:
        r = os.path.abspath(root).replace("\\", "/").rstrip("/") + "/"
        ap = os.path.abspath(path).replace("\\", "/")
        if ap.lower().startswith(r.lower()):
            p = ap[len(r):]
    p = p.lstrip("./")
    if not p.startswith(PREFIX):
        p = p[len("application-dev/"):] if p.startswith("application-dev/") else p
        p = PREFIX + p
    if not p.endswith(".md"):
        raise ValueError(f"不是 .md：{path}")
    return p


def to_link(path, root=None, raw=False):
    return (RAW if raw else BLOB) + repo_path(path, root)


def from_link(url):
    m = LINK_RX.search(url or "")
    return m.group(1) if m else None


def find(root, name):
    out = []
    base = os.path.join(root, "zh-cn", "application-dev")
    for r, _, fs in os.walk(base):
        for f in fs:
            if f.lower() == name.lower():
                out.append(repo_path(os.path.join(r, f), root))
    return sorted(out)


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    root = None
    if "--root" in argv:
        i = argv.index("--root")
        root = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    raw, back, fnd = "--raw" in argv, "--back" in argv, "--find" in argv
    items = [a for a in argv if not a.startswith("--")]
    if not items:
        print(__doc__)
        return 2
    rc = 0
    for x in items:
        if back:
            print(from_link(x) or f"（不是 OpenHarmony 文档 master 的链接）{x}")
        elif fnd:
            if not root:
                raise SystemExit("--find 要给 --root <同步目录>")
            hits = find(root, x)
            if not hits:
                print(f"{x}：同步目录里没有这个文件")
                rc = 1
            for h in hits:
                print(f"{x}\t{BLOB + h}")
        else:
            print(to_link(x, root, raw))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
