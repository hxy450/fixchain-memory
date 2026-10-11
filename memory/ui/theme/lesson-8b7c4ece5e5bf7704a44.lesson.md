# 同时需要圆角与描边时把 radius 写进 .border()

ID：`lesson-8b7c4ece5e5bf7704a44` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为同一视图设置圆角与描边（按钮 cornerRadius 加 stroke、OutlinedBox、GradientDrawable setStroke）时

## 适用情境

目标写成 .borderRadius(X) 后接不带 radius 的 .border({ width, color })；映射参考可能把圆角与描边分列成两个属性。

## 原因

后续不带 radius 的 .border() 会把先前的 borderRadius 重置为直角。

## 做法

1. 写成 .border({ width, color, radius: X })，或保证 .borderRadius() 位于 .border() 之后。

## 可选检查

- 沿用旧写法的文件较多时，检索“.borderRadius( 之后紧跟不含 radius 的 .border({”组合

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c40332380c19d002090d](../../../store/cases/case-c40332380c19d002090d/20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9.json) · 结论：recommendation:2
  卡片版本：`20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9`
- [case-f226842558d82e3f3ad9](../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：recommendation:5
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
