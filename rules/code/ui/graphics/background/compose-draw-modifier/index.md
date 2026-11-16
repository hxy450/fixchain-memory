# Compose 用 drawWithContent 写的自定义 Modifier 扩展

agent 会看到什么：读到 Compose 组件调用 drawWithContent { drawContent(); drawRect(brush, blendMode = …) } 一类自定义 Modifier 扩展（渐变着色、渐变描边）；交回的代码改成单色 fillColor、兄弟节点单独混合，或描边宽度不是扩展里的默认值

## 规矩

- rule-8d28841daf62｜drawRect 用 BlendMode.Plus/Darken 给图标叠渐变时，图标和渐变层放进同一个离屏组｜读到：Compose drawWithContent { drawContent(); drawRect(brush, blendMode = BlendMode.Plus / Darken) } 给 Icon 着色；写错：Icon 写成 .fillColor(渐变首色) 单色，没有 .blendMode(...)
- rule-e80c3cb0b899｜组件调用同目录的自定义 Modifier 扩展时，按扩展定义的默认参数和绘制顺序写，环宽不自定｜读到：Compose 组件调用同目录文件里的自定义 Modifier 扩展（渐变描边、渐变着色等），调用时没传宽度参数，参数声明里带 Dp 默认值；写错：目标描边宽度不是扩展定义里的默认值，如用 .padding(1) 露出 1vp 的环
