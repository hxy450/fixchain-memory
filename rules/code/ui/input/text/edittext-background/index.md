# EditText 的背景与 TextInput 默认带出的外观

agent 会看到什么：读过的布局里 EditText 或 Spinner 没写 android:background、padding、高度（外观来自主题），或用 @null 去掉了默认装饰、没有密码显隐切换；交回的 TextInput / Select 带着 ArkUI 默认的填充底、圆角、内边距、高度、清除按钮或显隐图标，或写成凭记忆的静态下边框

## 通用查法

### EditText 没写 background 时顺主题查 editTextBackground，按状态写显式外观

审的是：代码
触发（任一种）：
- 读到：EditText 没写 android:background（外观来自主题），应用主题的 parent 是 android:Theme.Holo、Material、DeviceDefault 一类；写错的样子：TextInput 只写透明底或 .border({ width: { bottom: 1 } }) 静态下边框，色值是猜的，圆角、padding、height 用默认值，聚焦前后不变
适用范围：源输入框外观由主题的 editTextBackground 提供、迁成 ArkUI TextInput 时
做法：
- 顺着源 Activity 主题的 parent 链查 editTextBackground，打开它指向的状态选择器，读出未聚焦、聚焦各状态的 drawable
- 写成显式外观：.backgroundColor(Color.Transparent)、.borderRadius(0)，padding 取该 drawable 的内容区，height 按上下内边距加行高；各状态的背景随 .onFocus / .onBlur 切换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.EditText 的 background = ?attr/editTextBackground：EditText 不写背景时取主题的 editTextBackground（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.EditText（按应用的 compileSdk 取对应平台））
- Theme.Holo：editTextBackground = @drawable/edit_text_holo_dark；edit_text_holo_dark 里 state_focused → textfield_activated_holo_dark，其余 → textfield_default_holo_dark：例：Holo 暗色主题下单行输入框聚焦和未聚焦各用一张 9-patch（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo 的 editTextBackground；data/res/drawable/edit_text_holo_dark.xml（按应用的 compileSdk 取对应平台））
- onFocus(event: () => void): T；onBlur(event: () => void): T：获焦、失焦回调，用来切换背景状态（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onFocus / CommonMethod.onBlur）
- TextInput 的 padding 默认 { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }：不覆盖就带着这组内边距（出处：ts-basic-components-textinput.md，属性）
针对本应用要查的：
- 主题给输入框的背景、光标、字色：源工程 AndroidManifest.xml 里这个 <activity> 的 android:theme（没写看 <application>），顺着 res/values*/ 下 styles、themes XML 的 parent 链，到 Android SDK 平台资源 data/res/values/themes_holo.xml、themes_material.xml 或 themes_device_defaults.xml 里的对应主题；链上离控件最近的一项给出值；editTextBackground 指向选择器的，打开 data/res/drawable/ 下的选择器，读各状态指向的 drawable
- 各状态背景的内容区内边距和源输入框的高度：选择器指向的 9-patch（Android SDK 平台资源 data/res/drawable-<密度>/ 下的 .9.png），以及源 EditText 的字号；9-patch 右边和下边的黑线标出内容区，按密度目录换成 dp 写成 vp；上下内边距加文字行高即 wrap_content 的高度
未核实：主题继承 AppCompat、MaterialComponents 时 editTextBackground 由依赖库给出，族里规矩没有查实过对应的库资源；TextInput 默认填充底按卡里上机看到的写，声明里没查到默认背景色
来源：1 张卡，1 个应用
- case-0ce95f901f7e409784a3（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、建议 1

## 规矩

- rule-c7ccca47632c｜EditText 没写 background 且父主题是 android:Theme.* 时，按平台状态背景随焦点切换｜读到：源 EditText 没有 android:background、padding、高度，应用主题的父类是 android:Theme.Holo（或 Material、DeviceDefault）；写错：目标 TextInput 写成透明底 + .border({ width: { bottom: 1 }, color: … }) 的静态下边框，色值凭记忆猜，聚焦前后没有变化
- rule-e52f4beb0760｜TextInput 改透明底时显式写 borderRadius(0)、padding、height、caretColor｜读到：源 EditText 外观来自主题背景（没写 android:background、padding、高度），layout_height 是 wrap_content；写错：目标 TextInput 设了透明底或只设下边框，却没写 .borderRadius(0)、.padding(...)、.height(...)，边框两端随默认圆角上翘，高度和内边距是 ArkUI 默认值
- rule-6a87baab6566｜EditText / Spinner 译成 TextInput / Select 时清掉默认填充底，输入框补下划线｜读到：普通 <EditText>（Material 下是下划线、无底色）和 <Spinner>（无底色）；写错：TextInput(…).type(…).fontSize(…) 和 Select(…).font(…) 没写 .backgroundColor(Color.Transparent)
- rule-d447d2ddefb2｜对齐 EditText 时逐项核 TextInput 默认带出的外观，源端没有的显式关闭或覆盖｜读到：源 EditText 没写清除按钮、显隐图标，用 android:background="@null" 等去掉了默认装饰，高度按内容或 padding 决定；写错：TextInput 只覆盖了源 XML 写出的属性，没有处理 ArkUI 默认带出的外观：没写 .height()、.showPasswordIcon(false)、.cancelButton(...)、.caretStyle(...)
- rule-5ed1d883f048｜源 EditText 是密码掩码且无显隐切换时，TextInput 写 .showPasswordIcon(false)｜读到：EditText（或其子类）写 android:password="true" 或 android:inputType="textPassword" / "numberPassword"，外面没有 TextInputLayout 的 passwordToggleEnabled，也没有自绘的显隐按钮；写错：TextInput 只写了 .type(InputType.Password) 或 .type(InputType.NUMBER_PASSWORD)，没有 .showPasswordIcon(false)（或写成 .showPasswordIcon(true)），输入框末尾多出小眼睛图标
- rule-34392698b105｜AppCompat EditText 迁成 TextInput 时，补上背景的 inset 和下划线｜读到：源布局里的 EditText 在 AppCompat 主题下（AppCompatEditText），背景取 ?attr/editTextBackground，没有自定义 android:background；写错：目标 TextInput 写 backgroundColor(Color.Transparent)，没有 abc_edit_text_material 的上、下、左右 inset，也没有底部下划线
- rule-c63895482018｜Material 主题 EditText 的下划线按背景 inset 定位，inset 不当文字内距｜读到：EditText 没写 android:background，主题是 Theme.Material 系（editTextBackground = @drawable/edit_text_material，外层 <inset> 包着随聚焦切换的 9-patch selector）；写错：`TextInput` / `TextArea` 写 .padding({ left: 4, top: 10, right: 4, bottom: 7 })，下划线 Divider().width('100%') 贴在 Stack 底边
