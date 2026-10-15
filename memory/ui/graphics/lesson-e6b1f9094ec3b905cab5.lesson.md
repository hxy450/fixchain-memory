# animated-vector 按 atEnd 在起止帧之间实现过渡；同名静态 SVG 只是起始帧，不当作完整实现

ID：`lesson-e6b1f9094ec3b905cab5` · 版本：4

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为 AnimatedImageVector/animated-vector 图标确定实现方案、各状态显示的帧与状态切换时的过渡时；以及资源迁移阶段遇到 animated-vector 时

## 适用情境

源码用 AnimatedImageVector.animatedVectorResource 与 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定，animated-vector 的 objectAnimator 以 pathData 的 valueFrom/valueTo 描述两态之间的形变，带 duration 与 interpolator；目标没有直接等价组件，资源目录里的同名媒体可能是资源迁移从起始帧导出的静态 SVG；规格可能允许资源动画或等价符号，或写“图标态切换即可满足”。

## 例外与边界

- 决策记录以编号批准省略形变过渡、差异验收与之一致时，按批准的两态静态帧或等价符号实现，仍按状态分别给出起止帧
- objectAnimator 的 propertyName 不是 pathData（AnimatedVectorDrawable.java 列出的 rotation、fillAlpha、trimPathEnd 等）：不按本条在两组 pathData 间逐数值插值，按该属性另行映射；atEnd 两态与源 duration、插值器仍照源保留

## 原因

直接引用同名静态图，所有状态都显示起始帧，例如已完成的状态仍显示开始态图形；资源阶段导出起始帧时映射表若不标注，后续写者会把它当完整资源。两态静态帧或符号切换只修正了状态对应的帧，两态之间的过渡仍然丢失；规格以“无直接等价、图标态切换即可”定案时，下游会把未实现的过渡当作已覆盖。

## 做法

1. 规格阶段读 painter 的 atEnd 由哪个状态决定，再打开对应 *_anim.xml，取 objectAnimator 的 propertyName、valueFrom/valueTo、duration 与 interpolator，把两态之间的过渡写成保真要求并给出实现路线，不以“无直接等价、图标态切换即可”作转换决策。
2. 实现 atEnd 语义：false 画首帧、true 画末帧；propertyName 为 pathData 时，状态变化按源 duration 与插值器（fast_out_slow_in 的控制点为 (0.4, 0, 0.2, 1)，见 platforms/android-<api>/data/res/interpolator/fast_out_slow_in.xml；对应 Curve.FastOutSlowIn（@ohos.curves.d.ts 注为 cubic-bezier(0.4, 0.0, 0.2, 1.0)），或直接写 curves.cubicBezierCurve(0.4, 0, 0.2, 1)）在两组 pathData 的同序数值之间插值，在 Canvas 等可按进度重绘路径的载体中按源 viewport 缩放绘制；反向切换从当前帧回放。AVD 的 pathData 形变本身要求起止路径命令结构一致（AnimatorInflater.java 以 PathParser.canMorph 校验），可逐数值插值。
3. 只有批准的降级才用两态静态帧、语义相符的系统 SymbolGlyph（名称以本地 SDK 的 sysResource 为准）或独立终点图形，并按状态分别给出两帧；同名媒体已存在时打开核对它画的是哪一帧。
4. 资源迁移阶段为保证引用可解析导出起始帧静态 SVG 时，在资源映射表同一行写明“仅起始帧，动画与终点帧已丢弃”。

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-730269321014e7e1d765](../../../store/cases/case-730269321014e7e1d765/d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`d62d1ca408ead4c6087ee8493ffc6be944e20a88c5230ed7af8f16298d439621`
- [case-753b41488ff67ec1d068](../../../store/cases/case-753b41488ff67ec1d068/24570f598b1c5b1bdb181efddaac5a79a2aac2ad6e83f5f171a7107944d77842.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`24570f598b1c5b1bdb181efddaac5a79a2aac2ad6e83f5f171a7107944d77842`
