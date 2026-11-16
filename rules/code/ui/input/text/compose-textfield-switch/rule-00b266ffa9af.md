# 规格写开关色取主题令牌时，Toggle 用 selectedColor 和 switchStyle 配 M3 色

审的是：代码
触发（任一种）：
- 读到：规格写 Slider / Switch / SegmentedButton 的颜色取主题对象的 M3 令牌；写错的样子：Toggle({ type: ToggleType.Switch }) 没设颜色（显示系统蓝）；或写了 Toggle 上不存在的 .trackColor(...)，删掉后关闭态落回默认色
适用范围：规格已写明开关颜色取主题令牌、目标用 ArkUI Toggle 的 Switch 类型时
做法：
- 开：轨道 primary、滑块 onPrimary；关：轨道 surfaceContainerHighest、滑块 outline。写成 .selectedColor(tokens.primary).switchStyle({ unselectedColor: tokens.surfaceContainerHighest, pointColor: isOn ? tokens.onPrimary : tokens.outline })，颜色从主题对象读
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- selectedColor(value: ResourceColor): ToggleAttribute：开启态的颜色（Switch 的轨道）（出处：鸿蒙 SDK 的 ets/component/toggle.d.ts，ToggleAttribute.selectedColor）
- switchStyle(value: SwitchStyle): ToggleAttribute（@since 12）；SwitchStyle { pointRadius?, unselectedColor?: ResourceColor, pointColor?: ResourceColor, trackBorderRadius? }：unselectedColor 是关闭态轨道色，pointColor 是滑块色；Toggle 没有 trackColor（出处：鸿蒙 SDK 的 ets/component/toggle.d.ts，ToggleAttribute.switchStyle、SwitchStyle）
- switchPointColor(color: ResourceColor): ToggleAttribute：滑块色的另一种写法，只有一个颜色，不分开关态（出处：鸿蒙 SDK 的 ets/component/toggle.d.ts，ToggleAttribute.switchPointColor）
未核实：Toggle 只有一个滑块色属性，开、关两种滑块色按 isOn 切换是按声明推出的写法，卡里没写返修的具体写法
来源：1 张卡，1 个应用
- case-e3c66b268d55aba1f3f6（GameOfLife）：做法第 1 步 ← 建议 2
