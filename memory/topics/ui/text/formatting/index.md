# ui/text/formatting

显示值的加工在目标端复现：AnnotatedString 加工、setSpan 开区间、格式化精度与带兜底的访问器。

[上一级](../index.md)

## 本级经验

- [AnnotatedString 的链接识别与点击一并迁](lesson-57a52be767730880cbba.lesson.md) · 阶段：execute · 信号：AnnotatedString, buildAnnotatedStringWithUrls, LinkAnnotation, StyledString
- [setSpan 转 Span 按 end 开区间逐字核范围](lesson-eb59a95e5eb219c238b0.lesson.md) · 阶段：execute · 信号：SpannableString, setSpan, Span, ForegroundColorSpan
- [复用基类格式化 getter 前核精度，不同则子类全覆写](lesson-042445ba332611e04a80.lesson.md) · 阶段：execute · 信号：formatPrice, getPrice(, getValue(, toFixed
- [源端用兜底访问器取显示值，目标调等价访问器不自拟兜底](lesson-1fa08bf929cfced0ff34.lesson.md) · 阶段：execute · 信号：ResourceStr, toString(), $r(
