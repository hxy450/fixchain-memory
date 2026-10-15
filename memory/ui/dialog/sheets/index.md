# ui/dialog/sheets

半模态 bindSheet：BottomSheetDialogFragment 与 Compose ModalBottomSheet 的高度档与外壳参数，一个页面挂多个弹层的绑定节点，从半模态或页内面板内再打开的二级弹窗的承载层，从弹层内压入页面（SheetMode、targetId），自绘底部弹窗改 bindSheet 时的手势门禁

[上一级](../index.md)

## 本级经验

- [会从半模态内压入 Navigation 页的弹层用 SheetMode.EMBEDDED 并传宿主 targetId，不照搬选择器模板的 OVERLAY](lesson-97bf3cf56f55715f7e42.lesson.md)
  - 时机：界面实现或弹窗改造阶段，把页面内弹层改成 bindSheet/openBindSheet 系统半模态、确定 SheetMode 与挂载节点时
  - 情境：弹层内条目会通过 Navigation/NavPathStack 压入新页面（如节日详情、订阅详情），要求跳转时不关闭弹层、新页面盖住弹层、返回后弹层仍在；目标用 UIContext.openBindSheet 或基于它的弹窗库（如 showBindSheet），手头参考的是不从弹层内跳页的选择器类半模态模板。
  - 例外：弹层内只有选择或确认、不会打开页面，或产品允许跳转前先关闭弹层
- [多个相互独立的底部弹层不在同一组件上链式 bindSheet：分别挂到不同节点；只有外壳一致时才合并为按类型切换内容的一个 bindSheet](lesson-b661a3a6a4c0a1e2a3c9.lesson.md)
  - 时机：界面实现阶段，把源页面并列的多个底部弹窗映射为 ArkUI bindSheet、安排绑定节点时；修复“点击后弹层不出现”时
  - 情境：源页面并列存在两个及以上由各自 visible 状态控制的底部弹窗（如规格选择与优惠券）；目标页面用 @Local 状态加 bindSheet 实现，并把它们写在同一个容器的修饰链上。也包括同一页面要挂章节、定时、分享、日志、排序等多个半模态，或沿用这样连写的先例页。
- [底部面板迁 bindSheet 时按实际展开高度定高度档，显式关掉源端没有的关闭钮与拖拽条](lesson-df1f691759f84ba9e688.lesson.md)
  - 时机：规格提取、内容组件实现与宿主接线阶段，把 Material BottomSheetDialogFragment 或 Compose ModalBottomSheet 映射为 bindSheet，确定高度档、外壳参数与内容根高度时
  - 情境：源面板有的在显示时调用名称暗示“全高”的展开方法（方法体只回填原 LayoutParams 并展开），有的不改 peek/state；根布局随内容；Material 面板没有关闭按钮与拖拽把手。目标外壳参数由宿主配置，内容组件被多个宿主复用。也包括 Compose ModalBottomSheet 以 rememberModalBottomSheetState(skipPartiallyExpanded = true) 跳过半展开态，规格写成“全展开 detent”或 SheetSize.LARGE。
- [弹层内再打开的二级弹窗按父面板的挂载层选承载层：父面板是 bindSheet 时用窗口级弹窗，父面板在页内时放根 Stack 顶层](lesson-009212ca2c691b97d76c.lesson.md)
  - 时机：界面实现阶段，为从底部 sheet 或页内面板内部触发的二级弹窗（定时、新建输入、日历、选择器等）选择承载层时
  - 情境：Android 在 BottomSheetDialog 内再 show 居中 DialogFragment（点外可关），或在当前页 show 的底部面板内再弹同类底部选择器；目标父面板用 bindSheet 或宿主页内叠层；二级弹窗候选有页内 Stack 条件浮层、bindSheet(CENTER)、bindContentCover 与全局自定义弹窗。
- [自绘底部弹窗改成 bindSheet 时迁移原手势门禁：含列表的面板按手势起点是否在顶部决定下拉关闭，不照搬无列表模板的无条件 dismiss](lesson-f35f4912277e0c9a1b14.lesson.md)
  - 时机：弹窗改造阶段，把页面内自绘底部弹窗替换为系统 bindSheet/showBindSheet、配置 SheetOptions 与内部滚动时
  - 情境：旧的自绘面板含可滚动 List，用 PanGesture 记录手势起点是否在列表顶部，只有在顶部才跟手下拉、达阈值关闭、否则回弹；参考的现有 Sheet 模板是无列表的固定高度选择器，onWillDismiss 无条件关闭。
  - 例外：面板内没有可滚动内容，下拉关闭不需要与列表滚动区分
