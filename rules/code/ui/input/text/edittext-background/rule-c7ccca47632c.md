# EditText 没写 background 且父主题是 android:Theme.* 时，按平台状态背景随焦点切换

审的是：代码
触发（任一种）：
- 读到：源 EditText 没有 android:background、padding、高度，应用主题的父类是 android:Theme.Holo（或 Material、DeviceDefault）；写错的样子：目标 TextInput 写成透明底 + .border({ width: { bottom: 1 }, color: … }) 的静态下边框，色值凭记忆猜，聚焦前后没有变化
适用范围：源控件外观由 Android 框架主题的 editTextBackground 状态选择器提供、迁成 ArkUI TextInput 时
做法：
- 先查平台资源：主题的 editTextBackground、textCursorDrawable、editTextColor，沿 drawable 选择器找到未聚焦、聚焦（必要时禁用）各状态的 9-patch
- 按状态画背景并随 .onFocus(() => { this.focused = true }) / .onBlur(() => { this.focused = false }) 切换，padding 取 9-patch 的内容区；不要用 border bottom 加猜测色近似
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.EditText 的 background = ?attr/editTextBackground：EditText 不写背景时取主题的 editTextBackground（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.EditText（按应用的 compileSdk 取对应平台））
- Theme.Holo：editTextBackground = @drawable/edit_text_holo_dark，textCursorDrawable = @drawable/text_cursor_holo_dark：Holo 暗色主题下输入框背景和光标的提供方（Holo.Light 是对应的 _light 资源）（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo 的 editTextBackground、textCursorDrawable（按应用的 compileSdk 取对应平台））
- edit_text_holo_dark：state_enabled + state_focused → textfield_activated_holo_dark；state_enabled → textfield_default_holo_dark：单行输入框聚焦和未聚焦各用一张 9-patch（出处：Android SDK 平台资源 data/res/drawable/edit_text_holo_dark.xml，selector（按应用的 compileSdk 取对应平台））
- onFocus(event: () => void): T；onBlur(event: () => void): T：获焦、失焦回调，用来切换背景状态（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onFocus / CommonMethod.onBlur）
- 按平台 9-patch 画出未聚焦细线带端头竖线、聚焦粗线两态，随 onFocus/onBlur 切换，TextInput 透明、borderRadius(0)、padding 取 9-patch 内容区后与安卓两态一致：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 主题给输入框的背景、光标、字色：源工程 res/values/styles.xml 里应用主题的 parent 链，到 Android SDK 平台资源 data/res/values/themes_holo.xml（或 themes_material.xml、themes_device_defaults.xml）里对应主题；读 editTextBackground、textCursorDrawable、editTextColor 三项，顺着 @drawable/… 打开 data/res/drawable/ 下的选择器
- 每个状态 9-patch 的图样和内容区内边距：Android SDK 平台资源 data/res/drawable-<密度>/ 下选择器指向的 .9.png；看 9-patch 右边和下边的黑线标出的内容区，算出四边内边距，按密度目录换成 dp 写成 vp
来源：1 张卡，1 个应用
- case-0ce95f901f7e409784a3（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
