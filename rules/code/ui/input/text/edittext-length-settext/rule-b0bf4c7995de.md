# 粘贴或扫描回填写进带 maxLength 的输入框前，先截断到 maxLength 再赋值

审的是：代码
触发（任一种）：
- 读到：EditText 带 android:maxLength，粘贴或程序回填用 setText(text) 写入；写错的样子：目标的粘贴 / 回填回调直接把剪贴板或扫描结果赋给输入框绑定的状态变量，没有按该框的 maxLength 截断
适用范围：程序写入（粘贴、扫描回填等）带 maxLength 的 TextInput / TextArea 时
做法：
- 赋值前截断：this.value = text.substring(0, MAX_LEN)，MAX_LEN 取该框 .maxLength(...) 的同一个值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android:maxLength 会装上 InputFilter.LengthFilter(maxlength)：源端的 maxLength 是一个过滤器（出处：android.widget.TextView#TextView（读 maxLength 属性处））
- setText 会让文本依次经过 mFilters 的 filter：源端 setText(text) 写入的粘贴内容也被截断到 maxLength（出处：android.widget.TextView#setText）
- maxLength(value: number): TextInputAttribute：TextInput 的最大输入字符数（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.maxLength）
- 粘贴回调直接赋值时没有截断；改成先截断到 maxLength 再赋值：目标端程序写入要自己截断（出处：卡里修好并验证过）
- maxLength(value: number): TextAreaAttribute：同族接口：TextArea 的最大输入字符数（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.maxLength）
- maxLength(value: number): SearchAttribute：同族接口：Search 的最大输入字符数（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.maxLength）
未核实：目标端程序赋值是否会被 maxLength 截断，声明和文档没有写明，按卡里观察到的不截断处理；卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 4、诊断；取值 4 ← 诊断
