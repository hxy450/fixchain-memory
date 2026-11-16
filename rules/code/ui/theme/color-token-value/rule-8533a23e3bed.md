# 源码按资源 ID 取色而规格给 hex 时，代码先对照 color.json 的同名键，不一致按源端资源写

审的是：代码
触发（任一种）：
- 读到：安卓源码是 getColor(R.color.名) 或 getResources().getColor(R.color.名)，规格在同一处给的是 #hex；写错的样子：代码里直接 return '#…' 字面量、注释只引规格条目，这个值和目标工程 resources/base/element/color.json 里同名 name 的 value 不一样
适用范围：实现阶段，源端取色用的是资源 ID、规格给的是具体 hex 的地方
做法：
- 在目标工程 resources/base/element/color.json 里找 name 等于源资源名的条目，和规格给的 hex 比对；或者直接读这个资源，写成 $r('app.color.名')
- 不一致时按源端资源的值实现，注释写源资源名和它的定义文件，不只引规格条目；并在 source-notes 里回报规格
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- $r('app.type.name')，颜色写 $r('app.color.名')：按资源名访问本模块的颜色资源（出处：resource-categories-and-access.md，资源访问）
- type ResourceColor = Color | number | string | Resource：颜色属性可以直接收 $r 返回的 Resource，也可以收颜色字符串（出处：鸿蒙 SDK 的 ets/component/units.d.ts，ResourceColor）
- string 颜色：'#ffffff' 是 rgb，'#ff000000' 是 argb：8 位颜色串两边都是 ARGB 排列，源端 #AARRGGBB 可以照抄；透明度为 ff 时也可写成 6 位 #RRGGBB（出处：ts-types.md，ResourceColor）
- color.json 的 value 是八位十六进制，前两位表示透明度，后六位表示颜色值：同名键的 value 和源端 8 位值逐位可比（出处：resource-categories-and-access.md，资源文件示例）
来源：1 张卡，1 个应用
- case-dfb696dc3a3684ce21d1（Blockinger）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断
