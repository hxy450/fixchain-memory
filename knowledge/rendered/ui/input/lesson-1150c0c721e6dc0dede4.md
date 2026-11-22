# 按 EditText 对齐 TextInput 时，未声明 background 的输入框按主题状态背景（editTextBackground 的 9-patch，随聚焦切换并取其内边距）复刻，并显式关闭源端没有的 ArkUI 默认装饰：填充底与圆角、Password 显隐图标、清除按钮，核默认高度

## 何时使用

界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时；为未声明 background 的 EditText 写 TextInput 外观修饰链时

## 适用情境

源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。 也包括源 EditText 未声明 background、padding 与高度，外观来自框架主题的 editTextBackground 状态选择器（Holo 为 textfield_default/activated_holo_dark 两张 9-patch，含端头竖线与内容内边距；Material 系为 <inset> 包着随状态切换的 9-patch 选择器 edit_text_material）。

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-30、android-36；appcompat 1.1.0、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕TextInput 的 type 为密码类输入模式（InputType.Password，以及 API 11 起的 NUMBER_PASSWORD、NEW_PASSWORD）时，输入框末尾默认显示显隐（小眼睛）图标：showPasswordIcon 默认值在 TV 设备为 false、其他设备为 true。〔成立范围：对象：type 为 InputType.Password、NUMBER_PASSWORD（11+）或 NEW_PASSWORD（11+）的 TextInput；Normal、Number 等非密码类型不显示该图标。条件：应用未调用 showPasswordIcon；依据是文档说明。不成立的情形：TV 设备默认不显示。〕
- 〔做法第 3 步〕TextInput 未设 padding 时默认内边距为上下 8vp、左右 16vp；开启 showUnderline 下划线模式时默认改为上下 12vp、左右 0vp，下划线默认颜色 '#33182431'、粗 1px，文本框尺寸 48vp。〔成立范围：对象：TextInput 的通用属性 padding 与 showUnderline（API 10+）。条件：应用未显式设 padding。不成立的情形：下划线只支持 InputType.Normal，Password 等类型开启 showUnderline 不生效。〕
- 〔做法第 1 步〕InputType.Password 模式下 decoration、showUnderline、lineHeight 三个属性不生效，设置了也被忽略。〔成立范围：对象：type 为 InputType.Password 的 TextInput。条件：鸿蒙文档 InputType 枚举说明。不成立的情形：type 为 InputType.Normal 时这三个属性按各自说明生效。〕
- 〔做法第 1 步〕stateStyles 只对通用属性生效，TextInput 的 backgroundColor 是组件私有属性，写在 stateStyles 的 focused、normal 里不会切换，文档给的替代是 attributeModifier 动态设置。〔成立范围：对象：TextInput 放在 stateStyles 里的私有属性（backgroundColor 等）。条件：API 8+ 多态样式；焦点态还要求焦点激活态开启。不成立的情形：border、opacity 等通用属性可以在 stateStyles 里切换。〕
- 〔适用情境 / 做法第 1 步〕Material 系 editTextBackground 是 edit_text_material：<inset> 左右各 4dp、上 10dp、下 7dp，里面 9-patch 的内容区下侧再留 4dp，所以未声明 background 与 padding 的 EditText 文字内距为左 4dp、上 10dp、右 4dp、下 11dp；下划线未聚焦时着 colorControlNormal，聚焦或按下时着 colorControlActivated。〔成立范围：对象：Theme.Material.* 下的框架 EditText，以及 AppCompat 主题在 API 22+ 设备上的 EditText（appcompat 的 values-v22 把 editTextBackground 指回平台属性）。条件：android-30、android-36 资源一致；未写 android:background、padding。不成立的情形：AppCompat 主题在 API 21 及以下用库内 abc_edit_text_material，不按这组数。〕
- 〔适用情境 / 做法第 1 步〕Theme.Holo（暗色）的 EditText 背景 textfield_default_holo_dark、textfield_activated_holo_dark 两张 9-patch 的内容区都是左右 12dp、上 7dp、下 8dp，未声明 padding 时文字内距即此值；Widget.EditText 默认 gravity 为 center_vertical。〔成立范围：对象：Theme.Holo 下未写 background、padding 的 EditText。条件：android-30、android-36 的 mdpi 与 xhdpi 资源一致。不成立的情形：应用设了 android:padding 或自定义 background 时按应用值。〕
