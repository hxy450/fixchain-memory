# AVPlayer 设源前确保在 idle（不是先 reset），stop 只在允许的状态下调用

审的是：代码
触发（任一种）：
- 读到：源端播放器每次装载都先 `stop()` 再新建、`setDataSource`，调用时机不受状态机约束；写错的样子：目标对不在 idle 的 AVPlayer 直接设 `url` / `fdSrc` / `setMediaSource`，或在 idle、initialized、stopped 等状态调用 `stop()`，报 not idle 或 Operation not allowed
适用范围：目标代码对 AVPlayer 设源和停止时
做法：
- 设 `url`、`fdSrc` 或调 `setMediaSource` 前看 `avPlayer.state`：不是 'idle' 就先 `await avPlayer.reset()` 回到 idle 再设
- `stop()` 只在 state 为 'prepared'、'playing'、'paused'、'completed' 时调用，其他状态跳过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- url、fdSrc 只能在 idle 状态设置：设源前要处于 idle（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.url / AVPlayer.fdSrc）
- stop() 只能在 prepared、playing、paused、completed 状态调用：其他状态调用以 5400102 拒绝（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.stop）
- reset() 把 AVPlayer 置回 idle、可重新设源；可在 initialized、prepared、playing、paused、completed、stopped、error 状态调用：非 idle 时先 reset 再设源（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.reset）
- type AVPlayerState = 'idle' | 'initialized' | 'prepared' | 'playing' | 'paused' | 'completed' | 'stopped' | 'released' | 'error'：avPlayer.state 的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayerState）
- setMediaSource 同样要在 idle 下调用：卡里按状态表处理的设源入口之一；声明里没写状态要求（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-0b0bf6cdf94608e17cbb（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 5 ← 建议 3
