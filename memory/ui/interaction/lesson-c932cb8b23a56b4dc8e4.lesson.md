# 按钮selector按各自状态集合映射，setSelected态建成独立UI状态

ID：`lesson-c932cb8b23a56b4dc8e4` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与功能接线阶段，把按钮selector与setSelected/setEnabled调用点翻译成ArkUI图片状态，并接入恢复流程时

## 适用情境

同屏多个按钮引用状态集合不同的selector（有的含state_pressed，有的只有selected/enabled）；源码只在少数方法里调用setSelected，onResume等恢复路径只回填业务字段；目标用状态变量直接计算图片资源。

## 原因

照同屏按钮套用按下态，或因资源名含pressed就推定有按下态，会多出源端没有的视觉反馈；把业务字段直接当选中态，恢复或重建时会显示源端不会显示的状态，因为ArkTS没有安卓View随重建清零的视图状态。

## 做法

1. 逐个按钮读取其selector实际列出的state属性建映射；写出的条件表达式与注释里的状态顺序一致。
2. 源码只在少数方法里调setSelected/setEnabled时，建立独立的UI状态，只在这些调用点赋值；用grep对比调用点与业务字段的全部赋值点，不一致就拆开。
3. 接线恢复路径时，逐条核对源恢复代码是否同时更新View；冷启动或重建按全新View处理，验收时把冷启动和热返回分开检查。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-ba730daa5a84da1c7a02](../../../store/cases/case-ba730daa5a84da1c7a02/5d42eb38460e35a8b4188509d6638eb71739f097c16bbde3fe9e19d7ecff4b3a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`5d42eb38460e35a8b4188509d6638eb71739f097c16bbde3fe9e19d7ecff4b3a`
