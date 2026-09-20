# Compose Layout/MeasureScope 的整数几何公式运行在 px 域：spec 必须标注运算单位

ID：`lesson-ab7d9425cdfbe3070720` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，把源码自定义 Layout / MeasureScope 里的整数除法或 .toInt() 截断翻译成 ArkTS 目标公式并标注运算单位时

## 适用情境

源码在 constraints.maxWidth、placeable 宽高（Int px）上做 Kotlin 整数除法或 .toInt() 来分配槽宽/放置子项；目标侧宽度来自 onAreaChange（vp 浮点）或 measureText（px）。

## 例外与边界

- 源码公式作用于 Dp 值而非 constraints/placeable（如 56.dp、16.dp 常量）

## 原因

F001 spec 把 `constraints.maxWidth / (itemCount + 1)` 写成「W = barWidth（vp，整数）」「W mod 5 vp 空白，Android 原样」；实际 constraints 是 px，onAreaChange 的 vp 宽是浮点（377.14），Android 余量是 W_px mod 5 px（1320 上为 0）。vp 域 floor(377.14/5)=75 让四槽只铺 1313/1320px、图标左偏 1.4–2.3vp。

## 做法

1. 先写明该运算发生在 px（constraints、placeable 都是 Int px），再决定目标公式的运算域；不要用「vp，整数」描述 onAreaChange 回调值。
2. unit 用例至少放一个非整数 vp 宽（如 377.14）与对应 px 宽（1320）的对照行；「Android 原样留 W mod n 空白」这类等价性声明按 px 与 vp 各算一遍再写。

## 检查

- 按 spec 公式手算 W_px/(n+1) 与 W_vp/(n+1)：两者对应的 Row 总宽是否都等于容器 px 宽。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-0ff695bbe2304e899b77](../../../../store/cases/case-0ff695bbe2304e899b77/be35123f388a055305b4b37bd2d99d9274ca70c27c5b0c0082f6a7d3d52a4bcd.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`be35123f388a055305b4b37bd2d99d9274ca70c27c5b0c0082f6a7d3d52a4bcd`
