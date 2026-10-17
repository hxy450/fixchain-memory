# ui/theme/sources

控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

[上一级](../index.md)

## 本级经验

- [style 引用先展开再逐实例叠加覆写，圆角不照抄相邻](lesson-bc5b8558ab086168b462.lesson.md) · 阶段：execute/repair · 信号：@style/, styles.xml, @Builder, borderRadius
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](lesson-47785524c7f132ea7efe.lesson.md) · 阶段：spec/execute · 信号：colorPrimary, colorOnPrimary, Theme.MaterialComponents, LocalContentColor
- [布局引用的 @drawable 先打开取数值写进规格与修饰链](lesson-771d1ba1a032b769097a.lesson.md) · 阶段：spec/execute · 信号：progressDrawable, textCursorDrawable, layer-list, caretStyle
- [库与框架组件默认几何先查 SDK/库 res 分侧取](lesson-5a82d62ff7e087616968.lesson.md) · 阶段：spec/execute · 信号：TopAppBar, Snackbar, MaterialTheme.colorScheme, Tokens
- [视觉修复以源布局为准，截图差先折算 vp 再三方对照](lesson-8119d8bf0b58e4daac24.lesson.md) · 阶段：verify/repair · 信号：@Preview, docs/assets, setVisibility, getChannel
- [视觉属性逐项取自源布局、item 布局与适配器分支，不近似](lesson-e4e65a99e545871f96ae.lesson.md) · 阶段：execute/repair · 信号：drawableLeft, drawableStart, ImageView, TextView
