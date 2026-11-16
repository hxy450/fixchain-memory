# 源端颜色引用 ?attr/… 主题属性时，顺应用主题查出浅深两值，写成成对的颜色资源

审的是：代码
触发（任一种）：
- 读到：布局或样式里的颜色属性写 ?attr/…（如 android:textColor、自定义 View 的 app:foregroundColor），值由应用主题提供；写错的样子：目标的 .fontColor / 颜色 @Param 用了按属性名猜的色、借用的别的颜色，或写死某一模式的 Color.White
适用范围：源端颜色经应用主题的属性提供，迁成 ArkUI 颜色时
做法：
- 从 AndroidManifest.xml 的 android:theme 找到应用主题，在 res/values/ 和 res/values-night/ 的 styles.xml、themes.xml 里找给这个 attr 赋值的 <item name="…">
- 顺着 ?attr/、@color/ 引用解到颜色字面量（@color/ 到 colors.xml 里找），浅色、深色各记一个；每个调用点按它自己引用的 attr 分别解
- 在 base/element 和 dark/element 的 color.json 里补同名颜色，目标写 $r('app.color.<名>')；不按名字猜、不借用语义不同的颜色、不写死某一模式的色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在两个 color.json 里定义同名配色并赋予不同色值，系统切换深浅色时自动取对应的值：页面只要引用同名 token 就会随深浅色切换（出处：ui-dark-light-color-adaptation.md，应用跟随系统的深浅色模式）
针对本应用要查的：
- 这个主题属性在浅色、深色主题下的颜色值：源工程 AndroidManifest.xml 的 android:theme 指向的主题；res/values/ 与 res/values-night/ 下 styles.xml、themes.xml 里的 <item name="<attr 名>">，以及 colors.xml；item 是颜色字面量就直接用；是 @color/… 就到 colors.xml 解出颜色；是 ?attr/… 就再按同样的办法解下一层；浅色、深色各取一份
- 每个调用点引用的是哪个主题属性：源工程里用到这个控件的每个布局 XML，控件上的颜色属性；逐个记下引用的 attr，按上一项解出值后在对应调用点传参
未核实：应用主题没有给这个 attr 赋值、值来自父主题（平台主题或 AppCompat 库主题）时去哪个文件查、按什么顺序解析，族里规矩没有查实
来源：3 张卡，2 个应用
- case-0693d5ce6cf6356203d5（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-720d51456fccb920411f（AntennaPod）：做法第 1 步 ← 诊断；做法第 3 步 ← 诊断
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 3 步 ← 建议 3
