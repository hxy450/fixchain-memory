# 源端没有的入口控件

agent 会看到什么：派工、修复条目或台账要求补一个入口（按 Android 可达入口补 UI、在对等页面补替代页入口），交回的代码新增了源布局里没有的 Button、Row 或 Image

## 规矩

- rule-5a9012370d3e｜执行「按 Android 可达入口补 UI」前先找到源端控件，找不到就回报不适用，不新增按钮｜读到：修复条目要求「按 Android 可达入口补 UI」，源布局 XML 和 Fragment 的 setOnClickListener 里找不到对应控件；写错：ArkTS 页面新增源端没有的按钮行（如 `if (!isAuthenticated) { Row { Button(...) } }`），修复报告记为 FIXED
- rule-8e676514f475｜在对等页面补替代页入口时不加源端没有的可见控件，改用已有区域的 LongPressGesture｜写错：对等页面的组件里新增源端没有的 Button / Image 入口（onClick 跳到替代页），挤压原有内容；源端该组件只有固定几个子元素（如地址文本 + 下拉箭头），台账又限定不得改变该页布局；输出里自称「未越界」
