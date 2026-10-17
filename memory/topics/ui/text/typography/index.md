# ui/text/typography

文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

[上一级](../index.md)

## 本级经验

- [ellipsize=middle 无枚举时测量实现中间截断](lesson-a184209501ba02cb62e7.lesson.md) · 阶段：execute · 信号：ellipsize="middle", android:ellipsize, TextOverflow, measureText
- [动态文本字号行距按 dp×文字倍率落 vp，几何才乘画布比例](lesson-4c494b9f89c7e9db2b55.lesson.md) · 阶段：execute · 信号：dynamicTextScale, fontSizeScale, dpF, lineSpacing
- [单行盒高与多行行距分开，lineHeight 不同名直映](lesson-2a2924aaebbfbea80780.lesson.md) · 阶段：spec/execute/repair · 信号：lineHeight, .lineHeight(), lineSpacing, LengthMetrics.fp
- [单行省略补 BREAK_ALL，多行末行写差异](lesson-836a5414b52f0e062f1f.lesson.md) · 阶段：spec/execute · 信号：maxLines, TextOverflow.Ellipsis, android:ellipsize, textOverflow
- [可折叠正文按测量高度判溢出，默认 Clip](lesson-c61ac79c7db81729a544.lesson.md) · 阶段：execute/verify · 信号：onTextLayout, didOverflowHeight, hasVisualOverflow, maxLines
- [可能为空的 Text 保留一行高，不条件渲染](lesson-6668f8800d3ddaaf52ed.lesson.md) · 阶段：execute · 信号：TextView, wrap_content, INVISIBLE, Visibility.Hidden
- [缺枚举的 FontWeight 写数值，不换近名](lesson-605038b091e03c26c005.lesson.md) · 阶段：execute/repair · 信号：FontWeight.SemiBold, FontWeight.Light, FontWeight.ExtraBold, FontWeight.Thin
