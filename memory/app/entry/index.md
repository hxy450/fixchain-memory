# app/entry

入口 Ability 与应用级配置：onCreate/onDestroy 中基础设施的显式初始化时机、需要补上的平台级守护，系统配置变化（源 Activity 未声明 configChanges 时的重建语义，含旋转、非托管对话框与 NonConfigurationInstance 取回）在 onConfigurationUpdate 与页面中的承接与跟随系统字号的 configuration，以及 module.json5 中入口 Ability 的 skills（深链、App Links 的 domainVerify）声明、桌面快捷方式（shortcuts）声明与外部 Want 的入口分支；冷启动首帧前按偏好同步恢复主题的时机；进程回收后页面栈恢复（setRestoreEnabled、restoreWindowStage、recoverable）；AndroidManifest 各 intent-filter 到 skills 的逐条映射与入口载荷键；System.exit 式重启迁为 restartApp 并携带界面状态

[上一级](../index.md)

## 本级经验

- [System.exit/killProcess 式“重启”迁为 ApplicationContext.restartApp，并携带系统原本重建的界面状态](lesson-0880ecd4fe9a29885ba7.lesson.md)
  - 时机：规格提取与入口实现阶段，为源端进程退出类调用（System.exit、Runtime.exit、Process.killProcess）确定目标行为与状态保留要求时
  - 情境：源方法注释或调用点表明意图是重启（语言切换、数据恢复或重置后、导入完成通知点击），实现只有 System.exit(0)；源前台进程被杀后，Android 按残留任务栈重建 Activity 并交回 savedInstanceState（抽屉开合、列表位置、搜索条件等）；目标在 UIAbility.terminateSelf 与 ApplicationContext.restartApp 之间选择。
- [intent-filter 逐条映射为 module.json5 skills：有对应 action 的不合并，载荷键不自造，源端没有的不加](lesson-a23ad0b53c75e49ca117.lesson.md)
  - 时机：规格提取阶段把 AndroidManifest 的 intent-filter 与入口 Intent 载荷翻成 module.json5 skills 与 Want 参数契约时；接线阶段按笔记或 skill 参考给出的片段修改 skills 时
  - 情境：源 Activity 声明多条 intent-filter（SEARCH、VIEW 自定义 scheme、SEND/SEND_MULTIPLE */*、PROCESS_TEXT 等），入口分发读取 Intent.EXTRA_* 键，并可能在初始化或验密门之后才处理 Intent；目标为 UIAbility 的 module.json5 skills（actions、entities、uris，分享目标需 utd 与 maxFileSupported）与 Want parameters、systemShare 载荷；skill 参考或交接笔记可能给出“调用某系统能力须声明某 skill”的片段。
- [ohos.ability.shortcuts 挂在承载快捷方式的 UIAbility 的 metadata 下，不追加到 module 级 metadata](lesson-67118603fcc769a5edc9.lesson.md)
  - 时机：配置实现阶段，在 module.json5 中挂载桌面长按快捷菜单（ohos.ability.shortcuts）时；构建后长按不出菜单或快捷方式条目变少时；编译门报 module.json5 schema 不允许某字段时
  - 情境：把 Android App Shortcuts 迁为 HarmonyOS 静态快捷方式：在 resources/base/profile 下新建快捷方式配置，并在 module.json5 中用 metadata 引用；module 级已有 metadata 数组（如 client_id），入口 UIAbility 还没有 metadata。 也包括规格或笔记凭记忆给出 module 级 shortcuts 数组，构建 schema 报 propertyName shortcuts 不允许，编译门准备删掉整块并记缺口。
- [只经桌面快捷方式或通知点击进入的页面：module.json5 快捷方式声明、EntryAbility 的 Want 分支与目标页参数都要有确定写者](lesson-c46f182cf1d01a97e05f.lesson.md)
  - 时机：规格拆分、切片实现与入口接线阶段，迁移源端只由外部 Intent（桌面快捷方式、本地通知点击）进入的页面时
  - 情境：源端页面由静态或动态 shortcut、通知 PendingIntent 携带 extras（如 shortId、通知渠道）进入；目标规格把入口配置定为 module.json5 静态声明；页面与切片 worker 的写域不含 module.json5 和 EntryAbility。
- [深链 intent-filter 迁移时声明 module.json5 skills（App Links 加 domainVerify），用隐式 Want 验收](lesson-d77baa7494930d485425.lesson.md)
  - 时机：入口与导航接线阶段，把源端 Activity 的 VIEW/BROWSABLE intent-filter 迁成 UIAbility 的 Want 接收与路由解析时；以及规格提取阶段描述深链映射时
  - 情境：源 AndroidManifest 在启动 Activity 上声明 VIEW+BROWSABLE、http/https 与固定 host 的 intent-filter；目标 module.json5 的入口 Ability skills 仍是脚手架默认的 HOME 一项。 也包括 intent-filter 带 android:autoVerify="true"（App Links），或决策写明 https 由域名校验的 App Linking 承载。也包括导航图 navDeepLink 的 uriPattern 或分享/复制链接由常量拼接（如 "$baseUrl/item/{id}"），深链规格的源码锚点没有列入 AndroidManifest。也包括 scheme 常量定义在外部库里、仓库内看不到取值。
- [源 Activity 未声明 configChanges 时，旋转（未被 screenOrientation 锁定）、语言、深浅色、字号、显示大小变化都会重建它：目标 UIAbility 与页面不重建，逐页按源端重建时序显式处理——直接 show() 的非托管对话框关闭、托管对话框以新实例重显（setter 注入的监听与参数丢失）、文案与一次性状态刷新、新实例 onCreate/onResume 的可见效果重放；configChanges 不含 orientation 时旋转同样重建](lesson-94715d0df4c03a8fb5a5.lesson.md)
  - 时机：规格提取阶段把 Activity 生命周期回调与 Manifest 属性映射为目标生命周期契约时；实现阶段接线 UIAbility、页面生命周期，以及资源文案与一次性状态的缓存时；为只有静态列表与弹窗的页面写配置变化行为时；配置变化重放里或启动链上调用设置应用语言等会改动配置的接口时
  - 情境：源 Activity 在 AndroidManifest 中未声明 android:configChanges，实现了 onSaveInstanceState/savedInstanceState 恢复分支，或在 View 构造、onSizeChanged、绘制时读取资源文案与 firstRun 等一次性状态；目标 HarmonyOS UIAbility 在语言、深浅色、字号、显示大小变化时不重建，只回调 onConfigurationUpdate 或发出 display 'change'。 也包括页面用 AlertDialog.Builder.show()/Dialog.show() 直接弹出非托管对话框（不经 DialogFragment、showDialog 或 DialogPreference），目标用页内状态驱动的浮层承载，页面没有动态文案。 也包括 configChanges 已声明但不含 orientation（如只写 screenSize），Activity 持有 SurfaceView 与自建渲染线程，监听器里用 setBackgroundResource/setImageResource 等代码设置界面状态。 也包括源界面由 Compose setContent 承载：重建时整棵组合重新进入，组合内的 remember 与副作用随之重跑。
- [源 Activity 的 SEND 分享接收入口（standard 启动、无 onNewIntent）映射为独立 multiton Ability：skills 用 sendData 加 utd 声明，结束只 terminateSelf 本实例](lesson-51651155ed8226212e55.lesson.md)
  - 时机：规格提取与入口配置阶段，把源端 ACTION_SEND/SEND_MULTIPLE 接收入口映射为目标 Ability 的实例形态、module.json5 skills 声明与结束范围时；接线阶段给入口 Ability 加分享解析或结束逻辑时
  - 情境：源 AndroidManifest 在某 Activity（常是 LAUNCHER）上另有 SEND + DEFAULT + mimeType（如 text/plain）的 intent-filter，未声明 singleTop/singleTask/singleInstance，源码没有 onNewIntent，只在 onCreate 读 EXTRA_TEXT 等处理，结束时 finish()。目标工程只有入口 EntryAbility（launchType 默认 singleton），外部数据经系统分享面板送达，接收方用 systemShare.getSharedData 读取。
  - 例外：源 Activity 声明 singleTop/singleTask/singleInstance 或实现 onNewIntent 承接分享：按源端复用实例的语义映射到已有 Ability 的 onNewWant
- [源端“getLast(Custom)NonConfigurationInstance 为空才按启动参数建立状态”只在配置变化重建时取回实例：目标按“本次是否由配置变化重建”区分，正常进入一律按入口参数分支，不用单例是否存在代替](lesson-ed571550c44efdeb321e.lesson.md)
  - 时机：规格提取与页面实现阶段，翻译源 Activity.onCreate 中“取回保留实例为空才读启动参数”的建局或建状态逻辑时
  - 情境：源 Activity 未声明 configChanges，用 onRetain(Custom)NonConfigurationInstance 与 getLast(Custom)NonConfigurationInstance 跨配置变化保留对象，该对象可能同时是静态单例（只在退出时 destroy）；目标页面不因配置变化重建，单例跨页面常驻，同一页面有多个入口模式（如新开与续局）。
- [源端在入口 onCreate 首帧前按偏好设主题时，目标在 EntryAbility.onCreate 同步读取偏好并在 loadContent 前 setColorMode；恢复函数返回 Promise 而调用方不等待，就是首帧后才生效](lesson-dcb3c5e66dec2d126234.lesson.md)
  - 时机：入口与应用级配置阶段，规格提取或实现冷启动时应用持久化外观设置（深浅色等）的时机，并为启动恢复写移交或接线时
  - 情境：源入口 Activity 在 onCreate 首行（super.onCreate 之前）按 SharedPreferences 同步设置 DayNight 主题；目标 ApplicationContext.setColorMode 是进程态，偏好仓库只提供异步 init；功能规格只写“保存后即时生效”，没有冷启动恢复要求；恢复函数由一个任务写成 async，并以 HANDOFF 交给入口接线者调用。
- [源端返回栈靠框架在进程回收后重建（rememberNavController、savedInstanceState、Activity 任务栈）时，规格单列“回收后重建”分支：只在系统回收后恢复整栈并保留各页原参数，强停、划掉、覆盖安装后按冷启分流；目标显式开启 UIAbility 恢复与 Navigation recoverable](lesson-b0405a29415547485ecb.lesson.md)
  - 时机：规格提取阶段为宿主 Activity 生命周期与导航容器编写验收项、为“进程回收后重建”铸平台差异决策时；入口装配阶段实现 UIAbility 与根 Navigation 的恢复路由时
  - 情境：源 Activity 在 onCreate(savedInstanceState) 接收存档，或用 Compose rememberNavController + NavHost（以及 Fragment 返回栈）承载页面；源码里没有显式保存代码，进程在后台被系统回收后，返回栈与路由参数由框架恢复。也包括 View 体系的 Activity 任务栈（TaskStackBuilder 建出 \[主页, X\]、页面参数来自 Intent extra）：只有进程被系统回收而任务仍在时框架才重建整栈，重建页拿原始 Intent；强停、从最近任务划掉、覆盖安装、崩溃后任务已清空，再启动走启动页分流。目标为 UIAbility + Navigation/NavDestination + NavPathStack，页面栈恢复默认不开启；规格可能只写“冷启进入起始页”，或把回收重入合并进每次冷启动。
- [源端靠依赖注入或全局静态工具就绪的基础设施改成需显式 init 的封装后，在入口 onCreate 最早处调用，并确认启动期读写都晚于初始化](lesson-8a881c2e07f80f83447c.lesson.md)
  - 时机：网络、键值存储等基础设施实现与入口接线阶段：新建必须先 init 才能用的封装，或改写 EntryAbility.onCreate、宣告基础层完成时
  - 情境：源端网络 baseUrl 由 DI 模块在注入时带上、键值工具（SpUtils/MMKV 一类）全局静态可用，Application.onCreate 里看不到对应的初始化；目标端改为静态 HttpClient（baseUrl 默认空串）加 NetworkConfig.init()、偏好封装需先传入上下文；入口 Ability 由编排会话维护，Flutter 插件 onAttachedToEngine 等回调里也能拿到上下文。也包括网络层以静态运行期配置承接构建期注入值（configure 写入、未配置即 throw），基础模块不得改入口，启动接线者不知道这条调用义务。也包括源端数据层每次读写都无条件调用的能力（加解密等），目标由基座在 DAO 留 setter 注入接缝并配恒等或空实现默认值，实现由后续切片注入。
- [裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号](lesson-ea965b7baf2488be23cd.lesson.md)
  - 时机：规格的横切能力裁定阶段（i18n、深色、大字体、无障碍）判断系统字号缩放是否迁移时；派发应用身份或应用外壳任务、落定 AppScope/app.json5 的 configuration 时
  - 情境：源应用主体可能是固定 px 字号的 Canvas 自绘，但仍有系统 AlertDialog、Toast、菜单或 sp 单位文本；Activity 是否在 configChanges 声明 fontScale 决定字号变化时重建还是回调；目标 HarmonyOS 应用默认不跟随系统字号（nonFollowSystem），需在 AppScope 配置 configuration profile 才会跟随并下发配置变化。
