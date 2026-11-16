# EditText 的 inputType 和输入过滤

agent 会看到什么：读到 EditText / EditTextPreference 的 android:inputType（textCapCharacters、textNoSuggestions、number）、android:numeric、android:digits 或 setFilters / InputFilter.AllCaps；产物里 TextInput / TextArea 的 type、autoCapitalizationMode、enablePreviewText、inputFilter、聚焦和大写转换

## 规矩

- rule-f8ee0c0ac57a｜inputType 含 textCapCharacters 时设大写键盘模式，不转大写、不过滤｜读到：EditText 的 android:inputType 含 textCapCharacters（常与 textNoSuggestions 连写），没有 android:digits，也没有 setFilters / InputFilter.AllCaps；写错：对应的 TextInput / TextArea 在 onChange 里 toUpperCase()、或加了 inputFilter 正则当作「textCapCharacters 等价」；或者写「textCapCharacters 无对应」，没设 autoCapitalizationMode
- rule-5fb9b14703c2｜源端挂 InputFilter.AllCaps 时，在 aboutToIMEInput 里转大写自行插入｜读到：源端 EditText 设了 setFilters(new InputFilter[]{ new InputFilter.AllCaps() })；写错：目标输入时不转大写，toUpperCase 放在保存或校验时（ViewModel 里），粘贴进来的小写也原样保留
- rule-f6f623bd542b｜源控件没有 digits / InputFilter 时不加 inputFilter，校验留在原时机｜读到：EditText 只有 android:inputType，没有 android:digits、setFilters；内容合法性在点击计算或保存时才用 matches("[0-9A-Fa-f]+") 一类正则校验并 Toast；写错：目标输入框加了 .inputFilter('[0-9A-Fa-f]*') 一类正则在输入期丢字符；或公共输入组件把某一处的 InputFilter 推广成所有同类输入的默认组件
- rule-83f6ac8f11fa｜textNoSuggestions 的输入框目标设 enablePreviewText(false)｜读到：EditText 的 android:inputType 含 textNoSuggestions；写错：对应的 TextInput / TextArea 没有 .enablePreviewText(false)
- rule-9e6c2f6dac85｜EditTextPreference 对话框打开即聚焦输入框，数字型设 InputType.Number｜读到：<EditTextPreference android:numeric="integer">（或 android:inputType="number"）；写错：目标对话框里的 TextInput 打开时不聚焦、不弹键盘，也没有 .type(InputType.Number)
- rule-477b5c666772｜EditText 为 number 时，目标设 InputType.Number 并加 [0-9] 过滤，不只加正则｜读到：EditText 的 android:inputType 是 number（不带 numberSigned）；写错：对应的 TextInput 只加了 inputFilter 数字正则、键盘仍是默认 InputType.Normal，或者没设 .type(InputType.Number)
- rule-8dce5f6ecfe5｜numberSigned 用 PhoneNumber 键盘加 [0-9+-] 过滤，符号只许在首位｜读到：EditText 的 android:inputType 是 numberSigned 或 number|numberSigned；写错：对应的 TextInput 写 .type(InputType.Number)（打不出负号），或 InputType.Normal 加 '-?[0-9]*'（全键盘、不收 '+'）
- rule-f902abaf8fcf｜源端输入按小数解析时，TextInput 不用 InputType.Number，改 Normal 加 onChange｜读到：源端 EditText 没写数字类的 android:inputType（只有 android:maxLength 等），读输入的代码用 toDoubleOrNull() 解析；写错：目标 TextInput 写成 .type(InputType.Number)，输入框打不出小数点
