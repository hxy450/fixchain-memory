# 当前页底部弹窗在宿主页内叠层显示，不写成 @HMRouter 路由页加伪遮罩

审的是：代码
触发（任一种）：
- 读到：源码在当前 Activity 上 show 一个全宽底部 Dialog / BottomSheet，点背景关闭；写错的样子：目标把面板写成 @HMRouter 路由页，用半透明色块伪装遮罩，宿主用 HMRouterMgr.push 打开、面板用 HMRouterMgr.pop 关闭
适用范围：安卓当前页底部弹窗迁到 ArkUI 时的宿主页和面板组件
做法：
- 宿主页持有显示状态（@State），在根 Stack 里条件渲染面板组件并用 .zIndex 置顶，面板通过 @Prop 拿初始参数
- 遮罩是宿主页里的一层，面板本身背景不透明；遮罩 onClick 和面板的取消、保存都回调宿主，把显示状态置 false
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- zIndex(value: number): T：同一容器里兄弟组件的层级，值大的在上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex）
- 面板加 @Prop 初始参数和模态标志，关闭时通知宿主；宿主按显示状态在本页 zIndex 叠加，遮罩 onClick 关闭；路由页用半透明根背景伪装遮罩会在圆角外露出灰边，改为不透明：卡里最终保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-504604963e18f4b6e2f3（android-train-ticket-vest7）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 诊断、建议 2；取值 2 ← 诊断
