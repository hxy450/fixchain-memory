# FrameLayout子项的layout_gravity写到Stack直接子项的layoutGravity，不用align

ID：`lesson-6aa3acaf04e684c6328f` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把FrameLayout子项的layout_gravity转写为ArkUI Stack子项定位时

## 适用情境

源FrameLayout内多个子项各带不同layout_gravity（左/中/右、上/下及组合），目标用Stack承载；手头映射参考可能把它写成.align()或.alignSelf()。

## 原因

ArkUI通用属性align只对齐组件自身绘制区内的内容，不移动组件在Stack中的位置；子项位置统一由Stack的alignContent决定，gravity不同的子项会叠在同一点。

## 做法

1. 把每个子项的layout_gravity写到该Stack直接子项的.layoutGravity(LocalizedAlignment.*)（API 20起提供）。
2. 直接子项是自定义组件时，外包一层Column/Row等系统容器承载layoutGravity。
3. 目标SDK低于API 20时，改用Row/Column加justifyContent或分层Stack表达左中右分布。

## 可选检查

- 同一Stack中gravity不同的子项，布局dump中的bounds不应重合

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7d8be6ed3a7f672e0757](../../../store/cases/case-7d8be6ed3a7f672e0757/6343fe5719c898184c61c914c125f629d1c7f7385e5703edbdc5127ec76268d4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`6343fe5719c898184c61c914c125f629d1c7f7385e5703edbdc5127ec76268d4`
