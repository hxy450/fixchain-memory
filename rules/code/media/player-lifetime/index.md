# 跨卡片、跨退后台存活的播放器

agent 会看到什么：读到源端 ExoPlayer / MediaPlayer 是全局懒创建、多张卡共用的单例，或 stop / release 只在显式退出时调、宿主 onPause / onStop 不碰播放器；产物里播放器句柄放在哪、无可见项时 stop 还是靠卸载，有没有 AVSession 和 AUDIO_PLAYBACK 长时任务

## 规矩

- rule-4ee6ae84e1db｜多张 feed 卡共享一个 ExoPlayer 时，全局持一个 AVPlayer 会话按卡换绑 surface｜读到：多张 feed 卡共享一个 ExoPlayer：全局状态里 @Synchronized 懒创建的播放器单例，带 release，无可见项时 stop()；写错：全局状态里没有播放器句柄，共享实例换成「仅活跃卡挂一个 Video 节点」，无可见项时只置 activeId = null，靠卸载代替 stop
- rule-3c98a0e32ca4｜安卓播放会跨过退后台时，AVPlayer 控制器配 AVSession 和 AUDIO_PLAYBACK 长时任务｜读到：MediaPlayer/ExoPlayer 的 stop/release 只在显式退出或再次点击时调用，宿主 onPause/onStop 不碰播放器；写错：播放控制器只有 media.createAVPlayer、fdSrc、on('stateChange')/on('error') 和 release，没有 avSession.createAVSession，也没有 backgroundTaskManager.startBackgroundRunning
