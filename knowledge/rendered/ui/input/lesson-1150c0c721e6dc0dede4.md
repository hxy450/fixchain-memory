# 按 EditText 对齐 TextInput 时，未声明 background 的输入框按主题状态背景（editTextBackground 的 9-patch，随聚焦切换并取其内边距）复刻，并显式关闭源端没有的 ArkUI 默认装饰：填充底与圆角、Password 显隐图标、清除按钮，核默认高度

## 何时使用

界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时；为未声明 background 的 EditText 写 TextInput 外观修饰链时

## 适用情境

源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。 也包括源 EditText 未声明 background、padding 与高度，外观来自框架主题的 editTextBackground 状态选择器（Holo 暗色单行框为 textfield_default/activated_holo_dark 两张 9-patch（多行框换成 textfield_multiline_* 一组），含端头竖线与内容内边距；Material 系为 <inset> 包着随状态切换的 9-patch 选择器 edit_text_material；AppCompat、MaterialComponents 主题在 API 22 起也取框架的 edit_text_material，appcompat 1.7.x 及更早在 API 21 及以下取库自带的 abc_edit_text_material）。

## 例外与边界

- 源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式

## 原因

ArkUI 的 Password 输入框默认显示显隐图标（showPasswordIcon 默认 true），源 XML 里不会出现对应属性，只比对源端写出的属性就会漏掉；dumpLayout 的字段 bounds 也看不出这类内部装饰，几何全对不等于外观一致。来源中对齐会话两次读到三个裸 EditText，也已注意到 TextInput 默认高度与源端不同，差异清单仍未列显隐图标；验证只核几何，截图拍了没看，用户随后报告“三个小眼睛”。同一应用的登录页、找回密码页也有同类输入框。TextInput 自带填充底、圆角、内边距与默认高度；只设透明底加 bottom 边框时默认圆角让两端上翘，也没有聚焦态。另一应用的经验摘要写“TextInput 显式覆盖默认填充底为透明+下划线”，写者据此用静态下边框和猜测色近似了状态背景。

## 做法

1. 源 EditText 未声明 background 时外观是主题的状态背景：从本机 SDK 平台资源取 editTextBackground 选择器各状态的 9-patch，随 onFocus/onBlur 切换，padding 取 9-patch 内容区，高度按 wrap_content 结果（内边距 + 文字行高）设置，光标色按 textCursorDrawable；不用 border bottom 加猜测色近似。Material 系的 editTextBackground 是 <inset> 包着 9-patch 选择器：下划线只画在 inset 后的区域内（左右各缩 inset 水平值、离控件底边 inset 底值），文字内距 = inset + 9-patch 内容区，不把 inset 当文字 padding 再让下划线满宽贴底；多行框的最小高度用源字体实际行距 × minLines 加内距，内容不足 minLines 时按 EditText 默认 gravity 竖直居中。TextInput 改透明底时同时显式 borderRadius(0)。
2. 源端密码框没有显隐切换时，在 .type(InputType.Password) 旁写 .showPasswordIcon(false)；数字掩码的验证码框同样处理。
3. 对齐 TextInput 时，除源 XML 写出的属性外，逐项核源端没有、ArkUI 却默认带出的外观：默认填充底、圆角与内边距、默认高度、密码显隐图标、输入时的清除按钮（可用 cancelButton 设为 INVISIBLE）、光标样式；源端没有对应项就显式关闭或覆盖。
4. 修一处后在工程内检索 InputType.Password 等同类字段一并处理，不等用户逐页报告。

## 可选检查

- 真机验证输入框时打开截图目视对照（必要时裁剪输入框右端），不只看 dumpLayout 的 bounds。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 平台资源 android-30、android-36（9-patch 另看 android-34；颜色另比 android-33、34）；源码 android-36.1；appcompat 1.1.0、1.8.0；material 1.4.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕Widget.EditText 的 background 为 ?attr/editTextBackground、gravity 为 center_vertical（android-30、android-36 相同）；Widget.Material.EditText 继承 Widget.EditText，没有另设 background；布局、style 都没设 background 时 EditText 的背景就是主题的 editTextBackground
- 〔适用情境 / 做法第 1 步〕应用主题没另设 editTextBackground、textCursorDrawable 时：Theme.Holo 取 @drawable/edit_text_holo_dark、光标 text_cursor_holo_dark；Theme.Holo.Light 取 edit_text_holo_light、光标 text_cursor_holo_light；Theme.Material 与 Theme.Material.Light（平台资源里 Theme.DeviceDefault、Theme.DeviceDefault.Light 的这两项也取自它们）取 edit_text_material、光标 text_cursor_material（android-30、android-36 相同）
- 〔适用情境 / 做法第 1 步〕AppCompat 系主题没另设 editTextBackground 时：appcompat 1.1.0 到 1.7.x（核了 1.1.0、1.3.1、1.6.1、1.7.0）在 API 21 及以下取库自带的 @drawable/abc_edit_text_material，API 22 起经 ?android:attr/editTextBackground 取框架的 edit_text_material；appcompat 1.8.0（minSdk 23）一律取框架的 edit_text_material；Theme.MaterialComponents.Light（material 1.4.0、1.14.0）与 Theme.Material3.Light（material 1.14.0）的 editTextStyle 为 Widget.AppCompat.EditText：它的 background 在 API 22 及以下是库自己的 ?attr/editTextBackground（values/、values-v21），API 23 起 values-v23 把它重定义为直接继承平台 Widget.Material.EditText，取平台的 ?android:attr/editTextBackground，应用只覆写不带 android: 前缀的 editTextBackground 时 API 23 起不起作用
- 〔做法第 1 步〕edit_text_holo_dark 选择器按顺序取第一个匹配项：多行框（state_multiline）用 textfield_multiline_* 一组；单行框在窗口未获焦且可用时为 textfield_default_holo_dark、不可用时为 textfield_disabled_holo_dark；可用且聚焦为 textfield_activated_holo_dark；可用且 activated 为 textfield_focused_holo_dark；其余可用状态为 textfield_default_holo_dark；不可用且聚焦为 textfield_disabled_focused_holo_dark；其余为 textfield_disabled_holo_dark
- 〔做法第 1 步〕Holo 输入框 9-patch 的内容区内边距：textfield_default_holo_dark、textfield_activated_holo_dark、textfield_default_holo_light 在 mdpi、xhdpi、xxhdpi 下都是左 12dp、上 7dp、右 12dp、下 8dp（hdpi 的上边是 10px，合 6.67dp）；这就是 EditText 没另设 padding 时的文字内边距
- 〔做法第 1 步〕edit_text_material 是 <inset>：左右各 4dp、上 10dp、下 7dp（edit_text_inset_horizontal_material、edit_text_inset_top_material、edit_text_inset_bottom_material，android-30、android-36 相同），里面的选择器在不可用、以及未按下且未聚焦时用 textfield_default_mtrl_alpha 并按 ?attr/colorControlNormal 着色，其余（聚焦或按下）用 textfield_activated_mtrl_alpha 并按 ?attr/colorControlActivated 着色；两张 9-patch 的内容区内边距在各密度下都是左 0、上 0、右 0、下 4dp；InsetDrawable.getPadding 返回内层内边距加 inset，所以 EditText 没另设 padding 时文字内边距为左 4、上 10、右 4、下 11dp
- 〔做法第 1 步〕应用主题没另设 colorControlNormal、colorControlActivated、colorAccent、textColorSecondary 时：Theme.Material.Light 的 colorControlNormal（取 textColorSecondary）android-30 为 #8A000000、android-33 起为 #99000000，colorControlActivated（取 colorAccent）为 #FF008577；Theme.Material（暗色）的 colorControlNormal 为 #B3FFFFFF，colorControlActivated 为 #FF80CBC4。Theme.DeviceDefault.Light 在 Android 12 起改取系统色：colorAccent（即 colorControlActivated）为 system_accent1_600，资源默认值 android-31 到 34 为 #00668B、android-35 起为 #475D92，colorControlNormal 随 textColorSecondary（android-31 到 34 为 #40484D、android-35 起为 #44464F），设备按壁纸取色时实际值不同。AppCompat 系主题 API 21 起把框架的 colorControlNormal、colorControlActivated 指向自己的同名属性，所以框架的 edit_text_material 按应用主题的颜色着色：colorControlActivated 取 colorAccent（Theme.AppCompat.Light 默认 #FF008577；Theme.MaterialComponents.Light 的 colorAccent 取 colorSecondary，默认 #FF03DAC6；Theme.Material3.Light 默认 #FF625B71），colorControlNormal 取 ?android:attr/textColorSecondary（Theme.Material3.Light 为 #FF49454F）
- 〔做法第 1 步〕text_cursor_material 是 inset 2dp 的矩形 shape（宽 2dp），按 ?attr/colorControlActivated 着色；Holo 暗色光标 text_cursor_holo_dark 是 drawable-nodpi 下的 9-patch
- 〔适用情境〕EditText 的掩码写法：android:password 为 boolean（已废弃，建议用 inputType）；inputType 的 textPassword = 0x00000081、textWebPassword = 0x000000e1、numberPassword = 0x00000012 都按密码掩码显示（TextView.isPasswordInputType），textVisiblePassword = 0x00000091 不掩码
- 〔原因 / 做法第 2 步〕TextInputAttribute.showPasswordIcon(value: boolean)（@since 9）：密码模式下输入框末尾的显隐图标是否显示；没调用时 TV 设备为 false、其他设备为 true；InputType.Password、NUMBER_PASSWORD（@since 11）、NEW_PASSWORD（@since 11）三种密码模式都按这个默认显示该图标
- 〔原因〕InputType.Password 的 TextInput 没写 showPasswordIcon 时，设备上每个密码框末尾都显示显隐图标；dumpLayout 里 TextInput 节点的 bounds 看不出这个图标
- 〔原因 / 做法第 3 步〕TextInput 没另设 padding 时默认内边距为上 8vp、右 16vp、下 8vp、左 16vp；开启下划线模式时为上 12vp、右 0、下 12vp、左 0；padding 设为 0 时文档建议把 borderRadius 也设为 0，避免光标被截断
- 〔原因 / 做法第 1 步〕TextInput 设透明底、只设下边框、没设 borderRadius 时，设备上下边线两端随默认圆角向上弯
- 〔做法第 3 步〕TextInputAttribute.showUnderline(value: boolean)（@since 10）默认 false；文档同一句写下划线默认颜色 '#33182431'、粗细 1px、输入框默认高度 48vp；下划线只支持 InputType.Normal，密码模式下不生效
- 〔做法第 3 步〕TextInputAttribute.cancelButton(options: CancelButtonOptions)（@since 11）设置右侧清除按钮样式，没调用时默认为 { style: CancelButtonStyle.INPUT }，内联模式不支持；另有 cancelButton(symbolOptions: CancelButtonSymbolOptions)（@since 18）；CancelButtonStyle（声明在 search.d.ts，@since 10）：CONSTANT 常显、INVISIBLE 常隐、INPUT 输入样式
- 〔做法第 1、3 步〕通用方法 borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T（@since 7）、onFocus(event: () => void): T 与 onBlur(event: () => void): T（@since 8）；TextInputAttribute.caretColor(value: ResourceColor) 默认 '#007DFF'，caretStyle(value: CaretStyle)（@since 10）设光标宽度和颜色
