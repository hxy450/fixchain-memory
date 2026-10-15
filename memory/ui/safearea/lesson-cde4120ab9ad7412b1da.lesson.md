# 自绘固定高度标题栏接入顶部避让前先判定源端由谁避让：inset 与源顶距只取一份，并保持工具栏可见高度

ID：`lesson-cde4120ab9ad7412b1da` · 版本：5

[本主题](index.md)

## 何时使用

界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时

## 适用情境

Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop 承担（根无 fitsSystemWindows）；目标页以窗口模型的顶部避让值做前景避让，标题栏写固定 .height()，参照模板可能写成固定 height 加 padding top（避让值 + N）。

## 例外与边界

- 页面内容原点已在状态栏 inset 之下（宿主已消费 inset）时，按 lesson-c7ee1769ca29abd236d3 只补源端顶距的剩余部分，不再给标题栏加 topInset
- 根是 DrawerLayout 且 NavigationView 带 fitsSystemWindows 与 headerLayout 时，inset 只给主内容列，抽屉面板按抽屉头部的规则另行处理
- 源工具栏 paddingTop 里另含与状态栏无关的设计间距时，max(源 paddingTop, topInset) 会在状态栏更高的设备上吞掉这段间距，不直接套用第 2 步的公式

## 原因

ArkUI 固定 height 包含 padding：把 topInset 作为固定高度标题栏的内距，可见工具栏被压成 height − inset；源顶距本已承担状态栏留位时再加外层 inset，又叠出两份避让。

## 做法

1. 根布局 fitsSystemWindows=true（避让在工具栏之外）：把 topInset 放在包住标题栏的主内容列 padding，标题栏保持源高度（dp 数值按 1:1 写成 vp）。
2. 工具栏自带固定 paddingTop 为透明状态栏留位（根无 fitsSystemWindows，数值从源布局、style、dimen 读取）：用 max(源 paddingTop, topInset) 替换该内距，高度写成 源高度 − 源 paddingTop + 该 max 值，不再另加外层 inset。
3. 给固定高度的标题栏加顶部内距前算可见内容高度 = height − paddingTop，小于源工具栏高度就改为外层 inset 或同步增高；从页面根到标题栏的纵向链路只保留一处状态栏避让。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-7b7a48249f269a40a194](../../../store/cases/case-7b7a48249f269a40a194/57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:6
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
- [case-eebe8e71adf555fca84f](../../../store/cases/case-eebe8e71adf555fca84f/b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87.json) · 结论：recommendation:5
  卡片版本：`b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87`
