# 自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSystemWindows 时 inset 放包住工具栏的主内容列（DrawerLayout 下不包抽屉，NavigationView 头部画到状态栏下并叠 insetForeground）、工具栏保持源高；工具栏自带固定顶距时顶距与 inset 只取一份并同步高度

ID：`lesson-cde4120ab9ad7412b1da` · 版本：5 · 阶段：spec/execute · 主题：[ui/layout/insets](index.md)

概要：标题栏接 topInset 前判定源端避让方，内距只取一份

信号：`fitsSystemWindows`, `topInset`, `paddingTop`, `.height()`, `Toolbar`, `DrawerLayout`, `NavigationView`, `SideBarContainer`, `insetForeground`, `targetSdkVersion`

## 何时使用

界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时

## 适用情境

Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop（如 80dp 高、40dp 顶距，根无 fitsSystemWindows）承担；目标页以窗口模型的 topInset 做前景避让，标题栏写固定 .height()。也包括根为 DrawerLayout、NavigationView android:fitsSystemWindows="true" 且有 app:headerLayout，目标用同时承载抽屉与工具栏的共享基座（SideBarContainer）。 也包括源根布局 fitsSystemWindows=false、工具栏叠放在铺满的内容（如 WebView）之上、代码没有任何 insets 处理，构建配置 targetSdk≥35（可能经 gradle.properties 等间接给出），规格与实现只看 values-v21 的状态栏颜色就选定避让层。

## 例外与边界

- 页面内容原点已在状态栏 inset 之下（宿主已消费 inset），此时只补源端顶距的剩余部分，不再给标题栏加 topInset

## 原因

ArkUI 固定 height 包含 padding：把 topInset 作为固定高度标题栏的内距，可见工具栏被压成 height − inset；源顶距本已承担状态栏留位时再加外层 inset，又叠出两份避让。沉浸式 skill 的 TitleBar 示意写作固定 height 加 padding top（避让值 + N），照搬同样会压缩。来源两页分别出现压缩与叠加，页面规格都已给出源端避让方式，其中一页还写明“禁止重复内边距”。另一来源中“inset 放外层”被召回成“放在包 BasePage 的外层 Column”，整个侧边栏容器被推到状态栏下，抽屉头部随之下移。 源端无人处理 inset 时，状态栏位置还取决于构建前提：targetSdk≥35 的应用在 Android 15 及以上被强制 edge-to-edge，框架把 statusBarColor 置为透明，未处理 inset 的视图从窗口顶开始（本机 android-36.1 PhoneWindow.isEdgeToEdgeEnforced 与 attrs.xml 的 windowOptOutEdgeToEdgeEnforcement 注释）。不登记这一前提，只凭 values-v21 的 statusBarColor/colorPrimaryDark 推断，规格与实现对“源端工具栏在哪”的判断就没有依据。

## 做法

1. 选避让层之前先登记源端前提：根布局与工具栏的 fitsSystemWindows、代码中的 insets 处理、构建配置的 targetSdkVersion（含 gradle.properties 等间接值）以及是否被强制 edge-to-edge（targetSdk≥35 且运行于 Android 15 及以上；targetSdk=35 时主题 windowOptOutEdgeToEdgeEnforcement=true 可退出，targetSdk≥36 时该属性被忽略）。不凭 values-v21 的 statusBarColor/colorPrimaryDark 断定状态栏不透明。源端无人处理 inset 时，工具栏是否与状态栏重叠、目标是否复刻，按当前任务的对齐基准或已批准决策确定，并在规格中写明依据；以下分支适用于源端确有避让方的情形。
2. 根布局 fitsSystemWindows=true（避让在工具栏之外）：把 topInset 放在包住标题栏的主内容列 padding，标题栏保持源高度（如 52dp→52vp）。根是 DrawerLayout、NavigationView 也 fitsSystemWindows 且带 headerLayout 时，“外层”不能是同时包住抽屉的 SideBarContainer 或共享抽屉基座的外层：抽屉面板从窗口顶开始画，头部延伸到状态栏下并叠 insetForeground（默认 #44000000），主内容列顶部用状态栏高的 colorPrimaryDark 占位。
3. 工具栏自带固定 paddingTop 为透明状态栏留位：顶距与 topInset 只取一份，常用 max(源 paddingTop, topInset) 替换该内距，高度写成 源高度 − 源 paddingTop + 该值，不再另加外层 inset。
4. 给固定高度的标题栏加顶部内距前算可见内容高度 = height − paddingTop，小于源工具栏高度就改为外层 inset 或同步增高；从页面根到标题栏的纵向链路只保留一处状态栏避让。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [?attr 主题色逐主题取值导出 base/dark 对键](../../theme/tokens/lesson-1856958fc6d369f0e2bb.lesson.md)（共享 1 张卡）
- [状态栏图标按源浅色标志定，无标志即白色](../../theme/tokens/lesson-824031d5fddf81036b54.lesson.md)（共享 1 张卡）
- [导航图标按生效者画，菜单按 showAsAction 分流](../../interaction/app-bar/lesson-a6121cc7eaf207b702f7.lesson.md)（共享 1 张卡）
- [expandSafeArea 非避让，前景按避让区补内距](../immersion/lesson-a8452bfea5d42d3dcae3.lesson.md)（共享 1 张卡）

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

## 来源（按需复核）

- [case-0a77d32c850d4767a2d4](../../../../../store/cases/case-0a77d32c850d4767a2d4/f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f.json) · 结论：rec-45e7faa3c5, rec-a98b54513f
  卡片版本：`f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f`
- [case-7b7a48249f269a40a194](../../../../../store/cases/case-7b7a48249f269a40a194/57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5.json) · 结论：diagnosis, rec-3fabd63edd, rec-079f688213, rec-87c47e7994, rec-bd9646a338
  卡片版本：`57c870c2120fd77003685d94f6ed28de21a47a178a298a4d708b33203690ebc5`
- [case-ee2085c48fe78dbd3a2f](../../../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：rec-c789f45a29
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
- [case-eebe8e71adf555fca84f](../../../../../store/cases/case-eebe8e71adf555fca84f/b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87.json) · 结论：diagnosis, rec-67b9cff76d
  卡片版本：`b184689b889e0899496674801311e4fead883962b5e3789e02538c5e89259f87`
