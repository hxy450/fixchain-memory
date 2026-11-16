# inputType 含 textCapCharacters 时设大写键盘模式，不转大写、不过滤

审的是：代码
触发（任一种）：
- 读到：EditText 的 android:inputType 含 textCapCharacters（常与 textNoSuggestions 连写），没有 android:digits，也没有 setFilters / InputFilter.AllCaps；写错的样子：对应的 TextInput / TextArea 在 onChange 里 toUpperCase()、或加了 inputFilter 正则当作「textCapCharacters 等价」；或者写「textCapCharacters 无对应」，没设 autoCapitalizationMode
适用范围：安卓 EditText 的 inputType 含 textCapCharacters、迁成 ArkUI TextInput / TextArea 时（autoCapitalizationMode 出自声明 @since 20）
做法：
- 写成 TextInput(...).autoCapitalizationMode(AutoCapitalizationMode.ALL_CHARACTERS)（多行的 TextArea 同样写）；小写仍允许输入，不在 onChange 里 toUpperCase，也不加 inputFilter
- 拿输入原文做比较的逻辑（如复扫后与输入值比对）按输入的原样大小写比较
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- autoCapitalizationMode(mode: AutoCapitalizationMode): TextInputAttribute：TextInput 的自动大小写模式（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.autoCapitalizationMode）
- AutoCapitalizationMode.ALL_CHARACTERS = 3（NONE = 0、WORDS = 1、SENTENCES = 2）：全部字符大写的取值（出处：鸿蒙 SDK 的 ets/component/text_common.d.ts，AutoCapitalizationMode）
- 只提供接口能力，具体实现以输入法应用为主：它是给输入法的大写提示，不改写文本（出处：ts-basic-components-textinput.md，autoCapitalizationMode）
- textCapCharacters = 0x00001001，对应 InputType#TYPE_TEXT_FLAG_CAP_CHARACTERS，请求所有字符大写：源端是键盘大写请求，不限字符集（出处：Android SDK 平台资源 data/res/values/attrs.xml，inputType 的 textCapCharacters（按应用的 compileSdk 取对应平台））
- autoCapitalizationMode(mode: AutoCapitalizationMode): TextAreaAttribute：同族接口：TextArea 的自动大小写模式（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.autoCapitalizationMode）
- autoCapitalizationMode(mode: AutoCapitalizationMode): SearchAttribute：同族接口：Search 的自动大小写模式（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.autoCapitalizationMode）
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23；大写键盘的实际效果取决于输入法应用
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 4
