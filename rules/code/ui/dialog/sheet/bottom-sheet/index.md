# 底部弹层的承载和关闭

agent 会看到什么：源端 BottomSheetDialogFragment 子类弹出排序、选择面板；产物里用 bindSheet 还是页内 Stack 浮层，选中回调里有没有把显示状态置 false

## 规矩

- rule-55d622d6cc6c｜BottomSheetDialogFragment 的宿主嵌在壳内容区时用窗口级 bindSheet，不用页内浮层｜读到：对话框类 extends BottomSheetDialogFragment，onCreateDialog 里设 BottomSheetBehavior.STATE_EXPANDED；宿主页嵌在主壳内容区（标题栏、底部导航由外层提供）；写错：页面内容 Stack 里用 if 分支渲染遮罩加底对齐面板的页内浮层，遮罩和面板只能落在标题栏与底部导航之间；按钮写成扁平的 ButtonType.Normal 按钮
- rule-721344eff043｜源端排序面板点选只重绘并回调、不 dismiss 时，宿主选中回调里不关面板｜读到：源端排序对话框（BottomSheetDialogFragment 子类）点击排序项只原地重绘 ▲/▼ 并回调选择变化，回调里只写偏好或数据库，全程没有 dismiss()；有的面板内复选框要选中排序项后才 setEnabled(true)；写错：宿主的选中回调首行把 bindSheet 的显示状态变量置 false（注释「选择即 dismiss」），面板一选就关，看不到方向翻转，选中后才可勾的复选框够不着
