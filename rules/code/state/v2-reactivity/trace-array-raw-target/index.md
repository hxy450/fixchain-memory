# 定时器里逐格计算的 @Trace 数组

agent 会看到什么：读到源端在协程 delay 之后对普通 List 网格逐格计算、判定、计数再整体 copy 提交，目标网格是 @Trace 字段、tick 用 setTimeout；产物里回调把 @Trace 数组字段 this.… 直接交给逐格计算函数，没有 UIUtils.getTarget(...)

## 规矩

- rule-9c2357f2ccfe｜定时器里逐格同步计算 @Trace 数组时，开头用 UIUtils.getTarget 取原始数组｜读到：源端在协程 delay 之后对普通 List 网格逐格计算、判定、计数，再整体 copy 提交；规格要求网格是 @Trace 字段、tick 用 UI 线程 setTimeout；写错：setTimeout 回调里把 @Trace 装饰的（二维）数组字段 this.字段 直接传给逐格计算、结束判定和计数函数，没有 UIUtils.getTarget(...)
