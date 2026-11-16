# -*- coding: utf-8 -*-
"""memory-rules 各脚本共用的小工具：路径、读写 JSON、产物目录名、规矩号、词的切分和 IDF 余弦相似度。

词的切分（聚类、归族、召回共用）：
  - 标识符：按 [A-Za-z_$@?][A-Za-z0-9_$]* 切，允许用 . : / # 连成限定名（android:shadowColor、Text.textShadow、@color/x）。
    每个标识符产出「整体」词：整个限定名、按 . : / # 拆开的每一段（都转小写，去掉开头的 @ ? $）；以及「部分」词：每一段再按
    下划线和驼峰拆开、3 个字符以上的部分。整体词权重 1，部分词权重 0.5（同一个词两种都有时取 1）。
  - 语言关键字（public、return、const、this……）不算词。
  - 中文（只在聚类和归族里用，召回不用）：连续汉字切成两字一组的 bigram，权重 1。
相似度：IDF 在同一批文档上算，idf = ln((N + 1) / (df + 1)) + 1；文档向量的分量是 idf × 权重；两文档的相似度是余弦。"""
import sys

sys.dont_write_bytecode = True
import hashlib, io, json, math, os, re  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
STORE = os.path.join(ROOT, "store")
WORK = os.path.join(ROOT, "work")
INDEX = os.path.join(WORK, "cards_index.json")
PRODUCT_DIRS = {"规格": "spec", "计划与派工": "plan", "代码": "code", "资源": "resource"}
DIR_RX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOKEN = re.compile(r"[A-Za-z_$@?][A-Za-z0-9_$]*(?:[.:/#][A-Za-z_$][A-Za-z0-9_$]*)*")
CJK = re.compile(r"[一-鿿]+")
KEYWORDS = set("""abstract and as assert async await boolean break byte case catch char class const continue declare def default
delete do double else enum export extends false final finally float for from function if implements import in instanceof int
interface is let long native new null number object of override package private protected public readonly return short
static string super switch synchronized this throw throws transient true try type typeof undefined val var void volatile
while with yield fun when the and or not""".split())


def jload(p, default=None):
    if default is not None and not os.path.isfile(p):
        return default
    return json.load(io.open(p, encoding="utf-8"))


def jsave(p, o):
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(o, ensure_ascii=False, indent=1) + "\n")


def relpath(p):
    """写进批次清单、报告的路径：在分支根目录下的写相对分支根目录的路径（用 /），不写本机路径；不在分支里的原样。
    读的时候相对路径（相对分支根目录）和绝对路径都认，见 resolve_path。"""
    if not isinstance(p, str) or not p:
        return p
    a = os.path.abspath(p)
    r = os.path.abspath(ROOT)
    if os.path.normcase(a) == os.path.normcase(r):
        return "."
    if os.path.normcase(a).startswith(os.path.normcase(r) + os.sep):
        return a[len(r) + 1:].replace("\\", "/")
    return p


def resolve_path(p):
    """批次清单里的一行 → 本机路径：绝对路径原样，相对路径接在分支根目录后面。"""
    p = (p or "").strip()
    return p if os.path.isabs(p) else os.path.join(ROOT, *p.split("/"))


def rel_params(ns):
    """argparse 的参数 → 报告里的 params：字符串参数里的路径改成相对分支根目录的。"""
    return {k: (relpath(v) if isinstance(v, str) and (os.sep in v or "/" in v) else v) for k, v in vars(ns).items()}


def rule_id(product, title):
    return "rule-" + hashlib.sha1(f"{product}\n{title}".encode("utf-8")).hexdigest()[:12]


def camel_parts(seg):
    out = []
    for p in seg.split("_"):
        out += re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", p)
    return [x.lower() for x in out if len(x) >= 3]


def ident_terms(text):
    """{词: 权重}：文本里标识符的整体词（1）和部分词（0.5）。"""
    out = {}
    for m in TOKEN.finditer(text or ""):
        tok = m.group(0).lstrip("@?$")
        if not tok:
            continue
        segs = [s for s in re.split(r"[.:/#]", tok) if s]
        wholes = [tok.lower()] + [s.lower() for s in segs] if len(segs) > 1 else [tok.lower()]
        for w in wholes:
            if len(w) >= 2 and w not in KEYWORDS:
                out[w] = 1.0
        for s in segs:
            for p in camel_parts(s):
                if p not in KEYWORDS and p not in out:
                    out[p] = 0.5
    return out


def cjk_terms(text):
    out = {}
    for m in CJK.finditer(text or ""):
        s = m.group(0)
        for i in range(len(s) - 1):
            out[s[i:i + 2]] = 1.0
    return out


def merge_terms(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            out[k] = max(out.get(k, 0), v)
    return out


def idf_table(docs):
    n = len(docs)
    df = {}
    for d in docs:
        for t in d:
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}, n


def vector(terms, idf):
    v = {t: w * idf.get(t, 0.0) for t, w in terms.items() if idf.get(t)}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return v, norm


def cosine(a, b):
    (va, na), (vb, nb) = a, b
    if len(va) > len(vb):
        va, vb = vb, va
    return sum(x * vb[t] for t, x in va.items() if t in vb) / (na * nb)


def components(n, edges):
    """无向图的连通分量：edges 是 [(i, j)]，返回 [[成员下标…]]。"""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, j in edges:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def split_by_threshold(members, sims, threshold, max_size, step=0.05):
    """members 是下标列表，sims[(i, j)] (i < j) 是相似度。在 threshold 下连成分量，超过 max_size 的分量提高阈值再拆，
    直到都不超过 max_size；阈值到 1 仍拆不开的按相似度贪心切块。返回 [(成员列表, 拆出它时用的阈值)]。"""
    idx = {m: k for k, m in enumerate(members)}
    edges = [(idx[i], idx[j]) for (i, j), s in sims.items() if i in idx and j in idx and s >= threshold]
    out = []
    for comp in components(len(members), edges):
        group = [members[k] for k in comp]
        if len(group) <= max_size:
            out.append((group, threshold))
        elif threshold + step <= 1.0 + 1e-9:
            out += split_by_threshold(group, sims, round(threshold + step, 4), max_size, step)
        else:
            rest = list(group)
            while rest:
                seed = rest.pop(0)
                rest.sort(key=lambda x: -sims.get((min(seed, x), max(seed, x)), 0))
                chunk, rest = [seed] + rest[:max_size - 1], rest[max_size - 1:]
                out.append((chunk, threshold))
    return out


def pair_sims(vecs, floor=0.0, active=None):
    """{(i, j): 相似度}（i < j），只留大于 floor 的。给了 active（下标集合）时只算至少一头在 active 里的对
    （增量归并：新候选之间、新候选和已有规矩之间；已有规矩彼此之间不算）。先用共有词过滤掉没有交集的对。"""
    out = {}
    n = len(vecs)
    keys = [set(v[0]) for v in vecs]
    inv = {}
    for i, ks in enumerate(keys):
        for t in ks:
            inv.setdefault(t, []).append(i)
    for i in range(n):
        if active is not None and i not in active:
            cand = set()
            for t in keys[i]:
                cand.update(j for j in inv[t] if j > i and j in active)
        else:
            cand = set()
            for t in keys[i]:
                cand.update(j for j in inv[t] if j > i)
        for j in cand:
            s = cosine(vecs[i], vecs[j])
            if s > floor:
                out[(i, j)] = s
    return out


def quantiles(xs, qs=(0.5, 0.75, 0.9, 0.99, 1.0)):
    if not xs:
        return {}
    s = sorted(xs)
    return {str(q): round(s[min(len(s) - 1, int(len(s) * q))], 3) for q in qs}


def load_candidates(d):
    """[(临时号「卡号#序号」, 卡号, 序号, 规矩)]：d 下每个 <卡号>.json 的 rules。"""
    out = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        o = jload(os.path.join(d, fn))
        case = o.get("case") or fn[:-5]
        for i, r in enumerate(o.get("rules") or [], 1):
            out.append((f"{case}#{i}", case, i, r))
    return out


def load_rules(d):
    """{规矩号: 规矩}：d 下的 rule-*.json。"""
    return {fn[:-5]: jload(os.path.join(d, fn)) for fn in sorted(os.listdir(d)) if fn.startswith("rule-") and fn.endswith(".json")}
