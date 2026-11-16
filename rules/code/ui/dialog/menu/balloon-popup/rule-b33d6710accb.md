# 带布尔异或和三元的箭头位置公式，逐字保留括号、列真值表再写 arrowOffset

审的是：代码
触发（任一种）：
- 读到：源端 `setArrowPosition(…)` 的参数是 `0.25f + ((a ^ b) ? 0f : 0.5f)` 这类带布尔异或和三元运算的表达式；写错的样子：目标 `arrowOffset` 的条件与源式相反；注释里转述的公式丢了内层括号
适用范围：把第三方气泡的箭头位置公式（或其他布尔组合的三元表达式）翻译成 bindPopup 参数时
做法：
- 照源式逐字保留括号：const pos = 0.25 + ((a !== b) ? 0 : 0.5)（布尔异或即两者不等），对每个布尔输入列真值表，注释写明每种情况箭头指向哪里
- 再按相对位置换算 arrowOffset：arrowOffset = 气泡宽度 × pos
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按源式求值修正条件后（异或为真取 0、为假取 0.5，再加 0.25），箭头位置与源端一致：修好的写法（出处：卡里修好并验证过）
- arrowOffset?: Length：箭头在上下边时，0 表示在最左，其他值是箭头到最左的距离；默认居中：相对位置要换算成距离（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomPopupOptions.arrowOffset）
- arrowOffset?: Length：同族接口：PopupOptions（非自定义气泡）的箭头偏移（出处：鸿蒙 SDK 的 ets/component/common.d.ts，PopupOptions.arrowOffset）
- arrowOffset?: Length：同族接口：ContextMenuOptions 的箭头偏移（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ContextMenuOptions.arrowOffset）
来源：1 张卡，1 个应用
- case-1907ba587e6b1439f17d（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
