# 外观开关驱动的主题状态用 @ObservedV2/@Trace，带写入与应用路径，入口重放

审的是：代码
触发（任一种）：
- 读到：源端设置开关由 DataStore 持久化，并被 @Composable 主题函数实时读取；基础计划写「主题令牌支持 light/dark/dynamic」；写错的样子：目标的主题状态类只有默认值字段，没有 @ObservedV2 / @Trace、没有写入方法，也没有任何地方调 setColorMode 或应用调色板
适用范围：目标端用全局主题状态承接源端的外观开关（动态主题、深浅色等）时
做法：
- 主题状态写成 @ObservedV2 class，开关字段和调色板加 @Trace；切换时写入并应用（如 applicationContext.setColorMode(...)、更新调色板）
- 在 EntryAbility 启动时和 onConfigurationUpdate(newConfig) 里按已存的偏好重放一次主题
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare const ObservedV2: ClassDecorator；declare const Trace: PropertyDecorator：可观察的类和属性装饰器（@since 12）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ObservedV2、Trace）
- setColorMode(colorMode: ConfigurationConstant.ColorMode): void：ApplicationContext 设置应用的颜色模式（@since 18，只能在主线程调用）（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.setColorMode）
- ColorMode.COLOR_MODE_NOT_SET = -1、COLOR_MODE_DARK = 0、COLOR_MODE_LIGHT = 1：颜色模式取值，NOT_SET 是跟随系统（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.ConfigurationConstant.d.ts，ConfigurationConstant.ColorMode）
- onConfigurationUpdate(newConfig: Configuration): void：系统配置更新时回调，UIAbility 继承自 Ability（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
- 主题状态改为 @ObservedV2 / @Trace、切换时 setColorMode，EntryAbility 启动与 onConfigurationUpdate 时应用主题：修复后的接法（出处：卡里修好并验证过）
- onConfigurationUpdate(newConfig: Configuration): void：同族接口：AbilityStage 的配置更新回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityStage.d.ts，AbilityStage.onConfigurationUpdate）
未核实：卡里的行为出自 API 21（HarmonyOS 6.0.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-470d704a6ec794b4c3c9（Cofi）：做法第 1 步 ← 建议 2、建议 3、诊断；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
