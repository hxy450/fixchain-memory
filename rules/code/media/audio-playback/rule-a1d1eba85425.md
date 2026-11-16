# MediaPlayer 提示音迁 AVPlayer 时激活混音 AudioSession，播放中不重启

审的是：代码
触发（任一种）：
- 读到：源端 MediaPlayer.create(context, R.raw.x) 后 start()，没有焦点申请；或规格映射行写「AVPlayer，play() 重置重播」；写错的样子：目标 media.createAVPlayer() 后没设 audioRendererInfo、没调 activateAudioSession，playing 态 seek(0) 后重播
适用范围：把源端未申请音频焦点的短提示音迁成 AVPlayer 时
做法：
- 起播前 audio.getAudioManager().getSessionManager().activateAudioSession({ concurrencyMode: audio.AudioConcurrencyMode.CONCURRENCY_MIX_WITH_OTHERS })；AVPlayer 在 initialized 态、首次 prepare() 前设 audioRendererInfo = { usage: audio.StreamUsage.STREAM_USAGE_MUSIC, rendererFlags: 0 }
- state 为 'playing' 时再次触发直接忽略，不 seek(0)、不重播
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- activateAudioSession(strategy: AudioSessionStrategy): Promise<void>：激活当前应用的音频会话，strategy.concurrencyMode 定并发策略（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioSessionManager.activateAudioSession）
- getSessionManager(): AudioSessionManager：从 AudioManager 取会话管理器（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioManager.getSessionManager）
- AudioConcurrencyMode.CONCURRENCY_MIX_WITH_OTHERS = 1：和其他音频流并发，不打断别的应用（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioConcurrencyMode.CONCURRENCY_MIX_WITH_OTHERS）
- audioRendererInfo?: audio.AudioRendererInfo；只能在 initialized 态设置，要在首次 prepare() 前设；无视频时 usage 默认 STREAM_USAGE_MUSIC：AVPlayer 的渲染信息，设置时机有限制（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.audioRendererInfo）
- AudioRendererInfo { usage: StreamUsage; rendererFlags: number }，StreamUsage.STREAM_USAGE_MUSIC = 1：两项都要填（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioRendererInfo / StreamUsage.STREAM_USAGE_MUSIC）
- 加 activateAudioSession(CONCURRENCY_MIX_WITH_OTHERS) 与 STREAM_USAGE_MUSIC，并改为 playing 态不重启：修复后提示音不打断其他音乐、连续触发不重播（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e332c2cc4929f36c08c7（Cofi）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 诊断；取值 6 ← 诊断
