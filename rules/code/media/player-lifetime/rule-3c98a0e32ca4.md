# 安卓播放会跨过退后台时，AVPlayer 控制器配 AVSession 和 AUDIO_PLAYBACK 长时任务

审的是：代码
触发（任一种）：
- 读到：MediaPlayer/ExoPlayer 的 stop/release 只在显式退出或再次点击时调用，宿主 onPause/onStop 不碰播放器；写错的样子：播放控制器只有 media.createAVPlayer、fdSrc、on('stateChange')/on('error') 和 release，没有 avSession.createAVSession，也没有 backgroundTaskManager.startBackgroundRunning
适用范围：安卓端退后台仍继续播放的音频，迁成 AVPlayer 时的播放控制器代码
做法：
- 进入 playing 后：session = await avSession.createAVSession(context, tag, 'audio')，session.setAVPlaybackState({...})；再 backgroundTaskManager.startBackgroundRunning(context, backgroundTaskManager.BackgroundMode.AUDIO_PLAYBACK, wantAgent)
- 停止、播完、出错、页面销毁时都调 backgroundTaskManager.stopBackgroundRunning(context)，再 session.destroy()；不要只写 playback/startPlaying/stopPlaying 三段的前台等价
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- createAVSession(context: Context, tag: string, type: AVSessionType): Promise<AVSession>：创建媒体会话，第二个参数是自定义名字，第三个才是类型（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.avsession.d.ts，avSession.createAVSession）
- type AVSessionType = 'audio' | 'video' | 'voice_call' | 'video_call' | 'photo'：音频播放用 'audio'（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.avsession.d.ts，avSession.AVSessionType）
- setAVPlaybackState(state: AVPlaybackState): Promise<void>：AVSession 上报播放状态（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.avsession.d.ts，AVSession.setAVPlaybackState）
- destroy(): Promise<void>：AVSession 销毁会话、释放服务端资源（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.avsession.d.ts，AVSession.destroy）
- startBackgroundRunning(context: Context, bgMode: BackgroundMode, wantAgent: WantAgent): Promise<void>：申请长时任务，需要 ohos.permission.KEEP_BACKGROUND_RUNNING（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.startBackgroundRunning）
- BackgroundMode.AUDIO_PLAYBACK = 2：音频播放类长时任务（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.BackgroundMode）
- stopBackgroundRunning(context: Context): Promise<void>：取消长时任务（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.stopBackgroundRunning）
未核实：文档示例在 createAVSession 之后调 session.activate()，卡里没写这一步，是否必需未核实；卡里上机结果出自 HarmonyOS 6.1.1(24)，本机声明是 API 23
来源：1 张卡，1 个应用
- case-1dee716aadc97af875f2（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断
