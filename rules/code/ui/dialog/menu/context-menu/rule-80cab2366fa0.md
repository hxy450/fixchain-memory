# 源 onCreateContextMenu 在多选态早返回时，目标长按回调先判多选态再返回

审的是：代码
触发（任一种）：
- 读到：onCreateContextMenu 第一行判断多选（ActionMode）是否开着，开着就直接 return，不建菜单；写错的样子：目标长按回调（LongPressGesture().onAction 或列表组件的长按回调）只记下条目就打开菜单，多选态下长按照样弹菜单
适用范围：列表既有多选态又有长按上下文菜单的页面和区段组件，迁成 ArkUI 时
做法：
- 每个打开菜单的长按回调开头先判断当前是否处于多选态，是就直接 return，不记条目、不打开菜单；共享的列表组件和各宿主页面都要有这一句
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 多选态下长按提前返回，不弹菜单：修复后各页保留的写法（出处：卡里修好并验证过）
- void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo)：源端建菜单的回调，早返回就不出菜单（出处：android.view.View.OnCreateContextMenuListener#onCreateContextMenu）
来源：1 张卡，1 个应用
- case-3ca3658855acd903c4ca（AntennaPod）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
