# 横屏限定词的布局和资源变体

agent 会看到什么：读过的源工程有 layout-land / layout-port 布局变体，或 values-land 覆盖了进几何公式的 R.integer、R.dimen；交回的规格只写了竖屏或 base 的值，没写横屏下的不同和运行期读取

## 通用查法

### 源资源或布局有限定词目录时，在 res 下按名查全部变体，规格逐个配置写值

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

## 规矩

- rule-bd886333557b｜进入公式的 R.integer 等资源有限定词覆盖时，取值表写各配置的值和运行期读取｜读到：源码在绘制或首帧几何里用 getResources().getInteger(R.integer.x)（或 R.dimen、R.bool）读资源，该资源在 res/values-land 等限定词目录有覆盖值；写错：规格的精确取值表或公式只写一个字面值（如「名 | 2 | R.integer.名」），没写横屏等配置下的另一个值，也没写运行期读取
- rule-593ebd9c040f｜页面有 layout-land 变体时，规格写出横竖屏不同的控件属性和运行时覆盖范围｜读到：源页面有 layout-land 等布局变体，同一控件在不同变体里背景不同；Activity 代码只对部分控件调用 setBackgroundResource；写错：页面规格的结构段只描述竖屏控件属性（如按钮背景是某圆角 shape），没写横屏变体的不同，也没写运行时代码覆盖了哪些控件的哪些属性
- rule-74d70e2a9386｜几何随方向重算且所用资源有横屏覆盖时，几何验收补横屏样例｜读到：源端资源在 res/values-land 有覆盖值，页面有 layout-port / layout-land 两套布局或旋转重建 Activity；写错：几何验收条目只写竖屏的取值（如「资源名=2」），没有横屏下的样例
