# 源端禁用态只靠代码换背景、文字色固定时，不用 ArkUI .enabled(false)（会对整个组件降透明）：显式切换背景与投影，用 hitTestBehavior(HitTestMode.None) 或回调内判态拦截点击

## 何时使用

规格提取阶段为 setEnabled/android:enabled 切换的控件写转换决策时；界面实现阶段落实控件禁用态外观与点击拦截时

## 适用情境

源端在 setEnabled(false) 的同时 setBackgroundResource 换成没有 state_enabled 分支的灰色 drawable，textColor 是固定颜色而非 ColorStateList（AppCompat 按钮禁用时投影另归零）；映射参考把 setEnabled(false)/android:enabled 一律对到 .enabled(false)。

## 例外与边界

- 源端禁用外观本身来自 state_enabled 选择器或半透明（ColorStateList 的 disabled 项、Compose 组件默认禁用色）时，按源端色值显式写出；目标默认禁用透明度恰与源值一致时才直接用 .enabled()

## 原因

Android 的 setEnabled 只改状态，颜色由 drawable 与 textColor 选择器决定；ArkUI enabled(false) 会对整个组件（背景与文字）施加默认禁用透明度，源端“不透明灰底、纯白字”就变成发虚的浅灰。

## 做法

1. 先查源端禁用外观的来源：背景 drawable、textColor 有无 state_enabled 分支，按钮 stateListAnimator 在禁用时是否归零。只来自代码换背景时，规格写“禁用 = 换背景 + 不响应点击”，判据写禁用态取色等于源背景值、文字为源色。
2. 实现时不写 .enabled(false)：背景按启停态切换，禁用时投影置空，用 hitTestBehavior(HitTestMode.None) 拦截点击（或在回调内判态直接返回；None 只让本组件不参与触摸测试，不阻塞 Stack 里的下层兄弟和祖先，下层兄弟或祖先带点击处理、或设备接了键盘手柄时，用回调内判态）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；Android SDK 平台资源 android-30、android-34、android-36；appcompat 1.1.0、1.8.0；material 1.4.0、1.8.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕hitTestBehavior(HitTestMode.None) 只让组件自身不参与触摸测试，不阻塞它的子组件、兄弟组件和祖先组件：点在它上面时，子组件、Stack 里位于下层的兄弟组件或祖先组件上的点击、触摸处理仍可能响应。〔成立范围：对象：通用属性 hitTestBehavior。条件：触摸测试（鼠标左键按下也转换成触摸事件）。不成立：换成 HitTestMode.Block（自身响应，阻塞子、兄弟和祖先）时不放行；API 20 起的 BLOCK_DESCENDANTS 让自身和全部后代都不响应，但不影响祖先，祖先上的点击、触摸处理照样响应。〕
- 〔原因〕Android 里 setEnabled(false) 但可点击的 View 在 onTouchEvent 中仍返回 true 消费触摸事件，只是不响应点击，所以点击不会穿透到它下面的 View，也不会交给父布局处理。〔成立范围：对象：android.view.View#onTouchEvent 的禁用分支。条件：View 是 clickable、longClickable 或 contextClickable（设置了点击监听或 Button 默认样式即 clickable）。不成立：调用过 setAllowClickWhenDisabled(true)（android:allowClickWhenDisabled）的 View 禁用时照常处理点击。〕
- 〔适用情境（AppCompat 按钮禁用时投影归零）〕Android 平台 Widget.Material.Button 的 stateListAnimator 在启用态给 elevation 2dp（按下再加 translationZ 4dp），禁用态把 elevation 和 translationZ 都置 0；AppCompat 的 Widget.AppCompat.Button 在 API 21 起继承这个平台样式，MaterialComponents 的 Widget.MaterialComponents.Button 同样是启用 2dp、禁用 0dp。〔成立范围：对象：用这些按钮样式（或其子样式）且没改 stateListAnimator 的 Button / MaterialButton。条件：API 21 起；平台资源 android-30、android-34、android-36 取值一致，appcompat 1.1.0 与 1.8.0、material 1.4.0 与 1.14.0 已核。不成立：Borderless 系列样式的 stateListAnimator 为 @null，本来没有投影；Material3 的 Widget.Material3.Button 启用态 elevation 也是 0（level0），禁用前后都没有投影。〕
- 〔做法第 2 步（回调内判态）〕ArkUI 的 onClick 也可以由键盘或手柄在组件获焦时触发（事件 SourceType 为 KEY 或 JOYSTICK），这条路径不是触摸测试，hitTestBehavior 管不到。〔成立范围：对象：通用事件 onClick 与 hitTestBehavior。条件：设备接了键盘或手柄且组件可获焦；依据是文档说明（hitTestBehavior 文档只涉及触摸测试）。不成立：纯触屏操作时只有触摸路径，hitTestBehavior 生效；enabled(false) 会同时屏蔽按键和焦点事件。〕
- 〔例外与边界〕ArkUI 的 enabled 只在按下时判定：手指按下后、交互过程中再改 enabled 不生效；enabled(false) 时组件不响应点击、触摸、拖拽、按键、焦点、鼠标、悬浮和手势等事件。〔成立范围：对象：通用属性 enabled。条件：依据是文档说明。不成立：要挡住的是本次按下之前就已切成禁用的交互；按下之后才切禁用，这次点击照常完成。〕
