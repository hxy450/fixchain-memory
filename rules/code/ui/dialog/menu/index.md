# 菜单、气泡与下拉面板

源端有 PopupWindow 的 showAsDropDown / showAtLocation、registerForContextMenu / onCreateContextMenu、AttachPopupView、Balloon 气泡，目标端有 bindPopup、bindMenu、openMenu 或锚定在控件上的浮层时

## 触发族

- [PopupWindow 弹出面板（showAsDropDown / showAtLocation）](popup-window/index.md)（5 条）：读过的源码里 new PopupWindow 加载自定义布局，用 showAsDropDown(anchor) 锚在控件下方或 showAtLocation 整屏、底部弹出，可能 setHeight(MATCH_PARENT)；交回的写成原生 Select、整块替换列表的视图、所有面板共用一个 bindSheet，或 height('100%') 的面板和固定高度的兄弟节点叠在同一个 Column 里
- [锚定父页控件的 AttachPopupView 提示](attach-popup-tip/index.md)（3 条）：源端继承 AttachPopupView、用 atView(...) 锚定 parentFragment 控件的提示弹窗（弹出前判断 isShown 和一次性标记，onDismiss 里写标记），对应目标提示浮层放在哪一页、怎么定位、显示条件和子页怎么读它
- [安卓上下文菜单（registerForContextMenu / onCreateContextMenu）](context-menu/index.md)（10 条）：读到源端 registerForContextMenu、openContextMenu、onCreateContextMenu（setHeaderTitle、MenuInflater.inflate、MenuItem.setVisible）和菜单 XML 的 <item>；产物里的长按回调、菜单卡浮层、openCustomDialog / openMenu、bindMenu / bindPopup 承载的菜单
- [skydoves Balloon 气泡](balloon-popup/index.md)（2 条）：读过的源码里用 skydoves 的 Balloon.Builder（setBackgroundColor、setArrowPosition 等）；交回的代码里用 bindPopup 的 CustomPopupOptions 写气泡底色和 arrowOffset
- [下拉菜单式的选择项（ListPreference 的 DROPDOWN_MENU、DropdownMenu）](dropdown-menu-select/index.md)（1 条）：读到源端 ListPreference(type = ListPreferenceType.DROPDOWN_MENU) 或 DropdownMenu 从所在行弹出选项菜单；产物里是锚在该行的 bindMenu / Select，还是点击切 expanded、在行下插入选项列表的行内展开
- [Compose 的 DropdownMenu、Popup 和 cascade 菜单](compose-dropdown-menu/index.md)（3 条）：读到 Compose 的 DropdownMenu / me.saket.cascade 的 CascadeDropdownMenu 锚在触发 IconButton 的 Box 里、Popup(Alignment.Center) 加 Surface(tonalElevation) 的居中菜单、带 children 的子菜单；产物里页面级 Stack 浮层的灰遮罩和固定 .position、bindMenu 的自定义内容、子菜单并排或平铺、onBackPress 先不先关菜单
