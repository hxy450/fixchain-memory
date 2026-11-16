# TabLayout 译成 Tabs 时，tabBar 用 SubTabBarStyle 显式写标签字号字重、颜色和指示条

审的是：代码
触发（任一种）：
- 读到：com.google.android.material.tabs.TabLayout（tabMode、tabGravity 等），标签样式取库默认；写错的样子：TabContent().tabBar($r(…)) 或 .tabBar('…') 直接传字符串，用的是 ArkUI 默认标签样式
适用范围：Material TabLayout 迁成 ArkUI Tabs 时的标签栏样式
做法：
- 写成 .tabBar(new SubTabBarStyle(label).labelStyle({ font: { size, weight }, selectedColor, unselectedColor }).indicator({ color, height }))，各值取 TabLayout 的默认样式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- tabBar(value: SubTabBarStyle | BottomTabBarStyle): TabContentAttribute：TabContent 的标签可以传样式对象（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，TabContentAttribute.tabBar）
- constructor(content: ResourceStr)；labelStyle(value: LabelStyle): SubTabBarStyle；indicator(value: IndicatorStyle): SubTabBarStyle：SubTabBarStyle 的构造和定标签、指示条样式的方法（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，SubTabBarStyle）
- IndicatorStyle.height 默认 2vp，color 默认 #FF007DFF：不写 indicator 时指示条的高度和颜色（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，IndicatorStyle）
- SubTabBarStyle：14 Medium、选中 accent / 未选中 onSurface 对应的颜色、48vp 高、3vp 指示条：修好后的标签样式（出处：卡里修好并验证过）
- labelStyle(value: LabelStyle): BottomTabBarStyle：同族接口：BottomTabBarStyle 的标签样式（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，BottomTabBarStyle.labelStyle）
针对本应用要查的：
- TabLayout 默认的标签字号、字重、大小写、颜色和指示条高度：依赖库 com.google.android.material:material 包内 res/values/values.xml（按应用依赖的版本）：主题里 tabStyle 指向的 TabLayout 样式，及其 tabTextAppearance、tabIndicatorHeight、tabTextColor；顺着 textAppearance 读出 android:textSize、字重、textAllCaps，颜色 selector 读选中和未选中两项再到主题里解析。例：1.12.0 的 TextAppearance.Design.Tab 用 @dimen/design_tab_text_size
未核实：卡里没写应用依赖的 material 版本，例子按本机缓存的 1.12.0
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
