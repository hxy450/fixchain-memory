# 几何来自 onAreaChange 写入的状态时，不把宽高按值传给 @Builder

审的是：代码
触发（任一种）：
- 写错的样子：@Builder 函数带 (w: number, h: number) 这类参数，调用处传 onAreaChange 写进 @State 的宽高，旋转后布局不重算
适用范围：组件几何由 onAreaChange 或窗口尺寸写入的状态计算、并在 @Builder 里排布时
做法：
- @Builder 改成无参，在函数体内直接读组件上的宽高状态；或用带尺寸的 ForEach 键让它随尺寸重建
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 调用@Builder装饰的函数默认按值传递。当传递的参数为状态变量时，状态变量的改变不会引起@Builder函数内的UI刷新：按值传的宽高变了，Builder 里的布局不跟着变（出处：arkts-builder.md，按值传递参数）
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件尺寸变化回调，newValue 带宽高（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 竖横 Builder 改为无参，在内部读页面宽高状态：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-b0d293fe50601628c722（Privacy Friendly 2048）：做法第 1 步 ← 建议 5、诊断；取值 3 ← 诊断
