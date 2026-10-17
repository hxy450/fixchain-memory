# app/playback

音视频播放：AVPlayer/SoundPool 设源与状态机、错误通道、装载令牌与释放、后台播放

[上一级](../index.md)

## 本级经验

- [rawfile 设 fdSrc 不拼 fd:// 串](lesson-1267d6cabb117824c67a.lesson.md) · 阶段：spec/execute · 信号：getRawFdSync, getRawFd, fdSrc, AVFileDescriptor
- [surface 按对应源页绑定，画面等比内接](lesson-6b4950ca1655ae7bcb8f.lesson.md) · 阶段：execute · 信号：XComponent, SURFACE, surfaceId, AVPlayer
- [异步 AVPlayer 装载用代数令牌，停服务时显式复位](lesson-511385674c16eb68c88c.lesson.md) · 阶段：execute · 信号：AVPlayer, STOPPED, PLAYING
- [短提示音保留混播与播放中 start 不重启语义](lesson-5475edc47af05c1c6a5b.lesson.md) · 阶段：spec/execute · 信号：MediaPlayer.create, requestAudioFocus, AudioFocusRequest, AudioSessionManager.activateAudioSession
- [组合异源切换步骤时不先改写入口守卫读取的状态](lesson-6b2879705254045a49c5.lesson.md) · 阶段：execute · 信号：同一项即忽略
- [退后台续播时接 AVSession 与音频长时任务](lesson-65db317135138c3181c7.lesson.md) · 阶段：spec/execute · 信号：avSession.createAVSession, setAVPlaybackState, setBackgroundPlayMode, backgroundTaskManager.startBackgroundRunning
- [重载只释放实例并作废令牌，宿主销毁才全清 context](lesson-1a3150939a5e45c02b0e.lesson.md) · 阶段：execute · 信号：release(), loadMusic
- [错误只经 on('error') 报，调用接 catch](lesson-d0736ecd82af68edb87a.lesson.md) · 阶段：execute · 信号：on('error'), stateChange, onPlayerError, ExoPlayer
- [门面同步路径也要有源懒加载 getter 的回退来源](lesson-cd4a69e85ec59eabf5b9.lesson.md) · 阶段：execute · 信号：seekTo, getPosition, getDuration
