# app/identity

应用身份字段从 Android 迁到 AppScope 与入口模块：显示名及其 label 资源、bundleName/vendor、版本号的读取，以及应用级图标引用与 AppScope 图标资源，以及启动窗图标与底色

[上一级](../index.md)

## 本级经验

- [应用级图标按 AppScope 自身资源解析：身份落地时把 app.json5 icon 改指迁移后的分层图标并补齐其前景/背景，不把脚手架现值当作“不变”](lesson-feec63f65102f5396e51.lesson.md)
  - 时机：执行阶段应用身份落地（资源迁移之后），确定 AppScope/app.json5 的应用级 icon 引用，以及 AppScope 与入口模块分层图标的前景/背景资源时
  - 情境：脚手架 AppScope/app.json5 的 icon 仍指向模板占位图（如 $media:app_icon，AppScope media 下只有 1KB 以内的占位 PNG）；源 App 的启动图标（自适应前景/背景，矢量或位图）已由资源迁移落到 entry 模块并被入口 Ability 的 icon（如 $media:layered_image）引用；身份步骤的说明只描述 PNG 来源，或把 icon 写成“保持目标值（不变）”。也包括 entry 侧 layered_image 的前景/背景本身仍是脚手架 PNG（源前景为 ic_launcher_foreground 矢量、背景为 @color），资源迁移把启动图标层留给身份步骤，身份步骤只改了显示名。
  - 例外：AppScope 的 icon 已指向能解析到源 App 图标的资源；此时只需核对引用在 AppScope media 内闭合
- [沿用脚手架 bundleName/vendor 前核对所引决策、台账技术项与签名配置：无依据时按源包名写入，vendor 不随签名延后](lesson-fb996956b33a1ba65861.lesson.md)
  - 时机：资源前置阶段落地应用身份字段、执行编排为该步骤撰写派工、决定 bundleName 与 vendor 是否替换脚手架值时；规格/决策阶段登记模板身份技术项时
  - 情境：AppScope/app.json5 仍是 com.example.* 包名与 example 厂商，源 build.gradle 给出真实 applicationId（或 namespace）；执行规则或身份技能的受限范围（如只写显示名与版本的开发期身份）要求把包名、厂商留到部署期，并引用某个决策编号。也包括编排者自己写了“bundleName 对齐源 package”的台账技术项，执行规则仍引用台账里不存在的部署期决策编号要求跳过；以及源 applicationId 本身位于 com.example.* 下（教学或示例工程）。
  - 例外：决策台账里确有已批准的部署期身份决策且工程已有签名配置：只影响 bundleName，且仍不保留通用脚手架名 com.example.myapplication，至少换成由源包名派生的唯一值；vendor 不参与签名，仍按源端落地
- [源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量](lesson-a6ed8a9c6017ddb73beb.lesson.md)
  - 时机：接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时
  - 情境：源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。
- [源端未自定义 SplashScreen 时，启动窗按 Android 12+ 系统启动画面取自适应图标与主题窗口背景，dark 不留模板黑底](lesson-c4af68b3ee1456525e8e.lesson.md)
  - 时机：资源前置与应用身份迁移阶段，为目标启动窗（module.json5 的 startWindowIcon / startWindowBackground）选定图标与底色资源时
  - 情境：源主题未定义 windowSplashScreen* 属性、也未调用 SplashScreen API，在 Android 12+ 设备上显示系统启动画面；启动器图标是 adaptive-icon（前景层加背景）；主题是没有夜间变体的 Light 系主题，或 AppCompat 等库的 DayNight 主题；目标工程仍是脚手架 startIcon 与 start_window_background（base 白、dark 黑），身份技能只写“复制前景或 ic_launcher”。
  - 例外：源端用 windowSplashScreen* 属性或 SplashScreen API 自定义了启动画面，按其声明映射
- [落地应用显示名时同时改 AppScope 与入口 Ability 的 label 字符串，资源迁移合并而不覆盖模板 string.json](lesson-55f44e2efdc1a49ac387.lesson.md)
  - 时机：执行编排阶段的应用身份落地步骤（资源迁移之后、页面转换之前），资源迁移任务写入或重写 string.json 时，以及编译修复补回缺失的身份字符串时
  - 情境：目标工程由脚手架生成，AppScope/app.json5 的 label 与 entry 模块 module.json5 中入口 Ability 的 label 都指向 $string 资源，值仍是脚手架工程名；module.json5 还引用 module_desc、EntryAbility_desc 等模板键；Android 应用名来自 strings.xml 的 app_name（由 Manifest 的 android:label 引用），或由 build.gradle 的 resValue 提供。工程还可能有 en_US 等语言限定目录，含同名的脚手架身份键（可能由 i18n 补齐步骤以模板值填入）。
  - 例外：本条只处理显示名；bundleName、vendor 等部署身份字段按工程已记录的决策处理
- [阶段规则要跳过身份字段时，先对照下游验证门的模板值判定：冲突就安排验证前的落地步骤，或让验证门对已登记延后项给出 DEFERRED](lesson-60d5b35c4ca9c2ccce3b.lesson.md)
  - 时机：维护迁移流水线的阶段规则与身份技能范围时；执行编排以受限范围（如开发期身份）派发身份步骤、决定跳过某个字段时
  - 情境：执行规则或身份技能以“部署期再落地”为由跳过 bundleName、vendor 等字段并保留脚手架值；下游验证门对 com.example.* 包名、vendor=example 等模板默认值直接判失败；流水线在该阶段之后没有安排落地步骤。
