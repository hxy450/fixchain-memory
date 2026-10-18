# VectorDrawable 转 SVG 时 viewBox 取 viewport、width/height 取显示尺寸，vector 根的 android:tint 按解析色烘焙到每个可见 path

ID：`lesson-4e306a66aba5f1d76fdf` · 版本：3

[本主题](index.md)

## 何时使用

资源迁移阶段，编写 VectorDrawable 到 SVG 的批量转换脚本时

## 适用情境

源 vector 的 android:width/height（dp 显示尺寸）与 viewportWidth/Height（路径坐标系）常不相等，部分 fillColor 引用主题属性；也有 vector 根写 android:tint（含框架 color state list，如 control_checkable_material），path 的 fillColor 却是字面色（如不透明黑），并带 fillAlpha=0 的动画用 path。

## 原因

用同一字段同时填显示尺寸与 viewBox，路径坐标系与画布错配，图标只占画布一角或近乎空白；未解析的主题属性被写成 fill=none 后图形不可见。vector 根的 tint 按默认 SRC_IN 作用于全部 path，只在 fillColor 是 @ 或 ? 引用时才替换颜色的脚本会把字面填色原样写出，选中态图标变成黑色。

## 做法

1. 两组值分开传：viewBox 为 0 0 viewportWidth viewportHeight，width/height 取 dp 值。
2. 主题属性无法解析时用可见默认色并在映射文档列出，由代码层 fillColor 按主题着色，不写 fill=none。
3. vector 根有 android:tint 时，按 tint 链解析出的颜色替换每个可见 path 的填色（字面 fillColor 也替换），fillAlpha/strokeAlpha 为 0 的 path 保持透明；多态资源（checked/unchecked 等）按状态分别烘焙。
4. 页面阶段发现资源属转换器的同类缺陷时，回执写明系统性根因，安排全量审计或修正脚本后重跑，不只修当前页引用的文件。

## 可选检查

- 转换脚本自写或怀疑有比例异常时，按同名源 vector 全量比对 viewBox 与 viewport，抽样包含 width 与 viewport 不等的图标
- 写映射表前逐个读回输出 SVG 的 fill，与登记的解析色比对，不只抽查一两个文件

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-cec44d314b1979a41843](../../../store/cases/case-cec44d314b1979a41843/e607e78f3130ff9e90bb9d4934ab38e4fcf11ff8c2acdae34a2b05971435b07b.json) · 结论：diagnosis, recommendation:1, recommendation:5
  卡片版本：`e607e78f3130ff9e90bb9d4934ab38e4fcf11ff8c2acdae34a2b05971435b07b`
- [case-e82be6ce5af181afb98d](../../../store/cases/case-e82be6ce5af181afb98d/624c51c5632e8216a91f2394f4732d7277a8883acb80c6c0c092f4bad6693160.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`624c51c5632e8216a91f2394f4732d7277a8883acb80c6c0c092f4bad6693160`
