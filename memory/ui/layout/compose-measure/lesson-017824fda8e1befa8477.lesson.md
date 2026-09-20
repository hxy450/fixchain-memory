# 从 Compose 源码合成结构时先做 Row/Column 度量推演：fillMaxWidth 无 weight 子项之后的兄弟不会被绘制

ID：`lesson-017824fda8e1befa8477` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，在没有真机 dump、只能从纯 Compose 源码合成页面结构与分页 spec 时，判定某个声明的子组件是否真的会被绘制

## 适用情境

某个 Row/Column 里有一个不带 weight 的 fillMaxWidth()/fillMaxHeight() 子项，其后还跟着兄弟组件（IconButton/Text 等）；spec 或派工准备用「近乎不可见、parity 保留」描述该兄弟。

## 例外与边界

- 兄弟组件带 weight 或 Row 用了 IntrinsicSize/自定义度量使其仍分到宽度

## 原因

Compose Row 先度量不带 weight 的 fillMaxWidth 文本，尾部 IconButton 只剩 0 宽约束、内容被裁掉，Android 两态都不绘制 Reset；主会话按声明树逐字转写，只推了颜色（uiBackground 落在 uiFloated 上「近乎不可见」）没推布局度量，把「不渲染」误记成「渲染但看不见」，并在 F004 AC 与 D-005 固化为设计灰区。

## 做法

1. 对每个 Row/Column 做一次度量推演：不带 weight 的 fillMaxWidth()/fillMaxHeight() 子项吃满剩余主轴空间，其后兄弟以 0 约束度量；这类兄弟在 clickable_elements / 页面结构里标「源码有、实绘无」，不得给转换决策。

## 检查

- Android 基线 dump 中该兄弟是否只剩一个空的 enabled=false 节点、无文本；基线截图对应像素是否为纯底色。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-72a54efb333474d03d1a](../../../../store/cases/case-72a54efb333474d03d1a/94bccd83bcb9e1df1557f29dfae3ee6909aa7675f2c947d4aea0fa86828ac880.json) · 结论：diagnosis, recommendation:1
  卡片版本：`94bccd83bcb9e1df1557f29dfae3ee6909aa7675f2c947d4aea0fa86828ac880`
