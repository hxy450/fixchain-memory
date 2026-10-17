# app/platform

系统平台能力（后台任务与扩展能力承载类、module.json5 extensionAbilities 的 type 登记，通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载，打开系统设置的显式 Want）的实现、替代与降级，激励广告等能力门禁在能力不可用时的入口放行，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理，读当前系统值再增量写回的手势（亮度）读写映射，OAID 采集的跟踪授权；权限清单按已映射 API 在 d.ts 中的 @permission 汇总；画中画到 PiPWindow、动态取色到 wallpaper 的映射，后台计时与进度通知的降级边界，通知按钮 WantAgent 的 requestCode 与正文非空

[上一级](../index.md)

## 本级经验

- [Android 依赖厂商 SDK（地图、登录、支付、账号等）时，先查鸿蒙系统 Kit 与厂商 ohpm 包，再在 Kit、厂商包、H5 与受控降级之间取舍；查证前不写“鸿蒙无等价”](lesson-e9890889e591196c3d0d.lesson.md)
  - 时机：规格提取与迁移规划阶段，为三方 SDK 作依赖决策、判断是否“鸿蒙无等价”、为对应切片绑定 SDK 文档类 skill 时；实现阶段遇到规格要求的 SDK 能力而工程里还没有 SDK 时
  - 情境：Android 工程直接依赖厂商 SDK（com.amap.api.* 一类），功能规格与接口清单写明这些能力；项目 skill 映射表把该厂商列为 SDK 文档查询类 skill 的典型对象；用户在决策问答中没有提供鸿蒙 SDK 资料，只回复“采用建议”。也包括微信 OpenSDK 登录与支付（ohpm 有 @tencent/wechat_open_sdk）、华为账号（系统 @kit.AccountKit 提供）这类被规格或决策表与其他三方 SDK 并列为占位候选的能力，而 skill 映射表已把它们绑定到登录、支付 skill。
  - 例外：已查明厂商没有鸿蒙版本，且决策记录写明了替代方案与理由
- [Android 前台服务改用扩展能力承载时，先在项目 SDK 确认基类导出；module.json5 extensionAbilities 的 type 与基类成对，backgroundModes 只写在 UIAbility](lesson-16c24b9a44153d703f04.lesson.md)
  - 时机：后台服务迁移的规格、实现与编译/安装修复阶段，为源端 Foreground Service 选择承载类并在 module.json5 登记扩展能力时；因编译错误更换扩展基类时
  - 情境：源端以 Service/LifecycleService 加 startForeground 承载长任务；目标准备用扩展能力类承载并在 module.json5 extensionAbilities 注册；规格、决策或文件头注释凭经验写了 ServiceExtensionAbility、type=service 或 backgroundModes，生成批次可能不能编译。
- [写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空](lesson-652974ce64a9243faebc.lesson.md)
  - 时机：规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时
  - 情境：源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。
- [决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记](lesson-efb94f2d70d4df1c65d7.lesson.md)
  - 时机：实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色、地图承载等）或解决指向平台切片的前向占位时
  - 情境：源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色，或用第三方地图 SDK 的 MapView 显示当前位置与轨迹；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期。也包括规格把地图、POI 与导航列为核心功能并要求经能力适配层隔离，台账只批准了认证、广告、微信等少数能力的不可用降级，厂商 SDK 的 Key 尚未提供，计划汇总行却写“地图执行已批准不可用 UX”。
  - 例外：决策账本对该能力明确批准的是延期或仅前台实现
- [后台 Worker 计时与带动作的进度通知迁到 HarmonyOS 时，降级只覆盖做不到的执行载体：保活窗口内保留逐拍刷新与静默按钮，挂起后交代理提醒，回前台按步骤表补算并持久化会话](lesson-30643cd3f209b896ffd1.lesson.md)
  - 时机：规格提取与决策阶段，为源端后台计时任务（WorkManager Worker、前台服务）及其进度通知、通知按钮制定替代路径、差异验收与平台差异决策时；实现阶段按这类决策写计时会话与通知时
  - 情境：源端 Worker 逐拍刷新进度通知，在后台跨步推进：计时步结束续下一步，需输入步停住，末步发完成通知。偏移以 elapsedRealtime 计，任务经 WorkManager 持久化，回前台读取进度。通知按钮经 PendingIntent.getBroadcast 交给后台处理，不拉起应用。目标为第三方应用，退后台后会被挂起；规格准备写成“退后台停摆 + 单条静态常驻通知 + 按钮拉起应用 + 回前台从剩余时长续跑”，会话只放进程内状态。
- [开关控制的常驻通知由应用级服务订阅与发布，不绑在页面 ViewModel 的激活周期上](lesson-e9f03fcc7f1e781c4b24.lesson.md)
  - 时机：系统能力迁移阶段（规格提取与服务、ViewModel 实现），为由开关控制、由后台事件驱动的常驻通知确定订阅归属与生命周期时
  - 情境：源端在页面初始化时注册一次事件监听且不注销，回调在开关为真时用固定 ID 更新 ongoing 通知；二级页的监听随页面注销且不发通知。目标主壳以条件渲染承载 Tab，或页面在 NavDestination 中出栈，页面 ViewModel 在 aboutToAppear/aboutToDisappear 激活、释放订阅。
- [打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设备核对，启动失败要可观察，不照抄参考里标“已验证”的值](lesson-4bea916d1ff67e51d455.lesson.md)
  - 时机：系统能力实现阶段，为“打开系统设置/应用权限页”编写 startAbility 显式 Want（bundleName/abilityName）时；维护迁移 skill 参考中的系统应用包名时
  - 情境：源端经 Settings.ACTION_* 一类 Intent 跳转系统设置（全部文件访问、应用详情等）；目标为 HarmonyOS NEXT 应用，需要以显式 Want 指定系统设置应用，规格与源码都不给目标包名，可查到的参考文档给出硬编码的厂商设置包名并标注已验证。
- [拉起外部应用或系统能力前的可用性与权限门控逐段落实：隐式 Want 先 canOpenLink，不靠 startAbility 抛错](lesson-948d876672049969b865.lesson.md)
  - 时机：实现阶段把 IntentChecker.isAvailable、resolveActivity、hasSystemFeature 或运行时权限请求之后再 startActivity 的源方法迁为 startAbility、picker 调用时；规格阶段为这类 helper 写目标服务契约时
  - 情境：源方法按“可用性探测 → 权限 → 拉起 → 结果或回退”组织，例如 geo: 无接收者时转地图网页、mailto 走 ACTION_SENDTO、FEATURE_CAMERA 不可用时提示且不建附件；目标准备直接 startAbility 或调用 picker，用 catch 代替预检，或把探测推给通用的打开链接函数。
- [接入 identifier.getOAID 时同批声明 APP_TRACKING_CONSENT 并在隐私同意后申请；全零串按未授权处理](lesson-2b00c4ffaeb442d87e5e.lesson.md)
  - 时机：服务层实现阶段，把源端 OAID（MSA 或厂商通道）采集迁到鸿蒙 identifier.getOAID 时
  - 情境：源端在隐私协议同意后静默采集 OAID，写缓存、上送归因接口并发布就绪事件；鸿蒙 getOAID 需要 user_grant 权限 ohos.permission.APP_TRACKING_CONSENT，未授权时返回全零串；Android 端没有对应的运行期授权。
- [源端 Activity 对自身 getWindow() 加的标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）随该 Activity 窗口失效；映射到应用共享的 UIAbility 主窗口时按页面可见性成对开关（onShown 开、onHidden 关）](lesson-ea9a6cfecca9e091c7ea.lesson.md)
  - 时机：规格提取与页面实现阶段，把 Activity 的窗口标志映射为鸿蒙窗口 API 并写验收时
  - 情境：源端某个 Activity 在 onCreate 给 getWindow() 加标志且没有清除代码，靠该 Activity 不可见或 finish 时随窗口失效；目标各页以 Navigation/NavDestination 共用一个主窗口，经 window.getLastWindow 调 setWindowKeepScreenOn 等窗口级 API。
- [源端 Activity 画中画映射到 @ohos.PiPWindow：可用性用 isPiPEnabled，自动进入用 setAutoStartEnabled，画中画状态由 PiPController 的 stateChange 驱动](lesson-a45be20055d942e12052.lesson.md)
  - 时机：规格提取与实现阶段，迁移源端画中画（PictureInPictureParams 自动进入、onUserLeaveHint、onPictureInPictureModeChanged、画中画精简 UI 与设置开关）时
  - 情境：源 Activity 设置 PictureInPictureParams 或在 onUserLeaveHint 进入画中画，按 onPictureInPictureModeChanged 在完整 UI 与精简 UI 间切换；设置页有画中画开关，并检查系统是否允许。目标为 HarmonyOS 手机应用，项目 SDK 含 @ohos.PiPWindow.d.ts。
  - 例外：项目 compatibleSdkVersion 低于项目 SDK 中 PiPWindow 相关接口的 @since；决策已批准应用内替代（如应用内紧凑模式），此时按决策实现并登记差异
- [源端 Material You 动态取色迁到 HarmonyOS：用 wallpaper.getColors 探测并取种子生成明暗配色、订阅 colorChange，失败回退源端固定配色；该接口已弃用，决策写明风险](lesson-9769c8f754044944d3ad.lesson.md)
  - 时机：规格决策与主题层实现阶段，迁移源端 dynamicLightColorScheme/dynamicDarkColorScheme（Android 12+ 才启用、否则回退固定配色）与“动态配色”设置项时
  - 情境：源主题在 SDK_INT &gt;= S 且设置开启时使用壁纸取色配色，否则用固定的 light/dark scheme；设置页有动态配色开关。目标公开 SDK 的 @ohos.wallpaper（@kit.BasicServicesKit 导出）提供 getColors(WallpaperType) 与 on('colorChange')；getColors 自 API 9 标记弃用，替代接口不在公开 SDK 中。
  - 例外：审批在“降级为固定配色”与“弃用接口 + 回退”之间选了前者，此时设置项按决策呈现并登记差异
- [源端“先读当前系统值、再按位移增量写回”的手势（如亮度）分别映射读写两侧；异步读取在页面就绪时预读基线](lesson-33791daf74fc4298779e.lesson.md)
  - 时机：界面实现阶段，把源端按下时读取窗口亮度等系统值、移动时按增量写回的手势迁到鸿蒙时
  - 情境：源端手势在 ACTION_DOWN 读取窗口当前亮度，未覆写时回退系统亮度设置，移动时按位移增量写回窗口；规格只给出写入接口（setWindowBrightness），读取侧要实现者确定。
- [源端以杀进程实现“重启应用”时用 ApplicationContext.restartApp，不译成 terminateSelf 退出](lesson-73618bb856a8a7dfe7fc.lesson.md)
  - 时机：规格提取与实现阶段，迁移 System.exit(0)、Runtime.exit、Process.killProcess 等进程退出调用时
  - 情境：源方法注释或调用点表明意图是重启（如通知点击的重启动作、切换语言、恢复或重置数据之后调用）；Android 前台进程被杀后，系统按残留任务栈与 savedInstanceState 重建 Activity；目标准备写 context.terminateSelf()。
  - 例外：调用点只在用户主动退出或致命错误时结束进程，源端也不期待重新进入；此时按退出处理
- [源端定时提醒迁 reminderAgentManager 时按其自身 d.ts 映射按钮与贪睡，并写出发布失败、条数上限与到点无回调的回退](lesson-7f1bc7ddc88fab2d03bd.lesson.md)
  - 时机：规格提取与决策阶段，为源端 AlarmManager 定时提醒（带贪睡、延后、打开条目按钮的通知）选定代理提醒等替代路径时；实现阶段按规格写提醒调度与按钮处理时
  - 情境：源端到点由 AlarmManager/广播触发，应用自己构建带按钮的通知，按钮经 PendingIntent 拉起透明跳板 Activity 做贪睡、延后或打开条目，提醒数不设上限、可链式重挂。目标规格准备以“系统托管”整体替代，把 notificationManager 的 NotificationActionButton.wantAgent 写进 reminderAgentManager 的 ActionButton；或实现者发现规格与 d.ts 冲突后改用系统 CLOSE/SNOOZE 按钮作“最大近似”。
  - 例外：源端只需系统模板提醒：没有路由到应用的按钮、没有自定义贪睡间隔，发布失败时源端也不补偿
- [源端通知按钮与可空正文迁到 WantAgent 与 NotificationRequest：每个按钮、每次构建用不同 requestCode，并按需加 UPDATE_PRESENT_FLAG；正文不直接给空串](lesson-716d06e75b7c2102c36c.lesson.md)
  - 时机：实现阶段，把源端通知的多个 PendingIntent 动作按钮与可为 null 的 setContentText 映射为 wantAgent.getWantAgent 与 NotificationRequest 时
  - 情境：源端每次构建通知都给按钮取不同的 requestCode（如逐次取 elapsedRealtime），按钮 Intent 载荷随运行状态变化；部分通知（完成通知、没有文本的步骤）contentText 为 null。目标用 WantAgentInfo（wants、operationType、requestCode、wantAgentFlags）与 NotificationBasicContent（title、text）发布。
- [激励广告等能力门禁挡在核心功能入口前时，区分“用户未获奖励”与“广告能力不可用”：不可用时显式提示并按台账放行，不伪造奖励](lesson-0f67121af7969203b76b.lesson.md)
  - 时机：规格、巡检出单与接线实现阶段，为“先看激励广告、奖励回调后才导航”的入口确定各广告结果的去向时
  - 情境：源端功能入口先调起激励视频，仅在 onReward 回调后导航；目标端没有等价广告 SDK 或广告 provider 未装配，showRewarded 一类接口恒返回 unavailable；决策台账同时要求“能力不可用时显式失败、不伪造 SDK 成功”和核心功能流程真实可用，且没有对这些入口批准“不可用即阻断”。
  - 例外：台账对该入口明确批准“仅获得奖励才可继续”（如只对奖励用户开放的增值功能），此时按该决策阻断，并显示不可用原因
- [用应用内计时加长时任务替代后台 Worker 时，恢复入口共用逐步扣减函数，前台专属状态在每个退出点复位，通知正文按源端逐字段核对](lesson-35a684862ee500f08912.lesson.md)
  - 时机：实现或重写后台计时交接、持久化恢复、紧凑模式与进度通知时
  - 情境：源端由后台 Worker 跨步骤推进计时并发进度通知（正文含重量与步骤时长，具名高重要度渠道），回到前台取 Worker 已推进到的步骤；目标端改为应用内计时加长时任务，用应用内紧凑模式代替系统画中画、窗口常亮代替 WakeLock，恢复与退出清理都要自己写。
