# UI 侧播放控制器的取媒体和挂视频面

agent 会看到什么：读到源端 UI 侧播放控制器的取媒体方法在成员为空时懒加载（从偏好里存的媒体 ID 读库）、MediaController.buildAsync 成功回调里直接 setPlayer；产物里目标控制器同步的 seekTo / getPosition 只读服务实例，或挂视频面以 getStatus() === PLAYING 为前提

## 规矩

- rule-9cebf3389c81｜源端 getter 在服务未运行时懒加载媒体，目标的同步 seekTo、getPosition 也要有回退来源｜读到：源端 UI 控制器的取媒体方法在成员为空时懒加载（从偏好里存的当前媒体 ID 读库），seekTo / getPosition / getDuration 都经它取媒体；写错：目标控制器只有异步的取媒体方法带回查，同步的 seekTo、getPosition 只读服务实例上的 playable，服务没起时为 null，规格里「服务未运行」的分支成了死代码
- rule-b53fdb6f5d59｜源端 controller 就绪即 setPlayer 时，目标面就绪就挂视频面，不加 PLAYING 门｜读到：MediaController.buildAsync 成功回调里直接 playerView.setPlayer(mediaController)，没有播放状态判断；写错：绑定控制器、XComponent 面就绪、onShown 几处都以 getStatus() === PLAYING 作为挂视频面的前提，状态回调在 PLAYING 边沿不补挂
