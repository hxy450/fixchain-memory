# 条目里用图标画的勾选和评分

agent 会看到什么：源端条目里用 Icon 画的选中勾选图（Modifier.selectable 行）或星形评分（RatingBar、Icons.Filled.Star），目标写成了 Radio 或「好评 x.0」这类文本

## 规矩

- rule-5f9467ce6af9｜selectable 行只在选中时显示尾部勾选 Icon 时，按同一条件渲染勾选图，不用 Radio｜读到：Row 带 Modifier.selectable(selected) { … }，函数体里只有 if (selected) 时才出现尾部 Icon(…, tint = …) 勾选图；写错：写成了 Radio({ group: … })，每一行都有圆圈；或者勾选图没按 selected 条件出现
- rule-c43aeec1c441｜源端用五星评分控件时，目标画出五颗星，不写成「好评 x.0」文本｜写错：目标条目把评分写成 `Text('好评 ' + …)` 这类文本，而源端条目是星形评分控件
