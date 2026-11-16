# 按压背景来自主题或 drawable 时，打开 drawable 本体，按 ripple 或 selector 写按压态

审的是：代码
触发（任一种）：
- 读到：源控件按压反馈来自主题或 drawable：没写 background 的按钮、列表行，或写了 ?attr/selectableItemBackground、listSelector、actionBarItemBackground；写错的样子：stateStyles({ pressed: … }) 里是凭记忆或照兄弟页写的 backgroundColor 常量，没核对源 drawable 的类型
适用范围：安卓控件的按压反馈迁成 ArkUI stateStyles 的 pressed 时
做法：
- 沿控件的 style、background、listSelector 和主题父链找到按压背景的主题属性，到平台资源里读出它指向的 drawable，看根元素
- <selector> 的纯色按压项才取色写 backgroundColor；有 mask 或内容层的 <ripple> 在 pressed 里画限在视图内的 radialGradient；无 mask 无内容层、带 android:radius 的按半径画圆；colorControlHighlight 只当着色输入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- RippleDrawable 没有 mask 层时按子层的合成形状遮罩：有 mask 或内容层的涟漪画在视图边界内（有界）（出处：android.graphics.drawable.RippleDrawable）
- RippleDrawable 没有子层和 mask、又作为 View 背景时，画在祖先背景上，绘制区可超出 drawable 边界：无界涟漪不受控件矩形约束（出处：android.graphics.drawable.RippleDrawable）
- radialGradient(value: RadialGradientOptions): T：目标端画径向按压层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.radialGradient）
针对本应用要查的：
- 控件按压背景的 drawable 和它的类型：源工程布局、样式里控件的 style、background、listSelector 和 values-v21 等目录下的父主题；再到 Android SDK 平台资源的 data/res/values/themes_material.xml、styles_material.xml 找属性，打开 data/res/drawable 下对应的 xml（按应用的 compileSdk 取对应平台）；看根元素是 <ripple> 还是 <selector>、有没有 mask 或内容层、有没有 android:radius。例：Theme.Material 下 ListView 行的 listSelector 解析到带 mask 的 list_choice_background_material，是有界涟漪；ActionBar 按钮的 actionBarItemBackground 解析到无 mask、radius 为 20dp 的 action_bar_item_background_material，是无界涟漪
- 涟漪的颜色和不透明度：源主题链里的 colorControlHighlight，Android SDK 平台资源的 data/res/color/ripple_material_light.xml 和 data/res/values/colors_material.xml 的 highlight_alpha_material_light；颜色按 colorControlHighlight 解析（深色栏上是浅色）；highlight_alpha 随平台版本变，屏上稳态不透明度按对照设备实测，取不到就登记待测
未核实：涟漪稳态不透明度只在 Android 12 对照设备上实测过
来源：1 张卡，1 个应用
- case-b76baecf687e5ab5817a（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2、诊断
