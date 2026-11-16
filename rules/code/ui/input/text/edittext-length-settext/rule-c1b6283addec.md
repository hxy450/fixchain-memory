# maxLength 等输入限制只加在源上声明了它的那个框，批量改写前逐框核对

审的是：代码
触发（任一种）：
- 读到：一组 EditText 里只有某一个声明了 android:maxLength（或 android:inputType、android:singleLine），其他框没有；写错的样子：几个对应的 TextInput 都写了同一个 .maxLength(...)，多由 replace_all 或多框模板批量改写时一并写回，源上没声明它的框也被限长
适用范围：把源布局里一组输入框的限制属性逐控件迁成 ArkUI TextInput 属性，或批量改写已有输入框片段时
做法：
- 按控件逐个对照源 XML：.maxLength(n) 只加在源上写了 android:maxLength="n" 的那个框；.type(...)、单行与否同理，只照各框自己声明的写
- 用 replace_all 或多框模板批量改写前，确认一并写回的每个属性在每个源控件上都存在，不存在的从命中的框里去掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android:maxLength 的 format 是 integer：给这个 TextView 设一个按长度截断的输入过滤器：限长只作用于声明它的那个控件（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextView 的 maxLength（按应用的 compileSdk 取对应平台））
- maxlength = a.getInt(attr, -1)；读到时 setFilters(new InputFilter[] { new InputFilter.LengthFilter(maxlength) })：没声明时为 -1，不加过滤器，不限长（出处：android.widget.TextView#TextView(Context, AttributeSet, int, int)）
- maxLength(value: number): TextInputAttribute；不设时默认 Infinity，不限字数：源上没声明 maxLength 的框，目标端也不写（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.maxLength）
- maxLength(value: number): TextAreaAttribute：同族接口：TextArea 的最大长度（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.maxLength）
- maxLength(value: number): SearchAttribute：同族接口：Search 的最大长度（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.maxLength）
- type(value: InputType): TextInputAttribute；默认 InputType.Normal：源上 android:inputType 只照各框自己的写（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.type）
来源：1 张卡，1 个应用
- case-784ba4ab52f98f7156b6（企业安全培训）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断
