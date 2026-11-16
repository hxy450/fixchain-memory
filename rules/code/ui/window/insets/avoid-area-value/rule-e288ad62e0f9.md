# 页面订阅安全区时从主窗口取窗口对象，不用 window.getLastWindow

审的是：代码
触发（任一种）：
- 读到：参考或 skill 示例里用 window.getLastWindow(getContext(this)) 设置系统栏属性；工程 EntryAbility 在 windowStage.getMainWindowSync() 得到的主窗口上 on('avoidAreaChange') / getWindowAvoidArea 测量安全区；写错的样子：页面里用 window.getLastWindow(ctx) 取窗口，再在其上 on('avoidAreaChange') 或 getWindowAvoidArea 初始化顶部、底部避让高度
- 写错的样子：注释或报告写「与 EntryAbility 订阅同一窗口」，但页面取窗口的 API 和 EntryAbility 不同（一边 getLastWindow，一边 getMainWindowSync）
适用范围：ArkUI 全屏页面自行订阅状态栏、导航条避让区时
做法：
- 从承载页面的主窗口取窗口：复用工程现有的主窗口入口（封装 windowStage.getMainWindowSync() 的方法）或 EntryAbility 已维护的避让状态，再 on('avoidAreaChange', …) 并用 getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM) 初始化；不用 window.getLastWindow 推断页面所在窗口
- 注释或报告声称与 EntryAbility 订阅同一窗口时，在工程里搜 getMainWindow、getMainWindowSync、avoidAreaChange 的现有用法，确认两处取窗口的 API 一致
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getLastWindow(ctx: BaseContext): Promise<Window>：取当前应用最上层的窗口，没有子窗口时才返回主窗口（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.getLastWindow）
- getMainWindowSync(): Window：WindowStage 的主窗口（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，WindowStage.getMainWindowSync）
- on(type: 'avoidAreaChange', callback: Callback<AvoidAreaOptions>): void：窗口避让区变化监听；子窗口只有位置和大小与主窗口一致时才返回计算后的避让区，否则返回空（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('avoidAreaChange')；arkts-apis-window-Window.md，on('avoidAreaChange')）
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea：同步取避让区，初始化用；子窗口同样有「与主窗口一致才非空」的限制（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea；arkts-apis-window-Window.md，getWindowAvoidArea）
- AvoidAreaType.TYPE_SYSTEM = 0（系统栏）、TYPE_NAVIGATION_INDICATOR = 4（底部导航条）：顶部、底部避让高度分别取的类型（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.AvoidAreaType）
- getWindowAvoidAreaIgnoringVisibility(type: AvoidAreaType): AvoidArea：同族接口：不论该类区域当前是否可见都返回，@since 22（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidAreaIgnoringVisibility）
- 改为同步使用主窗口后，分享按钮位于状态栏下方且可点击：返修结果（出处：卡里修好并验证过）
针对本应用要查的：
- 工程里现有的主窗口入口和避让状态：目标工程的 .ets 文件里搜 getMainWindowSync、avoidAreaChange（EntryAbility 的 onWindowStageCreate、封装主窗口的工具类、AppStorage 里写入的避让高度键）；有封装好的主窗口方法或已维护的可观察避让状态就直接复用，页面不另取窗口
未核实：复现时成为最后窗口的具体是哪个子窗口，卡里没有确认
来源：1 张卡，1 个应用
- case-dfc66c797f37eb94114f（两步路）：做法第 1 步 ← 建议 1、建议 3、诊断；做法第 2 步 ← 建议 2；取值 7 ← 诊断
