# 音效和播放器的封装

agent 会看到什么：源端 SoundPool / MediaPlayer 播放短音效或 assets 音频、重载前 release；产物里 createSoundPool 还是每次 createAVPlayer、usage 和 loadComplete，以及播放封装类的 release 和短路分支

## 规矩

- rule-109a87a7d762｜源端 SoundPool 短音效，目标用 createSoundPool 预加载后 play，不每次建 AVPlayer｜读到：源端 new SoundPool(maxStreams, AudioManager.STREAM_MUSIC, srcQuality) 或 SoundPool.Builder，初始化时 load(context, resId, priority)，事件时 play(soundID, ...)；写错：每次播放都 media.createAVPlayer() → 设 fdSrc → prepare → prepared 后 play，播完 release
- rule-f7cd60a22c48｜源端播放 assets 音频时，目标用 SoundPool 从 rawfile 加载，usage 用 MUSIC｜读到：源端按键点击处理里按文件名播放 assets 目录下的 mp3（如 start("….mp3")）；写错：目标只开系统点击音或没有播放；或 media.createSoundPool 的 usage 写成 STREAM_USAGE_NOTIFICATION，没等 loadComplete 就 play
- rule-7b25c974e628｜源端重载开头的 MediaPlayer.release() 只丢旧实例，目标封装类拆出只释放实例的方法，重载路径不调全清｜读到：源端重新装载的方法开头只有 MediaPlayer.release(); 字段 = null，随后照常 MediaPlayer.create(...)；宿主 Context 引用只在整体 release() 的全清末段置 null；写错：目标封装类只有一个 release()，里面同时作废令牌、释放播放器并把 context 置 null，重载路径也调这个 release()；或者 load() 自己已先释放旧实例，调用方又调一次全清的 release()
- rule-56af216fe0eb｜播放通道因 context 为空短路时，分支里先写 hilog.warn 再回调失败｜写错：封装类的 load 等方法里 if (ctx === null) 之类的短路分支直接回调失败或 return，没有 hilog.warn 或 hilog.error
- rule-ba012c57fa82｜rawfile 的 getRawFd 描述符只经 AVPlayer.fdSrc 设源，不在 url 上拼 offset｜读到：安卓源端 SoundPool.load(context, R.raw.x) 或 MediaPlayer.create(context, R.raw.x)；规格写「getRawFd → url=fd://」；写错：代码写 player.url = `fd://${fd}?offset=${offset}&length=${length}`，或 getRawFd / getRawFdSync 的结果流向 .url
- rule-a1d1eba85425｜MediaPlayer 提示音迁 AVPlayer 时激活混音 AudioSession，播放中不重启｜读到：源端 MediaPlayer.create(context, R.raw.x) 后 start()，没有焦点申请；或规格映射行写「AVPlayer，play() 重置重播」；写错：目标 media.createAVPlayer() 后没设 audioRendererInfo、没调 activateAudioSession，playing 态 seek(0) 后重播
