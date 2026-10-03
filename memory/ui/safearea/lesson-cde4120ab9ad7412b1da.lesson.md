# 自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSystemWindows 时 inset 放外层、工具栏保持源高；工具栏自带固定顶距时顶距与 inset 只取一份并同步高度

ID：`lesson-cde4120ab9ad7412b1da` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时

## 适用情境

Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop（如 80dp 高、40dp 顶距，根无 fitsSystemWindows）承担；目标页以窗口模型的 topInset 做前景避让，标题栏写固定 .height()。

## 例外与边界

- 页面内容原点已在状态栏 inset 之下（宿主已消费 inset），此时只补源端顶距的剩余部分，不再给标题栏加 topInset

## 原因

ArkUI 固定 height 包含 padding：把 topInset 作为固定高度标题栏的内距，可见工具栏被压成 height − inset；源顶距本已承担状态栏留位时再加外层 inset，又叠出两份避让。沉浸式 skill 的 TitleBar 示意写作固定 height 加 padding top（避让值 + N），照搬同样会压缩。来源两页分别出现压缩与叠加，页面规格都已给出源端避让方式，其中一页还写明“禁止重复内边距”。

## 做法

1. 根布局 fitsSystemWindows=true（避让在工具栏之外）：把 topInset 放在包住标题栏的外层容器 padding，标题栏保持源高度（如 52dp→52vp）。
2. 工具栏自带固定 paddingTop 为透明状态栏留位：顶距与 topInset 只取一份，常用 max(源 paddingTop, topInset) 替换该内距，高度写成 源高度 − 源 paddingTop + 该值，不再另加外层 inset。
3. 给固定高度的标题栏加顶部内距前算可见内容高度 = height − paddingTop，小于源工具栏高度就改为外层 inset 或同步增高；从页面根到标题栏的纵向链路只保留一处状态栏避让。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7b7a48249f269a40a194](../../../store/cases/case-7b7a48249f269a40a194/57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5`
