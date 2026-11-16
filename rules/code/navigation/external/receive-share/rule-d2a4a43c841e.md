# 分享承接 Ability 用 getSharedData 取数据、经 LocalStorage 传页面，只结束自己

审的是：代码
触发（任一种）：
- 读到：源码只在 onCreate 读 getIntent() 的 EXTRA_TEXT，没有 onNewIntent，处理完 setResult + finish()；写错的样子：唯一的 EntryAbility 在 onCreate 和新加的 onNewWant 里都解析分享 want，经全局事件或静态中转变量送页面；页面在分享分支里调 terminateSelf()，关掉整个应用
适用范围：目标端接收系统分享（ShareKit）的承接 Ability 和它加载的页面
做法：
- 分享承接 Ability 的 onCreate 里 await systemShare.getSharedData(want)，在 getRecords() 里取 utd 与 skills 声明一致（文本是 'general.plain-text'）的记录的 content
- windowStage.loadContent(页面, storage) 用 LocalStorage 传入参，页面用 this.getUIContext().getSharedLocalStorage() 读；分享实例结束时调 terminateSelf，只结束这个实例
- 源端没有 onNewIntent 时不补 onNewWant 热启动分支；入口 Ability 只有一个时不在分享流程里调 terminateSelf，先回规格核对实例形态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getSharedData(want: Want): Promise<SharedData>：从拉起分享承接 Ability 的 want 里解析分享数据（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.systemShare.d.ts，systemShare.getSharedData）
- SharedData.getRecords(): Array<SharedRecord>；SharedRecord.utd: string、content?: string：按 utd 选记录，文本在 content 里（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.systemShare.d.ts，SharedData.getRecords、SharedRecord）
- loadContent(path: string, storage?: LocalStorage): Promise<void>：WindowStage 加载页面时把 LocalStorage 交给页面（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，WindowStage.loadContent）
- getSharedLocalStorage(): LocalStorage | undefined：页面取 loadContent 传入的 LocalStorage（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getSharedLocalStorage）
- loadContent(path: string, storage: LocalStorage): Promise<void>：同族接口：Window 的 loadContent 也接收 LocalStorage（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.loadContent）
来源：1 张卡，1 个应用
- case-4e3bf06f478ee642f9cb（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 诊断、建议 1；做法第 3 步 ← 建议 3
