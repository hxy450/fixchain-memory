# app/platform

系统平台能力（后台任务与扩展能力承载类、module.json5 extensionAbilities 的 type 登记，通知与常驻通知的订阅归属、画中画回退、动态取色、地图承载，打开系统设置的显式 Want）的实现、替代与降级，激励广告等能力门禁在能力不可用时的入口放行，厂商 SDK 鸿蒙版本的查询与选型，以及后台计时的恢复和退出清理，读当前系统值再增量写回的手势（亮度）读写映射，OAID 采集的跟踪授权

[上一级](../index.md)

## 本级经验

- [Android 依赖厂商 SDK（地图、登录、支付、账号等）时，先查鸿蒙系统 Kit 与厂商 ohpm 包，再在 Kit、厂商包、H5 与受控降级之间取舍；查证前不写“鸿蒙无等价”](lesson-e9890889e591196c3d0d.lesson.md)
  - 时机：规格提取与迁移规划阶段，为三方 SDK 作依赖决策、判断是否“鸿蒙无等价”、为对应切片绑定 SDK 文档类 skill 时；实现阶段遇到规格要求的 SDK 能力而工程里还没有 SDK 时
  - 情境：Android 工程直接依赖厂商 SDK（com.amap.api.* 一类），功能规格与接口清单写明这些能力；项目 skill 映射表把该厂商列为 SDK 文档查询类 skill 的典型对象；用户在决策问答中没有提供鸿蒙 SDK 资料，只回复“采用建议”。也包括微信 OpenSDK 登录与支付（ohpm 有 @tencent/wechat_open_sdk）、华为账号（系统 @kit.AccountKit 提供）这类被规格或决策表与其他三方 SDK 并列为占位候选的能力，而 skill 映射表已把它们绑定到登录、支付 skill。
  - 例外：已查明厂商没有鸿蒙版本，且决策记录写明了替代方案与理由
- [Android 前台服务改用扩展能力承载时，先在项目 SDK 确认基类导出；module.json5 extensionAbilities 的 type 与基类成对，backgroundModes 只写在 UIAbility](lesson-16c24b9a44153d703f04.lesson.md)
  - 时机：后台服务迁移的规格、实现与编译/安装修复阶段，为源端 Foreground Service 选择承载类并在 module.json5 登记扩展能力时；因编译错误更换扩展基类时
  - 情境：源端以 Service/LifecycleService 加 startForeground 承载长任务；目标准备用扩展能力类承载并在 module.json5 extensionAbilities 注册；规格、决策或文件头注释凭经验写了 ServiceExtensionAbility、type=service 或 backgroundModes，生成批次可能不能编译。
- [决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记](lesson-efb94f2d70d4df1c65d7.lesson.md)
  - 时机：实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色、地图承载等）或解决指向平台切片的前向占位时
  - 情境：源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色，或用第三方地图 SDK 的 MapView 显示当前位置与轨迹；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期。
  - 例外：决策账本对该能力明确批准的是延期或仅前台实现
- [开关控制的常驻通知由应用级服务订阅与发布，不绑在页面 ViewModel 的激活周期上](lesson-e9f03fcc7f1e781c4b24.lesson.md)
  - 时机：系统能力迁移阶段（规格提取与服务、ViewModel 实现），为由开关控制、由后台事件驱动的常驻通知确定订阅归属与生命周期时
  - 情境：源端在页面初始化时注册一次事件监听且不注销，回调在开关为真时用固定 ID 更新 ongoing 通知；二级页的监听随页面注销且不发通知。目标主壳以条件渲染承载 Tab，或页面在 NavDestination 中出栈，页面 ViewModel 在 aboutToAppear/aboutToDisappear 激活、释放订阅。
- [打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设备核对，启动失败要可观察，不照抄参考里标“已验证”的值](lesson-4bea916d1ff67e51d455.lesson.md)
  - 时机：系统能力实现阶段，为“打开系统设置/应用权限页”编写 startAbility 显式 Want（bundleName/abilityName）时；维护迁移 skill 参考中的系统应用包名时
  - 情境：源端经 Settings.ACTION_* 一类 Intent 跳转系统设置（全部文件访问、应用详情等）；目标为 HarmonyOS NEXT 应用，需要以显式 Want 指定系统设置应用，规格与源码都不给目标包名，可查到的参考文档给出硬编码的厂商设置包名并标注已验证。
- [接入 identifier.getOAID 时同批声明 APP_TRACKING_CONSENT 并在隐私同意后申请；全零串按未授权处理](lesson-2b00c4ffaeb442d87e5e.lesson.md)
  - 时机：服务层实现阶段，把源端 OAID（MSA 或厂商通道）采集迁到鸿蒙 identifier.getOAID 时
  - 情境：源端在隐私协议同意后静默采集 OAID，写缓存、上送归因接口并发布就绪事件；鸿蒙 getOAID 需要 user_grant 权限 ohos.permission.APP_TRACKING_CONSENT，未授权时返回全零串；Android 端没有对应的运行期授权。
- [源端“先读当前系统值、再按位移增量写回”的手势（如亮度）分别映射读写两侧；异步读取在页面就绪时预读基线](lesson-33791daf74fc4298779e.lesson.md)
  - 时机：界面实现阶段，把源端按下时读取窗口亮度等系统值、移动时按增量写回的手势迁到鸿蒙时
  - 情境：源端手势在 ACTION_DOWN 读取窗口当前亮度，未覆写时回退系统亮度设置，移动时按位移增量写回窗口；规格只给出写入接口（setWindowBrightness），读取侧要实现者确定。
- [激励广告等能力门禁挡在核心功能入口前时，区分“用户未获奖励”与“广告能力不可用”：不可用时显式提示并按台账放行，不伪造奖励](lesson-0f67121af7969203b76b.lesson.md)
  - 时机：规格、巡检出单与接线实现阶段，为“先看激励广告、奖励回调后才导航”的入口确定各广告结果的去向时
  - 情境：源端功能入口先调起激励视频，仅在 onReward 回调后导航；目标端没有等价广告 SDK 或广告 provider 未装配，showRewarded 一类接口恒返回 unavailable；决策台账同时要求“能力不可用时显式失败、不伪造 SDK 成功”和核心功能流程真实可用，且没有对这些入口批准“不可用即阻断”。
  - 例外：台账对该入口明确批准“仅获得奖励才可继续”（如只对奖励用户开放的增值功能），此时按该决策阻断，并显示不可用原因
- [用应用内计时加长时任务替代后台 Worker 时，恢复入口共用逐步扣减函数，前台专属状态在每个退出点复位，通知正文按源端逐字段核对](lesson-35a684862ee500f08912.lesson.md)
  - 时机：实现或重写后台计时交接、持久化恢复、紧凑模式与进度通知时
  - 情境：源端由后台 Worker 跨步骤推进计时并发进度通知（正文含重量与步骤时长，具名高重要度渠道），回到前台取 Worker 已推进到的步骤；目标端改为应用内计时加长时任务，用应用内紧凑模式代替系统画中画、窗口常亮代替 WakeLock，恢复与退出清理都要自己写。
