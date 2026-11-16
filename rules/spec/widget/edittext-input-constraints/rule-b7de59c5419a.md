# 规格逐个列 EditText 的 inputType 等到目标属性，键盘提示和内容约束分开

审的是：规格
触发（任一种）：
- 读到：布局里的 EditText 带 textCapCharacters、textNoSuggestions、number、numberSigned 等 inputType 标志，可能另有 android:digits、maxLength；写错的样子：规格把 textCapCharacters 写成「大写过滤」「文本过滤转大写」、写「textCapCharacters 无对应」，把 numberSigned 写成 InputType.Number，或只写「输入过滤在 Service 校验」而没有键盘映射
适用范围：页面规格的控件映射表、公共输入组件的规格里写 EditText 映射时
做法：
- 逐个 EditText 列一行：inputType、digits、maxLength、InputFilter → 目标属性；键盘提示一栏写 textCapCharacters → autoCapitalizationMode(AutoCapitalizationMode.ALL_CHARACTERS)、textNoSuggestions → enablePreviewText(false)、number → InputType.Number、numberSigned → InputType.PhoneNumber + 首位符号规则
- 内容约束一栏只在源码有 android:digits / InputFilter 时写 inputFilter；源端点击或保存时的校验照原时机写，不写成输入期过滤或大写转换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- autoCapitalizationMode(mode: AutoCapitalizationMode)、AutoCapitalizationMode.ALL_CHARACTERS（@since 20）：textCapCharacters 的目标写法（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.autoCapitalizationMode；ets/component/text_common.d.ts，AutoCapitalizationMode）
- enablePreviewText(enable: boolean)，默认值 true：textNoSuggestions 的目标写法里设成 false（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.enablePreviewText）
- InputType.Number 不支持负数、小数；InputType.PhoneNumber 支持数字、+、- 等：number 和 numberSigned 的键盘选法（出处：ts-basic-components-textinput.md，InputType枚举说明）
- 按映射修正后：大写键盘不改写输入、无候选、数值框键盘正确、粘贴截断、hex 合法性在计算时校验：修复后统一的映射（出处：卡里修好并验证过）
针对本应用要查的：
- 每个 EditText 的 inputType、digits、maxLength 和挂在它上面的 InputFilter：源工程布局 XML 里各 EditText 的属性，以及对应 Activity / Fragment 里对它的 setFilters、setInputType 调用；逐个写进映射表的一行，没有的那一栏写「无」
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 5、建议 2、建议 3；做法第 2 步 ← 建议 2、建议 1；取值 4 ← 诊断
