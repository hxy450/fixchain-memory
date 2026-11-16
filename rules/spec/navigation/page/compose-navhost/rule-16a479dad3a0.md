# tab 切换带 popUpTo(startDestination) 时，规格分写返回栈后果和状态保留两条验收

审的是：规格
触发（任一种）：
- 读到：Compose Navigation 切 tab 用 navigate(route) { popUpTo(startDestination) { saveState = true }; launchSingleTop = true; restoreState = true }，源注释说在其他底部 tab 按返回回到起始目的地；写错的样子：规格只把它抄成「launchSingleTop + restoreState + popUpTo(saveState)」标签，或只解释成切回 tab 时滚动位置保留；没有「非起始 tab 按系统返回回起始 tab」的验收条目
适用范围：规格提取阶段，为底部导航的 tab 切换写导航契约和验收条目时
做法：
- 写一条返回栈验收：非起始 tab 按系统返回回到起始 tab（tab 状态不重置），起始 tab 上按返回才退出；并写明目标的返回键入口是 @Entry 页的 onBackPress
- restoreState / saveState 另写一条：切回某 tab 时它的状态保留；源码注释里描述的导航行为原样转成验收条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 非起始 tab 按系统返回先回起始 tab，起始 tab 上才退出：修复时判定规格缺的就是这条验收（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-902870a7e6081dd22611（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；取值 1 ← 诊断
