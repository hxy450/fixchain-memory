# Video 的 src 里的本地文件地址

agent 会看到什么：读到源端把本地缓存文件路径经 Intent 交给 VideoView.setVideoPath 或播放器 setUrl，交回的代码把缓存、预载接口的输出或路由参数原样传进 Video({ src: … })

## 规矩

- rule-8d3510831a48｜Video 的 src 来自本地文件路径参数时，在消费处补成 file:// URI，网络地址原样传｜读到：源端把本地缓存文件路径经 Intent 传给播放器（VideoView.setVideoPath 或第三方播放器 setUrl(path)）；映射参考的本地视频示例是 Video({ src: '/sdcard/video.mp4' }) 这类裸路径；写错：Video({ src: … }) 拿到的是以 / 开头的沙箱绝对路径，没有 file:// 前缀，也没经过 fileUri 转换
- rule-7d0656a8c0ce｜跨页把缓存或预载接口的输出接到播放器前，先核对它返回的是路径还是可播放 URI｜读到：目标工程的缓存 / 预载工具同时有返回裸绝对路径的方法和返回 file:// 播放地址的方法，同工程已有 Video 的 src 经后者取源；写错：路由参数里传的是返回裸路径那个方法的输出，参数类型或注释没写格式，消费页原样交给 Video({ src: … })；同一任务里只给部分 Video 改用了播放地址
