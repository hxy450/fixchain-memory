# ui/input

输入控件：源端输入约束到 TextInput 等组件属性的转换（含小数输入），格子式密码输入层与获焦，自定义控件 XML 属性的初值

[上一级](../index.md)

## 本级经验

- [源端受控输入框的长度上限用 TextInput.maxLength 实现，不靠 onChange 里拒绝写回](lesson-617ffbd840398cf95efc.lesson.md)
  - 时机：界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时
  - 情境：源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length &lt;= N) name = it）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框。
- [自定义 View 上的 android:* 属性只有被该类读取才生效：控件初值取运行时生效值](lesson-a6edef3bb44e01a82b72.lesson.md)
  - 时机：界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时
  - 情境：源布局在继承 View 的自定义控件（非 CheckBox/CompoundButton）上声明 android:checked 等框架属性，该类构造只读取自己的 styleable 属性；目标用状态变量表示勾选或开关的首显状态。
- [透明 TextInput 叠在掩码格上时，输入层铺满格区并显式获焦，多段输入各用独立节点](lesson-90a7888a65eefb3e94b3.lesson.md)
  - 时机：界面实现阶段，把格子式密码框等自定义输入控件转成“透明 TextInput + 掩码格”叠层时
  - 情境：源端弹窗内是固定尺寸的格子式输入控件（如 4 位数字密码），多段流程（设置、再次确认）各弹独立 Dialog 并各带新输入框；目标用页内条件挂载的浮层，透明 TextInput 与掩码 Row 叠放，外层卡片有吞点击的 onClick。
- [金额类输入可含小数时不用 InputType.Number：按源端解析函数选择允许小数点的输入方式](lesson-a5aeed3d4c376cd085d1.lesson.md)
  - 时机：界面实现阶段，把源端输入弹窗的 EditText 转成 ArkUI TextInput 并确定输入类型时
  - 情境：源端 EditText 未设数字 inputType（或为 numberDecimal），保存时用 toDoubleOrNull 一类解析允许小数；目标 TextInput 准备用 InputType.Number。
