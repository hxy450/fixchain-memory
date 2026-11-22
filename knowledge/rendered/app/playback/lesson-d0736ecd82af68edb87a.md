# AVPlayer 错误只经一条通道上报，Promise 调用接 catch 并按状态表调用

## 何时使用

播放服务实现阶段，映射 ExoPlayer 的单次 onPlayerError，并调用 AVPlayer 的 prepare/play/pause/stop/reset 时

## 适用情境

AVPlayer 同时有 on('error') 与 stateChange('error') 两条错误通道，控制方法返回 Promise；参考模板可能同时处理两条通道、prepare() 也不接 catch。

## 例外与边界

- “stateChange('error') 只做状态处理”指不在这里再发一次错误事件，不是删掉它：状态切到 error 时用 reset()（仍为 error 再 release()）退出播放的处理要保留；on('error') 触发而状态没有切到 error 时，只做提示、不必停止播控。

## 原因

两条通道各自上报会弹两个错误对话框；同步 try/catch 接不住 Promise 拒绝，未处理的拒绝会被全局错误处理记成崩溃；在不允许的状态调用会再次报错。

## 做法

1. 只用 on('error')（带具体原因）发错误事件，stateChange('error') 只做状态处理；同一实例只上报一次。
2. 对已由 on('error') 上报的 Promise 调用接 .catch；设 url/fdSrc 前确保处于 idle（否则先 reset），stop 只在 prepared/playing/paused/completed 下调用。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕AVPlayer 的 on('error') 事件用户操作和系统都会触发，只用于错误提示，不要求停止播控；若 AVPlayerState 也切到 error，要调 reset() 或 release() 退出播放
- 〔做法第 2 步〕AVPlayer 的 url、fdSrc 只能在 idle 状态设置；setMediaSource 同样只能在 idle 状态调用
- 〔做法第 2 步〕AVPlayer.stop() 只能在 prepared、playing、paused、completed 状态调用，其他状态下以 5400102（Operation not allowed）拒绝
- 〔做法第 2 步〕AVPlayer.reset() 把播放器置回 idle、可重新设源，只能在 initialized、prepared、playing、paused、completed、stopped、error 状态调用
- 〔原因〕卡里设备上 AVPlayer 播控方法返回的 Promise 被拒绝而没有 catch 时，拒绝落到 unhandledRejection，被应用的全局错误处理记成崩溃报告
