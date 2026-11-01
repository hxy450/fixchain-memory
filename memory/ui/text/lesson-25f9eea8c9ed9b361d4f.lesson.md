# 自研 Markdown 或富文本把文本按多条规则切成 run 时，命中与间隔文本按原位置顺序输出、未闭合的分隔符按字面保留；契约同时覆盖解析库的核心语法

ID：`lesson-25f9eea8c9ed9b361d4f` · 版本：2

[本主题](index.md)

## 何时使用

Markdown 渲染的规格提取与解析实现阶段，确定语法覆盖、文本切分后 run 的拼装顺序与自动链接规则时；为共用首字符的长短分隔符（** 与 *）编写未闭合回退路径时

## 适用情境

源端用 Markwon 一类库（CommonMark 核心解析，加 Linkify、提及简写等文本插件，按触点命中 span）渲染 Markdown；目标自研解析器，把文本切成有序 run 序列交给 StyledString/Span 渲染。 也包括以单趟扫描替代 react-markdown/remark-gfm 等 CommonMark 渲染器，依次判断 `code`、[text](url)、**bold**、*italic*，并承诺不成对标记按字面文本输出。

## 原因

在循环里先把每个命中推入结果、间隔文本留到循环结束才输出，链接会排到前文之前；正则逐行的块解析丢掉嵌套、惰性续行与松紧列表。只按插件清单写验收时，核心语法没有任何条目约束，单测只测正则命中也发现不了顺序错乱。 较长分隔符找不到闭合时若落入共享首字符的较短分隔符分支，短分支会把长分隔符的第二个字符当作闭合，`**b` 变成空斜体加 b，两颗星丢失；CommonMark 对未匹配的分隔序列按字面文本输出。

## 做法

1. 切 run 时单次扫描合并各规则的命中区间，按原位置依次输出间隔文本与命中；单测断言 run 文本拼接等于原文、链接位置不变。
2. 较长分隔符（**、~~、```）找不到闭合时，把整段分隔符写入字面缓冲并跳过，不落入共享首字符的较短分隔符分支；单测覆盖只有开头标记的输入（`**b`、`*a`、`` `c ``、`[x`），断言同一行 span 文本拼接等于原行。
3. 规格迁移整套 Markdown 库时，契约同时覆盖库的 CommonMark 核心语法（嵌套、惰性续行、松紧列表、引用内的块、行内元素按原文顺序）与插件，并给核心语法可断言的样例。
4. 验收写明平台匹配语义（如 Linkify WEB_URLS）时，移植源平台正则（含无协议域名与过滤规则），与其他规则重叠时按源端监听注册顺序处理，不缩窄匹配范围。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4c5f901f2b0bbfd26152](../../../store/cases/case-4c5f901f2b0bbfd26152/e737b62ac2d27d7231cd09d70b8d9a3806dbd845a07a2d678fa39858f0f6d498.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e737b62ac2d27d7231cd09d70b8d9a3806dbd845a07a2d678fa39858f0f6d498`
- [case-8b307e33adf3d2817a04](../../../store/cases/case-8b307e33adf3d2817a04/2585469b6f2560d0a8b4e6ced070f91257eea43766cb634ab5779774aabdcc80.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`2585469b6f2560d0a8b4e6ced070f91257eea43766cb634ab5779774aabdcc80`
