# AVPlayer 的状态机和异步播控

agent 会看到什么：源端 MediaPlayer / ExoPlayer 的装载（stop → setDataSource → prepare）、播控和错误回调，对应目标 AVPlayer 的设源、prepare / play / stop 的 Promise 和 on('error') / stateChange

## 规矩

- rule-0dbfd31761c1｜AVPlayer 设源前确保在 idle（不是先 reset），stop 只在允许的状态下调用｜读到：源端播放器每次装载都先 `stop()` 再新建、`setDataSource`，调用时机不受状态机约束；写错：目标对不在 idle 的 AVPlayer 直接设 `url` / `fdSrc` / `setMediaSource`，或在 idle、initialized、stopped 等状态调用 `stop()`，报 not idle 或 Operation not allowed
- rule-e86223a6bcbc｜源端同步装载改成带 await 的 AVPlayer 装载时，每次装载带代数并持有自己的实例｜读到：源端播放器在调用线程（或内部单线程 executor）内顺序执行 stop → 新建播放器 → `setDataSource` → `prepare`；写错：目标装载函数经过多个 `await` 后才对共享的 `this.avPlayer` 设源，`completed` 回调不核对是不是当前实例；两次装载交错时后到的设源报 not idle，前一次照常起播并按播完收尾
- rule-e220e9c0030a｜AVPlayer 播控方法返回 Promise，要接 .catch，不靠同步 try/catch｜写错：对 `avPlayer.prepare()`、`play()`、`pause()`、`stop()`、`reset()` 只包同步 `try { … } catch`，既没 `await` 也没 `.catch`，拒绝落到 unhandledRejection
- rule-c3c3b86250d1｜源端单次 onPlayerError 迁到 AVPlayer 时，只由 on('error') 发错误事件｜读到：源端只注册一个错误回调（ExoPlayer 的 `onPlayerError` 或 `setOnErrorListener`），出错时发一次错误事件弹一个对话框；写错：目标在 `on('stateChange')` 收到 `'error'` 和 `on('error')` 里各自上报一次，一次失败弹出两个错误对话框
- rule-fb266304f9c3｜源端依赖缓冲态或缓冲位时用 AVPlayer+XComponent，接 bufferingUpdate｜读到：派工或决策台账写「视频播放用 AVPlayer」，源端 STATE_BUFFERING → LOADING、bufferedPosition.coerceAtLeast(currentPosition)；写错：写成 Video({ src, controller })：onPrepared 后直接 SUCCESS，没有 BUFFERING 态，bufferedMs = currentMs
