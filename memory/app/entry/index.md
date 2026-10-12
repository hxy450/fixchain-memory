# app/entry

入口 Ability 与应用级配置：onCreate/onDestroy 中基础设施的显式初始化时机、需要补上的平台级守护，系统配置变化（源 Activity 未声明 configChanges 时的重建语义）在 onConfigurationUpdate 中的承接与跟随系统字号的 configuration，以及 module.json5 中入口 Ability 的 skills（深链、App Links 的 domainVerify）声明、桌面快捷方式（shortcuts）声明与外部 Want 的入口分支；冷启动首帧前按偏好同步恢复主题的时机；进程回收后页面栈恢复（setRestoreEnabled、restoreWindowStage、recoverable）

[上一级](../index.md)

## 本级经验

- [ohos.ability.shortcuts 挂在承载快捷方式的 UIAbility 的 metadata 下，不追加到 module 级 metadata](lesson-67118603fcc769a5edc9.lesson.md)
  - 时机：配置实现阶段，在 module.json5 中挂载桌面长按快捷菜单（ohos.ability.shortcuts）时；构建后长按不出菜单或快捷方式条目变少时
  - 情境：把 Android App Shortcuts 迁为 HarmonyOS 静态快捷方式：在 resources/base/profile 下新建快捷方式配置，并在 module.json5 中用 metadata 引用；module 级已有 metadata 数组（如 client_id），入口 UIAbility 还没有 metadata。
- [入口 Ability 注册全局未捕获异常观察器，Android 源里没有对应代码也要补](lesson-c6132bf52c26ec226788.lesson.md)
  - 时机：入口装配阶段，改写 EntryAbility（或 AbilityStage）的 onCreate/onDestroy 并决定入口需要哪些平台级守护时
  - 情境：目标为 HarmonyOS Stage 模型应用，入口 UIAbility 由模板改写而来；Android 源没有可对照的全局异常处理，按源码迁移不会产生这段代码，而验收（如 ECAT crash_risk 规则）要求存在全局异常观察。
  - 例外：工程已在 AbilityStage 或其他入口注册了 errorManager 观察器或等效的崩溃监听
- [只经桌面快捷方式或通知点击进入的页面：module.json5 快捷方式声明、EntryAbility 的 Want 分支与目标页参数都要有确定写者](lesson-c46f182cf1d01a97e05f.lesson.md)
  - 时机：规格拆分、切片实现与入口接线阶段，迁移源端只由外部 Intent（桌面快捷方式、本地通知点击）进入的页面时
  - 情境：源端页面由静态或动态 shortcut、通知 PendingIntent 携带 extras（如 shortId、通知渠道）进入；目标规格把入口配置定为 module.json5 静态声明；页面与切片 worker 的写域不含 module.json5 和 EntryAbility。
- [源 Activity 未声明 configChanges 时，语言、深浅色、字号、显示大小变化会重建它：目标 UIAbility 不重建，在 onConfigurationUpdate 与 display 变化中按源端重建时序显式刷新](lesson-94715d0df4c03a8fb5a5.lesson.md)
  - 时机：规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期，以及资源文案与一次性状态的缓存时
  - 情境：源 Activity 在 AndroidManifest 中未声明 android:configChanges，实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化时不重建，只回调 onConfigurationUpdate 或发出 display 'change'。
- [源端在入口 onCreate 首帧前按偏好设主题时，目标在 EntryAbility.onCreate 同步读取偏好并在 loadContent 前 setColorMode；恢复函数返回 Promise 而调用方不等待，就是首帧后才生效](lesson-dcb3c5e66dec2d126234.lesson.md)
  - 时机：入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时
  - 情境：源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。
- [源端返回栈靠 rememberNavController 或 savedInstanceState 在进程回收后恢复时，规格单列“回收后重建”分支，目标显式开启 UIAbility 恢复与 Navigation recoverable](lesson-b0405a29415547485ecb.lesson.md)
  - 时机：规格提取阶段为宿主 Activity 生命周期与导航容器编写验收项时；入口装配阶段实现 UIAbility 与根 Navigation 时
  - 情境：源 Activity 在 onCreate(savedInstanceState) 接收存档，或用 Compose rememberNavController + NavHost（以及 Fragment 返回栈）承载页面；源码里没有显式保存代码，进程在后台被系统回收后，返回栈与路由参数由框架恢复。目标为 UIAbility + Navigation/NavDestination + NavPathStack，页面栈恢复默认不开启，入口每次 loadContent 首页并在空栈时 push 起始页；规格只写“冷启进入起始页”。
- [源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封装后，在入口 onCreate 最早处调用，并确认启动期读写都晚于初始化](lesson-8a881c2e07f80f83447c.lesson.md)
  - 时机：网络、键值存储等基础设施实现与入口接线阶段：新建必须先 init 才能用的封装，或改写 EntryAbility.onCreate、宣告基础层完成时
  - 情境：源端网络 baseUrl 由 DI 模块在注入时带上、键值工具（SpUtils/MMKV 一类）全局静态可用，Application.onCreate 里看不到对应的初始化；目标端改为静态 HttpClient（baseUrl 默认空串）加 NetworkConfig.init()、偏好封装需先传入上下文；入口 Ability 由编排会话维护，Flutter 插件 onAttachedToEngine 等回调里也能拿到上下文。也包括网络层以静态运行期配置承接构建期注入值（configure 写入、未配置即 throw），基础模块不得改入口，启动接线者不知道这条调用义务。
- [裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号](lesson-ea965b7baf2488be23cd.lesson.md)
  - 时机：规格的横切能力裁定阶段（i18n、深色、大字体、无障碍）判断系统字号缩放是否迁移时；派发应用身份或应用外壳任务、落定 AppScope/app.json5 的 configuration 时
  - 情境：源应用主体可能是固定 px 字号的 Canvas 自绘，但仍有系统 AlertDialog、Toast、菜单或 sp 单位文本；Activity 是否在 configChanges 声明 fontScale 决定字号变化时重建还是回调；目标 HarmonyOS 应用默认不跟随系统字号（nonFollowSystem），需在 AppScope 配置 configuration profile 才会跟随并下发配置变化。
- [迁移深链 intent-filter 时同时声明 module.json5 的 skills（actions、entities、uris，App Links 加 domainVerify），并用隐式 Want 验收](lesson-d77baa7494930d485425.lesson.md)
  - 时机：入口与导航接线阶段，把源端 Activity 的 VIEW/BROWSABLE intent-filter 迁成 UIAbility 的 Want 接收与路由解析时；以及规格提取阶段描述深链映射时
  - 情境：源 AndroidManifest 在启动 Activity 上声明 VIEW+BROWSABLE、http/https 与固定 host 的 intent-filter；目标 module.json5 的入口 Ability skills 仍是脚手架默认的 HOME 一项。 也包括 intent-filter 带 android:autoVerify="true"（App Links），或决策写明 https 由域名校验的 App Linking 承载。也包括导航图 navDeepLink 的 uriPattern 或分享/复制链接由常量拼接（如 "$baseUrl/item/{id}"），深链规格的源码锚点没有列入 AndroidManifest。
