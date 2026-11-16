# 全屏沉浸页的避让 padding

agent 会看到什么：读到入口 Ability 调 setWindowLayoutFullScreen(true)、规格标 needs_immersive_safearea / full_screen_page 或源端 enableEdgeToEdge，产物里是页面上的 expandSafeArea、固定 padding、安全区注释和引用避让值的 padding 表达式

## 通用查法

### 开了 setWindowLayoutFullScreen 时，查出顶部和底部避让值，每页贴边那层显式写 padding

审的是：代码
触发（任一种）：
- 读到：入口 Ability 调 setWindowLayoutFullScreen(true)，或规格标 needs_immersive_safearea=true；源端是 enableEdgeToEdge 加 safeDrawingPadding；写错的样子：页面只靠 .expandSafeArea(...)、固定的 .padding({ bottom: 8 }) 或安全区注释，贴顶、贴底那层没有引用避让值的 .padding
适用范围：窗口全屏布局后，各页面前景对状态栏和底部导航条的避让
做法：
- 到入口 Ability 找避让值：getWindowAvoidArea(TYPE_SYSTEM).topRect.height 作顶部、TYPE_NAVIGATION_INDICATOR 的 bottomRect.height 作底部，读出它发布到的 AppStorage 键或共享避让模型、发布前是否已 px2vp；没有就照此补上
- 每页订阅同一份值：贴顶那层写 .padding({ top: 顶部避让 + 源端额外间距 })，伸到窗口底边的那层写 .padding({ bottom: 底部避让 + 原有间距 })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea；AvoidAreaType.TYPE_SYSTEM = 0、TYPE_NAVIGATION_INDICATOR = 4：取状态栏、底部导航条的避让区（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea、window.AvoidAreaType）
- AvoidArea.topRect: Rect、AvoidArea.bottomRect: Rect；UIContext.px2vp(value: number): number：取 Rect 的 height，再换成 vp 作 padding（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，AvoidArea；ets/api/@ohos.arkui.UIContext.d.ts，UIContext.px2vp）
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T：只把组件区域扩展进安全区，不替前景做避让（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- 沉浸式布局下要在组件布局时做额外的布局避让，可加 padding 或占位组件：官方说法：全屏布局本身不做避让（出处：immersive-window-feature.md，布局避让）
- 例：移除容器上的 expandSafeArea，按 TYPE_SYSTEM / TYPE_NAVIGATION_INDICATOR 测得的高度经 px2vp 给根 Navigation 加 top / bottom padding 后，标题落在状态栏下方：带条件的例子：入口页是根 Navigation 加 Tabs / NavDestination 壳（出处：卡里修好并验证过）
针对本应用要查的：
- 应用发布避让值用的 AppStorage 键名（或共享避让模型的字段）和单位：目标工程入口 Ability 的 .ets 文件里 getWindowAvoidArea 与 AppStorage.setOrCreate 那几行；页面用同一个键（@StorageProp）或同一个模型字段；看发布前有没有 px2vp，决定页面端是否还要换算
- 源端在状态栏、导航条高度之外另加的间距：源工程里这一页在 safeDrawingPadding / WindowInsets 之外再写的 padding 或 dp 常量；读出 dp 数，加在避让值后面
未核实：Rect.height 的单位声明里没写，按卡里修好的做法当 px 用 px2vp 换算；卡里的观察出自 API 24（HarmonyOS 6.1.1），本机声明按 API 23 核实
来源：3 张卡，3 个应用
- case-436d1b16d79796c667d6（android-panorama-map-vest7）：做法第 2 步 ← 建议 3
- case-57a2aab5dd7835648d69（Meshtastic）：做法第 1 步 ← 建议 2；取值 5 ← 诊断
- case-b0970c46149a1a9dbb98（android-train-ticket-vest7）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-c92b5474b408｜全屏布局页面按 getWindowAvoidArea 的高度补 padding，不靠 expandSafeArea｜读到：规格标了 `needs_immersive_safearea=true` 或 `page_type=full_screen_page`；源端是 `enableEdgeToEdge` 加 `safeDrawingPadding`；写错：EntryAbility 里 `setWindowLayoutFullScreen(true)`，页面只在容器上加 `.expandSafeArea([SafeAreaType.SYSTEM], …)`，没有 `getWindowAvoidArea` 读取和基于避让高度的 padding
- rule-b2b83cf4634d｜全屏沉浸后每个 NavDestination 页都要真用避让值加 padding，不能只写注释标记｜读到：窗口 setWindowLayoutFullScreen(true)，根 Navigation 加了四向 expandSafeArea；派工的安全区修复口径写「复用 ImmersiveScaffold 或手动 padding windowTop/BottomPadding」；写错：NavDestination 页里只有「// ImmersiveScaffold contract: …」之类的注释，没有订阅共享避让模型，顶部仍是固定 top 间距，找不到 windowTopPadding / windowBottomPadding 的 .padding 表达式
- rule-83d339c9d590｜全屏铺到底边的页面要把底部导航条避让加到底部内容容器上，不用固定 padding｜读到：页面规格标 page_type = full_screen_page、needs_immersive_safearea = true；入口 Ability 调 setWindowLayoutFullScreen(true)，或外层容器对 SafeAreaEdge.BOTTOM 做了 expandSafeArea；写错：页面根容器只写固定的 .padding({ bottom: 8 })，没读入口 Ability 发布到 AppStorage 的底部避让值（@StorageProp），也没取 getWindowAvoidArea，底部按键行或 Tab 栏落进导航指示条区
- rule-a349791b99a8｜开 setWindowLayoutFullScreen(true) 前逐个 NavDestination 页核顶部避让｜写错：EntryAbility 里开启 `setWindowLayoutFullScreen(true)`，注释写「各页已接」，但有 NavDestination 页没有 windowTopPadding 一类的顶部避让
- rule-3a73c187ee9a｜作为宿主 Tab 子组件的页面，宿主已加安全区时不在根容器上重复叠加｜读到：宿主页面的 `Tabs` 容器已经 `.padding({ top: …, bottom: … })` 加了顶部、底部安全区；写错：Tab 子组件的根 `Column` 又加了同样的底部安全区 `.padding({ bottom: … })`
- rule-352b318e0463｜底部 Tab 栏固定高度已含底部留白时，导航条避让替代这段留白，不整额叠加｜读到：Tabs 原有 .barHeight(固定值)，tabBar 的自定义构建函数内容顶对齐、图标文字下方留有空白；避让值取自 getWindowAvoidArea(AvoidAreaType.TYPE_NAVIGATION_INDICATOR).bottomRect.height；写错：.barHeight(原固定值 + px2vp(避让高度))，把整额避让加在已含留白的高度上
- rule-4acd62b5ab38｜底部元素已有固定 bottom 偏移时，先和实测避让高度比，够用就不追加避让｜读到：底部定位元素已写 .position({ bottom: 固定值 })，避让值来自 TYPE_NAVIGATION_INDICATOR 的 bottomRect.height；写错：改成 .position({ bottom: 固定值 + px2vp(避让高度) })，或把用户没提到的组件也一并加上避让
- rule-9530ec8ed096｜收口安全区 FWD-REF 或开启全屏前，逐页查自绘标题栏有没有消费 windowTopPadding｜读到：安全区 FWD-REF 的注释只写底部份额；base-contracts 写 WindowModel 共享 windowTopPadding / windowBottomPadding；写错：收口时只改成 .padding({ bottom: 12 + windowBottomPadding }) 并删掉 marker，自绘标题栏仍没有 windowTopPadding
- rule-d41d51c1c6c3｜收尾闸报全屏页缺 Layer 3 时，grep 到宿主实际避让才可标沉浸豁免 false｜读到：沉浸检查结果报某全屏页未发现任何安全区响应，修复方式为 windowTopPadding，仅确无前景避让需求才可标 false；写错：页头加了 needs_immersive_safearea=false 豁免注释（理由如「原生标题栏自动避让」「壳层统一处理」），而本页和宿主都没有 windowTopPadding
