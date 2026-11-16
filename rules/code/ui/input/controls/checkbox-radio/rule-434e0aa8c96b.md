# Checkbox/Radio 另配 Text 时，外层统一 onClick，框设 HitTestMode.None

审的是：代码
触发（任一种）：
- 读到：CheckBox / RadioButton 带 android:text，或代码里 setText(...)，文字本身属于可点控件；写错的样子：目标写成 Row { Checkbox(); Text(...) } 或 Row { Radio(); Text(...) }，Text 和外层容器都没有 onClick，只有方框或圆环可点
适用范围：ArkUI Checkbox / Radio 不带文字、要另配 Text 复刻安卓复合按钮时，含单选组、对话框里的复选框和动态列表项
做法：
- 外层容器挂 .onClick(() => { 切换选中状态 })，内层 Checkbox / Radio 设 .hitTestBehavior(HitTestMode.None) 避免点框时双触发；单选组、对话框里的复选框和动态列表项逐个核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hitTestBehavior(value: HitTestMode): T：组件的触摸命中方式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- HitTestMode.None：自身不响应触摸命中，子组件照常响应：勾选控件自己不收点击，点击交给外层容器（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.None）
- 选项行写成 Row { 勾选控件, Text } 整体 onClick 后，文字和框都能切换：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6d1435e3e9257286cfbf（MifareClassicTool）：做法第 1 步 ← 建议 2；取值 3 ← 诊断
