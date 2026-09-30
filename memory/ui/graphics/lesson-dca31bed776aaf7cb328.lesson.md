# 自绘图表的折线点与节点标签共用同一坐标原点：点坐标已含顶部留白时，不再给图形节点加同向 position 偏移

ID：`lesson-dca31bed776aaf7cb328` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android 自定义 ItemDecoration/Canvas 图表（温度折线、趋势图）转换为 ArkUI Canvas、Polyline 或 Shape 时

## 适用情境

源端在同一画布坐标里用 valToY 一类函数（已含 paddingTop 与文字高度）画折线和节点标签；目标把折线画在 Polyline/Shape 上并用 position 定位，标签另用 Text 定位。

## 原因

源端映射函数里已计入的顶部留白，若再通过图形节点的 position 偏移一次，折线相对标签整体下移、落到容器底部被裁剪。来源中重建趋势图时 y 已计入 150dp 顶部留白，又把 Polyline 定位在 y:150，用户反馈“两条折线太靠下看不清”。

## 做法

1. 让折线点与标签使用同一原点：图形节点设了 position 偏移时，点坐标扣除同一偏移；或都在同一 Canvas 坐标系中绘制。

## 可选检查

- 需要确认时，用最高、最低两组边界值算出屏幕 y，确认都在容器高度内且与标签对齐。

## 来源（按需复核）

- case-9d7fa754a567e2ecec7e · 结论：diagnosis, recommendation:1
  卡片版本：`bea0753f350d28c7200a88687c9f9206bfffa2cb74e927a39a4a094bdf56a08e`
