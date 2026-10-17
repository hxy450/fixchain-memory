# MediaPlayer 短提示音迁 AVPlayer 时保留源端隐式语义：未申请音频焦点就与其他音频混播，start() 在播放中调用不重启；源端为 SoundPool 时不适用

ID：`lesson-5475edc47af05c1c6a5b` · 版本：3 · 阶段：spec/execute · 主题：[app/playback](index.md)

概要：短提示音保留混播与播放中 start 不重启语义

信号：`MediaPlayer.create`, `requestAudioFocus`, `AudioFocusRequest`, `AudioSessionManager.activateAudioSession`, `CONCURRENCY_MIX_WITH_OTHERS`, `audioRendererInfo`, `STREAM_USAGE_MUSIC`, `AVPlayer`, `seek(0)`

## 何时使用

规格提取与服务实现阶段，把 MediaPlayer.create(...).start() 一类短提示音映射到 AVPlayer 并写映射行、实现播放封装时

## 适用情境

源端用 MediaPlayer.create(context, R.raw.x) 加 start() 播放计时提示音等短音效，没有调用 requestAudioFocus；同一实例可能在上一次未播完时再次 start()。目标用 AVPlayer 播 rawfile，规格映射行只写“AVPlayer + rawfile，play() 重置重播”。 不包括源端 SoundPool（先 load 预解码、事件时 play、maxStreams 多路叠播）。

## 例外与边界

- 源端申请了音频焦点（requestAudioFocus/AudioFocusRequest），此时按其焦点类型映射目标的焦点与打断策略
- 源端用 android.media.SoundPool（new SoundPool(...) 或 SoundPool.Builder，load 与 play 分开调用）播放短音效：目标用 media.createSoundPool，按 lesson-1267d6cabb117824c67a 的 SoundPool 分支处理，不用“每次播放新建 AVPlayer 实例”模拟叠播

## 原因

Android 的音频焦点要由应用主动申请，源端不申请时提示音与其他应用的音乐混播；MediaPlayer 在播放中再调 start() 没有效果。目标不声明音频用途与并发方式时，按系统焦点策略可能打断用户正在听的音乐；把再次触发写成 seek(0) 重播，又改变了连续触发时的听感。映射行没写这两点，实现者只能照“重置重播”落实。 AVPlayer 每次发声都要经过 create → 设源 → prepare → play 的状态机，prepare 完成前不出声；拿它模拟 SoundPool 预加载后的即时叠播，发声会明显滞后。

## 做法

1. 映射行写明源端的焦点与重入语义：是否申请音频焦点、与其他音频混播还是独占；播放中再次触发时是忽略、排队还是重启。 源端是 SoundPool 时本条不适用，见例外。
2. 源端未申请焦点的短提示音，播放前经 AudioSessionManager.activateAudioSession 把并发模式设为 CONCURRENCY_MIX_WITH_OTHERS，并给 AVPlayer 设置 audioRendererInfo（MediaPlayer 默认媒体流对应 STREAM_USAGE_MUSIC）。
3. 源端 start() 在播放中调用无效时，目标在 playing 态再次触发直接忽略，只在播放完成或停止后从头播放。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [Float 运算比较按 float32 后用 ===](../../arkts/runtime-semantics/lesson-0deb51172ebdd2e056a9.lesson.md)（共享 1 张卡）
- [rawfile 设 fdSrc 不拼 fd:// 串](lesson-1267d6cabb117824c67a.lesson.md)（共享 1 张卡）
- [拒绝输入用 maxLength 或 onWillChange](../../ui/interaction/input/lesson-617ffbd840398cf95efc.lesson.md)（共享 1 张卡）
- [长按手势显式补系统长按触感](../../ui/interaction/gestures/lesson-8a752faf9f5dff52e3ff.lesson.md)（共享 1 张卡）
- [Slider steps 翻步长：区间/(steps+1)](../../ui/interaction/selectors/lesson-d715fa78ada2e79a5fd2.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-6734103a0f798cbf6699](../../../../store/cases/case-6734103a0f798cbf6699/bde268ebe7dbbe6e8f8e6dafc53b7811c47d729c8579d1eda716a60e9db26712.json) · 结论：diagnosis, rec-1a90a16660
  卡片版本：`bde268ebe7dbbe6e8f8e6dafc53b7811c47d729c8579d1eda716a60e9db26712`
- [case-e332c2cc4929f36c08c7](../../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, rec-2997eb68b9
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
