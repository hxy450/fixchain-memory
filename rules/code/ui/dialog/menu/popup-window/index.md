# PopupWindow 弹出面板（showAsDropDown / showAtLocation）

agent 会看到什么：读过的源码里 new PopupWindow 加载自定义布局，用 showAsDropDown(anchor) 锚在控件下方或 showAtLocation 整屏、底部弹出，可能 setHeight(MATCH_PARENT)；交回的写成原生 Select、整块替换列表的视图、所有面板共用一个 bindSheet，或 height('100%') 的面板和固定高度的兄弟节点叠在同一个 Column 里

## 规矩

- rule-0e008332a22d｜PopupWindow 自定义布局锚定下拉，目标用 bindPopup 自定义菜单，不用 Select｜读到：源端点击触发控件时 new PopupWindow，inflate 一个自定义布局（固定宽度、固定行高、背景图、箭头图、选中项勾选图），再 showAsDropDown(anchor) 锚在触发控件下方；写错：目标把这个下拉写成原生 Select([...]) 或系统菜单，只改了字色和背景；或者做成整页替换的视图；自定义的宽度、行高、勾选图都没落地
- rule-36b5e075deed｜同一筛选栏里 showAsDropDown 的快捷项做原位下拉，只有整屏弹出的“更多筛选”做独立面板｜读到：同一筛选栏有几种入口：快捷项点击时先把置顶筛选栏设为可见、setSelectionFromTop 把列表滚到筛选位置，再 showAsDropDown 在置顶栏下展开；“更多筛选”走另一个弹窗的 show(...) 整屏弹出；写错：快捷项和“更多筛选”调用同一个打开面板的方法，build() 里条件成立时用筛选面板整块替换列表（标题也改成筛选），置顶栏和背景列表不见了
- rule-b122f27dd016｜源端几个工具面板容器各不相同时，不共用一个 bindSheet 只改底色文字，按面板拆开｜读到：源端工具面板各用不同容器：底部 PopupWindow 面板（图标按钮切换选项）、锚定在标题栏右上角带箭头的弹出菜单（固定宽度）、多步覆盖层；写错：目标用同一个 .bindSheet(...)（固定 height、dragBar、showClose、SheetType.BOTTOM）承载全部面板，只按面板改了 backgroundColor、文字颜色和文案
- rule-448b039da52e｜MATCH_PARENT 的 PopupWindow 用 showAsDropDown 弹出时，目标只占锚点以下高度｜读到：安卓 PopupWindow 设了 setHeight(MATCH_PARENT)（或布局 match_parent），用 showAsDropDown(标题栏) 挂在锚点下方弹出；写错：目标端把 match_parent 译成相对父容器的 .height('100%')，再和标题栏等兄弟节点在同一 Column 里相加
- rule-f29521b6cd58｜嵌入根节点 height('100%') 的面板时，不在同一 Column 里再叠固定高度的兄弟节点｜读到：被嵌入的自定义组件 build 根节点写 .height('100%')，自带标题行、layoutWeight(1) 的 Scroll 和底部操作栏；写错：宿主页根 Column(height('100%')) 里先放固定高度的标题栏，再在 if 分支里直接放这个面板，面板槽位没有 layoutWeight(1)，也没有外包有界容器或改成覆盖层；底栏被挤出屏幕
