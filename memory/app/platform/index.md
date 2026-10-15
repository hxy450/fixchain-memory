# app/platform

系统平台能力（后台任务与扩展能力承载类、module.json5 extensionAbilities 的 type 登记，通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载，打开系统设置的显式 Want）的实现、替代与降级，激励广告等能力门禁在能力不可用时的入口放行，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理，读当前系统值再增量写回的手势（亮度）读写映射，OAID 采集的跟踪授权；权限清单按已映射 API 在 d.ts 中的 @permission 汇总；画中画到 PiPWindow、动态取色到 wallpaper 的映射，后台计时与进度通知的降级边界，通知按钮 WantAgent 的 requestCode 与正文非空

[上一级](../index.md)

## 本级经验

- [Android 依赖厂商 SDK（地图、登录、支付、账号）时，先查鸿蒙系统 Kit 与厂商 ohpm 包再定依赖，查证前不写“鸿蒙无等价”](lesson-e9890889e591196c3d0d.lesson.md)
  - 时机：规格提取与迁移规划阶段，为三方 SDK 作依赖决策、判断是否“鸿蒙无等价”、为对应切片绑定 SDK 文档类 skill 时；实现阶段遇到规格要求的 SDK 能力而工程里还没有 SDK，或接入已决策的厂商 SDK（地图承载、Key 缺失时的行为）时
  - 情境：Android 工程直接依赖厂商 SDK（com.amap.api.* 一类），功能规格与接口清单写明这些能力；项目 skill 映射表把该厂商列为 SDK 文档查询类 skill 的典型对象；用户在决策问答中没有提供鸿蒙 SDK 资料。也包括被规格或决策表与其他三方 SDK 并列为占位候选的能力：微信 OpenSDK 登录与支付（ohpm 有 @tencent/wechat_open_sdk，skill 映射表已把它们绑定到登录、支付 skill）、华为账号（系统 @kit.AccountKit 提供）。也包括源端 MapView 等地图视图，决策要求以平台地图能力或厂商鸿蒙 SDK 真实承载，Key、client_id 等配置尚未提供。
  - 例外：已查明厂商没有鸿蒙版本，且决策记录写明了替代方案与理由
- [写目标权限清单时按已映射 API 在 d.ts 中的 @permission 汇总，并按权限级别选申请方式，不因 Android 无需权限就断言为空](lesson-652974ce64a9243faebc.lesson.md)
  - 时机：规格提取（权限契约）、实现与构建收口阶段，确定 module.json5 的 requestPermissions 与运行期申请时
  - 情境：源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。
- [决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记](lesson-efb94f2d70d4df1c65d7.lesson.md)
  - 时机：实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色等）或解决指向平台切片的前向占位，而决策账本对该能力批准的是等价实现、可验证承载或应用内回退时
  - 情境：源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色等平台能力；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期；接手者可能认定“没有对应 API”，或把“禁止伪造进度”理解为可以不实现。
  - 例外：决策账本对该能力明确批准的是延期或仅前台实现
- [前台服务改用扩展能力承载前先确认三方应用能在目标设备启动它；type 与基类成对，backgroundModes 只写在 UIAbility](lesson-16c24b9a44153d703f04.lesson.md)
  - 时机：后台服务迁移的规格、实现与编译/安装修复阶段，为源端 Foreground Service 选择承载类并在 module.json5 登记扩展能力时；因编译错误更换扩展基类时
  - 情境：源端以 Service/LifecycleService 加 startForeground 承载长任务；目标准备用扩展能力类（如 AppServiceExtensionAbility）承载并在 module.json5 extensionAbilities 注册；规格、决策或文件头注释凭经验写了 ServiceExtensionAbility、type=service 或 backgroundModes，工程可能还不能编译。
  - 例外：目标改用 UIAbility 加长时任务（backgroundTaskManager.startBackgroundRunning）承载时，只在 abilities\[\] 的 UIAbility 声明 backgroundModes 与 ohos.permission.KEEP_BACKGROUND_RUNNING，不注册扩展能力
- [后台 Worker 计时与带动作的进度通知迁到 HarmonyOS 时，降级只覆盖确实不可用的执行载体：保活窗口内保留逐拍刷新，挂起后交代理提醒](lesson-30643cd3f209b896ffd1.lesson.md)
  - 时机：规格提取与决策阶段，为源端后台计时任务（WorkManager Worker、前台服务）及其进度通知、通知按钮制定替代路径、差异验收与平台差异决策时；实现阶段按这类决策写计时服务与通知时
  - 情境：源端 Worker 逐拍刷新进度通知，在后台跨步推进（计时步结束续下一步、需输入步停住、末步发完成通知），通知按钮经 PendingIntent.getBroadcast 交给后台处理、不拉起应用。目标为第三方应用，退后台会被挂起；规格准备写成“退后台停摆 + 单条静态常驻通知 + 按钮拉起应用 + 回前台从剩余时长续跑”，并以“平台无对等”为由不查 SDK。
- [应用内计时替代后台 Worker 时恢复计时会话：会话落盘、锚点用单调时钟并判断重启，所有恢复入口共用逐步扣减函数](lesson-35a684862ee500f08912.lesson.md)
  - 时机：规格与实现阶段，为替代后台 Worker 的应用内计时编写持久化恢复、回前台补算与后台 tick 时
  - 情境：源端由后台 Worker 跨步骤推进计时（计时步结束续下一步、需输入步停住、末步完成），偏移以 SystemClock.elapsedRealtime 计，任务经 WorkManager 持久化，回前台读取 Worker 已推进到的步骤；目标改为应用内计时（配短时或长时任务），恢复要自己写，会话可能只放在 AppStorageV2 等进程内状态，或只把停机时长加到当前步。
  - 例外：源端计时只在前台运行、退后台即暂停，没有后台推进与持久化
- [开关控制的常驻通知由应用级服务订阅与发布，不绑在页面 ViewModel 的激活周期上](lesson-e9f03fcc7f1e781c4b24.lesson.md)
  - 时机：系统能力迁移阶段（规格提取与服务、ViewModel 实现），为由开关控制、由后台事件驱动的常驻通知确定订阅归属与生命周期时
  - 情境：源端在页面初始化时注册一次事件监听且不注销，回调在开关为真时用固定 ID 更新 ongoing 通知；二级页的监听随页面注销且不发通知。目标主壳以条件渲染承载 Tab，或页面在 NavDestination 中出栈，页面 ViewModel 在 aboutToAppear/aboutToDisappear 激活、释放订阅。
- [打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设备核对，直达子页带该页参数，启动失败要可观察](lesson-4bea916d1ff67e51d455.lesson.md)
  - 时机：系统能力实现阶段，为“打开系统设置/应用权限页”编写 startAbility 显式 Want（bundleName/abilityName）时；维护迁移 skill 参考中的系统应用包名时
  - 情境：源端经 Settings.ACTION_* 一类 Intent 跳转系统设置（全部文件访问、应用详情等）；目标为 HarmonyOS NEXT 应用，需要以显式 Want 指定系统设置应用，规格与源码都不给目标包名，可查到的参考文档给出硬编码的厂商设置包名并标注已验证。
- [接入 identifier.getOAID 时同批声明 APP_TRACKING_CONSENT 并在隐私同意后申请；全零串按未授权处理](lesson-2b00c4ffaeb442d87e5e.lesson.md)
  - 时机：服务层实现阶段，把源端 OAID（MSA 或厂商通道）采集迁到鸿蒙 identifier.getOAID 时
  - 情境：源端经 MSA SDK 或厂商通道采集 OAID，写缓存、上送归因并发布就绪事件；鸿蒙 identifier.getOAID 需要 user_grant 权限 ohos.permission.APP_TRACKING_CONSENT，未授权时返回全零串；Android 端没有对应的运行期授权。
- [源端 Activity 画中画映射到 @ohos.PiPWindow：可用性用 isPiPEnabled，自动进入用 setAutoStartEnabled，画中画状态由 PiPController 的 stateChange 驱动](lesson-a45be20055d942e12052.lesson.md)
  - 时机：规格提取与实现阶段，迁移源端画中画（PictureInPictureParams 自动进入、onUserLeaveHint、onPictureInPictureModeChanged、画中画精简 UI 与设置开关）时
  - 情境：源 Activity 设置 PictureInPictureParams 或在 onUserLeaveHint 进入画中画，按 onPictureInPictureModeChanged 在完整 UI 与精简 UI 间切换；设置页有画中画开关，并检查系统是否允许。目标为 HarmonyOS 手机应用，项目 SDK 含 @ohos.PiPWindow.d.ts。
  - 例外：项目 compatibleSdkVersion 低于项目 SDK 中 PiPWindow 相关接口的 @since；决策已批准应用内替代（如应用内紧凑模式），此时按决策实现并登记差异
- [源端 Material You 动态取色迁到 HarmonyOS 时，用已弃用的 wallpaper.getColors 取种子并回退固定配色，决策写明风险](lesson-9769c8f754044944d3ad.lesson.md)
  - 时机：规格决策与主题层实现阶段，迁移源端 dynamicLightColorScheme/dynamicDarkColorScheme（Android 12+ 才启用、否则回退固定配色）与“动态配色”设置项时
  - 情境：源主题在 SDK_INT &gt;= S 且设置开启时使用壁纸取色配色，否则用固定的 light/dark scheme；设置页有动态配色开关。目标公开 SDK 的 @ohos.wallpaper（@kit.BasicServicesKit 导出）提供 getColors(WallpaperType) 与 on('colorChange')，两者都自 API 9 标记弃用，替代接口不在公开 SDK 中。
  - 例外：审批在“降级为固定配色”与“弃用接口 + 回退”之间选了前者，此时设置项按决策呈现并登记差异
- [源端“先读当前系统值、再按位移增量写回”的手势（如亮度）分别映射读写两侧；异步读取在页面就绪时预读基线](lesson-33791daf74fc4298779e.lesson.md)
  - 时机：界面实现阶段，把源端按下时读取窗口亮度等系统值、移动时按增量写回的手势迁到鸿蒙时
  - 情境：源端手势在 ACTION_DOWN 读取窗口当前亮度，未覆写时回退系统亮度设置，移动时按位移增量写回窗口；规格只给出写入接口（setWindowBrightness），读取侧要实现者确定。
- [源端多个通知动作按钮迁到 WantAgent 时，按处理方选 operationType，每个按钮、每次构建用不同 requestCode](lesson-716d06e75b7c2102c36c.lesson.md)
  - 时机：实现阶段，把源端通知的多个 PendingIntent 动作按钮映射为 wantAgent.getWantAgent 时
  - 情境：源端通知按钮经 PendingIntent.getBroadcast（交给后台处理、不拉起应用）或 getActivity 发出，每次构建通知都给按钮取不同的 requestCode（如逐次取 elapsedRealtime），按钮 Intent 载荷随运行状态变化；目标用 WantAgentInfo（wants、operationType、requestCode、wantAgentFlags）。
- [源端通知构造迁到 NotificationRequest 时，按源端构造代码逐字段映射正文与渠道；可空正文不直接给空串](lesson-a7149a05c8f8e06c9f27.lesson.md)
  - 时机：实现阶段，把源端 NotificationCompat.Builder 的正文、标题、进度与通知渠道映射为 NotificationRequest 与通知槽时
  - 情境：源端在构造通知的函数里拼接正文（如进度、数量与步骤时长）、创建具名通知渠道（NotificationChannel，含重要度），部分通知（完成通知、没有文本的步骤）的 setContentText 为 null；目标用 NotificationBasicContent（title、text）与通知槽发布，实现者为展示自定义了快照字段。
- [源端靠窗口销毁或会话结束自动解除的常亮、安全标志与画中画态，迁到共享主窗口或应用自管状态后按拥有者成对复位](lesson-ea9a6cfecca9e091c7ea.lesson.md)
  - 时机：规格提取与页面实现阶段，把 Activity 窗口标志、WakeLock 或画中画映射为鸿蒙窗口 API 与应用内状态并写验收时；实现计时等会话的后台交接、完成与停止路径时
  - 情境：源端某个 Activity 在 onCreate 给 getWindow() 加标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）且没有清除代码，靠该 Activity 不可见或 finish 时随窗口失效；或计时等会话持有 WakeLock、进入系统画中画，随会话结束或退出画中画由系统复位。目标各页以 Navigation/NavDestination 共用一个主窗口，用 setWindowKeepScreenOn、setWindowPrivacyMode 等窗口级 API，或用应用内紧凑模式代替画中画，复位要自己写。
  - 例外：源端已在 onPause/onStop 或会话结束处显式 clearFlags、release 时，按其代码位置映射
- [激励广告等能力门禁挡在核心功能入口前时，区分“用户未获奖励”与“广告能力不可用”：不可用时显式提示并按台账放行，不伪造奖励](lesson-0f67121af7969203b76b.lesson.md)
  - 时机：规格、巡检出单与接线实现阶段，为“先看激励广告、奖励回调后才导航”的入口确定各广告结果的去向时
  - 情境：源端功能入口先调起激励视频，仅在 onReward 回调后导航；目标端没有等价广告 SDK 或广告 provider 未装配，showRewarded 一类接口恒返回 unavailable；决策台账同时要求“能力不可用时显式失败、不伪造 SDK 成功”和核心功能流程真实可用，且没有对这些入口批准“不可用即阻断”。
  - 例外：台账对该入口明确批准“仅获得奖励才可继续”（如只对奖励用户开放的增值功能），此时按该决策阻断，并显示不可用原因
