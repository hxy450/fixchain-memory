# 源窗口按 adjustResize 避让软键盘（声明 adjustResize，或未声明 windowSoftInputMode 而窗口含可滚动视图）时设 KeyboardAvoidMode.RESIZE：各页都如此时在窗口级统一设置，否则在该页显示期间设置、离开时还原；不以默认 OFFSET 记作等价

## 何时使用

页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时；为未声明 windowSoftInputMode 的含输入框窗口确定目标避让方式时（源窗口非 windowFullscreen/FLAG_FULLSCREEN）

## 适用情境

源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；规格或页面元数据写明 adjustResize + imePadding 并要求等价避让；目标未设键盘避让模式，转换者不确定默认行为是否等价。前提是源窗口不是全屏标志窗口：主题 windowFullscreen=true 或代码给窗口加了 FLAG_FULLSCREEN 时，adjustResize 被平台忽略、窗口不缩小，不按这条改成 RESIZE，按源端键盘弹出时的实际表现定。 也包括源 Activity 未声明 windowSoftInputMode、内容含 ListView/ScrollView（平台隐式 adjustResize），规格只写“默认弹出”，召回因“源端未声明 adjustResize”而排除了本条。

## 原因

ArkUI 默认的 KeyboardAvoidMode.OFFSET 把页面整体上移以露出焦点输入框，顶部栏可能被推出屏幕、内容区不收缩；源端 adjustResize + imePadding 保留顶栏、收缩内容区。对默认行为不确定却以“保持默认并记录”收尾，会把可实现的避让语义降级。

## 做法

1. 源 Activity 各页都按 resize 避让（含平台隐式 adjustResize）时，在 EntryAbility 的 loadContent 成功回调里经窗口 UIContext 统一调用 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)；只有个别页需要时，在该页 NavDestination 的 onShown 中记下当前模式（getKeyboardAvoidMode）并调用 this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)，onHidden 中还原。
2. 源端 imePadding 加在滚动内容尾部、为末项留出键盘空间时，核对 RESIZE 后末项能滚出键盘；仍被遮挡再按键盘高度补尾部留白，同一边界只避让一次。
3. 对目标默认模式与源端是否等价不确定时，先查 KeyboardAvoidMode 的 SDK 声明与说明再决定。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、3 步〕UIContext.setKeyboardAvoidMode 设置窗口的软键盘避让模式，应用没有调用它时为 KeyboardAvoidMode.OFFSET
- 〔原因 / 做法第 1 步〕KeyboardAvoidMode.OFFSET 为布局整体上移，RESIZE 为布局被压缩；OFFSET_WITH_CARET、RESIZE_WITH_CARET 在输入框光标位置变化时也会调整，NONE 不为键盘调整布局
- 〔适用情境 / 原因〕windowSoftInputMode 的 adjustResize：总是调整窗口大小，内容区缩小为软键盘让出空间
- 〔适用情境 / 做法第 1 步〕没有声明 adjust 类取值时为 adjustUnspecified：系统按窗口内容里有没有能滚动内容的视图在 resize 和 pan 之间选，有就 resize；框架实现是 mScrollContainers 里任一个视图 isShown() 时取 SOFT_INPUT_ADJUST_RESIZE，否则取 SOFT_INPUT_ADJUST_PAN
- 〔适用情境 / 做法第 1 步〕View 没有显式设置 android:isScrollContainer、但启用了竖向滚动条时，构造时自动登记为滚动容器；布局和样式没有另设 android:scrollbars 时，平台样式 Widget.AbsListView（ListView 的父样式）和 Widget.ScrollView 的 scrollbars 为 vertical
- 〔适用情境〕windowSoftInputMode 的 stateUnspecified 是缺省：软键盘是否显示由系统按它认为合适的方式决定，不是无条件弹出
