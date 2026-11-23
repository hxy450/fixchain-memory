# 对话框几何由三方库或 Dialog 主题决定时，自绘窗口宽度按提供方公式计算并随窗口重算，不写容器 100%

## 何时使用

规格提取与界面实现阶段，为三方库对话框封装（如 material-dialogs）、MaterialAlertDialog 或 Dialog 主题 Activity 改成的卡片页确定窗口宽度，以及遮罩、点外关闭、底色与圆角等窗口属性，且源码只给出库或主题、没有窗口宽度数值时

## 适用情境

源码只出现库的 Builder、库名或 manifest 的 Theme.*.Dialog 主题，源码树里没有宽度等数值；目标用 openCustomDialog 自绘，或把 Dialog 主题 Activity 做成 NavDestination 卡片页，需要显式给出卡片宽度；同族页面或共享弹窗组件可能已按 width('100%')、固定比例或工程里现成的半透明颜色资源写成先例。

## 例外与边界

- 源码在对话框显示后自己设了窗口宽度（Window.setLayout，或改 window 的 LayoutParams.width，如设为 MATCH_PARENT 或具体像素值）时，以代码设的宽度为准，不再套第 1 步的库或主题公式；设成 MATCH_PARENT 的，目标写整窗宽是对的

## 原因

对话框窗口宽度不由内容或父容器决定，而由库 dimens、对话框主题的 windowMinWidthMinor/Major 或框架对浮动窗口的测量规则给出；openCustomDialog 缺省宽、width('100%') 或凭印象的比例会得到整屏宽或比例错误的卡片，被同族页面当作约定后偏差随之扩散。遮罩浓度、点外关闭与卡片外观同样来自对话框主题，工程里语义不同的半透明颜色资源不是平台 dim。

## 做法

1. 规格的跨栈映射基线为每类对话框写出宽度公式与出处，库不在源码树时从 Gradle 缓存的 AAR 或 APK 合并资源取值：material-dialogs 取库 dimens（例：0.9.x 为 min(md_dialog_max_width, 屏宽 − 2 × md_dialog_horizontal_margin)，即 min(356dp, 屏宽 − 56dp)）；MaterialAlertDialog 按主题基底取值（MaterialComponents 基底为 windowMinWidthMinor/Major 再减背景 inset，Material3 基底另有规则）；根布局 wrap_content 的 Dialog 主题 Activity 按框架对 wrap_content 浮动窗口的测量（ViewRootImpl.measureHierarchy 以 config_prefDialogWidth 为首选宽，例：320dp，再与屏宽取小），有参照机时以实测宽核对。取不到值就登记缺口，不只写库名或主题名。
2. 实现自绘容器时按输入给出的公式计算 dialogWidth 或卡片宽，窗口尺寸或方向变化时重算；没有公式先回规格或库资源查，不写 width('100%')、openCustomDialog 缺省宽或凭印象的 80%、95%。
3. Dialog 主题 Activity 改成卡片页时，逐项从其对话框主题解析窗口属性并写进规格：遮罩取 backgroundDimAmount，点外关闭取 windowCloseOnTouchOutside（可关闭时遮罩点击与返回走同一关闭），卡片底色与圆角取 windowBackground 指向的 drawable；不用工程里语义不同的半透明颜色资源充当 dim。
4. 复用同族页面或共享弹窗组件的宽度写法前，先确认该写法已按源端窗口几何核对；已判断出源端是浮动窗口而非全屏时，不为对齐既有页面改回 100%。

来源支持：3 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码；androidx.appcompat:appcompat 1.7.1；com.google.android.material:material 1.12.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕平台 config_prefDialogWidth 在默认 values 下为 320dp，values-large 下为 440dp，values-sw600dp 下为 580dp；ViewRootImpl.measureHierarchy 对宽度为 wrap_content 的窗口先按它试排
- 〔做法第 1 步〕应用主题没有另设 windowMinWidthMinor、windowMinWidthMajor 时，平台对话框主题引用的 dialog_min_width_minor 在默认 values 下为 95%（values-large 为 80%、values-xlarge 为 72%），dialog_min_width_major 为 65%
- 〔做法第 1、3 步〕appcompat 1.7.1 的 Base.V7.Theme.AppCompat.Light.Dialog 设 android:windowBackground 为 @drawable/abc_dialog_material_background、windowIsFloating 为 true、windowCloseOnTouchOutside 为 true
- 〔做法第 3 步〕appcompat 1.7.1 的 abc_dialog_material_background（drawable-v21）是四边 inset 16dp、白色实底、圆角 ?attr/dialogCornerRadius 的形状，dialogCornerRadius 指向 abc_dialog_corner_radius_material，即 2dp
- 〔做法第 1、3 步〕material 1.12.0 的 Platform.MaterialComponents.Light.Dialog 以 Theme.AppCompat.Light.Dialog 为父主题，MaterialComponents 浅色对话框主题链上没覆盖的窗口属性取 appcompat 对话框主题的值
- 〔做法第 3 步〕平台基础主题 Theme 的 backgroundDimAmount 为 0.6，主题链上没有覆盖时对话框遮罩按这个暗化比例
- 〔做法第 3 步〕应用主题没有另设 windowCloseOnTouchOutside 时，平台 Theme.Dialog 的 windowCloseOnTouchOutside 取 @bool/config_closeDialogWhenTouchOutside，默认 values 下为 true
- 〔做法第 3 步〕openCustomDialog 的 BaseDialogOptions 没写 maskColor 时蒙层为 0x33000000（约 0.2 的暗化），没写 autoCancel 时为 true（点击遮罩层关闭弹窗）
- 〔做法第 3 步〕CustomDialogController 的 CustomDialogControllerOptions 没写 maskColor 时为 0x33000000，没写 autoCancel 时为 true
