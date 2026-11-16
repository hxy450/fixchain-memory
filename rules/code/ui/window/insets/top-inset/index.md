# 全屏页的顶部状态栏避让

agent 会看到什么：读到根布局、DrawerLayout、AppBarLayout 上的 android:fitsSystemWindows 或工具栏自带的 paddingTop；产物里 .padding({ top: 顶部安全区值 }) 或状态栏高度占位落在哪一层容器、落了几处

## 通用查法

### 全屏页顶部避让：先找源端哪一层消费状态栏 inset，目标只在对应那一层加一次

审的是：代码
触发（任一种）：
- 读到：源布局的根、DrawerLayout、CoordinatorLayout 或 AppBarLayout 上有 android:fitsSystemWindows="true"，或工具栏容器自带固定 android:paddingTop 留白，或 Activity 的 setOnApplyWindowInsetsListener 只处理了部分边；写错的样子：目标的顶部避让（.padding({ top: … }) 或状态栏高度占位）落的层和源端消费 inset 的那一层对不上：不止一处、塞进固定 .height() 的标题栏、加在包住抽屉的容器上，或一处都没有
适用范围：Android 全屏页的状态栏避让由某一层布局或代码承担，迁成 ArkUI 页面接入顶部安全区时
做法：
- 在这一页的源布局和 Activity 里找出顶部 inset 由哪一层消费：带 android:fitsSystemWindows="true" 的那个 View、工具栏自带的 android:paddingTop，或 insets 监听里处理顶部的那一处；源端隐式消费的顶部也算
- 目标只在对应的那一层容器上加一次顶部避让值，其余层不再加；固定 .height() 的标题栏保持源高度，避让放在它外层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fitsSystemWindows 为 true 时调整这个 View 的 padding，给状态栏等系统窗口留出空间：源端顶部避让落在带这个属性的那一层，它里面的工具栏本身不缩（出处：Android SDK 平台资源 data/res/values/attrs.xml，fitsSystemWindows（按应用的 compileSdk 取对应平台））
- ArkUI 固定 .height() 包含 padding；安全区移到标题 Row 外层后，工具栏可见高度恢复为源高度：避让不要塞进固定高度的容器里（出处：卡里修好并验证过）
针对本应用要查的：
- 源端顶部 inset 由哪一层消费：源工程这一页的 Activity / Fragment 布局 XML：根布局、DrawerLayout、CoordinatorLayout、AppBarLayout 的 android:fitsSystemWindows，工具栏容器的 android:layout_height 和 android:paddingTop；以及 Activity 里的 setOnApplyWindowInsetsListener；按这一页的源布局从根往下逐层记下谁消费了顶部，不照搬别的页面；例：根布局 fitsSystemWindows="true"、工具栏固定 52dp 且没有 paddingTop 时，避让放在标题 Row 外层的容器上，Row 保持 52vp
来源：2 张卡，2 个应用
- case-7b7a48249f269a40a194（掌上燃气管家）：做法第 2 步 ← 建议 1、建议 4；取值 2 ← 诊断
- case-b4a2f2d65e01a68393e3（AntennaPod）：做法第 1 步 ← 建议 2

## 规矩

- rule-41d426bd09b2｜根布局 fitsSystemWindows=true 时，顶部安全区放标题栏外层，标题栏保持源高度｜读到：全屏页根布局 android:fitsSystemWindows="true"，里面的工具栏 FrameLayout / Toolbar 是固定 layout_height（如 52dp），自身没有 paddingTop；写错：标题 Row 写成 .height(<源高度>).padding({ top: <顶部安全区值> })，把安全区塞进固定高度里；或者外层和 Scroll 又各加一层顶部安全区
- rule-699a1c477b94｜给固定 height 的容器加顶部 padding 前，按可见高度 = height − paddingTop 核对｜写错：固定 .height(N) 的标题栏或工具栏上又加了 .padding({ top: … })（安全区或其他顶距），没有同步增高
- rule-c4dae016be2a｜工具栏自带固定 paddingTop 时，用 max(源顶距, 安全区) 替换它，不再另加外层安全区｜读到：根布局没有 android:fitsSystemWindows，工具栏 FrameLayout 固定 layout_height（如 80dp）并自带 android:paddingTop（如 40dp）给状态栏留白，正文 layout_marginTop 等于工具栏高度；写错：外层 Column 写 .padding({ top: <顶部安全区值> })，同时标题 Row 保留 .height(<源高度>) 和源 paddingTop，两次避让叠加
- rule-7f2f94b4e122｜从根到标题栏的纵向链路上只保留一处状态栏避让｜写错：外层容器、标题 Row、Scroll 中不止一处写了 .padding({ top: <顶部安全区值> }) 或源顶部留白
- rule-d6dbbe7f4600｜DrawerLayout 根 fitsSystemWindows 时，状态栏避让只加在主内容列，不加在包住抽屉的容器上｜读到：源布局根是 DrawerLayout 且 android:fitsSystemWindows="true"，内容列（Toolbar + 主内容）和 NavigationView 是它的两个子视图；写错：目标在同时包住抽屉面板和内容列的容器（SideBarContainer、共享抽屉基座，或包住它们的 Column）上写 .padding({ top: 状态栏高度 })，抽屉面板跟着整体下移
- rule-ac45f599d976｜NavigationView fitsSystemWindows 时，抽屉头部从窗口顶画并叠 #44000000 条｜读到：NavigationView 自身 android:fitsSystemWindows="true"，并带 app:headerLayout；写错：抽屉面板或头部被 .padding({ top: 状态栏高度 }) 推到状态栏下；或头部从窗口顶画了，但状态栏那一段没有叠半透明黑的前景
- rule-bc2f333803eb｜工具栏由子组件或内嵌子页自绘时，宿主页包住它的外层容器补 windowTopPadding｜读到：源端顶部 inset 由根布局或子 Fragment `AppBarLayout` 的 `android:fitsSystemWindows="true"` 隐式消费，Activity 只显式处理 systemBars 的底部和左右；目标工具栏改由共享基座或内嵌子页绘制；写错：宿主 NavDestination 包住它的外层容器只有 `windowBottomPadding`，没有 `.padding({ top: windowTopPadding })`
- rule-275c83a4133d｜源布局没处理 insets 时 Toolbar 置于 y=0，不为过闸补 windowTopPadding｜读到：源布局根 android:fitsSystemWindows="false" 或没有 WindowInsets 处理，Toolbar 叠放在 WebView 等内容上，targetSdkVersion ≥ 35；写错：目标页给叠放的 Toolbar 或根 Column 加 .padding({ top: windowTopPadding })，注释「Layer 3：前景避让状态栏」，出现状态栏高度的色条、工具栏下移
