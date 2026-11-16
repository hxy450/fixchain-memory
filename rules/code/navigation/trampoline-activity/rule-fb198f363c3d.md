# 调用方 Intent 指向开头即跳走的 Activity 时，鸿蒙路由直接指向用户实际看到的首屏页

审的是：代码
触发（任一种）：
- 读到：调用方 startActivity(Intent(context, X::class.java))，而 X 的 onCreate 或 initView 开头无条件 startActivity 到别的页并 finish()；写错的样子：调用方的鸿蒙代码按 Activity→Page 的名称映射写成 pushPathByName 到 X 对应的页，没有复核 X 一进入就跳走
适用范围：翻译调用方里的 Intent 跳转、确定鸿蒙路由目标时
做法：
- 翻译 Intent(X) 时先读 X 的 onCreate/initView：开头就按条件 startActivity 到别页并 finish() 的，调用方改成 NavPathStack.pushPathByName 到那个实际目标对应的页（源端有条件分支的照写同样的分支），不指向 X 对应的页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 的方法：按名字把页压入导航栈；animated 默认 true（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- pushPathByName(name: string, param: Object, onPop: import('../api/@ohos.base').Callback<PopInfo>, animated?: boolean): void：同一方法带返回回调的重载，源端用 startActivityForResult 等要拿回结果时用（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- 调用方路由改指实际目标页后，从入口点进去的首屏与源端一致：修复的落点在调用方的路由目标（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-327636c44f08419021a9（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断
