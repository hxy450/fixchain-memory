# ui/layout/material-defaults

Material 库组件隐含尺寸与内部留白

[上一级](../index.md)

## 本级经验

- [Material 交互组件的 .size(x&lt;48) 是修饰符字面，实绘按 minimumInteractiveComponentSize 为 48](lesson-7e0d06d6a8e9a544c53a.lesson.md)
  - 时机：规格提取阶段，为页面 spec 转换决策表与功能 spec 视觉验收判据确定 Material IconButton/Button 等交互组件的目标尺寸与位置时
  - 情境：源为 Jetpack Compose，页面含 Material3 IconButton（或同类交互组件），源码在其外层显式写 .size(x) 且 x &lt; 48dp 并带 background(CircleShape)；目标端要用固定 width/height 的 Button 复刻。
  - 例外：源码显式关闭了最小触控尺寸（LocalMinimumInteractiveComponentSize / minimumInteractiveComponentEnforcement=false）
- [实现者收到 &lt;48 的 Material IconButton 尺寸时按 48 圆心不变实现并上报差异](lesson-2ae981b896931bd7bb58.lesson.md)
  - 时机：界面实现阶段，按 spec 给出的固定尺寸落地 Material 交互组件（IconButton/Button）时
  - 情境：spec 或派工词给出 &lt;48 的尺寸，源组件类型是 Material3 IconButton 且未关闭最小触控尺寸。
- [由 Material 库组件内部布局提供的留白要分侧写出，不把单侧 token 扩成对称 padding](lesson-f648d0ae072e9bcf83c3.lesson.md)
  - 时机：界面实现阶段，为源侧由 Material 组件内部布局（而非源码显式 modifier）决定的留白确定 ArkUI padding 时；规格提取阶段写入同一组件的 M3 默认值时
  - 情境：源是 Compose Material3 TopAppBar / IconButton 等库组件，标题槽内是 Row { Text(weight 1) + IconButton }，源码本身没有 padding 修饰符；库的内部留白（TopAppBarTitleInset、导航/动作槽宽度）需要实现者自行补出；spec 只写了容器高度等部分 M3 默认值。
