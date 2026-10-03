# ui/input

输入与选择控件：源端输入约束到 TextInput 等组件属性的转换（含小数输入），格子式密码输入层与获焦，会被子页覆盖再返回的页面里获焦来源的判别，自定义控件 XML 属性的初值，Compose Slider 的 steps 取值，选择列表行的选中标记（条件勾选与 Radio 的取舍），选择器回填的多级字段（省市区），密码显隐图标、清除按钮等 ArkUI 默认装饰的显式关闭，未定制光标外观的取证基准与 caretStyle

[上一级](../index.md)

## 本级经验

- [Compose Slider 的 steps 是两端之间的离散值个数：取值共 steps+2 个，步长为区间/(steps+1)](lesson-d715fa78ada2e79a5fd2.lesson.md)
  - 时机：规格提取或界面实现阶段，把 Compose Slider 的 valueRange 与 steps 翻成目标滑杆步长和验收条款时
  - 情境：源端 Slider(valueRange = a..b, steps = n) 做离散取值；目标用 ArkUI Slider 的 min、max、step。
- [会被子页覆盖再返回的页面里，TextInput 的获焦回调先判别是否由用户触摸引起再写业务状态](lesson-4c476a62732697c56c22.lesson.md)
  - 时机：界面实现阶段，把 TextInput 的焦点回调接到页面业务状态，且页面常驻 NavBar 或保活容器、会被 pushPath 覆盖时
  - 情境：页面用 focused 之类的业务字段决定显示分支（如建议列表与分类）；从子页系统返回后，框架可能把焦点交还该 TextInput。
- [按 EditText 对齐 TextInput 时显式关闭源端没有的 ArkUI 默认装饰：Password 的显隐图标、输入时的清除按钮，并核默认高度](lesson-1150c0c721e6dc0dede4.lesson.md)
  - 时机：界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时
  - 情境：源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。
  - 例外：源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式
- [源码用 selectable 行加条件尾部勾选表示选中时按同一结构实现，不按“单选”语义换成 Radio](lesson-d53223f43ad454261f26.lesson.md)
  - 时机：界面实现阶段，把 Compose 排序、筛选等选择列表行转换为 ArkUI 行组件并确定选中标记时
  - 情境：源端每行是 Row(Modifier.selectable(selected) { ... })，行首图标加文字，选中时才出现尾部 Icon(ic_check, tint = brand)，未选中行不显示任何标记；目标有 ArkUI Radio 等现成单选控件可用。
  - 例外：源码本身使用 RadioButton/Radio 控件
- [源端以只读字段加选择器一次回填的多级值（省市区等），目标实现选择流程并一次写入各级字段，不退化成并列自由输入](lesson-b845647090bfeac053ed.lesson.md)
  - 时机：界面实现阶段，迁移表单中由选择器回填的地区等字段，确定输入方式与写回方式时
  - 情境：源端表单字段是只读文本框，点击覆盖层打开级联选择弹窗，选中后通过回调把省、市、区等多级值一次写回模型；目标准备用多个 TextInput 分别绑定。
- [源端受控输入框的长度上限用 TextInput.maxLength 实现，不靠 onChange 里拒绝写回](lesson-617ffbd840398cf95efc.lesson.md)
  - 时机：界面实现阶段，把源端输入框的长度上限等输入约束翻译成 ArkUI TextInput 属性与事件时
  - 情境：源端 Compose TextField/OutlinedTextField 以 value = 状态受控，在 onValueChange 中按条件决定是否写回（如 if (it.length &lt;= N) name = it）；目标端用 TextInput({ text: this.x }) 加 onChange 实现同一个输入框。
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
