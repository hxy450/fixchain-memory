# ui/dialog/mounting

弹窗挂载层级与宿主节点：sheet 之上、覆层挂整窗根、锚点所在页、SheetMode 与 targetId

[上一级](../index.md)

## 本级经验

- [sheet 内二级弹窗用全屏模态承载，自绘遮罩居中卡片](lesson-009212ca2c691b97d76c.lesson.md) · 阶段：execute · 信号：bindSheet, bindContentCover, BottomSheetDialog, DialogFragment
- [依附式弹窗宿主按锚点视图所在页确定，按实测坐标定位](lesson-29f62d177a17d08b4e4f.lesson.md) · 阶段：execute/verify · 信号：AttachPopup, atView, componentUtils, Fragment
- [多个独立底部弹层不在同一节点链式 bindSheet](lesson-b661a3a6a4c0a1e2a3c9.lesson.md) · 阶段：execute/repair · 信号：bindSheet, @Local, BottomSheetDialog, SheetOptions
- [弹层内跳页的半模态用 EMBEDDED 挂宿主节点](lesson-97bf3cf56f55715f7e42.lesson.md) · 阶段：execute · 信号：SheetMode.EMBEDDED, openBindSheet, targetId, showBindSheet
- [组件外开自定义弹窗用 ComponentContent 承载](lesson-a3ac761b0d52a6bccb9f.lesson.md) · 阶段：execute · 信号：ComponentContent, wrapBuilder, openCustomDialog, closeCustomDialog
- [页内覆层挂覆盖整窗的宿主根，按钮行先定高再撑分隔线](lesson-0a26e0cfc44a183d3a02.lesson.md) · 阶段：execute · 信号：Theme.Dialog, windowIsFloating, layout_height=match_parent, Stack
