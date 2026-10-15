# 源端文字尺寸只乘文字缩放倍率、几何另乘画布比例时，字号与行距按源公式落成 vp，只让 bounds、padding 等几何乘画布比例

ID：`lesson-4c494b9f89c7e9db2b55` · 版本：3

[本主题](index.md)

## 何时使用

实现按设计稿宽度缩放的预览、画布或动态布局渲染，统一缩放函数将同时作用于字号与几何时；为同一渲染新增测量或原生绘制路径时

## 适用情境

源端动态文本字号由 dp 值乘文字倍率得到（例：fontSize.dpF × dynamicTextScale × fontSizeScale），行距同样按 dp；只有节点宽高、位置、padding、背景按根尺寸与设计宽度之比缩放；目标预览用画布比例（例：renderWidth / document.width）统一换算几何。

## 原因

写出通用的缩放函数后对所有数值一律调用，会把几何画布比例套到字号与行距上，画布比例小于 1 时文字整体变小；新增的测量或原生绘制路径照搬现有表达式，偏差随之扩散。

## 做法

1. 逐属性核对源端单位与缩放链：字号、行距、最小与最大字号按源端公式落为 vp，只有几何属性乘画布比例；文字倍率（例中的 dynamicTextScale、fontSizeScale）按当前渲染路径取实际值，某条路径倍率为 1 时可直接用 dp 值，不把它推到其他路径；新增 measureText、Paragraph 等路径时从源端公式重新推导字号，几何比例作为单独参数传入，px 换算只用 vp2px(1)。

## 可选检查

- 加一条回归：画布比例不为 1 时，字号等于源端完整文字公式的结果（dp 值乘当前文字倍率），不额外乘画布比例；几何仍按比例缩放。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5f0ce074cb523583f87e](../../../store/cases/case-5f0ce074cb523583f87e/e381b3352a49394357835d2b6354828dcdca89fb0fdac1b7c0f691c7f8538b82.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e381b3352a49394357835d2b6354828dcdca89fb0fdac1b7c0f691c7f8538b82`
