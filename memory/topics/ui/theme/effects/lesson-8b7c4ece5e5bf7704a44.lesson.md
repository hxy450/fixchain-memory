# 同时需要圆角与描边时把 radius 写进 .border()

ID：`lesson-8b7c4ece5e5bf7704a44` · 版本：2 · 阶段：execute/repair · 主题：[ui/theme/effects](index.md)

概要：圆角加描边时 radius 写进 .border()

信号：`.border(`, `.borderRadius(`, `cornerRadius`, `setStroke`, `GradientDrawable`, `OutlinedBox`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../sources/lesson-47785524c7f132ea7efe.lesson.md)（共享 2 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 2 张卡）
- [不补源端没有的元素；框架默认元素须保留](../../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）
- [源端层层委托时追到最终实现再写规格与代码](../../../process/inferred-not-traced/lesson-4606ccc434e247d4a240.lesson.md)（共享 1 张卡）
- [回调中置位的状态按回调门控并补控件过滤](../../state/binding/lesson-af89611fa71ea0eb6f45.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c40332380c19d002090d](../../../../../store/cases/case-c40332380c19d002090d/20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9.json) · 结论：rec-d87a106829
  卡片版本：`20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9`
- [case-f226842558d82e3f3ad9](../../../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：rec-e3cb2d5124
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
