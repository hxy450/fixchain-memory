# 源工具栏无返回键、标题居中或带右侧动作时，用 hideTitleBar 加页内头部，不塞系统标题栏的 title/menus 槽

## 何时使用

界面实现阶段，把源页面工具栏（标题、动作按钮、有无返回键）落成 NavDestination 系统标题栏或页内头部时；验证或返修发现自定义标题槽运行期为空时

## 适用情境

源页面头部是自定义工具栏（如 Ionic iOS 模式的 IonToolbar：居中图标加标题、slot=end 一组图标按钮、没有 IonBackButton），目标页是 Navigation 下 push 的 NavDestination，需要在系统标题栏 title/menus 的 CustomBuilder 槽与 hideTitleBar(true) 后在内容区自绘头部之间选择。

## 例外与边界

- 源头部与系统标题栏语义一致（有返回键、普通文本标题、无自定义动作区）时，直接用 .title() 字符串标题
- 源工具栏有返回键（上箭头），只是标题居中或带右侧动作而改用页内头部时，头部里要画出这个返回键并接到出栈：hideTitleBar(true) 会把系统标题栏连同其中的返回键一起隐藏，「不附加返回键」只针对源端本来没有返回键的页面。

## 原因

系统标题栏自带返回键，title/menus 的自定义 builder 也不会按源端居中或右对齐排布；把整条源工具栏拼进这两个槽，既多出源端没有的返回键，写时又无法运行验证。已观察到的工具链中，自定义 title/menus 槽在引用、() 调用、对象加箭头闭包、bind(this) 四种传参形态下都没有渲染，同一 builder 放进页内头部则正常显示，根因未查明。

## 做法

1. 先按源头部结构选承载方式：源工具栏没有返回键、标题居中或带右侧动作按钮时，NavDestination 设 hideTitleBar(true)，在内容区顶部写头部：Stack 居中标题，右侧动作放靠 end 的 Row，顶部按页面的安全区约定补避让；不附加源端没有的返回键（系统返回与侧滑仍可用）。
2. 只在源头部与系统标题栏一致时用 .title()；确需用 CustomBuilder 填 title/menus，就在运行验证中确认标题文本与菜单图标节点存在、有尺寸且可点击。
3. 自定义 title/menus 槽运行期为空时，不在引用、() 调用、闭包、bind 等传参形态之间反复试；先把同一 builder 放进页内头部验证，能渲染就改为 hideTitleBar 加页内头部。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕NavDestination 没有另设 hideTitleBar 时默认为 false，显示系统标题栏；设为 true 时整条标题栏（连同其中的返回键）都不显示
- 〔原因 / 做法第 1 步〕NavDestination 标题栏中的返回键在没有另设 hideBackButton 时显示（默认 false，API 15 起可设）；隐藏返回键后仍可通过系统返回手势、onBackPressed 回调返回上一页
- 〔原因 / 做法第 3 步〕卡里环境中给 NavDestination 的 title、menus 传自定义 builder 时，按引用、() 调用、NavDestinationCustomTitle 对象加箭头闭包、bind(this) 几种传参都没有渲染出内容；同一 builder 放在页内头部能正常渲染；根因没有查明，不能排除应用级布局因素
