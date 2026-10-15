# app/entry

入口 Ability 与应用级配置：onCreate/onDestroy 中基础设施的显式初始化时机、需要补上的平台级守护，系统配置变化（源 Activity 未声明 configChanges 时的重建语义，含旋转、非托管对话框与 NonConfigurationInstance 取回）在 onConfigurationUpdate 与页面中的承接与跟随系统字号的 configuration，以及 module.json5 中入口 Ability 的 skills（深链、App Links 的 domainVerify）声明、桌面快捷方式（shortcuts）声明与外部 Want 的入口分支；冷启动首帧前按偏好同步恢复主题的时机；进程回收后页面栈恢复（setRestoreEnabled、restoreWindowStage、recoverable）；EntryAbility 中依赖 UIContext 的步骤放进 loadContent 成功回调

[上一级](../index.md)

## 本级经验

- [EntryAbility 里依赖 UIContext 的步骤放进 loadContent 成功回调，之前调 getUIContext 抛 1300002](lesson-63fe5e10a98fe3cd3f5d.lesson.md)
  - 时机：入口实现阶段，在 EntryAbility.onWindowStageCreate 中安排依赖 UIContext 的步骤（getUIContext、px2vp 换算避让区、setKeyboardAvoidMode 等）相对 loadContent 的时机时；改动 EntryAbility 生命周期后自检时
  - 情境：目标在 EntryAbility 里做窗口全屏、系统栏或键盘避让设置，并测量避让区换算成 vp 写入共享窗口模型；这些步骤写在 onWindowStageCreate 中、位于 windowStage.loadContent 调用之前，或在其回调之外同步执行；模板只说“窗口设置放在 onWindowStageCreate”，没写与 loadContent 的先后。
- [ohos.ability.shortcuts 挂在承载快捷方式的 UIAbility 的 metadata 下，不追加到 module 级 metadata](lesson-67118603fcc769a5edc9.lesson.md)
  - 时机：配置实现阶段，在 module.json5 中挂载桌面长按快捷菜单（ohos.ability.shortcuts）时；构建后长按不出菜单或快捷方式条目变少时
  - 情境：把 Android App Shortcuts 迁为 HarmonyOS 静态快捷方式：在 resources/base/profile 下新建快捷方式配置，并在 module.json5 中用 metadata 引用；module 级已有 metadata 数组（如 client_id），入口 UIAbility 还没有 metadata。
- [只经桌面快捷方式或通知点击进入的页面：入口声明、EntryAbility 的 Want 分支与目标页参数都要有确定写者](lesson-c46f182cf1d01a97e05f.lesson.md)
  - 时机：规格拆分、切片实现与入口接线阶段，迁移源端只由外部 Intent（桌面快捷方式、本地通知点击）进入的页面时
  - 情境：源端页面由桌面快捷方式、通知 PendingIntent 携带 extras（如 shortId、通知渠道）进入；目标规格把入口配置定为 module.json5 静态声明；页面与切片 worker 的写域不含 module.json5 和 EntryAbility。
- [源 Activity 未声明 configChanges 且直接 show() 非托管对话框时，目标页内浮层补配置变化关闭路径](lesson-4b117abf301aa86efda2.lesson.md)
  - 时机：规格提取阶段为每个 Activity 把 configChanges/screenOrientation 缺省翻译成页面生命周期与弹窗状态契约时；实现阶段用页内状态驱动的浮层承载源端对话框时
  - 情境：源 Activity 未声明 android:configChanges 且未锁定 screenOrientation（旋转、语言、深浅色等都会重建它），页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框，不经 DialogFragment、showDialog 或 DialogPreference；目标用页内状态驱动的浮层承载该对话框，HarmonyOS 页面在旋转等配置变化时不重建。页面只有静态列表与弹窗、没有动态文案时同样适用。
  - 例外：对话框经 DialogFragment、Activity.showDialog 或 DialogPreference 托管时，源端重建后会恢复，目标保持浮层显示；源 Activity 在 configChanges 中声明了 orientation、screenSize 等并自行处理时，按其处理代码迁移
- [源 Activity 的 configChanges 未覆盖某项配置（只写 screenSize 时包括旋转）时，目标按源端重建时序刷新资源文案与一次性状态](lesson-94715d0df4c03a8fb5a5.lesson.md)
  - 时机：规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期与资源文案、一次性状态的缓存时
  - 情境：源 Activity 在 AndroidManifest 中未声明 android:configChanges，或声明里缺 locale、uiMode、fontScale、density、orientation 等项（只写 screenSize 时旋转同样重建），实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态，或在监听器里用 setBackgroundResource 一类调用改了视图属性；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化与旋转时不重建，只回调 onConfigurationUpdate、发出 display 'change' 或改变窗口尺寸。
  - 例外：源 Activity 已在 configChanges 中声明对应项、在 onConfigurationChanged 自行处理时（ActivityInfo.configChanges：声明的项由 Activity 自行处理、不重建），按其处理代码迁移；边界：直接 show() 的非托管对话框在配置变化时的关闭路径见非托管对话框一条；深浅色切换中的命令式取色、系统栏与画布重解析按应用内主题切换的经验；跟随系统字号的 configuration 声明按大字体裁定的经验；SurfaceView 自建渲染线程在重建时的结果见 lesson-25731279fbe14dcecc69
- [源端按 getLastNonConfigurationInstance 是否为空决定是否读启动参数时，目标按“是否配置变化重建”区分](lesson-ed571550c44efdeb321e.lesson.md)
  - 时机：规格提取与页面实现阶段，翻译源 Activity.onCreate 中“取回保留实例为空才读启动参数”的建局或建状态逻辑时
  - 情境：源 Activity 未声明 configChanges，用 onRetain(Custom)NonConfigurationInstance 与 getLast(Custom)NonConfigurationInstance 跨配置变化保留对象，该对象可能同时是静态单例（只在退出时 destroy）；目标页面不因配置变化重建，单例跨页面常驻，同一页面有多个入口模式（如新开与续局）。
- [源端返回栈靠框架在进程回收后重建时，规格单列“回收后重建”分支，目标开启 UIAbility 恢复与 Navigation recoverable](lesson-b0405a29415547485ecb.lesson.md)
  - 时机：规格提取阶段为宿主 Activity 生命周期与导航容器编写验收项、为“进程回收后重建”铸平台差异决策时；入口装配阶段实现 UIAbility 与根 Navigation 的恢复路由时
  - 情境：源 Activity 在 onCreate(savedInstanceState) 接收存档，或用 Compose rememberNavController + NavHost 承载页面，源码里没有显式保存代码，进程在后台被系统回收后返回栈与路由参数由框架恢复。也包括 View 体系的 Activity 任务栈（TaskStackBuilder 建出 \[主页, X\]、页面参数来自 Intent extra）：进程被系统回收而任务仍在时框架重建整栈，重建页拿原始 Intent。目标为 UIAbility + Navigation/NavDestination + NavPathStack，页面栈恢复默认不开启；规格可能只写“冷启进入起始页”，或把回收重入合并进每次冷启动。
  - 例外：源 Manifest 给相关 Activity 设了 clearTaskOnLaunch、finishOnTaskLaunch 或 noHistory 时，重回任务不会恢复这些页面，按这些属性迁移
- [源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封装后，在入口 onCreate 最早处调用，并确认启动期读写都晚于初始化](lesson-8a881c2e07f80f83447c.lesson.md)
  - 时机：网络、键值存储等基础设施实现与入口接线阶段：新建必须先 init 才能用的封装，或改写 EntryAbility.onCreate、宣告基础层完成时
  - 情境：源端网络 baseUrl 由 DI 模块在注入时带上（Application.onCreate 里没有网络初始化调用），键值工具（SpUtils/MMKV 一类）在读写处全局静态可用；目标端改为静态网络客户端（baseUrl 默认空串）加需显式调用的网络初始化入口、偏好封装需先传入上下文；入口 Ability 由编排会话维护，Flutter 插件 onAttachedToEngine 等回调里也能拿到上下文。也包括网络层以静态运行期配置承接构建期注入值（configure 写入、未配置即 throw），基础模块不得改入口，启动接线者不知道这条调用义务。
- [源端首帧前按偏好设主题时，入口 onCreate 同步读偏好并在 loadContent 前 setColorMode，不用不等待的异步恢复](lesson-dcb3c5e66dec2d126234.lesson.md)
  - 时机：入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时
  - 情境：源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。
- [裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号](lesson-ea965b7baf2488be23cd.lesson.md)
  - 时机：规格的横切能力裁定阶段（i18n、深色、大字体、无障碍）判断系统字号缩放是否迁移时；派发应用身份或应用外壳任务、落定 AppScope/app.json5 的 configuration 时
  - 情境：源应用主体可能是固定 px 字号的 Canvas 自绘，但仍有系统 AlertDialog、Toast、菜单或 sp 单位文本；Activity 是否在 configChanges 声明 fontScale 决定字号变化时重建还是回调；目标 HarmonyOS 应用默认不跟随系统字号（nonFollowSystem），需在 AppScope 配置 configuration profile 才会跟随并下发配置变化。
- [迁移深链 intent-filter 时同时声明 module.json5 的 skills，并用隐式 Want 验收](lesson-d77baa7494930d485425.lesson.md)
  - 时机：入口与导航接线阶段，把源端 Activity 的 VIEW/BROWSABLE intent-filter 迁成 UIAbility 的 Want 接收与路由解析时；以及规格提取阶段描述深链映射时
  - 情境：源 AndroidManifest 在启动 Activity 上声明 VIEW+BROWSABLE、http/https 与固定 host 的 intent-filter；目标 module.json5 的入口 Ability skills 仍是脚手架默认的 HOME 一项。 也包括 intent-filter 带 android:autoVerify="true"（App Links），或决策写明 https 由域名校验的 App Linking 承载。也包括导航图 navDeepLink 的 uriPattern 或分享/复制链接由常量拼接（如 "$baseUrl/item/{id}"），深链规格的源码锚点没有列入 AndroidManifest。
- [验收或任务明确要求全局未捕获异常观察、且规格没有保留源端崩溃退出时，在入口 Ability 注册 errorManager 观察器](lesson-c6132bf52c26ec226788.lesson.md)
  - 时机：入口装配阶段，改写 EntryAbility（或 AbilityStage）的 onCreate/onDestroy，且本次验收或任务要求存在全局异常观察时
  - 情境：目标为 HarmonyOS Stage 模型应用，入口 UIAbility 由模板改写而来；Android 源没有可对照的全局异常处理，按源码迁移不会产生这段代码，而本次验收（如 ECAT crash_risk 规则）或任务明确要求存在全局异常观察。“任务明确要求”只认验收规则或用户需求原文；规格、plan、派工里引用本经验而来的条目不算独立要求。
  - 例外：本次任务与验收都没有全局异常观察要求：按源码迁移，不默认新增观察器；规格保留了源端未捕获异常导致的崩溃退出（照源复刻的缺陷或崩溃验收项）：不注册；验收又同时要求全局异常观察时，作为差异决策登记，写明这些崩溃路径在目标端的结果；工程已在 AbilityStage 或其他入口注册了 errorManager 观察器或等效的崩溃监听
