# 贴合内容的描边、选中背景画在由内容定尺寸的节点自身，不用 width/height('100%') 覆盖层

ID：`lesson-a58ebfe7a4c55b041b14` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景时

## 适用情境

源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。

## 例外与边界

- 父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用

## 原因

ArkUI 的百分比尺寸在由内容定尺寸的父级里会向上取到最近的确定尺寸，把格子撑大（工程迁移陷阱表与设备实测一致）。来源中选中格内的 height('100%') 描边层解析到被撑高的 Tab 行高度，选中格变成约 299×597vp；与横向 Scroll 未定高叠加后，首帧只看得到前两项。

## 做法

1. 描边、背景直接写在内容节点上（.border()、.backgroundColor()、.borderRadius()），描边与内容的间距用 padding 表达；源端描边相对内容有内缩时，把内缩量拆到外层与内容节点的 padding 里。
2. 选中与未选中两态保留同样宽度的描边，未选中用 Color.Transparent，切换时尺寸不变。
3. 写完 grep width('100%') 与 height('100%')，逐处确认父级有确定尺寸。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-2018daf21990f553ec22 · 结论：diagnosis, recommendation:2
  卡片版本：`e73ba5bd838a18a9b94e05e12dbfae2f0ecffa50fd8f3932e49acdca470eb753`
