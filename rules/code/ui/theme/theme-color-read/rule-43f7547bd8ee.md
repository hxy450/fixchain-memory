# MaterialTheme.colorScheme 取色改读共享主题状态，不直接 import LightColors

审的是：代码
触发（任一种）：
- 读到：主题函数按 isSystemInDarkTheme() 在 DarkColors / LightColors 间选择并经 MaterialTheme(colorScheme = …) 下发；组件取色写 MaterialTheme.colorScheme.primary 等；写错的样子：组件或页面 import { LightColors } 后写 LightColors.surface 之类，或保留只有亮色值的本地色板常量；应用壳没读取系统 colorMode
适用范围：源端主题随系统深色切换、目标端用品牌双色板跟随系统深色时的公共组件、页面和应用壳
做法：
- 新建可观察的共享主题状态：@ObservedV2 class 里 @Trace isDark 与 colors（isDark ? DarkColors : LightColors），用 AppStorageV2.connect(该类, () => new 该类()) 共享
- 应用壳读取配置的 colorMode（ConfigurationConstant.ColorMode.COLOR_MODE_DARK 为深色）设 isDark，并订阅配置变化随系统切换
- 组件和页面里源端的 MaterialTheme.colorScheme.X 一律写成 this.theme.colors.X，不直接 import LightColors / DarkColors 其中一套；Base 层只出两套常量时也留出这个运行时切换入口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static connect<T extends object>(type: TypeConstructorWithArgs<T>, keyOrDefaultCreator?: string | StorageDefaultCreator<T>, defaultCreator?: StorageDefaultCreator<T>): T | undefined：应用级共享的 UI 状态，与应用同生命周期（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，AppStorageV2.connect）
- declare const ObservedV2: ClassDecorator；declare const Trace: PropertyDecorator：主题状态类和它的 isDark、colors 字段用这两个装饰器，改动后读它的组件刷新（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ObservedV2、Trace）
- colorMode?: ConfigurationConstant.ColorMode：应用当前的颜色模式（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Configuration.d.ts，Configuration.colorMode）
- COLOR_MODE_DARK = 0：深色模式的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.ConfigurationConstant.d.ts，ConfigurationConstant.ColorMode.COLOR_MODE_DARK）
- 共享 ThemeState（@ObservedV2，isDark + colors，AppStorageV2 共享）+ 应用壳读 colorMode 并订阅后，页面和公共组件随系统深色切换：修复用的结构（出处：卡里修好并验证过）
针对本应用要查的：
- 源端两套色板的每个颜色角色：源工程 ui/theme 下定义 lightColorScheme / darkColorScheme 的 Kotlin 文件；逐个角色（primary、surface、onSurface…）写进目标的 LightColors 和 DarkColors，键名一致，供 theme.colors.X 读取
未核实：卡里记了两组鸿蒙版本（5.0.0(12) 与 26.0.0 / 6.1.1(24)），本机声明是 API 23；卡里没写应用壳订阅配置变化用的具体接口
来源：1 张卡，1 个应用
- case-a45ab89c0b8c0037985c（Jetnews）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 2；做法第 3 步 ← 建议 3、诊断；取值 5 ← 诊断
