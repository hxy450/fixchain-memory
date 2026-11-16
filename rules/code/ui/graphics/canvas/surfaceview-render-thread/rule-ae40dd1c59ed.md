# 源端帧循环跟 vsync、逻辑按帧计时，目标用 displaySync 驱动，不用 setInterval(16)

审的是：代码
触发（任一种）：
- 读到：源端游戏线程 while 循环里没有 Thread.sleep，每轮 SurfaceHolder.lockCanvas() → 更新 → onDraw → unlockCanvasAndPost；速度、周期按「每帧」计（px/帧、N 帧），没有 delta-time；写错的样子：目标帧循环写成 setInterval(…, 16)，帧间隔常量写 16，注释写「16ms 等价节流」
- 读到：源端用 Choreographer.postFrameCallback 续帧，或 onDraw 尾部 invalidate() 自续帧，逻辑按帧计；写错的样子：目标用 setInterval / setTimeout 驱动 update + render
适用范围：源端帧节拍由显示刷新决定、逻辑按帧计数的游戏或动画循环迁到 Canvas 时
不适用的情形：源端本来就按固定周期 tick 的逻辑（Handler.postDelayed、Timer、带 sleep 的循环）可以用定时器
做法：
- import { displaySync } from '@kit.ArkGraphics2D'；ds = displaySync.create(); ds.setExpectedFrameRateRange({ expected: 源端帧率, min: 同, max: 同 }); ds.on('frame', () => this.frame()); ds.start()，frame() 里串行 update + render
- 停循环时 ds.stop() 并 ds.off('frame')，用令牌校验丢弃迟到的回调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 60Hz 模拟器上 setInterval(16) 实际约 39 帧/秒（安卓约 60 帧/秒），按帧计的子弹和下压整体变慢；改成 displaySync 期望 {60,60,60} 的 on('frame') 后，关卡节奏与安卓实测一致：定时器不跟 vsync，实际频率明显低于 1000/周期（出处：卡里修好并验证过）
- function create(): DisplaySync：新建 DisplaySync 实例（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，displaySync.create）
- setExpectedFrameRateRange(rateRange: ExpectedFrameRateRange): void；不调时 min/max/expected 默认都是 60：设定帧回调的期望帧率范围（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，DisplaySync.setExpectedFrameRateRange）
- ExpectedFrameRateRange { min: number; max: number; expected: number }，min ≤ expected ≤ max：期望帧率范围的三个字段，单位是帧/秒（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ExpectedFrameRateRange）
- on(type: 'frame', callback: Callback<IntervalInfo>): void；off(type: 'frame', callback?: Callback<IntervalInfo>): void（不传 callback 时移除全部）：注册和注销帧回调，IntervalInfo 带 timestamp、targetTimestamp（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，DisplaySync.on / DisplaySync.off）
- start(): void 加入渲染管线启用回调；stop(): void 移出管线停用回调：开关帧回调（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.displaySync.d.ts，DisplaySync.start / DisplaySync.stop）
- postFrameCallback(frameCallback: FrameCallback): void（在下一帧运行，每帧重投）：卡里建议的另一种 vsync 驱动写法；FrameCallback.onFrame(frameTimeInNano: number)（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.postFrameCallback）
- setExpectedFrameRateRange(rateRange: ExpectedFrameRateRange): void：同族接口：AnimatorResult 的期望帧率范围（出处：鸿蒙 SDK 的 ets/api/@ohos.animator.d.ts，AnimatorResult.setExpectedFrameRateRange）
针对本应用要查的：
- 期望帧率范围填多少：源端帧循环的写法（无 sleep 的 lockCanvas 循环跟设备显示刷新率）和源端同场景的实测帧率；取源端帧率填 min、max、expected；例：源端在 60Hz 设备上约 60 帧/秒时填 {60,60,60}
未核实：UIContext.postFrameCallback 每帧重投的写法卡里没有上机验证，验证过的是 displaySync
来源：1 张卡，1 个应用
- case-4a352d41e71bd8f199f0（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 3；例外 1 ← 建议 1；取值 1 ← 诊断；取值 7 ← 建议 1
