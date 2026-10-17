# VectorDrawable 转 SVG 时 viewBox 取 viewport，width/height 取显示尺寸

ID：`lesson-4e306a66aba5f1d76fdf` · 版本：2 · 阶段：execute · 主题：[ui/graphics/icons](index.md)

概要：viewBox 取 viewport，宽高取 dp 尺寸

信号：`VectorDrawable`, `viewBox`, `viewportWidth`, `viewportHeight`, `android:width`, `fillColor`, `fill=none`

## 何时使用

资源迁移阶段，编写 VectorDrawable 到 SVG 的批量转换脚本时

## 适用情境

源 vector 的 android:width/height（dp 显示尺寸）与 viewportWidth/Height（路径坐标系）常不相等，部分 fillColor 引用主题属性。

## 原因

用同一字段同时填显示尺寸与 viewBox，路径坐标系与画布错配，图标只占画布一角或近乎空白；未解析的主题属性被写成 fill=none 后图形不可见。

## 做法

1. 两组值分开传：viewBox 为 0 0 viewportWidth viewportHeight，width/height 取 dp 值。
2. 主题属性无法解析时用可见默认色并在映射文档列出，由代码层 fillColor 按主题着色，不写 fill=none。
3. 页面阶段发现资源属转换器的同类缺陷时，回执写明系统性根因，安排全量审计或修正脚本后重跑，不只修当前页引用的文件。

## 可选检查

- 转换脚本自写或怀疑有比例异常时，按同名源 vector 全量比对 viewBox 与 viewport，抽样包含 width 与 viewport 不等的图标

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e82be6ce5af181afb98d](../../../../../store/cases/case-e82be6ce5af181afb98d/624c51c5632e8216a91f2394f4732d7277a8883acb80c6c0c092f4bad6693160.json) · 结论：diagnosis, rec-a75909afaa, rec-61910edf21, rec-e94c60b2bf, rec-3fc40f90bf
  卡片版本：`624c51c5632e8216a91f2394f4732d7277a8883acb80c6c0c092f4bad6693160`
