# ui/interaction/input

EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

[上一级](../index.md)

## 本级经验

- [TextInput 显式关闭源端没有的显隐图标与清除按钮](lesson-1150c0c721e6dc0dede4.lesson.md) · 阶段：execute/repair · 信号：showPasswordIcon, InputType.Password, cancelButton, textPassword
- [未定制的光标外观以指定页真机取证，帧差分定位](lesson-fb5a092e750a3101b862.lesson.md) · 阶段：repair · 信号：caretStyle, textCursorDrawable, caretWidth, TextInput
- [透明 TextInput 铺满掩码格并获焦，多段各独立节点](lesson-90a7888a65eefb3e94b3.lesson.md) · 阶段：execute · 信号：requestFocus, onAppear, TextInput, Stack
- [金额含小数时不用 InputType.Number](lesson-a5aeed3d4c376cd085d1.lesson.md) · 阶段：execute · 信号：InputType.Number, InputType.NUMBER_DECIMAL, toDoubleOrNull, numberDecimal
- [长度上限写 maxLength，onChange 只同步状态](lesson-617ffbd840398cf95efc.lesson.md) · 阶段：execute · 信号：maxLength, onValueChange, onChange, inputFilter
