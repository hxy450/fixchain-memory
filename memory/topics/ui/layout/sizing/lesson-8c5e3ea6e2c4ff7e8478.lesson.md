# 权重分高且带大 padding 的 ImageView：槽高可能小于上下 padding 之和时，不把 padding 放到 ArkUI Image 上

ID：`lesson-8c5e3ea6e2c4ff7e8478` · 版本：2 · 阶段：execute · 主题：[ui/layout/sizing](index.md)

概要：权重槽可能小于 padding 时不放在 Image 上

信号：`layout_weight`, `ImageView`, `FIT_CENTER`, `layoutWeight`, `onSizeChange`, `.padding(`

## 何时使用

界面实现阶段，为 0dp + layout_weight 等由父容器分配尺寸、且带较大 padding 的 ImageView 确定 ArkUI 尺寸约束时

## 适用情境

源 ImageView 的尺寸由 layout_weight 分配，padding 取 dimen 资源；横屏或小屏时分得的槽高可能小于上下 padding 之和；目标准备写 Image.layoutWeight(n).padding(p)。

## 例外与边界

- 各配置下槽高都大于上下 padding 之和

## 原因

ArkUI Image 的 padding 计入组件最小尺寸，槽不足时组件被撑大并挤压兄弟；Android 不撑大槽，内容区高为负（槽高减上下 padding），FIT_CENTER 以负缩放绘制，表现为按 |内容高| 倒置绘制。

## 做法

1. 先按各方向配置估算槽高与上下 padding 之和；可能不足时，用 Stack 等容器承接分得的槽，onSizeChange 取实际槽高，图片绘制高度取 |槽高 − 上下 padding 之和|，差值为负时按源端结果旋转 180° 绘制，不把 padding 写在 Image 上。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [内容定尺寸的父级里不写 100%，描边画在自身](../intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-5916095777c21ec74389](../../../../../store/cases/case-5916095777c21ec74389/70e9253633bc4dd9bf5141a3152c9235dc38fad10033b18499d7c30acdf14804.json) · 结论：rec-1276657fe3
  卡片版本：`70e9253633bc4dd9bf5141a3152c9235dc38fad10033b18499d7c30acdf14804`
