# 源 textColor 引用应用主题自定义 attr 而目标缺同名颜色时，按主题值补建资源，不借用别的颜色

审的是：代码
触发（任一种）：
- 读到：源布局 TextView 写 android:textColor="?attr/…"，引用的是应用自己在主题里定义的属性（不是 android: 平台属性），值在应用主题的 styles.xml 里；写错的样子：目标 color.json 里没有对应颜色，Text 的 .fontColor($r('app.color.…')) 换成了另一个已有颜色（如通用错误色）；既没补建资源，也没登记 resource-pending 或 UNC 占位
适用范围：界面实现阶段，源控件颜色经应用主题的自定义属性提供、目标工程还没有对应颜色资源时
做法：
- 在源工程应用主题（含 values-night 变体）里查这个 attr 的 item 值，在 resources/base/element/color.json 补建与 attr 同名的颜色（深色主题值不同时 dark 也补），Text 写 .fontColor($r('app.color.<与 attr 同名>'))
- 这次任务不能补资源时登记 resource-pending 或 UNC 占位，不拿语义不同的已有颜色顶替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 改为 $r('app.color.<与 attr 同名>')，颜色值取自源主题：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 这个自定义 attr 在应用主题里的取值：源工程 AndroidManifest.xml 的 android:theme 指向的主题，到 res/values/ 和 res/values-night/ 的 styles.xml 或 themes.xml 里找 <item name="<attr 名>">；item 是颜色值就直接用；是 @color/… 就到 colors.xml 里解析出颜色；浅色、深色主题各取一份
来源：1 张卡，1 个应用
- case-720d51456fccb920411f（AntennaPod）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；取值 1 ← 诊断
