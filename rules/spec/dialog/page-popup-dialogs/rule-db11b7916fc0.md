# 源端在当前页 show 底部弹窗时，规格写叠层契约，不因「路由统一用 HMRouter」改成路由页

审的是：规格
触发（任一种）：
- 读到：源码在当前 Activity 上 show 一个 Dialog / BottomSheet（全宽底部面板），面板里还可能再弹同类底部日历；工程另有「路由统一使用 HMRouter」的基座约束；写错的样子：规格写「可以用 HMRouter 页面承载等价的底部弹层」，映射表、数据流写成宿主页 → HMRouter 路由页，验收以 route 判定，没写宿主页可见、点背景关闭、不入返回栈
适用范围：把安卓在当前页弹出的 Dialog、BottomSheet 映射到 ArkUI 承载方式时，规格里写呈现方式、映射表和验收的那几处
做法：
- 把呈现方式写成可验收契约：叠加在宿主页之上、遮罩下可见宿主页、点背景或取消关闭、不新增返回栈；注明「路由统一用 HMRouter」只约束页面跳转
- 承载方式写宿主页内 Stack 顶层叠层，或 bindSheet / CustomDialog，并规定关闭回调由宿主持有
- 若选路由页或独立窗口，先确认它能保留宿主页可见和点背景关闭，并在验收条目里写明对应检查
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 宿主页持有显示状态，在本页以 zIndex 叠加面板组件，遮罩 onClick 关闭：卡里最终保留的承载方式；改前的路由页方案露出伪遮罩、进了返回栈（出处：卡里修好并验证过）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：给组件绑定半模态面板，显隐由 isShow 控制（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- constructor(value: CustomDialogControllerOptions)；autoCancel?: boolean（点弹窗外部是否关闭）：CustomDialog 的控制器构造和点外部关闭的选项（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogController.constructor、CustomDialogControllerOptions.autoCancel）
- zIndex(value: number): T：同一容器里兄弟组件的层级，值大的在上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex）
来源：1 张卡，1 个应用
- case-504604963e18f4b6e2f3（android-train-ticket-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 1 ← 诊断
