# ui/interaction/input

EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

[上一级](../index.md)

## 本级经验

- [TextInput 关默认装饰，按主题状态背景复刻](lesson-1150c0c721e6dc0dede4.lesson.md) · 阶段：execute/repair · 信号：showPasswordIcon, InputType.Password, cancelButton, textPassword
- [inputType 只映射键盘，有 digits 才过滤](lesson-0457a04c31208e1fb916.lesson.md) · 阶段：spec/execute · 信号：inputType, textCapCharacters, textNoSuggestions, numberSigned
- [setError 迁尾部图标加聚焦气泡、改动即清](lesson-f7edea01f8308bf563ef.lesson.md) · 阶段：spec/execute · 信号：setError, TextInputLayout, showError, errorMessage
- [可编辑且分段着色用 RichEditor 承载](lesson-ef93bb2086aef9604aa1.lesson.md) · 阶段：spec/execute · 信号：RichEditor, addTextSpan, EditText, Spannable
- [平台正则按定义逐段移植并全串匹配](lesson-90e0f1db3e1e13a6fd6a.lesson.md) · 阶段：execute/verify · 信号：Patterns.WEB_URL, Patterns.EMAIL_ADDRESS, String.matches, (?i)
- [拒绝输入用 maxLength 或 onWillChange](lesson-617ffbd840398cf95efc.lesson.md) · 阶段：execute · 信号：maxLength, onValueChange, onChange, onWillChange
- [未定制的光标外观以指定页真机取证，帧差分定位](lesson-fb5a092e750a3101b862.lesson.md) · 阶段：repair · 信号：caretStyle, textCursorDrawable, caretWidth, TextInput
- [透明 TextInput 铺满掩码格并获焦，多段各独立节点](lesson-90a7888a65eefb3e94b3.lesson.md) · 阶段：execute · 信号：requestFocus, onAppear, TextInput, Stack
- [金额含小数时不用 InputType.Number](lesson-a5aeed3d4c376cd085d1.lesson.md) · 阶段：execute · 信号：InputType.Number, InputType.NUMBER_DECIMAL, toDoubleOrNull, numberDecimal
