# Java 把资源 int 与字符串相加时，目标显示资源 id 数字，不换成资源文案

审的是：代码
触发（任一种）：
- 读到：Java 源码 `R.string.x + ": " + e.getMessage()` 这类资源 int 直接与 String 相加后显示；写错的样子：ArkTS 写成先取资源文案再拼接（如 getStringSync / resText($r('app.string.x')) 后接 `: ${detail}`），显示出了文字
适用范围：源端把 R.string / R.xxx 的 int 常量当数字拼进提示文本时
做法：
- 照源码拼数字：`${$r('app.string.x').id}: ${detail}`，用 Resource 的 id 数字，不取资源文案
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Resource.id: number（resource id in hap）：$r(...) 得到的 Resource 带数字 id（出处：鸿蒙 SDK 的 ets/api/global/resource.d.ts，Resource.id）
未核实：目标显示的 id 数字与源端 R 常量的值不同，卡里按「显示资源 id 数字」验收
来源：1 张卡，1 个应用
- case-3cdc388116566cb08735（omni-notes-hmos）：做法第 1 步 ← 诊断
