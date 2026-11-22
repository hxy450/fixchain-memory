# -*- coding: utf-8 -*-
"""把 OpenHarmony 文档仓库的最新 master 同步到本机一个目录（只取 zh-cn/application-dev 下的 .md），打印提交号和提交日期。
每次开工先跑一遍；知识文件 sdk 栏的 docs_commit、docs_date 就填它打印的值。

  目录不存在：git clone --filter=blob:none --no-checkout --depth 1 https://gitcode.com/openharmony/docs.git <目录>
              git -C <目录> sparse-checkout init --no-cone
              git -C <目录> sparse-checkout set '/zh-cn/application-dev/**/*.md'
              git -C <目录> checkout master
  目录已存在：git -C <目录> fetch --depth 1 origin master，再 git -C <目录> reset --hard FETCH_HEAD（拉到最新 master）。
              工作区有改动（git status --porcelain 不空）时不拉，报出来退出：同步目录只当只读镜像用，不在里面改东西。
  --dry-run：只打印要跑的命令；目录已存在时打印它现在的提交号和日期（只读）。
  --show：只读，打印同步目录现在的提交号和日期，不联网、不改目录（几个人共用一个同步目录时，写的人只用这个）。

几个人共用一个同步目录时：同时拉会在 .git 里抢锁（index.lock），一个人拉的时候别人读到的文件可能半新半旧，各人记的提交号也会不同。
所以只由协调方在开工前拉一次，写的人只跑 --show 记提交号；协调方在写的人做完之前不再拉。
脚本自己也加了一把锁：拉之前在 <目录>/.git/ 下建 sync_ohdocs.lock（新建目录时建在目录旁边的 <目录>.sync.lock），
已有锁就不拉、报出来退出；拉完删锁。上次异常退出留下的锁，确认没人在拉之后手动删掉。

单篇原文也可以直接取：https://raw.gitcode.com/openharmony/docs/raw/master/<仓库内路径>（返回 Markdown 原文）；
gitcode.com/…/raw/… 那种返回的是网页，不能用。出处里写的是 blob 链接，见 ohdocs_link.py。

用法：py -3.12 -B -X utf8 sync_ohdocs.py <目录> [--dry-run | --show]
要 git 2.25 以上（sparse-checkout）。只用标准库。"""
import sys

sys.dont_write_bytecode = True
import os, subprocess  # noqa: E401,E402

REPO = "https://gitcode.com/openharmony/docs.git"
SPARSE = "/zh-cn/application-dev/**/*.md"


def git(args, cwd=None, capture=False):
    r = subprocess.run(["git"] + args, cwd=cwd, text=True, encoding="utf-8",
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失败（退出码 {r.returncode}）" + (f"：{(r.stderr or '').strip()}" if capture else ""))
    return (r.stdout or "").strip() if capture else ""


def head(d):
    h, iso, short = git(["log", "-1", "--format=%H%n%cI%n%cd", "--date=short"], cwd=d, capture=True).split("\n")
    return h, iso, short


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    d = os.path.abspath(args[0])
    dry = "--dry-run" in argv
    exists = os.path.isdir(os.path.join(d, ".git"))
    if "--show" in argv:
        if not exists:
            raise SystemExit(f"{d} 还没有同步过（不是 git 目录）；请协调方先跑一次不带 --show 的同步")
        h, iso, short = head(d)
        print(f"OpenHarmony 文档 master（同步目录现状，只读）：提交 {h}，提交日期 {short}（{iso}）")
        print(f"知识文件 sdk 栏填：docs_commit = {h}，docs_date = {short}")
        return 0
    if exists:
        cmds = [["fetch", "--depth", "1", "origin", "master"], ["reset", "--hard", "FETCH_HEAD"]]
    else:
        if os.path.exists(d) and os.listdir(d):
            raise SystemExit(f"{d} 已存在、不是 git 目录、也不空；换一个目录或先清掉")
        cmds = [["clone", "--filter=blob:none", "--no-checkout", "--depth", "1", REPO, d],
                ["sparse-checkout", "init", "--no-cone"], ["sparse-checkout", "set", SPARSE], ["checkout", "master"]]
    if dry:
        for c in cmds:
            print("将要跑：git " + ("" if c[0] == "clone" else f"-C {d} ") + " ".join(c))
        if exists:
            h, iso, short = head(d)
            print(f"现在：提交 {h}，提交日期 {short}（{iso}）")
        return 0
    lock = os.path.join(d, ".git", "sync_ohdocs.lock") if exists else d.rstrip("\\/") + ".sync.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(f"有人正在同步（锁 {lock} 在）；等他拉完，或确认没人在拉之后删掉这个锁再跑")
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    try:
        if exists:
            dirty = git(["status", "--porcelain"], cwd=d, capture=True)
            if dirty:
                raise SystemExit("同步目录里有改动，不拉；先处理掉：\n" + dirty[:2000])
            before = head(d)[0]
            for c in cmds:
                git(c, cwd=d)
        else:
            before = None
            git(cmds[0])
            for c in cmds[1:]:
                git(c, cwd=d)
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass
    h, iso, short = head(d)
    n = sum(len([f for f in fs if f.endswith(".md")]) for r, _, fs in os.walk(os.path.join(d, "zh-cn", "application-dev")))
    print(f"OpenHarmony 文档 master：提交 {h}，提交日期 {short}（{iso}）；application-dev 下 .md {n} 个"
          + ("" if before is None else ("；和同步前相同" if before == h else f"；同步前是 {before[:8]}")))
    print(f"知识文件 sdk 栏填：docs_commit = {h}，docs_date = {short}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
