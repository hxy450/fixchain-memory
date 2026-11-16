# 源资源或布局有限定词目录时，在 res 下按名查全部变体，规格逐个配置写值

审的是：规格
触发（任一种）：
- 读到：源工程 res 下有 values-land、layout-land 这类限定词目录，代码用 getResources().getInteger(R.integer.x)、R.dimen 读资源，或页面布局有变体；写错的样子：规格的取值表、结构段或验收只写 res/values 或竖屏布局里的一个值，没写别的配置下的值和运行期按配置读取
适用范围：规格阶段为带限定词变体的资源和布局写取值表、页面结构和验收时
做法：
- 按资源名或布局文件名在源工程 res/ 下全部 values*、layout* 目录检索（如搜 name="资源名"），命中的目录名就是限定词，读出各自的值或控件属性
- 规格写成「base 2 / land 1，运行期按当前方向读取」的形式，布局变体逐项写出横竖屏不同的控件属性和运行时代码覆盖了哪些；目标端横竖屏对应 horizontal / vertical 限定词目录
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 安卓资源系统靠成套的替代资源适配不同设备配置：getResources() 读到的值随当前配置的限定词目录变化（出处：android.content.res.Resources）
- 横竖屏限定词：vertical（竖屏）、horizontal（横屏）：鸿蒙资源目录里对应 values-land 的限定词（出处：resource-categories-and-access.md，限定词目录）
- 系统按当前设备状态先从匹配的限定词目录找资源，找不到才去 base：目标端同样按方向解析资源（出处：resource-categories-and-access.md，资源匹配）
针对本应用要查的：
- 这个资源或布局在各限定词目录下的值：源工程 res/ 下所有 values*、layout* 目录的 XML，按 name="资源名" 或布局文件名检索；每个命中的目录名就是它的限定词（values-land 即横屏），读出各自的值；布局变体逐个控件比对属性
来源：2 张卡，2 个应用
- case-14fd5b307673d523bead（Privacy Friendly 2048）：做法第 2 步 ← 建议 3
- case-671195967d859fca683d（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
