# 库对话框与 Dialog 主题 Activity 的自绘窗口按提供方取宽度公式、遮罩、圆角、投影与点外关闭，不写 width('100%')

ID：`lesson-1bff1c90d9df6c9609ec` · 版本：2 · 阶段：spec/execute · 主题：[ui/dialog/frame](index.md)

概要：库对话框窗宽遮罩按提供方取值，不写 100%

信号：`material-dialogs`, `md_dialog_max_width`, `md_dialog_horizontal_margin`, `windowMinWidthMinor`, `config_prefDialogWidth`, `backgroundDimAmount`, `windowCloseOnTouchOutside`, `setCanceledOnTouchOutside`, `windowElevation`, `black_overlay`, `openCustomDialog`

## 何时使用

规格提取与界面实现阶段，为三方对话框库（如 material-dialogs）的封装组件，或 manifest 以 Theme.*.Dialog 承载、目标做成 openCustomDialog 或 Dialog 形态页卡片的浮动 Activity，确定窗口宽度、遮罩、底色圆角、投影与点外关闭时

## 适用情境

源码只出现库名或 Dialog 主题名，没有窗口几何数值，应用 res 里也没有（值在库 dimens 或对话框主题与框架默认里）；目标自绘卡片准备用 width('100%')、整屏减边距或凭印象的 80%/95%，用工程里语义不同的半透明颜色资源（如 black_overlay）当遮罩；同族页面已有这种写法可被沿用。

## 例外与边界

- 对话框由 AlertDialog.Builder、MaterialAlertDialogBuilder 构造时，按对应平台或 Material 主题代际的警告框经验取值

## 原因

对话框的宽度、暗化、圆角与投影由库资源或对话框主题在窗口层提供，源布局与应用 res 里看不到；按容器 100% 或兄弟页先例实现，浮动窗口变成整屏宽卡片，遮罩深浅与点外关闭也与源端不同。已经判断出“不是全屏”的写者，常为对齐既有页面而放弃这个判断。

## 做法

1. 先定提供方再取宽度公式，写进规格映射行并注明出处：material-dialogs 取 min(md_dialog_max_width, 屏宽 − 2×md_dialog_horizontal_margin)（0.9.6.0 的 values 为 356dp、28dp）；Material/AppCompat 警告框主题按 windowMinWidthMinor/Major（竖屏/横屏百分比）再扣窗口背景 inset；wrap_content 的 Theme.*.Dialog 浮动 Activity 由框架按 config_prefDialogWidth 测量（框架 res/values/config.xml，例：320dp），取 min(该值, 屏宽)。版本不同时从当前依赖 AAR 与本机 SDK 资源重取。
2. 遮罩取对话框主题的 backgroundDimAmount（例：AppCompat/Material 对话框主题为 0.6），不用工程里语义不同的颜色资源代替；卡片底色与圆角取窗口背景 drawable 的 inset 与 corner。
3. 主题带 windowElevation 时补窗口投影；点外关闭按主题 windowCloseOnTouchOutside 与源码 setCanceledOnTouchOutside 决定，可关闭时遮罩点击与返回键走同一关闭路径（Dialog 形态页即出栈）。
4. 窗口尺寸或方向变化时按同一公式重算，共享组件导出宽度函数供同族弹窗复用；沿用兄弟页写法前先核它的窗口几何是否对照过源端。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [按源弹层类型选形态：底部面板才用 bindSheet](../carriers/lesson-21db515a505be4845497.lesson.md)（共享 2 张卡）
- [源弹窗按布局或库模板逐控件还原不用通用弹窗](../content/lesson-1f366fe4ccdc917ce0fc.lesson.md)（共享 1 张卡）
- [真弹窗迁成系统弹窗或半模态，不用可见性叠层充当](../carriers/lesson-368c4592e4c7075c1871.lesson.md)（共享 1 张卡）
- [库与框架组件默认几何先查 SDK/库 res 分侧取](../../theme/sources/lesson-5a82d62ff7e087616968.lesson.md)（共享 1 张卡）
- [三方 UI 库先取 AAR 核几何行为再定映射](../../libraries/lesson-f79082832a2fb18c8754.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-ac1b65b76f72e7be3fa6](../../../../../store/cases/case-ac1b65b76f72e7be3fa6/cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895.json) · 结论：rec-e2841dbe92, rec-0275ee5758
  卡片版本：`cdb9faac1ebcaa9e773f9d8554ce300513bd212e668336b1f874cbab05359895`
- [case-e91d2b9a9a156d1023ec](../../../../../store/cases/case-e91d2b9a9a156d1023ec/3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8.json) · 结论：rec-a82dfa8886
  卡片版本：`3558471f038583b62bb0d5d4b2516ab8ea7ee5c983b222032cb253201c25aec8`
- [case-f4ebb1d613a2d9343ee5](../../../../../store/cases/case-f4ebb1d613a2d9343ee5/42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95.json) · 结论：diagnosis, rec-f746a62147, rec-2fdf9528ca, rec-abb7d45fd0
  卡片版本：`42debda6548084b597fd3fae3277c26d5564470d9fea934415a27bdc2e0c3a95`
