# ArkUI onTouch 判末指抬起写 type===Up 且 touches.length===1，不写 0

审的是：代码
触发（任一种）：
- 读到：源端或规格要求在最后一根手指抬起（ACTION_UP，「非末指 Up 不进状态机」）时结算手势；写错的样子：目标 .onTouch 的 Up 分支写成 event.touches.length === 0（或 touches 为空）才结算，滑动永远不触发
适用范围：用 ArkUI .onTouch 手写手势状态机、要在最后一根手指抬起时结算的代码
做法：
- 末指抬起写成 event.type === TouchType.Up && event.touches.length === 1，或者按 changedTouches[0].id 跟踪手指；Up 事件的 touches 仍含正在抬起的那根手指
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- if (event.type === TouchType.Up && event.touches.length === 1) // 所有手指都已抬起：官方示例里末指抬起的判法（出处：arkts-interaction-development-guide-touch-screen.md，多指信息）
- 单指滑动抬起时实测 type=1（Up）、touches.length=1：Up 事件的 touches 含正在抬起的手指，touches.length === 0 的条件永不成立（出处：卡里修好并验证过）
- touches: TouchObject[]：全部屏幕触点（多指）的信息（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TouchEvent.touches）
- changedTouches: TouchObject[]：发生变化而产生这次事件的手指（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TouchEvent.changedTouches）
来源：1 张卡，1 个应用
- case-a1849836a1bfff3c265c（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
