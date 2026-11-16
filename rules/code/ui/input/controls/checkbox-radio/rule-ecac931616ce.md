# RadioButton 或单选列表译成 Radio 时，用 indicatorType CUSTOM 画外环加圆点

审的是：代码
触发（任一种）：
- 读到：RadioButton，或 AlertDialog.Builder.setSingleChoiceItems 单选列表，Material 下选中态是外环加圆点；写错的样子：Radio({ value, group }) 只设 .radioStyle({ checkedBackgroundColor, uncheckedBorderColor })，没写 indicatorType
适用范围：Material 风格的单选控件迁成 ArkUI Radio 时（声明里 indicatorType 自 API 12 起有）
做法：
- 写成 Radio({ value, group, indicatorType: RadioIndicatorType.CUSTOM, indicatorBuilder: 画外环和中心圆点的 @Builder })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- indicatorType?: RadioIndicatorType；indicatorBuilder?: CustomBuilder（给 CUSTOM 用）：RadioOptions 里定选中样式的两项（出处：鸿蒙 SDK 的 ets/component/radio.d.ts，RadioOptions.indicatorType / RadioOptions.indicatorBuilder）
- RadioIndicatorType.TICK = 0、DOT = 1、CUSTOM = 2：选中样式的三个取值（出处：鸿蒙 SDK 的 ets/component/radio.d.ts，RadioIndicatorType）
- API 12 起 Radio 选中默认样式由 DOT 变为 TICK：不写 indicatorType 就是勾（出处：ts-basic-components-radio.md，Radio（开头的说明））
- Radio 改 CUSTOM 外环加圆点：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
