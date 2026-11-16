# 由主题或库决定的对话框窗口外观

agent 会看到什么：读到 Activity 的 android:theme 是 Theme.*.Dialog，或对话框由 material-dialogs（MaterialDialog.Builder）这类库包装、源码里只有主题名或库名；规格只写「Dialog 主题」「Dialog 形态页」「→ CustomDialog」，没有暗化、窗口宽度、点外关闭、底色圆角的值和出处

## 通用查法

### 对话框窗口只给了主题名或库名时，顺主题链和库资源查出窗口属性写进规格

审的是：规格
触发（任一种）：
- 读到：Activity 的 android:theme 是 Theme.*.Dialog，或对话框由 material-dialogs（MaterialDialog.Builder）包装，源码里只有主题名或库名；写错的样子：规格只写「Dialog 主题」「Dialog 形态页」「→ CustomDialog」，没有暗化、窗口宽度、点外关闭、底色圆角的值和出处，也没标「未知」
适用范围：规格里写 Dialog 主题 Activity、库封装对话框的窗口形态那一节
做法：
- 从主题名或库的依赖坐标出发，按 style 的 parent 链在依赖库包内 res/values/values.xml、平台 themes.xml 里取离主题最近的 backgroundDimAmount、windowMinWidthMinor、windowCloseOnTouchOutside、windowBackground；库自带的几何 dimens（如 md_dialog_max_width）在库 AAR 里找
- 值是 @dimen / @drawable / ?attr / @bool 引用的再解析到具体值，逐项写进规格并注出处，窗口宽度写成公式
- 查不到的项写「未知」并登记为缺口，不只写主题名或库名
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <item name="backgroundDimAmount">0.6</item>：链上都没覆盖暗化比例时落到的平台基础主题值（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme 的 backgroundDimAmount（按应用的 compileSdk 取对应平台））
- Theme.Dialog 的 windowCloseOnTouchOutside 取 @bool/config_closeDialogWhenTouchOutside，值为 true：平台对话框主题的点外关闭默认（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme.Dialog；data/res/values/config.xml，config_closeDialogWhenTouchOutside（按应用的 compileSdk 取对应平台））
- config_prefDialogWidth = 320dp：wrap_content 的浮动窗口先按这个宽度试排（出处：Android SDK 平台资源 data/res/values/config.xml，config_prefDialogWidth（按应用的 compileSdk 取对应平台）；android.view.ViewRootImpl#measureHierarchy）
针对本应用要查的：
- 主题链上实际提供每一项窗口属性的 style，以及库自带的窗口几何 dimens：依赖库（material、appcompat、material-dialogs 等，按应用依赖的版本）包内 res/values/values.xml 里按 style 的 parent 往上找；链上没有覆盖时取 Android SDK 平台资源的 themes.xml、dimens.xml、config.xml（按应用的 compileSdk）；取链上离主题最近的那一项，引用解析到具体值。例：material 1.12.0 + appcompat 1.7.1 下 Theme.MaterialComponents.Light.Dialog 的窗口底来自 appcompat 的 abc_dialog_material_background
未核实：material-dialogs 的 md_dialog_max_width、md_dialog_horizontal_margin 本机没有这个库的制品，取自卡；plain Light.Dialog 链上 windowMinWidthMinor 由哪一层提供没有逐层核到
来源：2 张卡，1 个应用
- case-ac1b65b76f72e7be3fa6（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
- case-f4ebb1d613a2d9343ee5（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-db0a88ac38f7｜Theme.*.Dialog 主题的 Activity，规格逐项写库主题定的暗化、宽度、点外关闭和底色圆角｜读到：AndroidManifest.xml 里 Activity 的 android:theme 是 Theme.*.Dialog（如 Theme.MaterialComponents.Light.Dialog、Theme.AppCompat.Light.Dialog）；写错：规格只写「Dialog 主题」「居中卡片形态」，没写暗化比例、窗口宽度和 inset、点外是否关闭、窗口底色和圆角，也没标「未知」
- rule-1432d895296e｜对话框几何由第三方库或 Dialog 主题决定时，规格的跨栈基线写出窗口宽度公式和出处｜读到：共享组件表或跨栈基线写着对话框由 material-dialogs（MaterialDialog.Builder）包装，或 Activity 的 android:theme 是 Theme.*.Dialog；源码树里只有库名或主题名，没有数值；写错：跨栈基线只写「material-dialogs → ArkUI CustomDialog」「Dialog 主题 Activity → Dialog 形态页」，没有窗口宽高公式和出处，也没登记取不到库资源的缺口
