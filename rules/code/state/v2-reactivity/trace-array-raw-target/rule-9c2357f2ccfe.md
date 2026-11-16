# 定时器里逐格同步计算 @Trace 数组时，开头用 UIUtils.getTarget 取原始数组

审的是：代码
触发（任一种）：
- 读到：源端在协程 delay 之后对普通 List 网格逐格计算、判定、计数，再整体 copy 提交；规格要求网格是 @Trace 字段、tick 用 UI 线程 setTimeout；写错的样子：setTimeout 回调里把 @Trace 装饰的（二维）数组字段 this.字段 直接传给逐格计算、结束判定和计数函数，没有 UIUtils.getTarget(...)
适用范围：@ObservedV2 模型或 @ComponentV2 组件里，定时器或帧回调中同步执行的逐格、逐元素计算读 @Trace、@Local 数组（嵌套数组的每一行也是代理）时
做法：
- tick 开头 const raw = UIUtils.getTarget(this.字段)，计算、结束判定、比较、计数都用 raw；需要上一代时把它作参数传进判定函数，不在函数里再逐格读 this.字段
- 提交时仍整体赋值给 @Trace 字段（this.字段 = 新数组）来触发刷新，不靠改 raw 的内容刷新
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static getTarget<T extends object>(source: T): T：UIUtils 取状态管理代理前的原始对象，入参不是代理时原样返回；@since 12（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，UIUtils.getTarget）
- V2 给 @Trace、@Local 装饰的 Date、Map、Set、Array 添加一层代理：直接遍历这些数组时每次读取都经过代理（出处：arkts-new-getTarget.md，概述）
- 更改 getTarget 获取的原始对象中的内容不会被观察到变化，也不会触发 UI 刷新：原始数组只用来读和算，提交要整体赋值给 @Trace 字段（出处：arkts-new-getTarget.md，限制条件）
- 逐格计算改读原始数组后，每代计算从十几到二十多毫秒降到 2–5ms，世代节拍接近源端：定时器回调里的同步耗时会直接加到间隔上（出处：卡里修好并验证过）
未核实：对外层数组 getTarget 后内层行是否也都不经代理，文档没写嵌套情形，按卡里修好后的耗时下降写
来源：1 张卡，1 个应用
- case-31dcdb74eb848ff217c8（GameOfLife）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
