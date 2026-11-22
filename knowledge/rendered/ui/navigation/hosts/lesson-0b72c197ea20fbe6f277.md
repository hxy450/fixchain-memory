# 一进入就无条件跳转并 finish 的 Activity 是路由跳板：目标按同样条件直达实际页面，不把它的布局做成可见页

## 何时使用

页面转换阶段迁移入口类 Activity、以及调用方为 Intent(X) 确定目标路由时

## 适用情境

Android Activity 在 onCreate/initView 开头按条件 startActivity 到另一页并立即 finish()（如登录入口按配置转到短信登录或一键登录），它的布局文件仍含可渲染的按钮；多个调用方以 Intent 指向这个跳板 Activity。只在 onCreate/initView 的每条分支都 startActivity 并 finish()、用户在任何条件下都看不到它的布局时才算跳板；若有分支不跳转、留下显示布局（如条件不满足时停在本页），这个布局仍是可见页，照常转换，只把跳走的分支按跳板处理。

## 原因

照布局渲染会凭空多出一层用户在 Android 上看不到的选择页，无条件跳转被降级成“点击后跳转”；调用方按类名映射把入口指向这一页，就多了一步。来源中转换者读到入口判断与两支 finish 后，仍以布局为真值建了可见的登录方式选择页，并在报告里称其“对应启动后 finish”；个人中心的登录入口随之指向选择页。

## 做法

1. 页面转换时先读 onCreate/initView：开头无条件跳转并 finish 的按跳板处理；目标页进入时按同样条件 replacePath 到实际目标，或在转换报告中要求调用方直接路由到实际目标。
2. 调用方翻译 Intent(X) 时，确认 X 是否一进入就跳走，导航指向用户实际看到的首屏。
3. 报告若把无条件跳转改成了点击后跳转，把它作为行为改变显式标出。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Activity 在 onCreate 里调用 finish() 时，onCreate 之后立即执行 onDestroy，onStart、onResume、onPause 等其余生命周期都不执行，这个 Activity 的布局不会显示给用户
- 〔做法第 1 步〕NavPathStack.replacePathByName 把当前路由栈栈顶页退出、再把 name 指定的页面入栈；animated 不写时为 true（有转场动画）
