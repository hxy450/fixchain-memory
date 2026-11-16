# 多张 feed 卡共享一个 ExoPlayer 时，全局持一个 AVPlayer 会话按卡换绑 surface

审的是：代码
触发（任一种）：
- 读到：多张 feed 卡共享一个 ExoPlayer：全局状态里 @Synchronized 懒创建的播放器单例，带 release，无可见项时 stop()；写错的样子：全局状态里没有播放器句柄，共享实例换成「仅活跃卡挂一个 Video 节点」，无可见项时只置 activeId = null，靠卸载代替 stop
适用范围：feed 内嵌视频、多卡复用同一播放器的实现
做法：
- 全局状态里保留一个 AVPlayer 会话，暴露 getOrCreate() / release()；当前活跃卡把自己 XComponent 的 surfaceId 绑定到会话（按 owner 绑定、解绑），切卡时只换 surface，不新建播放器
- 无可见卡时调用会话的 stop()，对应源端的 exoPlayer.stop()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- surfaceId 可在 initialized 状态设置，在 prepared、playing、paused、completed、stopped 状态可再次设置，之后画面在新窗口播放：同一个 AVPlayer 切卡时换绑 surface 即可（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.surfaceId）
- 全局会话按 owner 绑定，getOrCreate / release：修好后切卡不重建解码器、不丢播放状态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-dfd68051bcdcc94eba9f（jerboa）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 诊断；取值 2 ← 诊断
