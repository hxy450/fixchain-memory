# 当前页底部弹层的承载和层级

agent 会看到什么：读到在当前页 show 的底部 Dialog / BottomSheetDialog / PopupWindow，或弹层里点条目直接 startActivity；产物里面板写成 @HMRouter 路由页、插在内容列里的 if 块，以及 SheetOptions 的 mode 和 openBindSheet 的 targetId

## 规矩

- rule-69aad08eca50｜当前页底部弹窗在宿主页内叠层显示，不写成 @HMRouter 路由页加伪遮罩｜读到：源码在当前 Activity 上 show 一个全宽底部 Dialog / BottomSheet，点背景关闭；写错：目标把面板写成 @HMRouter 路由页，用半透明色块伪装遮罩，宿主用 HMRouterMgr.push 打开、面板用 HMRouterMgr.pop 关闭
- rule-5413d35b73ff｜规格写「日历弹层」时放在根 Stack 顶层盖住面板和键盘，不在内容列里内嵌切换｜读到：源端点日期再 show 一个同类底部日历 Dialog；规格或计划写「日历弹层」；写错：目标用 `if (…Visible) { 日历块 }` 插在 layoutWeight(1) 的内容列里、键盘面板之上的流式布局中，日历被挤压、不覆盖键盘
- rule-609205883881｜弹层内会跳页且要保留弹层时，半模态用 SheetMode.EMBEDDED，不照搬 OVERLAY｜读到：源端弹窗（PopupWindow、Dialog 等）里的条目点击直接 startActivity 打开整页，弹窗不先 dismiss；写错：目标半模态的 SheetOptions 照选择器类模板写 mode: SheetMode.OVERLAY，弹层内动作又走 NavPathStack 压栈，新页面显示在弹窗下面
- rule-c191456cd584｜openBindSheet 用 EMBEDDED 时传宿主页内组件的 targetId，否则回退 OVERLAY｜写错：SheetOptions 写了 mode: SheetMode.EMBEDDED，但 uiContext.openBindSheet(content, options) 没传第三个参数 targetId，弹窗配置接口只有 uiContext
