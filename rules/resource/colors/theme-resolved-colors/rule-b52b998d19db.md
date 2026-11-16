# tint 用随深浅主题变的颜色做渐变时，base 和 dark 各写一份主题色和它的透明变体

审的是：资源
触发（任一种）：
- 读到：ImageView 的 app:tint 引用 ?android:attr/colorBackground 这类随主题变的颜色，给白到透明的渐变 shape 着色；写错的样子：目标 resources/base/element/color.json 只有主题色没有对应的透明变体，或 resources/dark/element/color.json 里缺这两项
适用范围：目标工程有深色资源目录、装饰渐变改用 linearGradient 引用颜色资源时
做法：
- base/element/color.json 和 dark/element/color.json 各写一对颜色：主题色（如 background）和同色的透明变体（如 background_transparent，透明度两位写 00、后六位与主题色相同）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 颜色值八位十六进制，前两位是透明度，后六位是颜色：透明变体就是前两位改成 00、后六位不变（出处：resource-categories-and-access.md，资源文件示例）
- dark/element：颜色模式限定词为 dark 的元素资源目录（出处：resource-categories-and-access.md，限定词目录）
针对本应用要查的：
- 主题色在浅色和深色主题下各自的色值：源工程 values/ 与 values-night/ 下的主题，和它们引用的颜色；没覆盖时查 Android SDK 平台资源 data/res/values/themes_material.xml 里父主题的 colorBackground；浅色主题的值写进 base，深色主题的值写进 dark
未核实：透明变体取同色 00 透明度是按建议里「对应的透明变体」写的，卡里没给具体色值
来源：1 张卡，1 个应用
- case-5b7b00a1deb25ed0b8d3（AntennaPod）：做法第 1 步 ← 建议 3
