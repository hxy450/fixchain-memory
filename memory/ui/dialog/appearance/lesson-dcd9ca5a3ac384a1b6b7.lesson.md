# 对话框几何由三方库或 Dialog 主题决定时，自绘窗口宽度按提供方公式计算并随窗口重算，不写容器 100%

ID：`lesson-dcd9ca5a3ac384a1b6b7` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为三方库对话框封装（如 material-dialogs）、MaterialAlertDialog 或 Dialog 主题 Activity 改成的卡片页确定窗口宽度，以及遮罩、点外关闭、底色与圆角等窗口属性时

## 适用情境

源码只出现库的 Builder、库名或 manifest 的 Theme.*.Dialog 主题，源码树里没有宽度等数值；目标用 openCustomDialog 自绘，或把 Dialog 主题 Activity 做成 NavDestination 卡片页，需要显式给出卡片宽度；同族页面或共享弹窗组件可能已按 width('100%')、固定比例或工程里现成的半透明颜色资源写成先例。

## 原因

对话框窗口宽度不由内容或父容器决定，而由库 dimens、对话框主题的 windowMinWidthMinor/Major 或框架对浮动窗口的测量规则给出；openCustomDialog 缺省宽、width('100%') 或凭印象的比例会得到整屏宽或比例错误的卡片，被同族页面当作约定后偏差随之扩散。遮罩浓度、点外关闭与卡片外观同样来自对话框主题，工程里语义不同的半透明颜色资源不是平台 dim。

## 做法

1. 规格的跨栈映射基线为每类对话框写出宽度公式与出处，库不在源码树时从 Gradle 缓存的 AAR 或 APK 合并资源取值：material-dialogs 取库 dimens（例：0.9.x 为 min(md_dialog_max_width, 屏宽 − 2 × md_dialog_horizontal_margin)，即 min(356dp, 屏宽 − 56dp)）；MaterialAlertDialog 按主题基底取值（MaterialComponents 基底为 windowMinWidthMinor/Major 再减背景 inset，Material3 基底另有规则）；根布局 wrap_content 的 Dialog 主题 Activity 按框架对 wrap_content 浮动窗口的测量（ViewRootImpl.measureHierarchy 以 config_prefDialogWidth 为首选宽，例：320dp，再与屏宽取小），有参照机时以实测宽核对。取不到值就登记缺口，不只写库名或主题名。
2. 实现自绘容器时按输入给出的公式计算 dialogWidth 或卡片宽，窗口尺寸或方向变化时重算；没有公式先回规格或库资源查，不写 width('100%')、openCustomDialog 缺省宽或凭印象的 80%、95%。
3. Dialog 主题 Activity 改成卡片页时，逐项从其对话框主题解析窗口属性并写进规格：遮罩取 backgroundDimAmount，点外关闭取 windowCloseOnTouchOutside（可关闭时遮罩点击与返回走同一关闭），卡片底色与圆角取 windowBackground 指向的 drawable；不用工程里语义不同的半透明颜色资源充当 dim。
4. 复用同族页面或共享弹窗组件的宽度写法前，先确认该写法已按源端窗口几何核对；已判断出源端是浮动窗口而非全屏时，不为对齐既有页面改回 100%。

来源支持：3 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-ac1b65b76f72e7be3fa6](../../../../store/cases/case-ac1b65b76f72e7be3fa6/cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895.json) · 结论：diagnosis, recommendation:2, recommendation:6
  卡片版本：`cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895`
- [case-e91d2b9a9a156d1023ec](../../../../store/cases/case-e91d2b9a9a156d1023ec/3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8.json) · 结论：recommendation:2
  卡片版本：`3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8`
- [case-f4ebb1d613a2d9343ee5](../../../../store/cases/case-f4ebb1d613a2d9343ee5/42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95`
