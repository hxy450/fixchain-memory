# -*- coding: utf-8 -*-
"""查鸿蒙声明的小工具（只读，只用标准库）。

对 .d.ts 里每一行匹配正则的（不是注释行），打印它前面最后一段 jsdoc 注释（去掉 @since 以外的标签行）、所属的
class / interface / namespace / enum / type，以及这一行本身。一个方法前常有好几段注释，最后一段是当前版本的说法；
「从哪一版开始有」要看首段注释的 @since，标题行里另外打印出来（照最后一段写起始版本是常见的错）。
默认把匹配的每一处都打出来（同名的各个重载、多处声明，如组件的 interface 和 Attribute 类、新旧两个版本的声明），
末尾打总数。maxhits 给正数才截，截了会说还剩几处。

用法：py -3.12 -B -X utf8 -I dts_lookup.py <.d.ts 文件> <正则> [maxhits]"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    print(__doc__)
    sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help') else 2)
path, pat = sys.argv[1], sys.argv[2]
maxhits = int(sys.argv[3]) if len(sys.argv) > 3 else 0
lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
rx = re.compile(pat)
skip = re.compile(r'@(crossplatform|atomicservice|form|syscap|FaAndStageModel|systemapi|stagemodelonly|arkts\s*1\.\d)\b')
def first_since(lines, k):
    """lines[k] is the '/**' of the last comment block before the declaration. Walk up over the stacked blocks
    (only blank lines between them) and return the @since of the topmost one, with how many blocks there are."""
    top, n = k, 1
    while True:
        m = top - 1
        while m >= 0 and lines[m].strip() == '':
            m -= 1
        if m >= 0 and lines[m].strip().endswith('*/'):
            q = m
            while q >= 0 and '/**' not in lines[q]:
                q -= 1
            if q < 0:
                break
            top, n = q, n + 1
        else:
            break
    end = top
    while end < len(lines) and '*/' not in lines[end]:
        end += 1
    for x in lines[top:end + 1]:
        mm = re.search(r'@since\s+([\w.]+)', x)
        if mm:
            return mm.group(1), n
    return None, n


hits = 0
total = sum(1 for l in lines if rx.search(l) and not l.strip().startswith('*'))
for i, l in enumerate(lines):
    if rx.search(l) and not l.strip().startswith('*'):
        # find last doc block end before i
        j = i - 1
        while j >= 0 and lines[j].strip() == '':
            j -= 1
        block = []
        fs, nblocks = None, 0
        if j >= 0 and lines[j].strip().endswith('*/'):
            k = j
            while k >= 0 and '/**' not in lines[k]:
                k -= 1
            block = lines[k:j+1]
            fs, nblocks = first_since(lines, k)
        # find enclosing container
        depth = 0; owner = ''
        for m in range(i - 1, -1, -1):
            s = lines[m]
            depth += s.count('}') - s.count('{')
            if depth < 0:
                mm = re.search(r'(class|interface|namespace|enum|type)\s+(\w+)', s)
                if mm:
                    owner = mm.group(0); break
                depth = 0
        print(f'--- L{i+1} owner=[{owner}]' + (f'  起始版本（首段注释的 @since，共 {nblocks} 段）= {fs}' if nblocks else ''))
        for b in block:
            bs = b.strip()
            if skip.search(bs) or bs in ('*', '/**', '*/'):
                continue
            print('   ', bs[:220])
        print('>>', l.strip()[:300])
        hits += 1
        if maxhits > 0 and hits >= maxhits:
            break
print(f'=== 共 {total} 处匹配' + (f'，只打了前 {hits} 处，还有 {total - hits} 处没打（去掉 maxhits 全打）' if hits < total
                            else '，都在上面（同名的重载、多处声明逐一看，起始版本各看各的首段 @since）'))
