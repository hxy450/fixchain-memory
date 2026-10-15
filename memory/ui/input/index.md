# ui/input

输入与选择控件：源端输入约束到 TextInput 等组件属性的转换（含小数输入），用户输入校验正则（Android 平台 Patterns 常量）的逐段移植与全串匹配，格子式密码输入层与获焦，会被子页覆盖再返回的页面里获焦来源的判别，自定义控件 XML 属性的初值，Compose Slider 的 steps 取值，选择列表行的选中标记（条件勾选与 Radio 的取舍），选择器回填的多级字段（省市区），密码显隐图标、清除按钮等 ArkUI 默认装饰的显式关闭，未定制光标外观的取证基准与 caretStyle；inputType 键盘与候选提示和内容约束的分开映射、可编辑分段着色文本（RichEditor）、同页多组表单收集执行请求时的取值来源；源控件显式内容槽（Switch thumbContent）在原生控件缺槽时自绘，受控输入非长度类拒绝条件用 onWillChange

[上一级](../index.md)

## 本级经验

- [Android 平台公开正则常量按定义逐段移植并保持全串匹配语义](lesson-90e0f1db3e1e13a6fd6a.lesson.md)
  - 时机：界面实现阶段，移植 Patterns.WEB_URL、Patterns.EMAIL_ADDRESS 等平台正则对用户输入的校验时
  - 情境：源以 String.matches(Patterns.X.pattern()) 做全串校验，目标没有同名 API，需要自行提供正则。
- [Compose Slider 的 steps 是两端之间的离散值个数：取值共 steps+2 个，步长为区间/(steps+1)](lesson-d715fa78ada2e79a5fd2.lesson.md)
  - 时机：规格提取或界面实现阶段，把 Compose Slider 的 valueRange 与 steps 翻成目标滑杆步长和验收条款时
  - 情境：源端 Slider(valueRange = a..b, steps = n) 做离散取值，n 可能由表达式算出（如 (区间 / 某个名为 step 的常量).roundToInt() + 1）；当前值标签可能以 Float.toString 输出；目标用 ArkUI Slider 的 min、max、step。
- [Compose Switch 的 thumbContent（如选中时的勾选图标）等显式子内容，在目标原生开关没有对应参数时自绘承载，不假定 Toggle 会自动显示](lesson-c3a3797da8b412c31aa7.lesson.md)
  - 时机：界面实现阶段（含公共组件抽取），把 M3 Switch 等带内容槽的源控件映射为 ArkUI Toggle 等原生控件时
  - 情境：源端 Switch 传了 thumbContent = { if (checked) Icon(Icons.Rounded.Check) } 一类显式子内容；目标准备用 Toggle({ type: ToggleType.Switch })，写者认为原生开关打开时会自带勾选图标，或计划中的图标在落盘时被省略。
- [text 类 inputType 只映射键盘与输入法属性，内容约束只来自 digits、InputFilter 与 number 类过滤](lesson-0457a04c31208e1fb916.lesson.md)
  - 时机：界面实现阶段（含公共输入组件设计、页面规格的控件映射与页面转换），把 Android EditText 的 inputType、digits、InputFilter 翻译成 ArkUI TextInput/TextArea 属性时
  - 情境：源布局用 textCapCharacters、textNoSuggestions 等 text 类 inputType 标志声明键盘与输入法行为，多数未配 android:digits 或 InputFilter，内容合法性在点击计算或保存时才校验；个别控件挂了 InputFilter.AllCaps。映射参考只给“capitalize 无直接对应，使用文本转换”一类说法。
  - 例外：inputType 是 number、numberSigned、numberDecimal 等数值类：按数值输入框的键盘与过滤规则处理
- [向带 maxLength 或 InputFilter 的输入框程序写入（粘贴、扫描回填）时，先按源过滤器截断或转换再赋值](lesson-299950a4255a40c6baf5.lesson.md)
  - 时机：界面实现阶段，实现粘贴按钮、扫描回填、恢复草稿等向输入框程序写入文本的逻辑时
  - 情境：源端用 EditText.setText 向带 android:maxLength、InputFilter（AllCaps、自定义过滤）的输入框写入文本；目标把状态变量直接赋给 TextInput 的 text，再拿该值去比较或保存。
  - 例外：源端写入的控件不挂过滤器，或源端已在写入前自行截断、转换：照源端逻辑
- [常驻 NavBar 或保活页会被子页覆盖再返回时，TextInput 获焦回调先判别是否由用户触摸引起，再写业务状态](lesson-4c476a62732697c56c22.lesson.md)
  - 时机：规格提取阶段，把源端 remember（非 rememberSaveable）随组合销毁的状态翻译成目标复位方案时；界面实现阶段，把 TextInput 的焦点回调接到页面业务状态，且页面常驻 NavBar 或保活容器、会被 pushPath 覆盖时
  - 情境：源页面离开组合时丢弃全部状态，其中 focused 等由框架焦点事件驱动的业务字段决定显示分支（如建议列表与分类）；目标页面常驻 Navigation 的 NavBar（或 Stack、Tabs 保活），经 pushPath 进入子页后再系统返回，框架可能把焦点交还该 TextInput。
  - 例外：源端用 rememberSaveable 等方式让焦点与输入在返回后保留：返回时恢复焦点本就符合源端行为，不做判别
- [截图可见的选项列表按源数据源（ViewModel、数组、素材目录）迁移，截图只核视觉；列表中的动作项按源接到对应页面并写回会话](lesson-60c1c37b0703e5d3b8d6.lesson.md)
  - 时机：界面实现阶段，为选择区（色板、样式方案、素材列表等）确定选项列表与点击行为时，尤其任务要求“根据截图转换”时
  - 情境：Android 选择区由 Fragment + ViewModel 以 RecyclerView 列表提供选项（例：编辑器的背景色含渐变方案与图片素材、边框为位图素材且首项是调色盘），Fragment 泛型参数或布局 data-binding 的 variable 指向对应 ViewModel；迁移任务同时给出设备截图作为视觉参考。
- [把同页多组表单收集为执行请求时，按源执行方法实际读取的控件为每个模式设独立字段，不因同名复用其他表单的槽位](lesson-dee3401b34b8fab1a0fb.lesson.md)
  - 时机：功能实现阶段，把 Android Activity 上多组输入表单的字段收集为服务层执行请求、接到写入或计算方法时
  - 情境：源 Activity 在同一页面持有多组语义相近、同名的位置或数值输入控件，各执行方法分别读取自己那组控件；目标由页面收集参数构造一个请求对象交给共享服务，页面已为各表单建了独立状态。
- [按 EditText 对齐 TextInput 时，显式关闭源端没有的默认装饰：密码显隐图标、清除按钮、填充底与圆角](lesson-1150c0c721e6dc0dede4.lesson.md)
  - 时机：界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时
  - 情境：源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。
  - 例外：源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式；源 EditText 未声明 background 时的底线与聚焦态：按主题 editTextBackground 状态背景复刻，本条只负责关掉目标多出的装饰
- [数值输入框按源 inputType 与提交时的解析函数选键盘：可负用带符号键盘、可含小数用 NUMBER_DECIMAL](lesson-a5aeed3d4c376cd085d1.lesson.md)
  - 时机：界面实现阶段，把源端 EditText（含输入弹窗）的数值输入转成 ArkUI TextInput 并确定 type 与 inputFilter 时
  - 情境：源端 EditText 为 number、numberSigned、numberDecimal 等数值 inputType，或未设数字 inputType 而保存时用 toDoubleOrNull/toFloat 一类允许小数的函数解析；目标 TextInput 准备一律用 InputType.Number。
  - 例外：inputType 是 textCapCharacters 等 text 类标志：只映射键盘与输入法属性，不加内容过滤
- [源 EditText 未声明 background 时，按主题 editTextBackground 状态背景复刻底线与聚焦态，不用静态下边框近似](lesson-c18630b78d75e5e67282.lesson.md)
  - 时机：界面实现或 1:1 对齐修复阶段，为未声明 background、padding 与高度的 EditText 写 TextInput 外观修饰链时；规格提取阶段写这类输入框的转换决策时
  - 情境：源 EditText 未声明 android:background、padding 与高度，应用主题父链落到框架主题（android:Theme.*），外观来自主题的 editTextBackground：Holo 为 edit_text_holo_dark/light 选择器（聚焦与未聚焦两张 9-patch，含端头竖线与内容内边距），Material 为 edit_text_material（inset 包着按 colorControlNormal/colorControlActivated 着色的 9-patch，见 platforms/android-&lt;api&gt;/data/res/drawable/edit_text_material.xml）；目标用 ArkUI TextInput。
  - 例外：源端显式设置了 background 或 style：按该资源解析；应用主题继承 Theme.AppCompat、Theme.MaterialComponents 等库主题：editTextBackground 由库资源提供，不在 SDK platforms 的 res 里，本条的平台资源路径不适用，到该库 AAR 的 res 沿同一属性解析
- [源 EditText 未设光标样式时，按所在 Activity 主题解析光标资源，解析不出再以同页真机取证为准，写入 caretStyle](lesson-fb5a092e750a3101b862.lesson.md)
  - 时机：界面实现与还原修复阶段，为输入框光标这类源端未显式定制、取决于页面主题的外观确定 caretStyle 时
  - 情境：源 EditText 及其 style 没有 textCursorDrawable，光标外观取决于所在 Activity 的主题（父链到框架主题 android:Theme.* 时由其 textCursorDrawable 及着色属性提供）；同一应用其他页面可能有不同的光标配置；目标为 TextInput 的 caretStyle({ width, color })。
  - 例外：源端显式设置了 textCursorDrawable，此时打开该 drawable 取宽度与颜色
- [源码用 selectable 行加条件尾部勾选表示选中时按同一结构实现，不按“单选”语义换成 Radio](lesson-d53223f43ad454261f26.lesson.md)
  - 时机：界面实现阶段，把 Compose 排序、筛选等选择列表行转换为 ArkUI 行组件并确定选中标记时
  - 情境：源端每行是 Row(Modifier.selectable(selected) { ... })，行首图标加文字，选中时才出现尾部 Icon(ic_check, tint = brand)，未选中行不显示任何标记；目标有 ArkUI Radio 等现成单选控件可用。
  - 例外：源码本身使用 RadioButton/Radio 控件
- [源端以只读字段加选择器一次回填的多级值（省市区等），目标实现选择流程并一次写入各级字段，不退化成并列自由输入](lesson-b845647090bfeac053ed.lesson.md)
  - 时机：界面实现阶段，迁移表单中由选择器回填的地区等字段，确定输入方式与写回方式时
  - 情境：源端表单字段是只读文本框，点击覆盖层打开级联选择弹窗，选中后通过回调把省、市、区等多级值一次写回模型；目标准备用多个 TextInput 分别绑定。
- [源端受控输入框在 onValueChange 拒绝写回时，用 onWillChange 返回 false 或 maxLength 阻止显示](lesson-617ffbd840398cf95efc.lesson.md)
  - 时机：界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时
  - 情境：源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length &lt;= N) name = it，或数值格式不合法时直接 return、不回调上层）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框，可能由父组件持有值并以“父值不变即回退”设计公共输入组件。
  - 例外：源端的约束来自 EditText 的 digits、InputFilter 或 maxLength 等非受控过滤：按这些过滤器的语义映射
- [源端同一控件既可编辑又分段着色（Spannable、visualTransformation）时用 RichEditor 承载，不拆成两态](lesson-ef93bb2086aef9604aa1.lesson.md)
  - 时机：规格提取与界面实现阶段，为源端常驻可编辑、带分段着色的输入框（EditText + Spannable 与输入过滤，或带 visualTransformation 的 Compose TextField）选择 ArkUI 编辑组件时
  - 情境：源端数据单元是常驻可编辑的 EditText，文本以 setText(text, SPANNABLE) 分段着色，常挂输入过滤、宽度 wrap_content；或 Compose TextField/OutlinedTextField 以 visualTransformation（如按正则给 URL 段着色）在编辑态显示样式。规格可能写“TextArea + 分段 Span 着色”这类不可实现的组合，或写成“输入框内富文本高亮能力受限，编辑态降级为纯文本”；材料与映射参考里没有提到 RichEditor。
- [自定义 View 上的 android:* 属性只有继承链中某个类读取时才生效：控件初值取运行时生效值](lesson-a6edef3bb44e01a82b72.lesson.md)
  - 时机：界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时
  - 情境：源布局在自定义控件上声明 android:checked、android:enabled 等框架属性，该类直接继承 View（或继承链中没有读取该属性的类），构造只读取自己的 styleable 属性；目标用状态变量表示勾选、开关或可用态的首显状态。
- [透明 TextInput 叠在掩码格上时，输入层铺满格区并显式获焦，多段输入各用独立节点](lesson-90a7888a65eefb3e94b3.lesson.md)
  - 时机：界面实现阶段，把格子式密码框等自定义输入控件转成“透明 TextInput + 掩码格”叠层时
  - 情境：源端弹窗内是固定尺寸的格子式输入控件（如 4 位数字密码），多段流程（设置、再次确认）各弹独立 Dialog 并各带新输入框；目标用页内条件挂载的浮层，透明 TextInput 与掩码 Row 叠放，外层卡片有吞点击的 onClick。
- [首屏输入框按源端获焦并自动弹键盘时，先核 windowSoftInputMode 与获焦条件，再在窗口获焦后 requestFocus](lesson-9d42548ee3c075de3330.lesson.md)
  - 时机：界面实现阶段，为首屏含输入框的页面落实冷启动初始焦点与软键盘时；规格提取阶段写首屏焦点与是否自动弹键盘的验收时
  - 情境：源端没有 requestFocus/showSoftInput，首屏焦点由平台缺省给布局顺序中第一个可获焦视图（AdapterView 只在有数据时可获焦），获焦条件随数据分支变化（如列表为空时）；目标为 NavDestination 页 + TextInput，ArkUI 不会自动给输入框焦点。
  - 例外：Manifest 中该 Activity 的 windowSoftInputMode 为 stateHidden/stateAlwaysHidden：只给焦点、不拉键盘
