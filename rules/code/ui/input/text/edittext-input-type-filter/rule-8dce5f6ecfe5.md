# numberSigned 用 PhoneNumber 键盘加 [0-9+-] 过滤，符号只许在首位

审的是：代码
触发（任一种）：
- 读到：EditText 的 android:inputType 是 numberSigned 或 number|numberSigned；写错的样子：对应的 TextInput 写 .type(InputType.Number)（打不出负号），或 InputType.Normal 加 '-?[0-9]*'（全键盘、不收 '+'）
适用范围：安卓可带正负号的数值输入框迁成 ArkUI TextInput 时
做法：
- 写成 TextInput(...).type(InputType.PhoneNumber).inputFilter('[0-9+-]')；不要用 InputType.Number 承载可负值字段
- 在 onChange 里按 DigitsKeyListener 的规则整理：只保留首位的一个 '+' 或 '-'，其他位置的符号去掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- type(value: InputType): TextInputAttribute：TextInput 的键盘类型（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.type）
- InputType.Number：纯数字输入模式，不支持负数、小数；InputType.PhoneNumber：支持数字、空格、+、-、*、#、(、)：要能输入符号只能选 PhoneNumber 一类键盘，再用 inputFilter 收窄（出处：ts-basic-components-textinput.md，InputType枚举说明）
- 设置 inputFilter 且输入字符非空时，type 附带的文本过滤失效：允许的字符全靠 inputFilter 的正则定，所以正则要写全 [0-9+-]（出处：ts-basic-components-textinput.md，inputFilter）
- DigitsKeyListener 接受 0–9 和只能在开头的一个 + 或 - 号：源端 numberSigned 的输入规则（出处：android.text.method.DigitsKeyListener#getInstance；android.widget.TextView#setInputType）
- numberSigned = 0x00001002，对应 TYPE_CLASS_NUMBER | TYPE_NUMBER_FLAG_SIGNED：源端标志（出处：Android SDK 平台资源 data/res/values/attrs.xml，inputType 的 numberSigned（按应用的 compileSdk 取对应平台））
- type(value: TextAreaType): TextAreaAttribute；TextAreaType.PHONE_NUMBER = 3：同族接口：多行输入用 TextArea 时对应的键盘类型（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.type、TextAreaType）
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断
