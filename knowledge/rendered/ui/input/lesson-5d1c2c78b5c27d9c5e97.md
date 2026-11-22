# EditText.setError 迁为尾部错误图标加仅聚焦时显示的气泡、输入即清，不用 errorMessage 常显红字或行内文字

## 何时使用

规格提取与界面实现阶段，为源端 EditText.setError（含 AppCompatEditText）写转换决策并落实校验失败提示时

## 适用情境

源端校验失败时对输入框调用 setError(文案)，没有自定义错误视图；目标为 ArkUI TextInput，候选是 TextInput.errorMessage、输入框下方的行内红字或自绘气泡；规格可能写成“实时校验”或“HarmonyOS 自带错误提示”。

## 例外与边界

- 源端用 Material TextInputLayout.setError（框下常显错误文字）而不是 EditText.setError：按该控件的呈现实现
- 源端调两参的 setError(文案, 图标) 时，错误图标用源端给的 drawable，不换成平台 indicator_input_error；出错期间错误图标暂占该框末端的复合图位置，框原有的末端图标（drawableEnd/Right）在错误清除后恢复，目标叠错误图标时不删掉原末端图标
- 源端在文本变化回调（TextWatcher）里调用 setError 时，源端本来就是边输入边校验，照源端在输入时重设错误，不按「输入即清」处理

## 原因

TextView.setError 的呈现是尾部 compound drawable 位置的错误图标，加上只在该框获得焦点时弹出的错误气泡（Editor 的 ErrorPopup）；按键改变文本时图标与消息一起清除（本机 SDK android-36.1 源码 TextView.setError 的注释与实现）。errorMessage 或行内红字常显在框下、改变布局高度且不随焦点出现，校验时机也被改成实时校验。

## 做法

1. 规格转换决策写成“尾部错误图标 + 仅聚焦时显示的错误气泡 + 输入即清除”，并保留源端调用 setError 的时机（如点保存或确认时才校验）；不写成 errorMessage 或实时校验。
2. 实现时在输入框尾部叠错误图标（取平台 indicator_input_error 资源，本机 SDK platforms/android-<api>/data/res），用锚定该框的 bindPopup 或自绘气泡显示文案，可见条件为“有错误且该框聚焦”；用 bindPopup 时在 onStateChange 里把显示状态同步回去（autoCancel 默认 true，页面有操作时气泡会自行关闭）；该框 onChange 时清除其错误状态。多个框同时出错时各自保留图标，气泡只随聚焦的框显示。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕TextView.setError(文案) 把错误图标放在文字末端的 compound drawable 位置（LTR 在右、RTL 在左），文案只在该框获得焦点时以弹出气泡显示；setError(null) 同时清掉图标和文案
- 〔原因 / 做法第 2 步〕调用 setError 时该框已有焦点则立刻弹出气泡，没焦点则只显示图标；之后该框获得焦点时弹出气泡，失去焦点时气泡收起、图标保留
- 〔原因 / 做法第 2 步〕用户输入改动该框文本后，错误图标和文案一起被清掉；只有在这次改动的回调（如 TextWatcher）里又调用了 setError 时才保留新的错误
- 〔原因〕错误气泡是 Editor 里一个不可获焦的 PopupWindow（ErrorPopup），挂在输入框下方（下方放不下时翻到上方），箭头对准错误图标，不占布局、不改变输入框高度
- 〔做法第 2 步〕setError 用的平台图标 indicator_input_error 是位图，mdpi 下 20×20 像素（即 20dp，hdpi 到 xxhdpi 依次 30、40、60 像素），按图片原尺寸放置
- 〔做法第 2 步〕应用主题没有另设 errorMessageBackground 时：Theme.Material.Light 与 Holo Light 下气泡背景是 popup_inline_error_holo_light，Theme.Material 与 Holo 暗色下是 popup_inline_error_holo_dark；气泡文字用 textAppearanceSmall、颜色 textColorPrimaryInverse
- 〔做法第 1 步〕TextInput 的 showError 默认不显示错误状态；传 ResourceStr 时显示错误文本（单行放不下时末尾省略），传 undefined 时不显示；内联模式（TextInputStyle.Inline）不支持
- 〔做法第 2 步〕bindPopup 的 PopupOptions 不设时：placement 为 Placement.Bottom，mask 为 true（透明遮罩层），autoCancel 为 true（页面有操作时气泡自动关闭），showInSubWindow 为 false；显示状态变化经 onStateChange 回调告知
- 〔做法第 2 步〕绑定气泡的组件被销毁时气泡消失但不触发 onStateChange；横竖屏旋转或应用进入后台时气泡也会自动消失
- 〔做法第 2 步〕CustomPopupOptions 的 focusable 不设时为 false，自定义气泡弹出后不获焦
