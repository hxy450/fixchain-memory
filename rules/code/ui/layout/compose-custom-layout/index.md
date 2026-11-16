# Compose 自定义 Layout 的测量和摆放

agent 会看到什么：读到 Compose 自定义 Layout 里按 constraints、Placeable 的宽高算位置（placeRelative、constraints.maxWidth / n、动画进度乘文本宽）；产物里用 Stack 对齐、padding/margin、translate/position 和手写公式重现

## 规矩

- rule-7e615114f64e｜placeRelative 纵向居中的文字进 TopStart 的 Stack 时，用满高容器居中｜读到：Compose 自定义 `Layout` 里文字用 `placeRelative` 放置，y 取 `(maxHeight - height) / 2`（纵向居中）；写错：目标写成 `Stack({ alignContent: Alignment.TopStart })`，内容高的 `Text` 没有满高的框，只加了 `.align(...)` 想纵向居中，文字落到左上角
- rule-09ec1458aab1｜源端 px 域整除公式落成纯函数时，参数带 Px，调用处 vp2px → 公式 → px2vp｜读到：Compose Layout 里的 constraints.maxWidth / (itemCount + 1)，以及 placeable 位置上的 .toInt()；写错：Math.floor(w / (n + 1)) / Math.trunc(...) 的输入是 onAreaChange 回写的 vp 宽，measureText 的 px 结果先 px2vp 再进公式，头注释写「All lengths are vp」
- rule-0f36287f7ed2｜源端文本连同两侧间距随进度收到 0 时，目标的 padding/margin 也按选中条件取 0｜读到：Compose 自定义 Layout 里文本 Box 带 Modifier.padding(horizontal = …)，摆放时用文本 Placeable.width × 动画进度求图标 x，未选中时文本连同间距宽度为 0、图标居中；写错：对应 Text 上写着无条件的 .padding({ left: 常量 }) 或 .margin(...)，只靠 constraintSize({ maxWidth: 选中 ? N : 0 })、opacity、scale 折叠文本
