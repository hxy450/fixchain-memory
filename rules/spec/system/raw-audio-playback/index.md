# 源端 MediaPlayer / SoundPool 播 res/raw 音频

agent 会看到什么：源端用 MediaPlayer.create(context, R.raw.x) 或 SoundPool load / play 播 res/raw 音频，规格的映射行写成 AVPlayer 重播、url=fd:// 设源或 AVPlayer 实例池

## 规矩

- rule-3c0250fae9d9｜映射 MediaPlayer→AVPlayer 时，映射行写明源端不抢音频焦点、播放中 start() 无效｜读到：源端 MediaPlayer.create(context, R.raw.x) 后 start()，没有 AudioAttributes 或 requestAudioFocus；写错：规格映射行写「AVPlayer + rawfile/…，play() 重置重播」，没写与其他音频混播、播放中再触发不重启
- rule-490f71417db2｜规格写 rawfile 音视频设源契约时写 getRawFd 到 fdSrc，不写 url=fd://｜读到：安卓源端用 SoundPool.load(context, R.raw.x) 或 MediaPlayer.create(context, R.raw.x) 播 res/raw 资源，目标改为 AVPlayer 播 resources/rawfile；写错：规格实现映射的契约列写「资源经 getRawFd → url=fd://」，或同一格里只给其中一个 API（如 setVolume）标 d.ts 依据，设源方式没有依据
- rule-7611b17f35b2｜源端 SoundPool 预加载短音效时，规格映射和决策候选写 media.createSoundPool｜读到：源端 import android.media.SoundPool，new SoundPool(...) 或 SoundPool.Builder，初始化时 load、事件发生时 play，两者分开调用；写错：跨栈映射写成 SoundPool → AVPlayer 实例池（每次播放新实例）+ fdSrc，服务层写「每次调用新建 AVPlayer 实例，prepared 后 start，播完 release」；或选型决策的候选里没有 media.SoundPool
