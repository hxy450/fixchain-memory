# textNoSuggestions 的输入框目标设 enablePreviewText(false)

审的是：代码
触发（任一种）：
- 读到：EditText 的 android:inputType 含 textNoSuggestions；写错的样子：对应的 TextInput / TextArea 没有 .enablePreviewText(false)
适用范围：安卓 EditText 的 inputType 含 textNoSuggestions、迁成 ArkUI TextInput / TextArea 时
做法：
- 在对应输入框上加 .enablePreviewText(false)（默认是 true）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- enablePreviewText(enable: boolean): TextInputAttribute，默认值 true：TextInput 的输入预上屏开关（@since 12）（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.enablePreviewText）
- textNoSuggestions = 0x00080001，对应 InputType#TYPE_TEXT_FLAG_NO_SUGGESTIONS：输入法不显示基于词典的建议：源端标志的含义（出处：Android SDK 平台资源 data/res/values/attrs.xml，inputType 的 textNoSuggestions（按应用的 compileSdk 取对应平台））
- textNoSuggestions 的输入框统一加 enablePreviewText(false)：修复时采用的对应写法（出处：卡里修好并验证过）
- enablePreviewText(enable: boolean): TextAreaAttribute：同族接口：TextArea 的输入预上屏开关（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.enablePreviewText）
- enablePreviewText(enable: boolean): SearchAttribute：同族接口：Search 的输入预上屏开关（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.enablePreviewText）
- enablePreviewText(enable: boolean): RichEditorAttribute：同族接口：RichEditor 的输入预上屏开关（出处：鸿蒙 SDK 的 ets/component/rich_editor.d.ts，RichEditorAttribute.enablePreviewText）
未核实：声明和文档说 enablePreviewText 是输入预上屏开关，它是否同时关掉输入法候选词卡里没有单独核对；卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断
