# MediaPlayer 短提示音迁 AVPlayer 时保留源端隐式语义：未申请音频焦点就与其他音频混播，start() 在播放中调用不重启；源端为 SoundPool 时不适用

## 何时使用

规格提取与服务实现阶段，把 MediaPlayer.create(...).start() 一类短提示音映射到 AVPlayer 并写映射行、实现播放封装时

## 适用情境

源端用 MediaPlayer.create(context, R.raw.x) 加 start() 播放计时提示音等短音效，没有调用 requestAudioFocus；同一实例可能在上一次未播完时再次 start()。目标用 AVPlayer 播 rawfile，规格映射行只写“AVPlayer + rawfile，play() 重置重播”。 不包括源端 SoundPool（先 load 预解码、事件时 play、maxStreams 多路叠播）。

## 例外与边界

- 源端申请了音频焦点（requestAudioFocus/AudioFocusRequest），此时按其焦点类型映射目标的焦点与打断策略
- 第 3 步“播放中再次触发直接忽略”只适用于源端复用同一个 MediaPlayer 实例再调 start()：源端每次触发都 MediaPlayer.create(...) 新建实例时，连续触发是几个实例各自从头播、彼此重叠，不是忽略，目标照这种重入语义映射，不改成忽略
- 源端用 android.media.SoundPool（new SoundPool(...) 或 SoundPool.Builder，load 与 play 分开调用）播放短音效：目标用 media.createSoundPool，按 lesson-1267d6cabb117824c67a 的 SoundPool 分支处理，不用“每次播放新建 AVPlayer 实例”模拟叠播

## 原因

Android 的音频焦点要由应用主动申请，源端不申请时提示音与其他应用的音乐混播；MediaPlayer 在播放中再调 start() 没有效果。目标不声明音频用途与并发方式时，按系统焦点策略可能打断用户正在听的音乐；把再次触发写成 seek(0) 重播，又改变了连续触发时的听感。映射行没写这两点，实现者只能照“重置重播”落实。 AVPlayer 每次发声都要经过 create → 设源 → prepare → play 的状态机，prepare 完成前不出声；拿它模拟 SoundPool 预加载后的即时叠播，发声会明显滞后。

## 做法

1. 映射行写明源端的焦点与重入语义：是否申请音频焦点、与其他音频混播还是独占；播放中再次触发时是忽略、排队还是重启。 源端是 SoundPool 时本条不适用，见例外。
2. 源端未申请焦点的短提示音，播放前经 AudioSessionManager.activateAudioSession 把并发模式设为 CONCURRENCY_MIX_WITH_OTHERS，并给 AVPlayer 设置 audioRendererInfo（MediaPlayer 默认媒体流对应 STREAM_USAGE_MUSIC）。
3. 源端 start() 在播放中调用无效时，目标在 playing 态再次触发直接忽略，只在播放完成或停止后从头播放。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕安卓 MediaPlayer 没有调 setAudioAttributes 时，AudioAttributes 的 usage 为 USAGE_UNKNOWN，音量流按 STREAM_MUSIC 处理；MediaPlayer 自身不申请音频焦点
- 〔原因 / 做法第 3 步〕安卓 MediaPlayer 已处于 Started 状态时再调 start() 没有效果，不会从头重播
- 〔原因〕卡里设备上每次新建 AVPlayer 播短音效，要走完 create → 设源 → prepare → play，从 createAVPlayer 到 playing 约 290ms；SoundPool 预先 load 后出声约 40ms
- 〔做法第 2 步〕AudioConcurrencyMode.CONCURRENCY_MIX_WITH_OTHERS 让本应用音频流和其他音频流并发；要达到不被后起音乐打断、和后台音乐并发的效果，需在音频流启动前激活 AudioSession
- 〔做法第 2 步〕AVPlayer.audioRendererInfo 不设时，媒体源含视频则 usage 为 STREAM_USAGE_MOVIE，否则为 STREAM_USAGE_MUSIC；要生效须在 initialized 状态、首次调用 prepare() 之前设置
