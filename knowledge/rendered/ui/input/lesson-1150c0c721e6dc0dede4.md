# 按 EditText 对齐 TextInput 时，未声明 background 的输入框按主题状态背景（editTextBackground 的 9-patch，随聚焦切换并取其内边距）复刻，并显式关闭源端没有的 ArkUI 默认装饰：填充底与圆角、Password 显隐图标、清除按钮，核默认高度

## 何时使用

界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时；为未声明 background 的 EditText 写 TextInput 外观修饰链时

## 适用情境

源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。 也包括源 EditText 未声明 background、padding 与高度，外观来自框架主题的 editTextBackground 状态选择器（Holo 为 textfield_default/activated_holo_dark 两张 9-patch，含端头竖线与内容内边距；Material 系为 <inset> 包着随状态切换的 9-patch 选择器 edit_text_material）。应用主题属于 AppCompat 一系（含以 Theme.AppCompat 为祖先的 MaterialComponents 主题）时，editTextBackground 来自 appcompat 库的 abc_edit_text_material（同样是 <inset> 包着按 colorControlNormal 等着色的 9-patch 选择器），第 1 步的选择器、inset 和 9-patch 按应用依赖的 appcompat 版本的库资源取，不取平台资源。

## 例外与边界

- 源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式

## 原因

ArkUI 的 Password 输入框默认显示显隐图标（showPasswordIcon 未设置时 TV 设备为 false、其他设备为 true），源 XML 里不会出现对应属性，只比对源端写出的属性就会漏掉；dumpLayout 的字段 bounds 也看不出这类内部装饰，几何全对不等于外观一致。来源中对齐会话两次读到三个裸 EditText，也已注意到 TextInput 默认高度与源端不同，差异清单仍未列显隐图标；验证只核几何，截图拍了没看，用户随后报告“三个小眼睛”。同一应用的登录页、找回密码页也有同类输入框。TextInput 自带填充底、圆角、内边距与默认高度；只设透明底加 bottom 边框时默认圆角让两端上翘，也没有聚焦态。另一应用的经验摘要写“TextInput 显式覆盖默认填充底为透明+下划线”，写者据此用静态下边框和猜测色近似了状态背景。

## 做法

1. 源 EditText 未声明 background 时外观是主题的状态背景：从本机 SDK 平台资源取 editTextBackground 选择器各状态的 9-patch，随 onFocus/onBlur 切换，padding 取 9-patch 内容区，高度按 wrap_content 结果（内边距 + 文字行高）设置，光标色按 textCursorDrawable；不用 border bottom 加猜测色近似。Material 系的 editTextBackground 是 <inset> 包着 9-patch 选择器：下划线只画在 inset 后的区域内（左右各缩 inset 水平值、离控件底边 inset 底值），文字内距 = inset + 9-patch 内容区，不把 inset 当文字 padding 再让下划线满宽贴底；多行框的最小高度用源字体实际行距 × minLines 加内距，内容不足 minLines 时按 EditText 默认 gravity 竖直居中。TextInput 改透明底时同时显式 borderRadius(0)。
2. 源端密码框没有显隐切换时，在 .type(InputType.Password) 旁写 .showPasswordIcon(false)；数字掩码的验证码框同样处理。
3. 对齐 TextInput 时，除源 XML 写出的属性外，逐项核源端没有、ArkUI 却默认带出的外观：默认填充底、圆角与内边距、默认高度、密码显隐图标、输入时的清除按钮（可用 cancelButton 设为 INVISIBLE）、光标样式；源端没有对应项就显式关闭或覆盖。
4. 修一处后在工程内检索 InputType.Password 等同类字段一并处理，不等用户逐页报告。

## 可选检查

- 真机验证输入框时打开截图目视对照（必要时裁剪输入框右端），不只看 dumpLayout 的 bounds。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕平台 Widget.EditText 的 background 为 ?attr/editTextBackground：EditText 没写 background 时取主题的 editTextBackground
- 〔适用情境 / 做法第 1 步〕Theme.Holo 的 editTextBackground 为 @drawable/edit_text_holo_dark、textCursorDrawable 为 @drawable/text_cursor_holo_dark；基础 Theme 下分别为 @drawable/edit_text 与 @null
- 〔适用情境 / 做法第 1 步〕edit_text_holo_dark 选择器（单行）：可用且聚焦取 textfield_activated_holo_dark，可用且 activated 取 textfield_focused_holo_dark，其余可用态取 textfield_default_holo_dark；多行另有 textfield_multiline_* 一组
- 〔适用情境 / 做法第 1 步〕Theme.Material 系的 editTextBackground 为 edit_text_material：<inset> 左右各 4dp、上 10dp、下 7dp，内部选择器在禁用或未按下未聚焦时用 textfield_default_mtrl_alpha（按 colorControlNormal 着色），其余用 textfield_activated_mtrl_alpha（按 colorControlActivated 着色）
- 〔做法第 1、3 步〕TextInput 的通用属性 padding 默认 { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }；开启下划线模式时默认 { top: 12vp, right: 0vp, bottom: 12vp, left: 0vp }
- 〔做法第 1 步〕TextInput 的 padding 设为 0 时，可把 borderRadius 设为 0 避免光标被截断；光标在边缘显示异常多与 padding、borderRadius 有关
- 〔原因 / 做法第 1 步〕TextInput 改透明底、只设 bottom 边框而不覆盖 borderRadius 时，设备上默认圆角让底边两端上翘
- 〔原因 / 做法第 2 步〕TextInput 的 showPasswordIcon 只在密码类输入模式下生效；未设置时 TV 设备为 false、其他设备为 true
- 〔做法第 2 步〕InputType.Password、NUMBER_PASSWORD、NEW_PASSWORD：TV 设备上输入框末尾默认不显示密码显隐图标，其他设备默认显示
- 〔做法第 3 步〕TextInput 未调用 cancelButton 时清除按钮按 { style: CancelButtonStyle.INPUT }（输入样式）处理；CancelButtonStyle.INVISIBLE 为常隐、CONSTANT 为常显；内联输入模式不支持
