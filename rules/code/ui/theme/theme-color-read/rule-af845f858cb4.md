# 源码读 MaterialTheme 颜色和字体时，目标经单一主题入口取值，不写某套 light 值的静态 $r

审的是：代码
触发（任一种）：
- 读到：Compose 源码里 MaterialTheme.colorScheme.xxx、MaterialTheme.typography.xxx 读值，源端有多套 lightColorScheme / darkColorScheme 色板、明暗模式或字号缩放；写错的样子：用 $r('app.color.…')、$r('app.float.…') 直接绑定某一套色板的 light 色值和 M3 字号；接收颜色的参数类型写成 Resource；没有登记 FWD-REF
适用范围：Compose 界面迁成 ArkUI 时，源端经 MaterialTheme 在运行时取的颜色和排版
做法：
- 把这些读值都当运行时主题值，经单一主题访问入口读取（如 @ObservedV2 单例里 @Trace 的颜色、字体令牌，build 里直接读）；目标主题状态还没建好时登记主题绑定 FWD-REF
- 接收主题颜色的参数和字段类型写成 ResourceColor，不写 Resource
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare function $r(value: string, ...params: any[]): Resource：$r 引的是编译进包的静态资源，不随应用内的色板、字号设置变化（出处：鸿蒙 SDK 的 ets/component/common.d.ts，$r）
- declare type ResourceColor = Color | number | string | Resource：颜色参数写成 ResourceColor 才能同时收主题状态里的色值和资源（出处：鸿蒙 SDK 的 ets/component/units.d.ts，ResourceColor）
- declare const ObservedV2: ClassDecorator；declare const Trace: PropertyDecorator：全局主题状态类用的装饰器（@since 12）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ObservedV2、Trace）
- @ObservedV2 类里 @Trace 的属性变化时，会触发绑定它的 UI 组件刷新：单例主题状态被主题控制器改写后，读它的界面自动刷新（出处：arkts-new-observedV2-and-trace.md，观察变化）
- 新建 @ObservedV2 单例主题状态，主题控制器重算时写入它；页面里的静态 $r 主题引用换成该单例的颜色、字体值，颜色类型由 Resource 改为 ResourceColor：修好后的写法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK 6.1.1(24)，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-4f288900adbe48a3c049（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 5 ← 诊断
