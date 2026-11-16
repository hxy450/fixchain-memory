# 掩码层设 HitTestMode.None 盖住透明输入框时，改由掩码层 onClick 去 requestFocus

审的是：代码
触发（任一种）：
- 读到：源端整个格区就是一个可点的 EditText（android:focusableInTouchMode），点格区就弹键盘；写错的样子：掩码格 Row 设 .hitTestBehavior(HitTestMode.None)，下层 TextInput 没铺满格区，外层卡片 Column 带吞点击的空 onClick，点格区没反应
适用范围：掩码格层与透明输入层叠放、外层容器自带 onClick 的输入弹层
做法：
- 撤掉掩码 Row 的 HitTestMode.None，在 Row 上写 .onClick(...)，里面按输入框的 key 显式 requestFocus
- 逐层核对点按落点：上层若仍设 None，下层输入框的实际边界要覆盖整个格区；父容器的 onClick 会接住落空的点按
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HitTestMode.None：自身不响应触摸命中，子节点响应，不挡被它盖住的其他节点：点按穿过掩码层，落到下面实际覆盖那一点的节点上（输入框没铺满时落到父容器）（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.None）
- hitTestBehavior(value: HitTestMode): T：设置命中测试模式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- 掩码 Row 去掉 None、自己 onClick 里 requestFocus，键盘收起后再点能重新拉起：修复后保留的写法（出处：卡里修好并验证过）
未核实：「持焦态点按 TextInput 不会重拉输入法」是修复者的判断，卡里没单独验证
来源：1 张卡，1 个应用
- case-1822d49fe750e20bd3be（免费来电多多）：做法第 1 步 ← 诊断、建议 3；做法第 2 步 ← 建议 2；取值 3 ← 诊断
