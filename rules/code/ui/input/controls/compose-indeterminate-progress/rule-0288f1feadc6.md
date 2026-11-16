# 不传 progress 的 LinearProgressIndicator，用 Canvas 逐帧复刻并叠放

审的是：代码
触发（任一种）：
- 读到：Compose 里 `LinearProgressIndicator()` 没传 progress（不定进度，持续动画），可能带 `Modifier.zIndex` 叠在内容上；写错的样子：目标写成 `Progress({ value: 0 / 30 / 50, type: ProgressType.Linear })` 一类定值静止条，或换成圆形 `LoadingProgress`，或放进 Column 流里把列表往下推
适用范围：源端 Compose Material3 的线性不定进度条迁到 ArkUI 时，含共享组件和页面里内联的写法
做法：
- 在共享组件里用 Canvas + displaySync 逐帧绘制复刻 M3 线性不定进度（双线关键帧，颜色 primary / secondaryContainer，两线之间留间隙）：displaySync.create() 后 on('frame', cb) 里推进动画并重画，start() 开始，组件消失时 stop()
- 保留源端的叠放：放在 Stack 里叠在内容之上（源端有 zIndex 的照写 .zIndex），不放进 Column 流推挤内容
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ProgressOptions.value: number（必填），默认 0，取值范围 [0, total]：Progress 只显示定值进度，没有不定模式，写常量就是静止条（出处：鸿蒙 SDK 的 ets/component/progress.d.ts，ProgressOptions.value；ts-basic-components-progress.md，ProgressOptions对象说明）
- LoadingProgress：用于显示加载动效的组件：系统自带的加载动效，形状和 M3 线性条不同（出处：ts-basic-components-loadingprogress.md，LoadingProgress）
- function create(): DisplaySync：创建逐帧回调对象（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，displaySync.create）
- on(type: 'frame', callback: Callback<IntervalInfo>): void；start(): void；stop(): void：注册每帧回调（IntervalInfo.timestamp 是当前帧时间），start 加入管线开始回调，stop 移出管线停止（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，DisplaySync.on、DisplaySync.start、DisplaySync.stop）
- Canvas + displaySync 逐帧复刻 M3 线性不定进度（双线关键帧，primary / secondaryContainer，4dp 间隙）并叠放在内容上，与源端一致：验证过的复刻方式（出处：卡里修好并验证过）
针对本应用要查的：
- 源端线性不定进度条的颜色、track 颜色、高度和动画：源码调用处显式传的 color / trackColor / modifier；没传的，查源工程依赖的 androidx.compose.material3 版本（依赖声明或 Compose BOM）里 ProgressIndicatorDefaults 的默认值；显式值直接用；默认值是主题 colorScheme 的颜色角色，再按应用主题解析到色值，高度 dp 换成 vp
未核实：卡里的效果在目标 API 24 上验证，本机核对用的是 API 23 的声明；M3 线性不定进度的关键帧时长没在本机来源里核到
来源：1 张卡，1 个应用
- case-f0512caa793e1ad8016c（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
