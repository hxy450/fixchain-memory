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
- [EditText 的 inputType 键盘与候选提示和内容约束分开映射：textCapCharacters → autoCapitalizationMode、textNoSuggestions → enablePreviewText(false)、带符号数字用含 +/- 的键盘；只有源端有 digits/InputFilter 才过滤，程序写入按 maxLength 截断](lesson-0457a04c31208e1fb916.lesson.md)
  - 时机：界面实现阶段（含公共输入组件设计、页面规格的控件映射与页面转换），把 Android EditText 的 inputType、digits、InputFilter、maxLength 与粘贴回填翻译成 ArkUI TextInput/TextArea 属性时
  - 情境：源布局用 textCapCharacters、textNoSuggestions、number、numberSigned 等 inputType 标志声明键盘与输入法行为，多数未配 android:digits 或 InputFilter，内容合法性在点击计算或保存时才校验；个别控件挂了 InputFilter.AllCaps；页面另有粘贴或扫描回填写入带 maxLength 的输入框。目标 ArkUI（SDK 6.x 可用 autoCapitalizationMode、enablePreviewText、InputType.Number/PhoneNumber）；映射参考只给 number → InputType.Number 与“capitalize 无直接对应，使用文本转换”。
- [EditText.setError 迁成尾部错误图标加聚焦时弹出的气泡、改动即清，不改成 showError 下方文字或常显红字](lesson-f7edea01f8308bf563ef.lesson.md)
  - 时机：规格提取阶段为调用 setError 的输入框写转换决策时；界面实现阶段把 EditText.setError 校验提示落成 ArkUI 输入框时
  - 情境：源码对 EditText（或 TextView）调用 setError(msg) 提示校验失败（如保存时标题为空、两次密码不一致），布局里没有 TextInputLayout 或自定义错误视图；目标准备用 TextInput 的 showError/errorMessage 在框下显示错误文字、在输入框下常显红字，或规格写成“实时校验”。
  - 例外：源端用 TextInputLayout.setError（框下常显错误文字）或自绘错误视图时，按其呈现迁移
- [会被子页覆盖再返回的页面里，TextInput 的获焦回调先判别是否由用户触摸引起再写业务状态](lesson-4c476a62732697c56c22.lesson.md)
  - 时机：界面实现阶段，把 TextInput 的焦点回调接到页面业务状态，且页面常驻 NavBar 或保活容器、会被 pushPath 覆盖时
  - 情境：页面用 focused 之类的业务字段决定显示分支（如建议列表与分类）；从子页系统返回后，框架可能把焦点交还该 TextInput。
- [工具栏 SearchView（actionView）按控件状态机迁移：展开、焦点、提交、收起与菜单重建分开建模，不折成查询函数](lesson-4995a3977dc8bc7fa696.lesson.md)
  - 时机：规格提取与工具栏接线阶段，把源端菜单项上的 SearchView actionView 迁成目标标题栏搜索框时
  - 情境：源端在菜单 inflate 后为搜索项设置 SearchView：expandActionView/collapseActionView、OnActionExpandListener 的展开与收起回调（收起时清查询、重载列表、invalidateOptionsMenu）、焦点监听切换其他菜单项可见性、onQueryTextSubmit 的返回值决定是否由 SearchView 投递 ACTION_SEARCH，以及即时搜索偏好。目标规格写成应用内 ViewModel“内化等价”的几个查询函数，实现用一个布尔同时表示展开与焦点、用取消图标代替收起。
- [把同页多组表单收集为执行请求时，按源执行方法实际读取的控件为每个模式设独立字段，不因同名复用其他表单的槽位](lesson-dee3401b34b8fab1a0fb.lesson.md)
  - 时机：功能实现阶段，把 Android Activity 上多组输入表单的字段收集为服务层执行请求、接到写入或计算方法时
  - 情境：源 Activity 在同一页面持有多组语义相近的输入控件（写块的扇区/块与值块的扇区/块、值块数值与另一模式的数值），各执行方法分别读取自己表单的控件；目标由页面收集参数构造一个请求对象交给共享服务，页面已为各表单建了独立状态。
- [按 EditText 对齐 TextInput 时，未声明 background 的输入框按主题状态背景（editTextBackground 的 9-patch，随聚焦切换并取其内边距）复刻，并显式关闭源端没有的 ArkUI 默认装饰：填充底与圆角、Password 显隐图标、清除按钮，核默认高度](lesson-1150c0c721e6dc0dede4.lesson.md)
  - 时机：界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时；为未声明 background 的 EditText 写 TextInput 外观修饰链时；以及确定输入框软键盘动作键时
  - 情境：源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。 也包括源 EditText 未声明 background、padding 与高度，外观来自框架主题的 editTextBackground 状态选择器（Holo 为 textfield_default/activated_holo_dark 两张 9-patch，含端头竖线与内容内边距）。 也包括规格把 Password 显隐图标登记为“HarmonyOS 自带”的对应能力；以及多个单行 EditText 纵向排列、未写 imeOptions，目标 TextInput 未设 enterKeyType。
  - 例外：源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式
- [收软键盘用 hideTextInput，不用 hideSoftKeyboard 或 stopInputSession；焦点态绑 onFocus/onBlur](lesson-99da84bf5c70367eb3df.lesson.md)
  - 时机：界面与服务实现阶段，为搜索框等输入框实现“展开取焦、提交收键盘、菜单随焦点切换”并选择输入法控制 API 时
  - 情境：源端用 InputMethodManager.hideSoftInputFromWindow/showSoftInput 只收放键盘、焦点不变，或由 SearchView 焦点变化驱动菜单与工具栏；规格写“输入法方法实现期核实后钉死”；目标准备调用 showSoftKeyboard/hideSoftKeyboard、stopInputSession，或用点击时手工翻转的布尔量表示“输入框已聚焦”。
- [源码用 selectable 行加条件尾部勾选表示选中时按同一结构实现，不按“单选”语义换成 Radio](lesson-d53223f43ad454261f26.lesson.md)
  - 时机：界面实现阶段，把 Compose 排序、筛选等选择列表行转换为 ArkUI 行组件并确定选中标记时
  - 情境：源端每行是 Row(Modifier.selectable(selected) { ... })，行首图标加文字，选中时才出现尾部 Icon(ic_check, tint = brand)，未选中行不显示任何标记；目标有 ArkUI Radio 等现成单选控件可用。
  - 例外：源码本身使用 RadioButton/Radio 控件
- [源端以只读字段加选择器一次回填的多级值（省市区等），目标实现选择流程并一次写入各级字段，不退化成并列自由输入](lesson-b845647090bfeac053ed.lesson.md)
  - 时机：界面实现阶段，迁移表单中由选择器回填的地区等字段，确定输入方式与写回方式时
  - 情境：源端表单字段是只读文本框，点击覆盖层打开级联选择弹窗，选中后通过回调把省、市、区等多级值一次写回模型；目标准备用多个 TextInput 分别绑定。
- [源端受控输入框的拒绝条件要阻止文本显示：长度上限用 TextInput.maxLength，其他拒绝条件在 onWillChange 返回 false，不靠 onChange 里不写回](lesson-617ffbd840398cf95efc.lesson.md)
  - 时机：界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时
  - 情境：源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length &lt;= N) name = it，或数值格式不合法时直接 return、不回调上层）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框，可能由父组件持有值并以“父值不变即回退”设计公共输入组件。
- [源端同一控件既可编辑又分段着色（EditText + Spannable、Compose TextField 的 visualTransformation）时用 RichEditor 承载，不拆成只读着色与单色编辑两态，也不降级成纯文本；整体重建与焦点恢复照源实现](lesson-ef93bb2086aef9604aa1.lesson.md)
  - 时机：规格提取与界面实现阶段，为源端常驻可编辑、带分段着色的输入框（EditText + Spannable 与输入过滤，或带 visualTransformation 的 Compose TextField，如十六进制数据编辑器、编辑态 URL 高亮的描述框）选择 ArkUI 编辑组件并迁移刷新语义时
  - 情境：源端每个数据单元是常驻可编辑的 EditText：文本以 setText(text, SPANNABLE) 分段着色、挂 InputFilter.AllCaps、宽度 wrap_content，着色刷新靠删除重建整个编辑器并按序号恢复焦点；规格可能写“TextArea + 分段 Span 着色”这类不可实现的组合；材料与映射参考里没有提到 RichEditor。也包括 Compose TextField/OutlinedTextField 以 visualTransformation（如按正则给 URL 着色的 buildAnnotatedStringWithUrls）在编辑态显示样式，规格写成“输入框内富文本高亮能力受限，编辑态降级为纯文本”。
- [源端未显式定制的光标外观以用户指定页面的真机取证为基准：不借其他页面代取样，用帧差分定位光标](lesson-fb5a092e750a3101b862.lesson.md)
  - 时机：界面还原修复阶段，为输入框光标这类源端未显式定制、取决于页面主题或系统渲染的外观选取安卓基准，并写入 caretStyle 时
  - 情境：源 EditText 没有 textCursorDrawable，外观取决于所在 Activity 的主题和系统渲染；同一应用其他页面已有不同的光标配置；需要真机像素取证；目标为 TextInput 的 caretStyle({ width, color })。
  - 例外：源端显式设置了 textCursorDrawable，此时打开该 drawable 取宽度与颜色
- [自定义 View 上的 android:* 属性只有被该类读取才生效：控件初值取运行时生效值](lesson-a6edef3bb44e01a82b72.lesson.md)
  - 时机：界面实现阶段，把源布局中自定义控件的 XML 属性转换为目标组件初始状态时；联调修复判断是否为复刻缺陷时
  - 情境：源布局在继承 View 的自定义控件（非 CheckBox/CompoundButton）上声明 android:checked 等框架属性，该类构造只读取自己的 styleable 属性；目标用状态变量表示勾选或开关的首显状态。
- [色板、渐变方案、边框素材这类选项列表按源 Fragment/ViewModel 的数据源迁移，截图只核视觉；调色盘、相册、图库等动作项按源接到对应页面并写回编辑会话](lesson-60c1c37b0703e5d3b8d6.lesson.md)
  - 时机：界面实现阶段，为编辑页背景色、文字颜色、边框等选择区确定选项列表与点击行为时，尤其任务要求“根据截图转换”时
  - 情境：Android 选择区由各自 Fragment + ViewModel 以 RecyclerView 列表提供（背景含渐变方案与图片素材、文字为纯色列表、边框为位图素材且首项是调色盘），Fragment 泛型参数或布局 data-binding 指向对应 ViewModel；迁移任务同时给出设备截图作为视觉参考。
- [透明 TextInput 叠在掩码格上时，输入层铺满格区并显式获焦，多段输入各用独立节点](lesson-90a7888a65eefb3e94b3.lesson.md)
  - 时机：界面实现阶段，把格子式密码框等自定义输入控件转成“透明 TextInput + 掩码格”叠层时
  - 情境：源端弹窗内是固定尺寸的格子式输入控件（如 4 位数字密码），多段流程（设置、再次确认）各弹独立 Dialog 并各带新输入框；目标用页内条件挂载的浮层，透明 TextInput 与掩码 Row 叠放，外层卡片有吞点击的 onClick。
- [金额类输入可含小数时不用 InputType.Number：按源端解析函数选择允许小数点的输入方式](lesson-a5aeed3d4c376cd085d1.lesson.md)
  - 时机：界面实现阶段，把源端输入弹窗的 EditText 转成 ArkUI TextInput 并确定输入类型时
  - 情境：源端 EditText 未设数字 inputType（或为 numberDecimal），保存时用 toDoubleOrNull 一类解析允许小数；目标 TextInput 准备用 InputType.Number。
- [首屏输入框按源端平台缺省获焦时，在窗口获焦后再 requestFocus：冷启动窗口激活晚于首屏查询，提前请求不会拉起输入法](lesson-9d42548ee3c075de3330.lesson.md)
  - 时机：界面实现阶段，为首屏含输入框的页面落实冷启动初始焦点与软键盘时
  - 情境：源端靠平台缺省给第一个可获焦的 EditText 焦点并自动弹键盘（源码没有 requestFocus/showSoftInput），获焦条件随数据分支变化（如列表为空时）；目标为 NavDestination 页 + TextInput，ArkUI 不会自动给输入框焦点。
