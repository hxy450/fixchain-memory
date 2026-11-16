# ContextMenu、ActionMode 改写成页内 @Local 浮层时，同步实现返回键先关浮层、退多选

审的是：代码
触发（任一种）：
- 读到：源端 registerForContextMenu / setOnCreateContextMenuListener + onCreateContextMenu 弹系统 ContextMenu 窗口，或 startActionMode 进入多选；写错的样子：目标把长按菜单写成页面 @Local 状态浮层（遮罩 + 菜单卡）、多选写成一个布尔状态，只靠遮罩点击、菜单动作或清空选中关闭，没有返回键处理；照抄已有页内浮层写法
适用范围：把窗口型临时 UI（ContextMenu、ActionMode）改写成页面状态浮层时
做法：
- 给页面登记返回回调：菜单浮层打开时先关浮层，多选态时先退出多选，两种情况都返回 true 消费本次返回；都不在时返回 false 交给宿主
- 复制已有页内浮层写法前，先确认那份写法有没有接返回键
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPressed 回调返回 true 表示重写返回键逻辑，返回 false 表示回退到上一个页面：宿主分发到页面回调后，用返回值决定是否消费（出处：ts-basic-components-navdestination.md，onBackPressed）
- 菜单或多选态按返回只关菜单或退出多选，仍停在当前页：修好后上机看到的行为（出处：卡里修好并验证过）
未核实：ContextMenu 窗口先吃掉返回键属于平台隐含语义，卡里没有直接引用源码
来源：1 张卡，1 个应用
- case-f32c19bb6ab1caffe063（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
