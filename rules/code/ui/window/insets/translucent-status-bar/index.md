# 透明状态栏下的顶部留白和背景

agent 会看到什么：源端透明状态栏下用 layout_marginTop / topMargin 给顶栏留位、背景铺到状态栏后；产物里路由页的 .margin / .padding({ top })、状态栏高度和 expandSafeArea 写在哪个节点

## 规矩

- rule-37a90c907b86｜源端透明状态栏下的固定顶距，路由页只补「源顶距 − 已消费 inset」｜读到：源页面在透明状态栏（QMUIStatusBarHelper.translucent）下用 layout_marginTop 给标题栏留位，顶距从屏幕顶部量起、包含状态栏；写错：全屏窗口下的路由页（NavDestination / HMRouter 页）照搬源顶距写 .margin({ top: 源值 })，页面内容其实已从状态栏下沿排布，顶部多出一块空白
- rule-b7e585f6fc77｜源端背景铺到状态栏后、只把顶栏下移时，目标在背景节点本身加 expandSafeArea(TOP)｜读到：源码只给顶栏 updateLayoutParams { topMargin = 状态栏高度 }，背景铺在透明状态栏后面；写错：背景节点写成「固定高度 + 状态栏高度」、文字列 padding top 为「状态栏高度 + N」，背景节点本身没有 .expandSafeArea，背景到不了状态栏
