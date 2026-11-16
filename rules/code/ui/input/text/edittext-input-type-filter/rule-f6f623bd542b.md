# 源控件没有 digits / InputFilter 时不加 inputFilter，校验留在原时机

审的是：代码
触发（任一种）：
- 读到：EditText 只有 android:inputType，没有 android:digits、setFilters；内容合法性在点击计算或保存时才用 matches("[0-9A-Fa-f]+") 一类正则校验并 Toast；写错的样子：目标输入框加了 .inputFilter('[0-9A-Fa-f]*') 一类正则在输入期丢字符；或公共输入组件把某一处的 InputFilter 推广成所有同类输入的默认组件
适用范围：迁移 EditText 的内容约束、设计公共输入组件时
做法：
- 只有源码在控件上真实挂了 android:digits 或 InputFilter 时才写 .inputFilter(正则)；公共输入组件只封装这些真实存在的过滤，并在注释里写明适用哪个控件
- 源端在点击或保存时做的校验，目标也放在同一时机（点击计算、解码、保存时校验并提示），不前移成输入期过滤
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- inputFilter(value: ResourceStr, error?: Callback<string>): TextInputAttribute：TextInput 的输入期正则过滤，不匹配的输入被丢弃（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.inputFilter）
- 匹配表达式的输入允许显示，不匹配的输入将被过滤：加了 inputFilter 就是输入期丢字符，和源端保存期校验不是一回事（出处：ts-basic-components-textinput.md，inputFilter）
- 去掉输入期 hex 过滤和 toUpperCase，hex 合法性仍在计算 / 解码时校验：修复后保留的校验时机（出处：卡里修好并验证过）
- inputFilter(value: ResourceStr, error?: (value: string) => void): TextAreaAttribute：同族接口：TextArea 的输入期过滤（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.inputFilter）
- inputFilter(value: ResourceStr, error?: Callback<string>): SearchAttribute：同族接口：Search 的输入期过滤（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.inputFilter）
针对本应用要查的：
- 源控件上是否真有输入期过滤：源工程布局 XML 里这个 EditText 的 android:digits，以及对应 Activity / Fragment 里对它的 setFilters、setKeyListener 调用；有才映射成 inputFilter；只有点击或保存时的 matches 校验的，校验留在那个时机
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0852bbd20dbe34883a83（MifareClassicTool）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
