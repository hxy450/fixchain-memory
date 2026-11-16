# onClick 的 ClickEvent 没有 stopPropagation，不照搬别处的这一行

审的是：代码
触发（任一种）：
- 读到：交互映射参考把 stopPropagation() 列在触摸事件一节，注明只停止 Touch 事件；或 rg 到别处回调里的 event.stopPropagation() 行（结果行看不出回调的事件类型）；写错的样子：写成 .onClick((event: ClickEvent) => { event.stopPropagation() })，或给原本无参的 onClick 加上 ClickEvent 参数去调 stopPropagation
适用范围：ArkUI 组件的点击回调里想阻止事件冒泡时
做法：
- onClick 回调不调 stopPropagation，写成无参 .onClick(() => { … })
- rg 到 event.stopPropagation() 时，先看它所在回调的事件类型：onTouch 的 TouchEvent 有这个方法，ClickEvent 没有，不按行文本套到 onClick 上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onClick(event: (event: ClickEvent) => void): T：点击回调的参数是 ClickEvent（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- declare interface ClickEvent extends BaseEvent（成员里没有 stopPropagation）：ClickEvent 不提供 stopPropagation（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ClickEvent）
- stopPropagation: () => void：TouchEvent 的成员：阻止事件向上或向下冒泡（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TouchEvent.stopPropagation）
- onTouch(event: (event: TouchEvent) => void): T：带 stopPropagation 的 TouchEvent 出自触摸回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouch）
- 删去 ClickEvent 参数与 stopPropagation、改回无参回调后编译通过：修好后的写法（出处：卡里修好并验证过）
未核实：卡里的编译报错出自 API 26（target_sdk 26.0.0），本机核对用的是 API 23
来源：1 张卡，1 个应用
- case-ca8dec09be8655edbb02（组件岛Widget Island）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
