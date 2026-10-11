# 按 Android px 公式移植自绘 View 时先定画布上下文单位：用 LengthMetricsUnit.PX 构造，让字号、测宽、几何与触点同域，dp 常量与 vp 输入在边界换算

ID：`lesson-7083c6ad69ab19ad17dd` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与渲染实现阶段，创建 CanvasRenderingContext2D，并为字体串、measureText、几何公式、触点坐标、窗口避让值和 dp 常量确定单位域时

## 适用情境

源端是 Android 自定义 View：onSizeChanged 给出 int px 尺寸，Paint.setTextSize/measureText 在 px 域推导字号与派生间距，drawable 圆角等常量以 dp 声明；目标用 ArkUI Canvas 逐式移植，规格或已有代码对画布单位的表述不一致（字体串写 px、映射写 vp、触点写 px 域）。

## 原因

CanvasRenderingContext2D 默认按 vp 解释坐标与字号，要在 px 域运算须在构造时传入 LengthMetricsUnit.PX。单位没定下来时，各写者按各自理解混用：px 字号被当成 vp 放大、measureText 结果偏小、已 vp2px 的触点与 vp 几何比较而点不中。多数写法一致不能代替对构造签名的核对。

## 做法

1. 按源端运算域选择构造：源公式在 int px 上推导时用 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX)，再逐式移植布局函数；保留默认 vp 时，整套公式都按 vp 推导，不混用。
2. 选定域后逐项换算跨域输入：字体串后缀与上下文单位一致；TouchObject.x/y、窗口避让值等 vp 量按域决定是否 vp2px；来自 drawable 或 dimens 的 dp 常量（圆角、描边）在 px 域用 uiContext.vp2px 换算。
3. 规格提取时只写一份画布单位契约：上下文构造参数，以及字体串、measureText、ctx.width、触点、避让值和 dp 常量各自的单位，各 feature 映射引用同一表述。

## 可选检查

- 单位仍有疑问时，在目标设备打印一次 ctx.width 与组件尺寸、同字号的 measureText 结果，对照源端 px 值确认所在域。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-caa0a4c6289286b0e6ba](../../../../store/cases/case-caa0a4c6289286b0e6ba/b624132bc14cc2155a05833b935147b64bcfa0f884e37d7ede212a5e2200f31f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`b624132bc14cc2155a05833b935147b64bcfa0f884e37d7ede212a5e2200f31f`
