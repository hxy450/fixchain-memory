# 源 vector 用 ?attr 主题色填充时，显示它的 Image 加 .fillColor 按主题着色

审的是：代码
触发（任一种）：
- 读到：源 vector 的 android:fillColor="?attr/…"（随主题变色），布局里 ImageView 用 android:src 显示它；写错的样子：页面里显示转换后 SVG 的 Image 没有 .fillColor(...)，颜色固定成资源里的默认色或不可见
- 读到：代码里 setImageResource(R.drawable.…) 切换的矢量 drawable，其 android:fillColor="?attr/…"；写错的样子：目标 Image 只有尺寸、padding、objectFit，没有 .fillColor(...)，SVG 里固化为 #000000，深色主题下不变色
适用范围：显示由带主题属性颜色的 VectorDrawable 转来的 SVG 的 ArkUI Image
做法：
- 读 drawable 的 android:fillColor / android:tint；?attr 主题色在 SVG 里固化成固定色（如 #000000）时，写成 Image($r('app.media.<图标>')).fillColor($r('app.color.<与该主题属性同值的颜色键>'))；颜色资源按 lookups 查到的日夜值放 base 和 dark 的 element/color.json
- 不只沿用工程里未着色的先例，同一图标在各处都按 drawable 的主题属性着色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(value: ResourceColor): ImageAttribute：给 SVG 叠加填充色；只对 SVG 生效（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- fillColor(color: ResourceColor | ColorContent): ImageAttribute（@since 15）：同族接口：同一属性的新重载；默认不叠色，传无效值时用主题默认色（浅色黑、深色白）（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute：同族接口：同一属性再加 ColorMetrics 的重载，同样只对 SVG 图生效（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 圆角图 SVG 填 #000000，页面两处 Image 加 fillColor($r('app.color.<背景色>'))：修复后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- ?attr/… 在应用主题里的颜色：源工程 AndroidManifest 的 android:theme 所指主题及其在 res/values*/themes.xml、styles.xml（含 values-night）里的父主题链；找 <item name="属性名"> 并解析到具体颜色，日夜两个值分别写进目标的颜色资源
- drawable 用的主题属性对应哪个颜色键：源工程 res/drawable*/ 下该矢量 XML 的 android:fillColor，以及 res/values*/styles.xml 里应用主题对该属性的赋值；解出浅色、深色两值后，找目标 color.json（base 和 dark）里同值的键
来源：2 张卡，1 个应用
- case-590e7a719e7ced6a558d（AntennaPod）：做法第 1 步 ← 建议 5、诊断；做法第 2 步 ← 建议 5
- case-e82be6ce5af181afb98d（AntennaPod）：做法第 1 步 ← 诊断、建议 3；取值 4 ← 诊断
