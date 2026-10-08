# Compose Slider 的 steps 是两端之间的离散值个数：取值共 steps+2 个，步长为区间/(steps+1)

ID：`lesson-d715fa78ada2e79a5fd2` · 版本：4 · 阶段：spec/execute · 主题：[ui/interaction/selectors](index.md)

概要：Slider steps 翻步长：区间/(steps+1)

信号：`Slider`, `valueRange`

## 何时使用

规格提取或界面实现阶段，把 Compose Slider 的 valueRange 与 steps 翻成目标滑杆步长和验收条款时

## 适用情境

源端 Slider(valueRange = a..b, steps = n) 做离散取值；目标用 ArkUI Slider 的 min、max、step。

## 原因

steps 是两端之间的中间离散点数，取值共 n+2 个；读成“n 个间隔”或“n+1 个停靠点”会让步长和取值集整体错位，并随规格传到实现和验收。

## 做法

1. 步长 = (max − min)/(steps + 1)；规格和验收写出完整取值列表，而不只写“N 个停靠点”。

## 可选检查

- 对步长有疑问时，在目标端逐个停靠点取值，与源端取值列表逐一比对。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [M3 组件默认几何与留白从库 Tokens 分侧取值](../../theme/sources/lesson-5a82d62ff7e087616968.lesson.md)（共享 1 张卡）
- [规格与源码冲突时按源端语义实现并标注差异](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7f41c5604c3a5213023b](../../../../../store/cases/case-7f41c5604c3a5213023b/4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8.json) · 结论：diagnosis, rec-f6d6216c7b
  卡片版本：`4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8`
