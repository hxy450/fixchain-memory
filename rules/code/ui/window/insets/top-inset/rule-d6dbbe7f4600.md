# DrawerLayout 根 fitsSystemWindows 时，状态栏避让只加在主内容列，不加在包住抽屉的容器上

审的是：代码
触发（任一种）：
- 读到：源布局根是 DrawerLayout 且 android:fitsSystemWindows="true"，内容列（Toolbar + 主内容）和 NavigationView 是它的两个子视图；写错的样子：目标在同时包住抽屉面板和内容列的容器（SideBarContainer、共享抽屉基座，或包住它们的 Column）上写 .padding({ top: 状态栏高度 })，抽屉面板跟着整体下移
适用范围：源布局根是 DrawerLayout（android:fitsSystemWindows="true"），目标用 SideBarContainer 或共享抽屉基座同时承载抽屉面板和工具栏、内容列时
做法：
- 只在主内容列（工具栏 + 内容）顶部放一条状态栏高度的占位，颜色取源主题的 colorPrimaryDark，例如内容列 Column 里先放 Column().width('100%').height(状态栏高度).backgroundColor(…)；工具栏保持源高
- 抽屉收进共享基座时这条占位放在基座的内容列里，基座注释写明宿主页不在外层加顶部 padding；宿主页要在外层包一层避让前，先看被包住的组件里有没有不该跟着下移的抽屉或侧栏
- 给某一页补避让时按这一页的源布局逐个子视图核对，不照搬别的页面的外层 padding
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- statusBarColor = ?attr/colorPrimaryDark：平台 Material 主题里状态栏底色取 colorPrimaryDark，内容列占位的颜色按它取（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 statusBarColor（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 占位用的 colorPrimaryDark 的实际颜色：源工程 res/values 下主题文件里 Activity 或应用主题的 colorPrimaryDark 项；没写时顺 parent 到 appcompat 或 material 包内 res/values/values.xml 的父主题；取到 @color/… 时再到颜色资源里读出 #AARRGGBB，写成目标的颜色资源
来源：1 张卡，1 个应用
- case-eebe8e71adf555fca84f（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 4
