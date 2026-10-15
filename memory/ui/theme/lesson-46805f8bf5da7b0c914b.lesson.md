# Compose 以 Brush 渐变着色的背景迁为 linearGradient：把调色板名解析成具体色序，透明 Surface 背景设透明，不压成单一品牌色

ID：`lesson-46805f8bf5da7b0c914b` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与共享组件实现阶段，把 Compose 按钮、卡片的 Brush.horizontalGradient(colors.xxx) 背景，或页面里已有的渐变字面色值落为 ArkUI linearGradient 与颜色资源时

## 适用情境

源组件用主题中的渐变列表（如 JetsnackTheme.colors.interactivePrimary、gradient2_2）经 Brush 着色，常配 Surface(color = Transparent)；目标要求颜色走 color.json 资源引用，而 color.json 只收录了调色板的部分色阶。

## 原因

调色板名只是颜色列表的别名，不解析就只能用一个品牌色或名称相近的现有令牌代替：按钮从浅紫到深蓝的渐变变成单色块，分类卡的两组渐变被换成错值令牌。来源两例：共享按钮作者读到 Brush.horizontalGradient(interactivePrimary) 仍写 backgroundColor(brand)；页面 worker 把已正确的渐变字面色值替换为三处值不同的现有令牌，没有新增缺失色阶，也没回报缺令牌。

## 做法

1. 源背景是 Brush.horizontalGradient(colors.xxx) 时保留为 linearGradient({ direction: GradientDirection.Right, colors: [...] })，先在主题与 Color 定义中把调色板名解析成具体色阶顺序（如 interactivePrimary = Shadow4 → Shadow11）；源 Surface 为 Transparent 时目标 backgroundColor 也设透明。
2. 渐变色阶用 $r 引用时逐个核对令牌值与源色值；缺的色阶按调色板命名新增条目后引用，或按流程回报 design_tokens_missing。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4a0392021e915d5b60d1](../../../store/cases/case-4a0392021e915d5b60d1/378f0a8a42ee9a8396cd872dd333f44c057886acbe7053987099bc83f3af1790.json) · 结论：diagnosis, recommendation:3, recommendation:1
  卡片版本：`378f0a8a42ee9a8396cd872dd333f44c057886acbe7053987099bc83f3af1790`
