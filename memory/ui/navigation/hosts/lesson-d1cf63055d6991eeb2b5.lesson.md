# 源工具栏无返回键、标题居中或带右侧动作时，用 hideTitleBar 加页内头部，不塞系统标题栏的 title/menus 槽

ID：`lesson-d1cf63055d6991eeb2b5` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把源页面工具栏（标题、动作按钮、有无返回键）落成 NavDestination 系统标题栏或页内头部时；验证或返修发现自定义标题槽运行期为空时

## 适用情境

源页面头部是自定义工具栏（如 Ionic iOS 模式的 IonToolbar：居中图标加标题、slot=end 一组图标按钮、没有 IonBackButton），目标页是 Navigation 下 push 的 NavDestination，需要在系统标题栏 title/menus 的 CustomBuilder 槽与 hideTitleBar(true) 后在内容区自绘头部之间选择。

## 例外与边界

- 源头部与系统标题栏语义一致（有返回键、普通文本标题、无自定义动作区）时，直接用 .title() 字符串标题

## 原因

系统标题栏自带返回键，title/menus 的自定义 builder 也不会按源端居中或右对齐排布；把整条源工具栏拼进这两个槽，既多出源端没有的返回键，写时又无法运行验证。已观察到的工具链中，自定义 title/menus 槽在引用、() 调用、对象加箭头闭包、bind(this) 四种传参形态下都没有渲染，同一 builder 放进页内头部则正常显示，根因未查明。

## 做法

1. 先按源头部结构选承载方式：源工具栏没有返回键、标题居中或带右侧动作按钮时，NavDestination 设 hideTitleBar(true)，在内容区顶部写头部：Stack 居中标题，右侧动作放靠 end 的 Row，顶部按页面的安全区约定补避让；不附加源端没有的返回键（系统返回与侧滑仍可用）。
2. 只在源头部与系统标题栏一致时用 .title()；确需用 CustomBuilder 填 title/menus，就在运行验证中确认标题文本与菜单图标节点存在、有尺寸且可点击。
3. 自定义 title/menus 槽运行期为空时，不在引用、() 调用、闭包、bind 等传参形态之间反复试；先把同一 builder 放进页内头部验证，能渲染就改为 hideTitleBar 加页内头部。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4de74b9529eed506c432](../../../../store/cases/case-4de74b9529eed506c432/4b48fe662c5ea09224200cf9e6de7d2d550e51354bbc9f23c780929846715677.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`4b48fe662c5ea09224200cf9e6de7d2d550e51354bbc9f23c780929846715677`
