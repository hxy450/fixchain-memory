# 自绘组件的颜色属性写成 ?attr/… 时，先查主题实际值再定默认色，各调用点按自己布局传参

审的是：代码
触发（任一种）：
- 读到：布局 XML 里自定义 View（如自绘进度环）写 app:foregroundColor="?attr/…"；写错的样子：ArkTS 自绘组件颜色 @Param 的默认值按属性名猜成强调色（accent 一类的键），或调用点没有按各自布局里的 foregroundColor 传参
适用范围：把安卓自定义 View 的颜色属性（引用主题属性）迁成 ArkUI 自绘组件的颜色参数时
做法：
- 在源工程 attrs.xml、styles.xml / themes.xml（含 values-night）里查出这个主题属性的浅、深两值，映射到同值的颜色键，作为颜色 @Param 的默认值；不按属性名推测成强调色
- 每个调用点按它自己布局里写的 foregroundColor 传参，不同调用点可能引用不同的主题属性
针对本应用要查的：
- 自定义 View 颜色属性引用的主题属性在浅色、深色主题下的值：源工程 res/values/attrs.xml 里该 attr 的声明，res/values/styles.xml、themes.xml 和 res/values-night/ 下应用主题的 <item name="…">；找到应用主题里给这个 attr 赋值的 item，顺着 ?attr/、@color/ 引用解到颜色字面量，浅色、深色各记一个
- 每个调用点传的是哪个主题属性：源工程里用到这个自定义 View 的每个布局 XML，该控件上的 app:foregroundColor（或同类颜色属性）；逐个记下引用的属性，按上一项解出值后在对应调用点传参
来源：1 张卡，1 个应用
- case-0693d5ce6cf6356203d5（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
