# ui/navigation/handoff

跳转动作随行的交接：点击出口落实际跳转、跳前写入的共享状态、结果回传写回、同窗口 push 的方向切换与恢复。

[上一级](../index.md)

## 本级经验

- [副作用导航逐出口在 onClick 落实际跳转与参数](lesson-32af50a1dfb0c1c254af.lesson.md) · 阶段：execute/repair · 信号：findNavController().navigate, bundleOf, OpenTripDetail, onClick
- [带回调选择器改路由打开时同一改动接通结果回传](lesson-14509c64bd43100ce443.lesson.md) · 阶段：execute · 信号：DialogFragment, onPop, pushPathByName, show(
- [横屏可触发的 push 先切目标页方向返回后恢复](lesson-17b47c23f2d25008c808.lesson.md) · 阶段：execute · 信号：setRequestedOrientation, window.setPreferredOrientation, NavDestination.onShown, startActivity
- [跳转前写入的共享状态是契约，按原顺序迁移](lesson-dfcdbb19cd93d29159b2.lesson.md) · 阶段：execute/verify · 信号：setPlaylist, startActivity, pushPathByName, onClick
