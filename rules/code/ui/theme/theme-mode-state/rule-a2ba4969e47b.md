# 跟随系统深浅的主题，状态放 @ObservedV2 的 @Trace 字段并在入口两处同步

审的是：代码
触发（任一种）：
- 读到：Compose 主题 Theme(darkTheme = isSystemInDarkTheme()) 选 Light / Dark 两套颜色，经 CompositionLocal 下发，组件在组合期读取；写错的样子：主题层用模块级 `let` 布尔变量加一个同步函数存深浅状态（UI 不观察），注释只写「由宿主 EntryAbility 调用」；全工程 EntryAbility 的 onCreate / onConfigurationUpdate 里没有调用这个同步函数
适用范围：把 Compose 跟随系统深浅的主题迁成 ArkTS 主题层和入口 Ability 时；@ObservedV2、@Trace 声明里是 @since 12
做法：
- 深浅状态放进 @ObservedV2 类的 @Trace 字段（如 @Trace isDark: boolean），用 new 出来的单例；取色函数按它返回 Light / Dark 套，导出注释要求消费者在 build() 或 get 访问器里调用
- 入口 Ability 的 onCreate 按 this.context.config.colorMode、onConfigurationUpdate(newConfig) 按 newConfig.colorMode 各调用一次同步函数（ConfigurationConstant.ColorMode.COLOR_MODE_DARK 为深色）；交付前全工程搜同步函数名，确认这两处各有一次调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare const ObservedV2: ClassDecorator；declare const Trace: PropertyDecorator：V2 的类观测装饰器，@since 12（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ObservedV2 / Trace）
- 未被 @Trace 装饰的属性用在 UI 中无法感知到变化；@ObservedV2 类要用 new 实例化才可被观测：模块级 let 或普通字段不会触发重绘（出处：arkts-new-observedV2-and-trace.md，概述）
- onConfigurationUpdate(newConfig: Configuration): void：UIAbility（继承 Ability）收系统深浅变化的回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
- colorMode?: ConfigurationConstant.ColorMode；COLOR_MODE_NOT_SET = -1、COLOR_MODE_DARK = 0、COLOR_MODE_LIGHT = 1：配置里的深浅取值（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Configuration.d.ts，Configuration.colorMode；ets/api/@ohos.app.ability.ConfigurationConstant.d.ts，ColorMode）
- config: Configuration：冷启动时从 UIAbilityContext.config.colorMode 读当前深浅（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.config）
- onConfigurationUpdate(newConfig: Configuration): void：同族接口：AbilityStage 也有这个回调，可在 Stage 级同步（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityStage.d.ts，AbilityStage.onConfigurationUpdate）
- 深浅状态改为 @ObservedV2 / @Trace isDark，入口冷启动与 onConfigurationUpdate 调同步函数后，深色模式生效：修复后的形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-2c6857febfce92e5d5bc（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 7 ← 诊断
