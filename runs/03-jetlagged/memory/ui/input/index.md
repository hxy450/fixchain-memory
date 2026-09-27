# ui/input

输入控件：源端输入约束（长度、字符集、受控值）到 TextInput 等组件属性的转换

[上一级](../index.md)

## 本级经验

- [源端受控输入框的长度上限用 TextInput.maxLength 实现，不靠 onChange 里拒绝写回](lesson-617ffbd840398cf95efc.lesson.md)
  - 时机：界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时
  - 情境：源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length &lt;= N) name = it）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框。
