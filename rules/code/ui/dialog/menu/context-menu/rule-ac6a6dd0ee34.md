# 源列表用 registerForContextMenu 弹上下文菜单时，目标长按打开菜单，不直接进多选

审的是：代码
触发（任一种）：
- 读到：源列表或 Fragment 调 registerForContextMenu，并实现 onCreateContextMenu / onContextItemSelected，多选只在菜单里某一项被点时开始；写错的样子：目标列表项的长按（LongPressGesture().onAction 或列表组件的长按回调）直接进入多选，注释写「长按进入多选」，全文没有上下文菜单
适用范围：安卓列表条目靠 View 的上下文菜单（registerForContextMenu + onCreateContextMenu）响应长按，迁成 ArkUI 列表时
做法：
- 长按回调改为打开上下文菜单并记下被长按的条目；进入多选只写在菜单里「多选」那一项的点击分支里，对应源端 onContextItemSelected 里该项的处理
- 规格的验收条目写了「长按弹菜单」而已有页面代码是长按进多选时，按验收条目和源码改代码，不以「已接受的简化」或 FWD-REF 清单范围为由保留
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- registerForContextMenu(View view) 把 view 的 OnCreateContextMenuListener 设成这个 Fragment/Activity，长按时回调 onCreateContextMenu：源端长按的含义是弹上下文菜单（出处：android.app.Fragment#registerForContextMenu；android.app.Activity#registerForContextMenu）
- onContextItemSelected(MenuItem item)：上下文菜单里某一项被选中时回调：源端进多选等动作在这里按菜单项分派（出处：android.app.Fragment#onContextItemSelected）
- declare const LongPressGesture: LongPressGestureInterface；onAction(event: (event: GestureEvent) => void): LongPressGestureInterface：目标端长按手势，onAction 里打开菜单（出处：鸿蒙 SDK 的 ets/component/gesture.d.ts，LongPressGesture、LongPressGestureInterface.onAction）
- 整页列表长按改弹菜单、菜单的「多选」项才进多选：修复后保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3ca3658855acd903c4ca（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断
