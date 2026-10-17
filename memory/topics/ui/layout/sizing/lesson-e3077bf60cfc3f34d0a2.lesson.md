# layout_marginStart/End 写成 margin 的 start/end 时同一对象各边都用 LengthMetrics；不需要随语言方向翻转时改用 left/right 数值

ID：`lesson-e3077bf60cfc3f34d0a2` · 版本：4 · 阶段：execute · 主题：[ui/layout/sizing](index.md)

概要：方向边距用 end 时各边统一 LengthMetrics

信号：`LengthMetrics`, `layout_marginStart`, `layout_marginEnd`, `@kit.ArkUI`, `.margin({`, `marginEnd`, `RTL`, `supportsRtl`, `paddingStart`

## 何时使用

界面实现阶段，把 layout_marginStart/End、paddingStart/End 或 Compose padding(start/end) 一类方向相关边距写成 ArkUI margin/padding 时；维护映射参考的边距示例时

## 适用情境

源布局用 marginEnd/marginStart（常与 marginBottom 等写在同一控件上）；映射参考把它对到 .margin({ end }) 并给出纯数字示例。

## 原因

含 start/end 键的边距对象按 LocalizedMargin 解析，同一对象里的每一边（包括 top/bottom）都要求 LengthMetrics，写数字编译报 Type 'number' is not assignable to type 'LengthMetrics'。来源映射参考的示例直接写 margin({ end: 10 })，转换者照示例写出 { bottom: 16, end: 16 }，自检只核了 SDK 版本。

## 做法

1. 需要随布局方向翻转时写 .margin({ bottom: LengthMetrics.vp(16), end: LengthMetrics.vp(16) })，并从 @kit.ArkUI 导入 LengthMetrics；同一对象内不混用数字与 LengthMetrics。
2. 源应用未声明 supportsRtl（布局恒 LTR）或源端写的就是物理 left/right 时，统一写 left/right/top/bottom 数值（如 { bottom: 16, right: 16 }）；源端 supportsRtl=true 且用 start/end 时按第 1 条保留逻辑方向，不就近改成 left/right。映射参考示例与 SDK 声明不一致时以声明为准，并修正参考。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [源窗口延伸到系统栏下才全屏，底部避让加在屏底层](../immersion/lesson-0e1c846868f2683cc280.lesson.md)（共享 1 张卡）
- [属性方法不传 ResourceStr 联合值按重载定型](../../../arkts/api-signatures/lesson-63660a8304f7d3920bfc.lesson.md)（共享 1 张卡）
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](../../../arkts/api-signatures/lesson-6e558834938be19c04e2.lesson.md)（共享 1 张卡）
- [声明 RTL 时保留 start/end 并镜像图标](../variants/lesson-786a04847bf10d364d9d.lesson.md)（共享 1 张卡）
- [三键导航按 TYPE_SYSTEM 底高判定后给导航栏着色](../../theme/tokens/lesson-8bc258c2833be65f4fcd.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：rec-5164da4aeb
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-de8de9ff9274ca3ce884](../../../../../store/cases/case-de8de9ff9274ca3ce884/d059c48a9b93c30e4e67d4f95f146b58539dcd29ad987d6d6a4b1dcdd3f6e3f8.json) · 结论：diagnosis, rec-9ed04921b7
  卡片版本：`d059c48a9b93c30e4e67d4f95f146b58539dcd29ad987d6d6a4b1dcdd3f6e3f8`
