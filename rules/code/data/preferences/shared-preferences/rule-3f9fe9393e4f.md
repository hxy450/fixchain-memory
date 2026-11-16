# 应用级偏好存储封装在 UIAbility.onCreate 初始化，不只挂在 Flutter 插件 attach 上

审的是：代码
触发（任一种）：
- 读到：源端 MethodChannel 回调里直接读写全局静态键值工具（MMKV 或 SharedPreferences 工具类的 getString / putString），通道本身不初始化存储；写错的样子：偏好存储封装的唯一 init(context) 在 Flutter 插件的 onAttachedToEngine 里（用 binding.getApplicationContext()），EntryAbility 的 onCreate 里没有 init
适用范围：原生宿主内嵌 Flutter 引擎的混合应用，把源端全局键值工具迁成需要先传 context 的 preferences 封装时
做法：
- 在 UIAbility.onCreate 最前面（或 AbilityStage.onCreate）用当时可得的上下文调封装的 init（修复里是 this.context）；Flutter 插件、MethodChannel、页面只读写，不作唯一初始化点
- init 写成首次调用生效，后续调用不覆盖 context、不清缓存
- 列出全部启动期读写方（onCreate 里的网络配置或 token 加载、闪屏页恢复状态、通道取 token），逐个确认晚于 init；onCreate 新增读写方时再核一次
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void；context: UIAbilityContext：UIAbility 的创建回调和它持有的上下文（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onCreate、UIAbility.context）
- onCreate(): void（Called when the application is created，同步返回）；context: AbilityStageContext：AbilityStage 的创建回调，早于 UIAbility；持有 AbilityStageContext（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityStage.d.ts，AbilityStage.onCreate、AbilityStage.context）
- function getPreferences(context: Context, name: string): Promise<Preferences>：取首选项实例必须传 context，封装的 init 就是为了拿到它（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferences）
- function getPreferencesSync(context: Context, options: Options): Preferences：同族接口：同步取首选项实例，同样要 context（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferencesSync）
- preferencesDir：ApplicationContext 是 <路径前缀>/<加密等级>/base/preferences；AbilityStageContext、UIAbilityContext 是 <路径前缀>/<加密等级>/base/haps/<module-name>/preferences：init 传哪种上下文决定首选项文件在哪；前后要用同一种（出处：application-context-stage.md，获取应用文件路径（表1））
未核实：卡里修复后没有复测，token 丢失是否就因为初始化位置没有证实；卡里的环境是 HarmonyOS 6.0.2(22)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-f93cb4842b050b7fb269（polypal-app-ohos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2
