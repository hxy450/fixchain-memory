# 浮层关闭动画按触发源传时长，手势收起和自动出场不共用一个硬编码时长

审的是：代码
触发（任一种）：
- 读到：源端上滑超过阈值时 cancel() 主动画，改播另一个 setDuration(...) 不同的 Animator；写错的样子：dismiss() 里固定 animateTo({ duration: 300 }, …)，PanGesture 上滑和定时自动出场都调它
适用范围：把源端横幅、浮层窗口的多组动画迁成 ArkUI 显式动画时
做法：
- 关闭写成 dismiss(duration: number)：上滑手势传源端手势分支 Animator 的时长，自动出场传出场时长
- 对照源码 getView / setView / 触摸回调逐项核对摘要规格有没有漏掉可见行为；漏了就实现，或在交接里列为差异
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- animateTo(value: AnimateParam, event: () => void): void：UIContext 上的显式动画，时长由 AnimateParam.duration 传（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.animateTo）
- AnimateParam.duration：Animation duration, in ms，@default 1000：单位毫秒，和源端 setDuration 同单位，可照搬（出处：鸿蒙 SDK 的 ets/component/common.d.ts，AnimateParam.duration）
- 全局 animateTo：@deprecated since 18，@useinstead UIContext#animateTo：新写的代码用 UIContext 上的那个（出处：鸿蒙 SDK 的 ets/component/common.d.ts，animateTo）
- 改成 dismiss(duration)、上滑传手势分支的时长后，退出时长和源端一致：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-0a19acd6cfea1aafecbe（刺猬猫阅读）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 3；取值 4 ← 诊断
