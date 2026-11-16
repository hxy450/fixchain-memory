# 源端 controller 就绪即 setPlayer 时，目标面就绪就挂视频面，不加 PLAYING 门

审的是：代码
触发（任一种）：
- 读到：MediaController.buildAsync 成功回调里直接 playerView.setPlayer(mediaController)，没有播放状态判断；写错的样子：绑定控制器、XComponent 面就绪、onShown 几处都以 getStatus() === PLAYING 作为挂视频面的前提，状态回调在 PLAYING 边沿不补挂
适用范围：视频页用 XComponent(SURFACE) 加共享播放引擎，页面可能先于或晚于引擎进入播放态时
做法：
- 以目标页对应的源 Activity 为准：抽一个无状态门的挂面方法，在控制器绑定、XComponent 的 onLoad（面就绪）和 onShown 三处都调用；状态回调里再补一次绑定
- 若保留「面已就绪 ∧ PLAYING」双守卫，状态回调的 PLAYING 边沿必须补挂
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 无状态门的挂面方法在三处调用、状态回调补绑定后，页面先于引擎进入播放态也能出画面：修复后的写法（出处：卡里修好并验证过）
- AVPlayer.surfaceId?: string：initialized 态可设；initialized 态设过后，prepared、playing、paused、completed、stopped 态可再设并切到新窗口：播放器接收视频面的状态限制（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.AVPlayer.surfaceId）
针对本应用要查的：
- 引擎的挂面方法能否在非 PLAYING 态接收 surfaceId：目标工程共享播放引擎里挂面方法的实现，找给 AVPlayer.surfaceId 赋值的地方；看它在哪些状态下赋值；能在面就绪时直接赋值就面就绪即交付，否则按状态回调补挂
来源：1 张卡，1 个应用
- case-5e35bb283520acf3bd35（AntennaPod）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断
