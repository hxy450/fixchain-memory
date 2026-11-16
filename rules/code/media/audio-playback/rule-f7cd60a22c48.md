# 源端播放 assets 音频时，目标用 SoundPool 从 rawfile 加载，usage 用 MUSIC

审的是：代码
触发（任一种）：
- 读到：源端按键点击处理里按文件名播放 assets 目录下的 mp3（如 start("….mp3")）；写错的样子：目标只开系统点击音或没有播放；或 media.createSoundPool 的 usage 写成 STREAM_USAGE_NOTIFICATION，没等 loadComplete 就 play
适用范围：安卓按键音、提示音这类短音频迁成 ArkTS 播放时
做法：
- media.createSoundPool(maxStreams, { usage: audio.StreamUsage.STREAM_USAGE_MUSIC, rendererFlags: 0 }) 创建，不用 STREAM_USAGE_NOTIFICATION，也不靠系统点击音
- 每个音频用 resourceManager.getRawFd('文件名') 取 { fd, offset, length } 传给 soundPool.load(fd, offset, length)；on('loadComplete') 收到 soundID 后才可 play(soundID)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function createSoundPool(maxStreams: number, audioRenderInfo: audio.AudioRendererInfo): Promise<SoundPool>：创建 SoundPool，maxStreams 取 1–32（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.createSoundPool）
- STREAM_USAGE_MUSIC = 1：usage 为 UNKNOWN、MUSIC、MOVIE、AUDIOBOOK 时 SoundPool 播短音用混音模式，不打断其他音频（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，StreamUsage.STREAM_USAGE_MUSIC；ets/api/@ohos.multimedia.media.d.ts，media.createSoundPool）
- AudioRendererInfo { usage: StreamUsage; rendererFlags: number }，rendererFlags 建议填 0：createSoundPool 的第二个参数（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioRendererInfo）
- getRawFd(path: string): Promise<RawFileDescriptor>：取 rawfile 的 fd、offset、length（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getRawFd）
- load(fd: number, offset: number, length: number): Promise<number>：加载一个音频，返回 soundID（大于 0 才有效）（出处：鸿蒙 SDK 的 ets/api/multimedia/soundPool.d.ts，SoundPool.load）
- on(type: 'loadComplete', callback: Callback<number>): void：音频加载完成的事件，回调参数是 soundID（出处：鸿蒙 SDK 的 ets/api/multimedia/soundPool.d.ts，SoundPool.on）
- play(soundID: number, params?: PlayParameters): Promise<number>：播放已加载的音频，返回 streamID（出处：鸿蒙 SDK 的 ets/api/multimedia/soundPool.d.ts，SoundPool.play）
- SoundPool 用 STREAM_USAGE_MUSIC 并等 loadComplete 后能出声；改用系统点击音时无声：卡里上机看到的行为（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 4；取值 8 ← 诊断
