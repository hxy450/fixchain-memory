# 动态布局文本的字号、行距按源端 dp × 文字倍率落成 vp，只有 bounds、padding、背景等几何乘设计画布比例

ID：`lesson-4c494b9f89c7e9db2b55` · 版本：1

[本主题](index.md)

## 何时使用

动态或灵活组件的渲染实现阶段，把源端动态布局文本的字号、行距换算成 ArkUI 预览、测量或原生绘制尺寸时

## 适用情境

源端动态文本以 fontSize.dpF × dynamicTextScale × fontSizeScale 设字号、以 lineSpacing.dpF 设行距，只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用 renderWidth / document.width 一类画布比例统一换算几何。

## 原因

写出通用的 scaled() 后对所有数值一律调用，会把几何画布比例套到字号与行距上，画布比例小于 1 时文字整体变小；新增的测量或原生绘制路径照搬现有表达式，偏差随之扩散。

## 做法

1. 逐属性核对源端单位与缩放链：字号、行距、最小与最大字号按源端公式落为 vp，只有几何属性乘画布比例；新增 measureText、Paragraph 等路径时从源端公式重新推导字号，几何比例作为单独参数传入，px 换算只用 vp2px(1)。

## 可选检查

- 加一条回归：画布比例不为 1 时，字号仍等于源端 dp 值，几何仍按比例缩放。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5f0ce074cb523583f87e](../../../store/cases/case-5f0ce074cb523583f87e/e381b3352a49394357835d2b6354828dcdca89fb0fdac1b7c0f691c7f8538b82.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e381b3352a49394357835d2b6354828dcdca89fb0fdac1b7c0f691c7f8538b82`
