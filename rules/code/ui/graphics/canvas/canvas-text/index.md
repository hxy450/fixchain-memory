# 自绘 View 里的文字度量和 drawText

agent 会看到什么：读到自定义 View 用 Paint.ascent/descent、getTextBounds 算文字位置，用 canvas.drawText 画字；产物里 Canvas 的 TextMetrics 字段取错、fillText 前没设 direction，或多画了源端没画的文字

## 规矩

- rule-0d2fb8f4cd3f｜Paint.ascent/descent 算基线偏移时，目标取 emHeightAscent/Descent｜读到：安卓自绘 View 用 `Paint.ascent()` / `Paint.descent()`（主字体的字体级上下伸，ascent 为负）算文字垂直居中的基线偏移，如 `(descent() + ascent()) / 2`；写错：目标里写成 `fontBoundingBoxDescent - fontBoundingBoxAscent` 或用 actualBoundingBoxAscent/Descent 代替，注释称与源式同值
- rule-25bb87b5d3f5｜代码按 getTextBounds 算文字高度时，写 actualBoundingBox 两项各自 Math.ceil｜读到：源端 Paint.getTextBounds(text, start, end, rect) 后用 rect.height() 作文字高度；写错：目标写成 Math.trunc(m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)，或带着「需实测 hhea」注释保留 fontBoundingBox*
- rule-c301a279b2c3｜drawText 用默认 Paint 时，每次 fillText 前按首个强方向字符设 ctx.direction｜读到：`canvas.drawText(...)` 配默认 `new Paint()`，只改了 `setTextAlign`，没设 bidi 或方向；写错：`ctx.fillText(` 前没有设 `ctx.direction`，RTL 系统语言下句末标点被挪到行首
- rule-c1c43d0f9143｜截图里的空态文案在源图表绘制代码里找不到时，不在目标 Canvas 里补画｜读到：参考截图里图表附近有空态文案，但安卓图表 View 的绘制代码里没有画它：存这句文案的字段只被赋值、没有被绘制代码读取；用户文字只列出要画边框和图例名；写错：目标图表的 Canvas 绘制里新增了空态提示（如在副图面板里用 `fillText` 右对齐、垂直居中画一句无数据提示），并为它加了空数据标志参数
- rule-9c0e1e3f50b0｜Paint 字号按 scaledDensity 算时，Canvas font 用 fp2px 换成 px 并带 bold｜读到：源端 Paint.setTextSize(N * scaledDensity + 0.5f)（sp 字号），Paint.setTypeface(Typeface.create(Typeface.DEFAULT, Typeface.BOLD))；写错：目标端 ctx.font 写成固定的 '14px sans-serif' 这类：sp 数值直接当 px，没有按 fp 换算，也丢了 bold
- rule-711fed1b1e43｜Paint 状态读回迁到 ArkUI Canvas 时自己记字号和对齐，不读 ctx.font｜读到：源端绘制函数从 Paint 读回状态：paint.getTextAlign()、paint.getTextSize()，再据此算文字底衬的位置和大小；写错：目标端读取 ctx.font、ctx.textAlign（如从 ctx.font 解析字号的辅助函数、按 ctx.textAlign 分支）；运行时读到 undefined 抛 TypeError，编译照样通过
- rule-320e275a6547｜移植 getTextBounds 的顶部对齐时保留 top 为负的语义，写 ascent + padding - 1｜读到：源端 paint.getTextBounds(text, 0, len, bounds) 后顶部对齐写 top_y_diff = -bounds.top + padding - 1（bounds.top 是基线以上的负值，文字下移）；写错：目标端写成 -boundsHeight + padding - 1 这类符号相反的式子，文字往上跑
