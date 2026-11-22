# EditText.setError 迁为尾部错误图标加仅聚焦时显示的气泡、输入即清，不用 errorMessage 常显红字或行内文字

## 何时使用

规格提取与界面实现阶段，为源端 EditText.setError（含 AppCompatEditText）写转换决策并落实校验失败提示时

## 适用情境

源端校验失败时对输入框调用 setError(文案)，没有自定义错误视图；目标为 ArkUI TextInput，候选是 TextInput.errorMessage、输入框下方的行内红字或自绘气泡；规格可能写成“实时校验”或“HarmonyOS 自带错误提示”。

## 例外与边界

- 源端用 Material TextInputLayout.setError（框下常显错误文字）而不是 EditText.setError：按该控件的呈现实现

## 原因

TextView.setError 的呈现是尾部 compound drawable 位置的错误图标，加上只在该框获得焦点时弹出的错误气泡（Editor 的 ErrorPopup）；按键改变文本时图标与消息一起清除（Android 源码 TextView.setError 的注释与实现，android-36.1）。errorMessage 或行内红字常显在框下、改变布局高度且不随焦点出现，校验时机也被改成实时校验。

## 做法

1. 规格转换决策写成“尾部错误图标 + 仅聚焦时显示的错误气泡 + 输入即清除”，并保留源端调用 setError 的时机（如点保存或确认时才校验）；不写成 errorMessage（ArkUI TextInput 里对应的属性是 showError）或实时校验。
2. 实现时在输入框尾部叠错误图标（取平台 indicator_input_error 资源：Android SDK platforms/android-<api>/data/res 下 drawable-*dpi 目录里的 PNG，按 20vp × 20vp 显示；输入框尾部内边距加上图标宽，文字不压到图标下面），用锚定该框的 bindPopup 或自绘气泡显示文案，可见条件为“有错误且该框聚焦”（用 bindPopup 时设 mask: false、autoCancel: false，并在 onStateChange 里同步显示变量：两者默认都是 true，点按页面别处就会关掉气泡；源端气泡不获焦、不拦截气泡以外的触摸，点页面别处不会关掉，只在该框失焦、用户改动文本、代码清除错误或该框离开窗口时消失）；该框 onChange 时清除其错误状态。多个框同时出错时各自保留图标，气泡只随聚焦的框显示。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1；平台资源 android-36、android-37.0（indicator_input_error 另比对 android-30/33）；appcompat 1.1.0、1.8.0（字节码）；material 1.12.0（官方仓库源码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕TextView.setError(CharSequence error)：error 非空时取内部资源 indicator_input_error 作图标（边界设为固有尺寸）再调用 setError(error, icon)；error 为 null 时消息和图标一起清掉。setError(CharSequence, Drawable) 的图标要事先 setBounds。图标放在右侧 compound drawable 的位置（布局方向为 RTL 时放左侧），显示期间暂时顶替原来那一侧的 compound drawable，清掉错误后恢复原图标；图标所在那一侧的文字区内边距（getCompoundPaddingRight，RTL 时 getCompoundPaddingLeft）让出图标宽加 drawablePadding
- 〔原因〕错误气泡只在该框有焦点时显示：调用 setError 时框已获焦就立即弹出，否则只显示图标；之后框获得焦点且仍有错误时弹出，失去焦点时收起气泡、图标保留；框还没挂到窗口上时，等到挂上窗口那一刻才弹出；框从窗口卸下时也收起气泡
- 〔原因〕错误的自动清除：可编辑文本的每次改动先在 handleTextChanged 里复位「错误已改」标志，随后在 afterTextChanged（先通知各 TextWatcher.afterTextChanged）末尾调用 hideErrorIfUnchanged，标志仍是复位状态就 setError(null, null)，所以用户经输入法或按键改动文本时图标和消息一起消失，代码直接改 Editable（append、replace、clear 等）同样经过 handleTextChanged、也会清掉；同一次改动里 TextWatcher 又调用了 setError 的，新错误保留；按键由 KeyListener 处理后也会调用 hideErrorIfUnchanged。setText 换掉整个文本、不经过 handleTextChanged、不复位这个标志，单独调用 setText 不会清掉刚设的错误
- 〔原因〕错误气泡是 Editor.ErrorPopup（PopupWindow 子类），不在布局里、不占布局高度：内容是内部布局 textview_hint 的 TextView（textAppearance 为 ?android:attr/textAppearanceSmall，Material 主题下 14sp；文字色 ?android:attr/textColorPrimaryInverse）；setFocusable(false)，窗口不获焦、也不拦截气泡以外的触摸（FLAG_NOT_FOCUSABLE 同时开启 FLAG_NOT_TOUCH_MODAL）；输入法模式 INPUT_METHOD_NEEDED，按需要输入法的窗口排序，不盖在输入法上
- 〔原因 / 做法第 2 步〕错误气泡的位置和尺寸：用 showAsDropDown 挂在输入框下方，箭头尖指向错误图标水平中心（箭头尖距气泡右边缘 25dp），气泡顶边比图标底边高 2dp；下方放不下时翻到输入框上方并换用 errorMessageAboveBackground 背景。宽度为错误文本按最大 240dip（textview_error_popup_default_width，各屏幕配置都是这一值）折行后最宽一行的宽度加背景内边距，高度为文本高度加背景内边距
- 〔原因 / 做法第 2 步〕应用主题没有另设 errorMessageBackground、textColorPrimaryInverse 时，错误气泡的样子随主题：Theme.Material.Light 及其子主题（含 DarkActionBar 变体；API 21 起的设备上 Theme.AppCompat.Light、Theme.MaterialComponents.Light 系列也继承到它，appcompat 1.1.0–1.8.0、material 1.4.0–1.14.0 都没有动这两项）用 popup_inline_error_holo_light 九宫图（深灰底、顶边一条红色、靠右上的向上红色箭头），文字 #ffffffff；Theme.Material（深色）和 Theme.AppCompat 深色系列用 popup_inline_error_holo_dark（浅灰底、同样的红边和箭头），文字 #de000000；DayNight 主题日间取前者、夜间取后者。会动文字色的常见父主题：Theme.DeviceDefault 系列不动背景，Android 12（API 31）起设了 textColorPrimaryInverse——API 31–35 为 text_color_primary_device_default_dark / _light，android-36 起为系统动态色 system_on_surface_dark / system_on_surface_light（DeviceDefault.Light 下是浅色字，深色 DeviceDefault 下是深色字），Android 11 及以前不设；Material 组件库的 Theme.Material3.Light / Dark（material 1.8.0、1.12.0 都是）把 textColorPrimaryInverse 设为 M3 的 on_surface 色（Light 下浅色字，1.12.0 为 #ffe6e0e9；Dark 下深色字，1.12.0 为 #ff1d1b20），背景不动。翻到上方时用对应的 popup_inline_error_above_holo_*。两张背景都标了 autoMirrored，RTL 下镜像
- 〔做法第 2 步〕indicator_input_error 是框架内部资源（com.android.internal.R.drawable，不在公开的 android.R.drawable 里），以 PNG 放在 drawable-ldpi、mdpi、hdpi、xhdpi、xxhdpi，像素分别为 15、20、30、40、60 见方，各密度都是 20dp × 20dp；图案是红色实心圆里一个白色感叹号；android-30、33、36、37.0 都有这组文件
- 〔何时使用〕androidx AppCompatEditText 继承 android.widget.EditText，没有覆写 setError（appcompat 1.1.0、1.8.0 的字节码里都没有这个方法），setError 的呈现与平台 TextView 相同
- 〔例外与边界〕Material TextInputLayout.setError(CharSequence)（material 1.12.0）：错误消息显示在其中的 EditText 下方；传 null 或空串都清除；错误功能没开时，传非空文本会自动开启；先调用 setErrorEnabled(true) 的，错误出现时布局尺寸不变。它给 EditText 挂的 TextWatcher 不清错误，用户输入后错误仍显示，由应用自己调用 setError(null) 清掉
- 〔适用情境 / 做法第 1 步〕ArkUI TextInput 的错误文本属性是 showError(value?: ResourceStr | undefined): TextInputAttribute（API 10 起；value 支持 Resource 自 API 12）：值为 ResourceStr 时显示错误文本，单行放不下时末尾省略号；为 undefined 时不显示错误状态；默认不显示；内联模式（TextInputStyle.Inline）不支持；Wearable 设备上 13fp、居中。声明和文档都没有写它随焦点显示或隐藏。鸿蒙 SDK 的组件声明里没有名为 errorMessage 的属性
- 〔做法第 2 步〕TextInput 没有另设 padding 时，内边距默认 { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }；开启下划线模式时为 { top: 12vp, right: 0vp, bottom: 12vp, left: 0vp }
- 〔做法第 2 步〕bindPopup(show: boolean, popup: PopupOptions | CustomPopupOptions): T 是通用属性（CommonMethod，API 7 起），show 默认 false，API 18 起 show 支持 !! 双向绑定；页面还在构建时就把 show 设为 true，气泡的位置和形状会出错；宿主组件销毁、横竖屏旋转或应用进入后台时气泡自动消失，这时不触发 onStateChange、onWillDismiss；同一窗口里后弹出的气泡层级更高；不支持在 attributeModifier 里调用
- 〔做法第 2 步〕PopupOptions 的位置和外观（应用没有另设时）：message: string 必填；placement 默认 Placement.Bottom，设定位置放不下时自动避让到能完整显示的位置；targetSpace 默认 8vp；enableArrow 默认 true；arrowPointPosition（API 11 起，ArrowPointPosition.START / CENTER / END，默认 CENTER）决定箭头指向宿主的哪个位置点、不超出宿主范围，设了它 arrowOffset 就不生效；arrowWidth 16vp、arrowHeight 8vp；radius 20vp；popupColor 默认透明加 COMPONENT_ULTRA_THICK 模糊背景；shadow 默认 ShadowStyle.OUTER_DEFAULT_MD；文字样式用 messageOptions: { textColor, font }
- 〔做法第 2 步〕PopupOptions 的关闭行为（应用没有另设时）：mask 默认 true（透明遮罩层）；autoCancel（API 11 起）默认 true，页面有操作时气泡自动关闭；onWillDismiss（API 12 起）默认 true，响应点击、侧滑、三键 back 关闭；气泡打开或关闭时 onStateChange 回调 { isVisible }；PopupOptions 没有 focusable 字段，CustomPopupOptions.focusable（API 11 起）默认 false，气泡弹出后不获焦
- 〔做法第 2 步〕PopupOptions.keyboardAvoidMode（API 15 起）默认 KeyboardAvoidMode.NONE，气泡不避让软键盘；KeyboardAvoidMode.DEFAULT（0）为避让并在到达极限高度后压缩高度。这个 KeyboardAvoidMode 是 common.d.ts 里的全局枚举（DEFAULT = 0、NONE = 1），和 @ohos.arkui.UIContext 里页面级的 KeyboardAvoidMode（OFFSET、RESIZE 等）不是同一个
- 〔做法第 2 步〕焦点和改动回调：onFocus(event: () => void): T、onBlur(event: () => void): T 是通用事件（API 8 起）；TextInput.onChange(callback: EditableTextOnChangeCallback)，回调为 (value: string, previewText?: PreviewText, options?: TextChangeOptions) => void，value 是正式上屏的文本，输入法预上屏的内容在 previewText 里；onWillChange 在改动前触发、返回 false 可拦截，onChange 在改动完成后触发。文档没有写用代码改 text 时是否触发 onChange
