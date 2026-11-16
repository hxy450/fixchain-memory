# 标准 CheckBox 译成 Checkbox 时设成圆角方形 ROUNDED_SQUARE

审的是：代码
触发（任一种）：
- 读到：布局里标准的 <CheckBox>（没写 android:button 自定义图），Material 下呈方形复选框；写错的样子：Checkbox().select(…).selectedColor(…) 没写 .shape(…)
适用范围：Material 主题下没有自定义 button 的 CheckBox 迁成 ArkUI Checkbox 时
做法：
- Checkbox(...) 后加 .shape(CheckBoxShape.ROUNDED_SQUARE)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- shape(value: CheckBoxShape): CheckboxAttribute：设置复选框形状（出处：鸿蒙 SDK 的 ets/component/checkbox.d.ts，CheckboxAttribute.shape）
- CheckBoxShape.CIRCLE = 0、CheckBoxShape.ROUNDED_SQUARE = 1：圆形和圆角方形两个取值（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，CheckBoxShape）
- shape 默认值 CheckBoxShape.CIRCLE：不写 shape 就是圆形（出处：ts-basic-components-checkbox.md，shape）
- checkboxShape(value: CheckBoxShape): CheckboxGroupAttribute：同族接口：CheckboxGroup 全选框的形状（出处：鸿蒙 SDK 的 ets/component/checkboxgroup.d.ts，CheckboxGroupAttribute.checkboxShape）
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 1、诊断
