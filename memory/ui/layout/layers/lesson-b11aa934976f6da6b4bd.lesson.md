# 页面级全屏遮罩与一次性全屏动效层只在需要时作为条件子节点挂载，不常驻、不用 .overlay() 条件 builder

ID：`lesson-b11aa934976f6da6b4bd` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，为页面加保存中、引导等全屏遮罩，或实现彩纸等一次性全屏动效的覆盖层时

## 适用情境

页面要在带安全区 padding 的根容器上加全屏遮罩；或源端在触发瞬间向窗口根视图（rootView/decorView）添加全屏、不可点击的动效层并在播完后移除，目标准备改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。同仓可能已有用根 Stack 条件子节点实现的同类遮罩。

## 原因

已观察到 .overlay() 挂条件 builder 在条件为假时仍产生拦截触摸的层，挂在带 padding 的容器上又只覆盖内容盒、盖不到底部安全区。常驻的全屏组件即使内部 Canvas 设 None，外层组件节点仍按默认命中模式拦截，下层页面不能点击和滑动。

## 做法

1. 页面级全屏遮罩用无 padding 的根 Stack 条件子节点实现（条件为假时不产生节点）；复用同仓遮罩时连同挂载层级一起复用，不只复制遮罩内容。
2. 一次性全屏动效按源端生命周期只在播放期间条件渲染，结束或取消回调里移除；不让全屏组件常驻、只靠内部子节点的 HitTestMode.None 放行。

## 可选检查

- 改动后空闲态用 dumpLayout 确认该节点不存在，再实测点击、横滑与折叠；遮罩显示时核对从状态栏到底部安全区都被覆盖。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-37ef7d33ab4655385e6f](../../../../store/cases/case-37ef7d33ab4655385e6f/fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee`
- [case-51d51ad98738e338df19](../../../../store/cases/case-51d51ad98738e338df19/4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7.json) · 结论：diagnosis, recommendation:1
  卡片版本：`4b4648a54d0b19a84c842088554c0b057c5c8941db9a7d98ae885a39678a9db7`
