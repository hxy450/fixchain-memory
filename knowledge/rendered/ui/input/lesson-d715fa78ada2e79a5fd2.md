# Compose Slider 的 steps 是两端之间的离散值个数：取值共 steps+2 个，步长为区间/(steps+1)

## 何时使用

规格提取或界面实现阶段，把 Compose Slider 的 valueRange 与 steps 翻成目标滑杆步长和验收条款时

## 适用情境

源端 Slider(valueRange = a..b, steps = n) 做离散取值，n 可能由表达式算出（如 (区间 / 某个名为 step 的常量).roundToInt() + 1）；当前值标签可能以 Float.toString 输出；目标用 ArkUI Slider 的 min、max、step。steps 为 0 时源端没有刻度、连续取值，不套本条的步长公式；这时 ArkUI 的 step 不写就按 1 处理（最小可设 0.01），源端区间小（如 0..1）时要显式写小步长，否则只剩两端两个值。

## 原因

steps 是两端之间的中间离散点数，取值共 n+2 个；读成“n 个间隔”或“n+1 个停靠点”会让步长和取值集整体错位，并随规格传到实现和验收。

## 做法

1. 步长 = (max − min)/(steps + 1)；规格和验收写出完整取值列表，而不只写“N 个停靠点”。
2. steps 由表达式给出时先求出它的值再代入上式；表达式里名为 step 的常量只是求 steps 的中间量，不直接写成目标 step。
3. 显示当前值的标签按源端格式化输出：Kotlin Float.toString 对整数值带“.0”，小数位取能唯一区分该 float 的最少位数（见 Float 转字符串的经验）；不用 toFixed(n) 代替。

## 可选检查

- 对步长有疑问时，在目标端逐个停靠点取值，与源端取值列表逐一比对。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕源端 Compose Slider(valueRange = a..b, steps = n) 实测可停位置共 n + 2 个（含两端），相邻停靠点间隔为 (b − a)/(n + 1)
- 〔做法第 1 步〕ArkUI SliderOptions.step 是步长而不是停靠点个数：不写时为 1，取值范围 [0.01, max − min]，设成小于 0 或大于 max 的值时按默认值 1 处理
- 〔做法第 1 步〕SliderOptions.min 不写时为 0，max 不写时为 100
