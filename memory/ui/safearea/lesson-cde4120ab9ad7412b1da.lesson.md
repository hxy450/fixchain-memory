# 自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSystemWindows 时 inset 放包住工具栏的主内容列（DrawerLayout 下不包抽屉，NavigationView 头部画到状态栏下并叠 insetForeground）、工具栏保持源高；工具栏自带固定顶距时顶距与 inset 只取一份并同步高度

ID：`lesson-cde4120ab9ad7412b1da` · 版本：4

[本主题](index.md)

## 何时使用

界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时

## 适用情境

Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop（如 80dp 高、40dp 顶距，根无 fitsSystemWindows）承担；目标页以窗口模型的 topInset 做前景避让，标题栏写固定 .height()。也包括根为 DrawerLayout、NavigationView android:fitsSystemWindows="true" 且有 app:headerLayout，目标用同时承载抽屉与工具栏的共享基座（SideBarContainer）。 也包括源 targetSdk≥35（常经 gradle.properties 间接定义）、运行在 Android 15 及以上而强制 edge-to-edge：根 fitsSystemWindows=false、无 WindowInsets 处理，工具栏叠放在铺满的内容之上；目标套用沉浸式分层范式，结构检查按页面类型要求前景避让。

## 例外与边界

- 页面内容原点已在状态栏 inset 之下（宿主已消费 inset），此时只补源端顶距的剩余部分，不再给标题栏加 topInset

## 原因

ArkUI 固定 height 包含 padding：把 topInset 作为固定高度标题栏的内距，可见工具栏被压成 height − inset；源顶距本已承担状态栏留位时再加外层 inset，又叠出两份避让。沉浸式 skill 的 TitleBar 示意写作固定 height 加 padding top（避让值 + N），照搬同样会压缩。“inset 放外层”若落在同时包住抽屉与内容的最外层，整个侧边栏容器会被推到状态栏下，抽屉头部随之下移。 强制 edge-to-edge 下没有任何一层消费 inset 时，源端工具栏自窗口顶起画在透明状态栏下；按范式补前景避让或为通过结构检查补 padding，都会把它整体下移一个状态栏高。

## 做法

1. 先判定源端是否有一层消费顶部 inset：targetSdk≥35 在 Android 15 及以上强制 edge-to-edge，根布局 fitsSystemWindows=false、源码也无 WindowInsets 处理时，无人避让，工具栏与内容自窗口顶 y=0 起画在透明状态栏下，目标同样置顶、不加 topInset；结构检查给出豁免声明（如 needs_immersive_safearea=false）时用豁免，不为过检补 padding。有一层消费时按以下各步。
2. 根布局 fitsSystemWindows=true（避让在工具栏之外）：把 topInset 放在包住标题栏的主内容列 padding，标题栏保持源高度（例如 52dp→52vp）。根是 DrawerLayout、NavigationView 也 fitsSystemWindows 且带 headerLayout 时，“外层”不能是同时包住抽屉的 SideBarContainer 或共享抽屉基座的外层：抽屉面板从窗口顶开始画，头部延伸到状态栏下并叠 insetForeground（库默认值 #44000000），主内容列顶部用状态栏高的 colorPrimaryDark 占位。
3. 工具栏自带固定 paddingTop 为透明状态栏留位：顶距与 topInset 只取一份，常用 max(源 paddingTop, topInset) 替换该内距，高度写成 源高度 − 源 paddingTop + 该值，不再另加外层 inset。
4. 给固定高度的标题栏加顶部内距前算可见内容高度 = height − paddingTop，小于源工具栏高度就改为外层 inset 或同步增高；从页面根到标题栏的纵向链路只保留一处状态栏避让。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

## 来源（按需复核）

- [case-0a77d32c850d4767a2d4](../../../store/cases/case-0a77d32c850d4767a2d4/f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f`
- [case-7b7a48249f269a40a194](../../../store/cases/case-7b7a48249f269a40a194/57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:6
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
- [case-eebe8e71adf555fca84f](../../../store/cases/case-eebe8e71adf555fca84f/b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87.json) · 结论：diagnosis, recommendation:5
  卡片版本：`b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87`
