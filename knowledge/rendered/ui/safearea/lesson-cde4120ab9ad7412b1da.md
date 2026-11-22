# 自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSystemWindows 时 inset 放包住工具栏的主内容列（DrawerLayout 下不包抽屉，NavigationView 头部画到状态栏下并叠 insetForeground）、工具栏保持源高；工具栏自带固定顶距时顶距与 inset 只取一份并同步高度

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

来源支持：5 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码；androidx.appcompat:appcompat 1.1.0、1.8.0；com.google.android.material:material 1.4.0、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕应用 targetSdk 不低于 VANILLA_ICE_CREAM（35）时默认 edge-to-edge（targetSdk 为 35 且主题没有另设 windowOptOutEdgeToEdgeEnforcement=true 时；targetSdk 不低于 36 时这个属性被忽略）：Window.setDecorFitsSystemWindows 的行为等同于 false 且不能改，框架不再把内容视图适配到系统栏 insets
- 〔做法第 1 步〕targetSdk 不低于 VANILLA_ICE_CREAM（35）时 Window.setStatusBarColor 的颜色固定为透明、不能改，主题里的 statusBarColor、colorPrimaryDark 不再决定状态栏底色
- 〔做法第 1 步〕源应用 targetSdk≥35、运行在强制 edge-to-edge 的参照机上，根布局没有消费 insets 的页面，参照机截图显示工具栏从窗口顶 y=0 起画在透明状态栏下，没有被让到状态栏以下
- 〔做法第 2 步〕android:fitsSystemWindows 为 true 时调整这个 View 的 padding，为状态栏等系统窗口留出空间，只在非嵌入的 Activity 里生效：避让落在带这个属性的那一层，它里面的工具栏高度不变
- 〔原因 / 做法第 4 步〕设置了固定 width、height 的组件，内容区大小等于 width、height 减去 padding 和 border（padding 画在固定尺寸以内）
- 〔原因 / 做法第 2、3、4 步〕ArkUI 的 height、padding 传数字时单位都是 vp；padding 不设时为 0，传 Length 时四边同时生效
- 〔原因〕标题栏写固定 height(52) 再加 padding({ top: topInset }) 时，有状态栏的设备上工具栏可见内容高度变成 52 − topInset，比源端 52dp 矮
- 〔做法第 2、3 步〕窗口接口 getWindowAvoidArea、avoidAreaChange 返回的避让区矩形（Rect）以 px 为单位、取整数；ArkUI 的 padding、height 传数字时按 vp 解释，两者相加前要先用 px2vp 换算
- 〔做法第 1 步〕Window.setWindowLayoutFullScreen(true) 时应用主窗口或子窗口为沉浸式布局，布局不避让状态栏与三键导航栏，组件可能与它们重叠；false 时布局避让这两栏
- 〔做法第 2 步〕应用主题没有另设 actionBarSize 时，AppCompat 的 ActionBar 高度取 abc_action_bar_default_height_material：竖屏 values 下 56dp，values-land 下 48dp，values-sw600dp-v13 下 64dp（appcompat 1.1.0、1.8.0 相同）
- 〔做法第 2 步〕Material 组件库的 NavigationView 继承 Widget.Design.ScrimInsetsFrameLayout 的 insetForeground，应用没有另设时为 #4000（即 #44000000）；Widget.MaterialComponents.NavigationView、Widget.Material3.NavigationView 都沿用它（material 1.4.0、1.8.0）
