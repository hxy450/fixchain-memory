# 规格把 Activity/Fragment 生命周期和事务语义写成独立验收条目，不只写一行等价

审的是：规格
触发（任一种）：
- 读到：源码有 replace + addToBackStack、popBackStackImmediate 后换新实例、popBackStack、finish()，以及 onActivityCreated → init、onDestroyView、onStop 等回调；写错的样子：规格只写「navPathStack ← 各个切换 Fragment 的方法 等价」「onResume → onPageShow」「onPause → onPageHide」一行，没有视图销毁重建、finish 与 popBackStack 的区别、同名页能否复用
适用范围：规格提取时写回退栈和生命周期映射的验收条目
做法：
- 各写一条验收条目：onActivityCreated → init 的返回重建；onDestroyView 的视图销毁；finish 与 popBackStack 的区别（结束页面 / 回上一页、是否越根）；同名页面是否允许复用（每次新实例的写明 NEW_INSTANCE）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LaunchMode.NEW_INSTANCE：不复用栈里同名实例；默认 STANDARD：规格里写「同名页能否复用」时对应的目标写法（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，LaunchMode.NEW_INSTANCE、NavigationOptions.launchMode）
来源：1 张卡，1 个应用
- case-aebac48fa7acdb86e57e（omni-notes-hmos）：做法第 1 步 ← 建议 3
