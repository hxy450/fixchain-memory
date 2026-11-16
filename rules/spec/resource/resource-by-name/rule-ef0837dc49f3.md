# 源码用 getColor(R.color.名) 等取资源值时，规格按精确资源名查定义写值，不按颜色词近似

审的是：规格
触发（任一种）：
- 读到：安卓源码按资源 ID 取值：getResources().getColor(R.color.名)、getColor(R.color.名)、getDimension(R.dimen.名)；工程里另有名字含同一颜色词的近名资源；写错的样子：验收条目、算法说明或常量表里写成「R.color.名(#hex)」，而这个 hex 在 res/values*/ 里属于另一个 name 的资源；或者只写颜色词，不写定义所在的文件和值
适用范围：规格提取时，把安卓源码里的资源引用（color、dimen 等）转写成验收条目和常量表的具体取值
做法：
- 在源工程 res/values*/ 下的全部 XML 里按精确资源名搜 name="名"（颜色搜 <color name="名">），把定义文件和值一并写进验收条目和常量表，如「R.color.名 = #AARRGGBB（定义在 res/values/ 下的某个 XML）」
- 不按颜色词或相近的名字（不带前缀的名字和带用途前缀的名字）推断取值；名字不完全相同就是另一个资源
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getColor(@ColorRes int id, @Nullable Theme theme)，内部 impl.getValue(id, value, true)：按资源 ID 取色；第三个参数 true 表示定义的值是对别的资源的引用（@color/…）时一路解析到最终值，规格里也要写解析后的最终值（出处：android.content.res.Resources#getColor）
- #AARRGGBB：8 位 hex 前两位是透明度，后六位是 RGB：源端 8 位颜色值的读法（出处：android.graphics.Color#parseColor）
- color.json 的 value 是八位十六进制，前两位表示透明度，后六位表示颜色值：目标端颜色资源与源端 8 位值同为 ARGB 排列，规格里可以照抄源端定义的 hex（出处：resource-categories-and-access.md，资源文件示例）
针对本应用要查的：
- 源码引用的那个资源名的定义和值：源工程 res/ 下 values 及 values-* 目录里的全部 XML，按 name="资源名" 全文搜（不只搜 colors.xml）；取标签里的文本作为值；值是 @color/… 这类引用时按引用的名字再搜一次直到得到 hex；几个限定词目录都有定义时分别记下
来源：1 张卡，1 个应用
- case-dfb696dc3a3684ce21d1（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
