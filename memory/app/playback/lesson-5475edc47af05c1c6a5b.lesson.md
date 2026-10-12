# MediaPlayer 短提示音迁 AVPlayer 时保留源端隐式语义：未申请音频焦点就与其他音频混播，start() 在播放中调用不重启

ID：`lesson-5475edc47af05c1c6a5b` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与服务实现阶段，把 MediaPlayer.create(...).start() 一类短提示音映射到 AVPlayer 并写映射行、实现播放封装时

## 适用情境

源端用 MediaPlayer.create(context, R.raw.x) 加 start() 播放计时提示音等短音效，没有调用 requestAudioFocus；同一实例可能在上一次未播完时再次 start()。目标用 AVPlayer 播 rawfile，规格映射行只写“AVPlayer + rawfile，play() 重置重播”。

## 例外与边界

- 源端申请了音频焦点（requestAudioFocus/AudioFocusRequest），此时按其焦点类型映射目标的焦点与打断策略

## 原因

Android 的音频焦点要由应用主动申请，源端不申请时提示音与其他应用的音乐混播；MediaPlayer 在播放中再调 start() 没有效果。目标不声明音频用途与并发方式时，按系统焦点策略可能打断用户正在听的音乐；把再次触发写成 seek(0) 重播，又改变了连续触发时的听感。映射行没写这两点，实现者只能照“重置重播”落实。

## 做法

1. 映射行写明源端的焦点与重入语义：是否申请音频焦点、与其他音频混播还是独占；播放中再次触发时是忽略、排队还是重启。
2. 源端未申请焦点的短提示音，播放前经 AudioSessionManager.activateAudioSession 把并发模式设为 CONCURRENCY_MIX_WITH_OTHERS，并给 AVPlayer 设置 audioRendererInfo（MediaPlayer 默认媒体流对应 STREAM_USAGE_MUSIC）。
3. 源端 start() 在播放中调用无效时，目标在 playing 态再次触发直接忽略，只在播放完成或停止后从头播放。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:6
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
