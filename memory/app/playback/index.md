# app/playback

音视频播放：AVPlayer 封装的异步装载并发与停止复位、错误通道与 Promise 拒绝，控制门面同步路径的回退来源，跨实现组合切换步骤时的入口守卫，视频页 surface 绑定与画面比例

[上一级](../index.md)

## 本级经验

- [AVPlayer 错误只经一条通道上报，Promise 调用接 catch 并按状态表调用](lesson-d0736ecd82af68edb87a.lesson.md)
  - 时机：播放服务实现阶段，映射 ExoPlayer 的单次 onPlayerError，并调用 AVPlayer 的 prepare/play/pause/stop/reset 时
  - 情境：AVPlayer 同时有 on('error') 与 stateChange('error') 两条错误通道，控制方法返回 Promise；参考模板可能同时处理两条通道、prepare() 也不接 catch。
- [异步 AVPlayer 装载使用代数令牌与实例归属，停止服务时显式复位](lesson-511385674c16eb68c88c.lesson.md)
  - 时机：播放服务实现阶段，把源端在调用线程同步完成的停止、重建、设源、prepare 改写为含 await 的 AVPlayer 封装，并迁移前台服务停止生命周期时
  - 情境：源播放器在单线程上串行装载，服务停止时 shutdown 置 STOPPED、下次启动重建；目标为常驻单例、方法返回 Promise。
- [把一套实现的切换步骤接到另一套实现的入口时，不提前改写入口守卫读取的状态](lesson-6b2879705254045a49c5.lesson.md)
  - 时机：实现阶段，组合来自不同源实现的换集或切换步骤（例如先改当前项，再调用带“同一项即忽略”守卫的入口）时
  - 情境：入口函数以“当前项是否相同且正在播放”决定是否忽略请求；另一套源实现的切换步骤直接改写当前项。
- [控制门面的同步访问路径也要具备源端懒加载 getter 的回退来源](lesson-cd4a69e85ec59eabf5b9.lesson.md)
  - 时机：播放功能实现阶段，把源端控制器懒加载的当前媒体 getter 翻译为 seekTo、getPosition、getDuration 等同步路径时
  - 情境：源 getter 在服务未运行时从偏好中保存的当前媒体 id 读库；目标服务实例只在起播后持有当前媒体，门面把 getter 做成异步方法、同步路径只读服务实例。
- [视频页按对应源 Activity 绑定 surface，XComponent 按视频宽高比内接](lesson-6b4950ca1655ae7bcb8f.lesson.md)
  - 时机：功能实现阶段，移植视频播放页的 surface 绑定时机与画面尺寸时
  - 情境：源新版播放视图在控制器就绪后即挂接播放器、默认等比适配，旧版页另有“surface 就绪且 PLAYING”双守卫；目标用 XComponent(SURFACE) 加共享 AVPlayer 引擎。
