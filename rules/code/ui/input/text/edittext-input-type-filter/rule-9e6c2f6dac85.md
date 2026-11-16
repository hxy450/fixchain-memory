# EditTextPreference 对话框打开即聚焦输入框，数字型设 InputType.Number

审的是：代码
触发（任一种）：
- 读到：<EditTextPreference android:numeric="integer">（或 android:inputType="number"）；写错的样子：目标对话框里的 TextInput 打开时不聚焦、不弹键盘，也没有 .type(InputType.Number)
适用范围：页面实现时复刻 EditTextPreference 的输入对话框
做法：
- TextInput 设 .id('<输入框 id>')，在对话框内容的 onAppear 里调 this.getUIContext().getFocusController().requestFocus('<输入框 id>')；numeric / inputType 为数字时加 .type(InputType.Number)
- 点 OK 写入输入框里的原串，点 Cancel 或点外部不写入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- requestFocus(key: string): void，key 是组件的 inspector key；150001 组件不可获焦，150003 组件不在树上：FocusController 按 id 请求焦点（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，FocusController.requestFocus；UIContext.getFocusController）
- type(value: InputType): TextInputAttribute，默认 InputType.Normal；InputType.Number 是纯数字输入：数字键盘（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.type、InputType.Number）
- API 10 起 TextInput 获焦时默认拉起键盘（enableKeyboardOnFocus 默认 true）：requestFocus 后键盘随之弹出（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.enableKeyboardOnFocus）
- onDialogClosed(positiveResult) 只在 positiveResult 为 true 时 setText(mEditText.getText().toString())：源端只有 OK 写入原串（出处：android.preference.EditTextPreference#onDialogClosed）
未核实：FocusController.requestFocus 最后一段注释是 @since 22（首次出现在 API 12），卡里目标是 6.1.0(23)，版本可用
来源：1 张卡，1 个应用
- case-8539606efd3a93a5fcb0（Blockinger）：做法第 1 步 ← 建议 5、诊断；做法第 2 步 ← 建议 5
