# app/playback

音视频播放：AVPlayer 封装的异步装载并发与停止复位、错误通道与 Promise 拒绝，应用包 rawfile 资源经 fdSrc 设源，封装类释放方法按重载与宿主销毁分开，控制门面同步路径的回退来源，跨实现组合切换步骤时的入口守卫，视频页 surface 绑定与画面比例；短提示音的音频并发（混播/焦点）与播放中重入

[上一级](../index.md)

## 本级经验

- [AVPlayer 播放应用包内 rawfile 资源时用 getRawFd(Sync) 的 {fd, offset, length} 设 fdSrc，不把描述符拼成 fd://N?offset= 形式的 url](lesson-1267d6cabb117824c67a.lesson.md)
  - 时机：规格提取阶段为音视频资源加载写平台 API 契约时；播放服务实现阶段为 AVPlayer 绑定应用包内 rawfile 资源时
  - 情境：源端用 SoundPool.load(context, R.raw.x) 或 MediaPlayer.create(context, R.raw.x) 播放 res/raw 资源，目标改为 AVPlayer 播放 resources/rawfile；resourceManager.getRawFd/getRawFdSync 返回整个 HAP 的 fd 加该资源在 HAP 内的 offset/length；AVPlayer 有 url 与 fdSrc（AVFileDescriptor）两种设源方式。
- [AVPlayer 错误只经一条通道上报，Promise 调用接 catch 并按状态表调用](lesson-d0736ecd82af68edb87a.lesson.md)
  - 时机：播放服务实现阶段，映射 ExoPlayer 的单次 onPlayerError，并调用 AVPlayer 的 prepare/play/pause/stop/reset 时
  - 情境：AVPlayer 同时有 on('error') 与 stateChange('error') 两条错误通道，控制方法返回 Promise；参考模板可能同时处理两条通道、prepare() 也不接 catch。
- [MediaPlayer 短提示音迁 AVPlayer 时保留源端隐式语义：未申请音频焦点就与其他音频混播，start() 在播放中调用不重启](lesson-5475edc47af05c1c6a5b.lesson.md)
  - 时机：规格提取与服务实现阶段，把 MediaPlayer.create(...).start() 一类短提示音映射到 AVPlayer 并写映射行、实现播放封装时
  - 情境：源端用 MediaPlayer.create(context, R.raw.x) 加 start() 播放计时提示音等短音效，没有调用 requestAudioFocus；同一实例可能在上一次未播完时再次 start()。目标用 AVPlayer 播 rawfile，规格映射行只写“AVPlayer + rawfile，play() 重置重播”。
  - 例外：源端申请了音频焦点（requestAudioFocus/AudioFocusRequest），此时按其焦点类型映射目标的焦点与打断策略
- [异步 AVPlayer 装载使用代数令牌与实例归属，停止服务时显式复位](lesson-511385674c16eb68c88c.lesson.md)
  - 时机：播放服务实现阶段，把源端在调用线程同步完成的停止、重建、设源、prepare 改写为含 await 的 AVPlayer 封装，并迁移前台服务停止生命周期时
  - 情境：源播放器在单线程上串行装载，服务停止时 shutdown 置 STOPPED、下次启动重建；目标为常驻单例、方法返回 Promise。
- [把一套实现的切换步骤接到另一套实现的入口时，不提前改写入口守卫读取的状态](lesson-6b2879705254045a49c5.lesson.md)
  - 时机：实现阶段，组合来自不同源实现的换集或切换步骤（例如先改当前项，再调用带“同一项即忽略”守卫的入口）时
  - 情境：入口函数以“当前项是否相同且正在播放”决定是否忽略请求；另一套源实现的切换步骤直接改写当前项。
- [控制门面的同步访问路径也要具备源端懒加载 getter 的回退来源](lesson-cd4a69e85ec59eabf5b9.lesson.md)
  - 时机：播放功能实现阶段，把源端控制器懒加载的当前媒体 getter 翻译为 seekTo、getPosition、getDuration 等同步路径时
  - 情境：源 getter 在服务未运行时从偏好中保存的当前媒体 id 读库；目标服务实例只在起播后持有当前媒体，门面把 getter 做成异步方法、同步路径只读服务实例。
- [源端同一 release() 用在不同作用域时，目标封装拆成两个方法：重载前只释放实例并作废令牌，宿主销毁时才清空宿主 context 与事件](lesson-1a3150939a5e45c02b0e.lesson.md)
  - 时机：服务层实现阶段，把源端播放器等资源的释放调用（重载开头丢弃旧实例、宿主销毁时全清）映射到目标封装类的释放方法时
  - 情境：源端在 loadMusic 一类重载方法开头用 player.release(); player = null 只丢弃旧实例，宿主引用只在整体 release() 中置空；目标把播放器实例、宿主 context、代数令牌封装进一个通道类，由同一类提供释放方法。
- [视频页按对应源 Activity 绑定 surface，XComponent 按视频宽高比内接](lesson-6b4950ca1655ae7bcb8f.lesson.md)
  - 时机：功能实现阶段，移植视频播放页的 surface 绑定时机与画面尺寸时
  - 情境：源新版播放视图在控制器就绪后即挂接播放器、默认等比适配，旧版页另有“surface 就绪且 PLAYING”双守卫；目标用 XComponent(SURFACE) 加共享 AVPlayer 引擎。
