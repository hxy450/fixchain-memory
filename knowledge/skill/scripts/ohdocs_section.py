# -*- coding: utf-8 -*-
"""从文档同步目录里取「整个小节」来读（只读，只用标准库）。

为什么有它：核过的条目有出入的，多半是只读了出处的一处，漏了同一小节的「说明」「注意」、同名接口的另一处
（如 deprecated 的旧版本、别的重载）。这个脚本把整节原文和别处的线索一起打出来，读全成为默认。

打印：
  1. 小节名或关键词匹配到的每个小节的**全文**：从这个标题到下一个同级或更高级标题（下级小节、「说明」「注意」
     「警告」块、表格、示例都在内）；不截断。标题完全相同的（如同名接口的新版和 deprecated 版）都打。
  2. 这个小节的各级上级小节开头（到第一个下级标题为止）里的「说明」「注意」「警告」块，如模块开头的
     「本模块首批接口从 API version N 开始支持」；以及那里提到关键词的段落（常是「这几个组件默认就…」这类例外）。
  3. 同一个文件里别的提到同一关键词的小节：只列标题和行号，提醒去看。
  4. 出处写法：链接加小节名（出处里不写行号）。

用法：
  py -3.12 -B -X utf8 ohdocs_section.py <同步目录> <文件> <小节名或关键词> [--also 关键词 …] [--all]
    <文件>  仓库内路径（zh-cn/application-dev/…）、相对 application-dev 的路径、同步目录里的绝对路径，或只写文件名
    小节名  先按标题全等找（忽略 <sup>…</sup>、反引号、大小写），没有再按「标题包含」找；包含匹配超过 3 个时
            只列标题，要加 --all 才全打
    --also  第 3 项另外要搜的关键词（如接口名的另一种写法、参数类型名）"""
import sys

sys.dont_write_bytecode = True
import argparse, html, os, re  # noqa: E401,E402

BLOB = "https://gitcode.com/openharmony/docs/blob/master/"
PREFIX = "zh-cn/application-dev/"
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
NOTE = re.compile(r"说明|注意|警告|NOTE|Note|WARNING|CAUTION")


def norm(s, keep_sup=False):
    s = html.unescape(s)
    if not keep_sup:
        s = re.sub(r"<sup>.*?</sup>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("`", "").replace("\\", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def resolve_file(root, arg):
    cands = [arg, os.path.join(root, arg), os.path.join(root, PREFIX, arg)]
    for c in cands:
        if os.path.isfile(c):
            return [os.path.abspath(c)]
    name = os.path.basename(arg).lower()
    hits = []
    for r, _, fs in os.walk(os.path.join(root, *PREFIX.strip("/").split("/"))):
        for f in fs:
            if f.lower() == name:
                hits.append(os.path.join(r, f))
    return sorted(hits)


def repo_rel(root, path):
    return os.path.relpath(path, root).replace("\\", "/")


def headings(lines):
    out, fence = [], False
    for i, l in enumerate(lines):
        if FENCE.match(l):
            fence = not fence
            continue
        if fence:
            continue
        m = HEAD.match(l)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def section_end(heads, k, n):
    i, lvl, _ = heads[k]
    for j in range(k + 1, len(heads)):
        if heads[j][1] <= lvl:
            return heads[j][0]
    return n


def note_blocks(lines, a, b):
    """lines[a:b] 里含「说明 / 注意 / 警告」的引用块（连续的 > 行）。"""
    out, cur = [], []
    for i in range(a, b):
        if lines[i].lstrip().startswith(">"):
            cur.append(i)
        else:
            if cur and any(NOTE.search(lines[x]) for x in cur):
                out.append(cur)
            cur = []
    if cur and any(NOTE.search(lines[x]) for x in cur):
        out.append(cur)
    return out


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("file")
    ap.add_argument("query")
    ap.add_argument("--also", nargs="+", default=[])
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    files = resolve_file(a.root, a.file)
    if not files:
        print(f"同步目录里没有 {a.file}（按文件名也没找到；先用 ohdocs_link.py --find 或从 Readme-CN.md 顺着链接找）")
        return 1
    if len(files) > 1:
        print(f"文件名 {a.file} 有 {len(files)} 个，改给仓库内路径：")
        for f in files:
            print("  " + repo_rel(a.root, f))
        return 2
    path = files[0]
    rel = repo_rel(a.root, path)
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    heads = headings(lines)
    q = norm(a.query)
    exact = [k for k, h in enumerate(heads) if norm(h[2]) == q or norm(h[2], True) == q]
    contains = [k for k, h in enumerate(heads) if q in norm(h[2], True)]
    picked = exact or contains
    print(f"文件：{rel}（{len(lines)} 行，标题 {len(heads)} 个）")
    if not picked:
        print(f"没有标题是或包含「{a.query}」。下面第 3 项列出正文里提到它的小节。")
    elif not exact and len(contains) > 3 and not a.all:
        print(f"没有标题全等于「{a.query}」；包含它的标题有 {len(contains)} 个（加 --all 全打，或写全小节名）：")
        for k in contains:
            i, lvl, t = heads[k]
            print(f"  第 {i + 1} 行 {'#' * lvl} {t}")
        picked = []
    kws = [a.query] + a.also
    for k in picked:
        base = re.match(r"[\w.]+", norm(heads[k][2]))
        if base and base.group(0) not in [x.lower() for x in kws] and len(base.group(0)) >= 4:
            kws.append(base.group(0))
    kws = list(dict.fromkeys(kws))
    has_kw = lambda s: any(kw.lower() in html.unescape(s).lower() for kw in kws)  # noqa: E731
    shown = set()
    for k in picked:
        i, lvl, t = heads[k]
        end = section_end(heads, k, len(lines))
        while end > i + 1 and not lines[end - 1].strip():
            end -= 1
        shown.update(range(i, end))
        print(f"\n======== 第 {i + 1}–{end} 行：{'#' * lvl} {t}（整节，共 {end - i} 行）========")
        print("\n".join(lines[i:end]))
        # 上级小节开头的说明块
        anc, want = [], lvl
        for kk in range(k - 1, -1, -1):
            if heads[kk][1] < want:
                anc.append(kk)
                want = heads[kk][1]
        for kk in anc:
            ai, al, at = heads[kk]
            first_child = next((heads[j][0] for j in range(kk + 1, len(heads))), len(lines))
            blocks = [b for b in note_blocks(lines, ai + 1, first_child) if b[0] not in shown]
            for b in blocks:
                print(f"\n-------- 上级小节「{'#' * al} {at}」开头的说明块（第 {b[0] + 1}–{b[-1] + 1} 行）--------")
                print("\n".join(lines[x] for x in b))
                shown.update(b)
            kl = [x for x in range(ai + 1, first_child) if x not in shown and has_kw(lines[x])]
            if kl:
                print(f"\n-------- 上级小节「{'#' * al} {at}」开头提到关键词的段落 --------")
                for x in kl:
                    print(f"（第 {x + 1} 行）{lines[x]}")
                shown.update(kl)
        plain = re.sub(r"<[^>]+>", "", re.sub(r"<sup>.*?</sup>", "", html.unescape(t))).strip()
        print(f"\n出处写法：{BLOB}{rel}，{plain}")
    # 别处提到同一关键词的小节
    hits = {}
    hidx = [h[0] for h in heads]
    for i, l in enumerate(lines):
        if i in shown or not has_kw(l):
            continue
        owner = None
        for k in range(len(hidx) - 1, -1, -1):
            if hidx[k] <= i:
                owner = k
                break
        if owner is None:
            continue
        hits[owner] = hits.get(owner, 0) + 1
    print(f"\n同一文件里别处提到「{'」「'.join(kws)}」的小节（只列标题，去看有没有例外、旧版本、别的重载）：")
    if not hits:
        print("  没有")
    for n, (k, c) in enumerate(sorted(hits.items())):
        if n >= 40:
            print(f"  …还有 {len(hits) - 40} 个")
            break
        i, lvl, t = heads[k]
        print(f"  第 {i + 1} 行 {'#' * lvl} {t}（{c} 处）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
