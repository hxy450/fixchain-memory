# 底部元素已有固定 bottom 偏移时，先和实测避让高度比，够用就不追加避让

审的是：代码
触发（任一种）：
- 读到：底部定位元素已写 .position({ bottom: 固定值 })，避让值来自 TYPE_NAVIGATION_INDICATOR 的 bottomRect.height；写错的样子：改成 .position({ bottom: 固定值 + px2vp(避让高度) })，或把用户没提到的组件也一并加上避让
适用范围：全屏沉浸窗口里，已有固定底部偏移的指示器、圆点等底部定位元素
做法：
- 比较固定偏移和 px2vp(bottomRect.height)：偏移已大于避让高度就保持原 .position({ bottom: 固定值 })，不追加
- 用户没提出的组件不并入同一次避让改动
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- position(value: Position | Edges | LocalizedEdges): T：Edges 形式可写 bottom 偏移（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- Rect.height 单位 px：比较前先 px2vp（出处：arkts-apis-window-i.md，Rect）
- 实测两种导航栏都低于原有的固定底部偏移，恢复原偏移即可：凭猜测的导航栏高度追加避让是多余的（出处：卡里修好并验证过）
未核实：卡里的行为在 API 16（HarmonyOS 5.0.4）上观察
来源：1 张卡，1 个应用
- case-b8f680bbcacac3667ae0（五星智投）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 3 ← 诊断
