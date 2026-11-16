# 目标引用颜色资源时，读出源端实际色值和 color.json 里键的 value 逐字比对再选键

审的是：代码
触发（任一种）：
- 读到：源端颜色是布局里的字面量（android:textColor="#…"、android:background、渐变起止色）、@color/ 引用或代码里的 getColor(R.color.名)；写错的样子：目标写 $r('app.color.X') 时按名称、前缀或色系挑了已有键，或照规格写了 '#…'，这个值和源端色值不同
适用范围：为目标控件选颜色资源引用或写颜色值时
做法：
- 读出源端这处的实际色值：字面量直接读，@color/ 或 R.color.名 到源工程 res/values 的 colors.xml 按 name 找；#RRGGBB 补 FF 成八位
- 到目标工程 resources/base/element 下的颜色 json 读候选键的 value，统一小写后和源色值逐字比；相等才引用，不等就用同值的键或新增专属键，不按名称、前缀或色系挑
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- #RRGGBB 解析时 alpha 置为 FF，与 #FFRRGGBB 相同：比对前把六位色值补成八位（出处：android.graphics.Color#parseColor）
- color.json 的颜色值是八位十六进制，前两位透明度、后六位颜色：与安卓 #AARRGGBB 同序，可以逐字比对（出处：resource-categories-and-access.md，资源文件示例）
针对本应用要查的：
- 源端这处的确切色值：源工程布局 XML 里该元素的颜色属性；写的是 @color/ 引用或代码里 getColor(R.color.名) 时，去 res/values 的 colors.xml 按 name 找；读出 #RRGGBB 或 #AARRGGBB，六位的补 FF 作透明度
- 候选颜色键的实际值：目标工程 resources/base/element（及 dark 等限定目录）下的 color.json 和各页共享的颜色文件，按 name 或按 value 找；读 value，统一小写、补齐八位后和源色值比
来源：3 张卡，3 个应用
- case-0cd1e854cf161b2bb256（掌上燃气管家）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-ae1e7b09c5cfe5214cd2（骑行记录）：做法第 2 步 ← 建议 3
- case-dfb696dc3a3684ce21d1（Blockinger）：做法第 1 步 ← 建议 4
