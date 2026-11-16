# ScrollView 没写的滚动条外观和进页唤醒

agent 会看到什么：读到 HorizontalScrollView / ScrollView 没写 android:scrollbars、fadeScrollbars、scrollbarSize、scrollbarThumb*，外观和进页唤醒（initialAwakenScrollBars）取自平台和 Activity 主题；产物里 Scroll 的 .scrollBar(BarState…) 切换时机、有没有 .scrollBarWidth / .scrollBarColor

## 规矩

- rule-5ce1f4776407｜滚动视图没写滚动条外观时，Scroll 按源主题写 scrollBarWidth 和 scrollBarColor｜读到：源 `HorizontalScrollView` / `ScrollView` 没写 android:scrollbarSize、android:scrollbarThumbHorizontal / scrollbarThumbVertical，外观取自 Activity 主题（如 `Theme.Material.Light` 一族，不一定是 Holo）；写错：目标 `Scroll` 只写了 .scrollBar( 和 .edgeEffect(，没有 .scrollBarWidth( / .scrollBarColor(，转换报告里也没登记这项近似
- rule-0426b9d6d089｜复刻进页唤醒滚动条时，Scroll 到时切 BarState.Off，触摸按下再切 Auto｜读到：源 `HorizontalScrollView` / `ScrollView` 没写 android:fadeScrollbars、android:scrollbars 等滚动条属性，窗口可见时由 initialAwakenScrollBars 先显示滚动条再淡出；写错：目标 `Scroll` 进页设 `BarState.On`，setTimeout 到时切回 `BarState.Auto`（或先切 `BarState.Off`、不久再切 `BarState.Auto`）
