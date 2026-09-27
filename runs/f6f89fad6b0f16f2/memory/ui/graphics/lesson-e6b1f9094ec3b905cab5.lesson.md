# AnimatedImageVector/animated-vector 按状态分别给出起点帧和终点帧；同名静态 SVG 只是起始帧

ID：`lesson-e6b1f9094ec3b905cab5` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段转换 AnimatedImageVector/animated-vector 图标、决定各状态显示哪一帧时；以及资源迁移阶段遇到 animated-vector 时

## 适用情境

源码用 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定；目标资源目录里的同名媒体是资源迁移从 animated-vector 起始帧导出的静态 SVG；页面规格允许资源动画或等价符号，并要求保持可见的状态切换。

## 原因

直接引用同名静态图，所有状态都显示起始帧，例如完成的步骤仍显示播放三角。来源中资源阶段按规则应把 animated-vector 记为不可映射，却导出起始帧且没在映射表标注；转换者读过 XML 的 valueTo，仍只写起始帧并挂成待补资源。

## 做法

1. 读 painter 的 atEnd 由哪个状态决定，以及 XML 的 valueFrom/valueTo，按状态分支分别给出两帧的等价图形；规格允许等价符号时，可用语义相符的系统 SymbolGlyph（名称以本地 SDK 的 sysResource 为准），或把终点 path 画成独立图形。
2. 同名媒体已存在时，打开核对它画的是哪一帧。
3. 资源迁移阶段为保证引用可解析导出起始帧静态 SVG 时，在资源映射表同一行写明“仅起始帧，动画与终点帧已丢弃”。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-753b41488ff67ec1d068 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`9d1825268579fd1d8853872eb1bb05e3475531495ecf8ba5f58db3362ed5bf29`
