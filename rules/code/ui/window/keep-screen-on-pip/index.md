# 窗口常亮和画中画（FLAG_KEEP_SCREEN_ON、PictureInPicture）

agent 会看到什么：读到源端 getWindow().addFlags / clearFlags(FLAG_KEEP_SCREEN_ON)、WakeLock 或 PictureInPictureParams 进出画中画，产物里是 setWindowKeepScreenOn 的置位和复位位置、各退出路径上的状态复位，以及 PiPWindow 相关代码

## 规矩

- rule-64ad0c3d7558｜Activity 窗口常亮迁到页面时，在 onShown/onHidden 成对调常亮开关｜读到：源端 Activity.onCreate 里 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)，没有 clearFlags；写错：页面在 aboutToAppear 里 window.getLastWindow 后 setWindowKeepScreenOn(true)，onHidden、aboutToDisappear 里都没有 setWindowKeepScreenOn(false)
- rule-d74b4a61ef77｜源码在校验前置位 FLAG_KEEP_SCREEN_ON 时，目标按源码的置位和清除位置复刻｜读到：源码在前置操作成功后、范围或参数校验之前 addFlags(FLAG_KEEP_SCREEN_ON)，收尾段第一步 clearFlags(FLAG_KEEP_SCREEN_ON)，校验失败提前返回的路径不清除；写错：目标把常亮置位（setWindowKeepScreenOn(true) 或包它的方法）挪到成功路径才做，注释或源码笔记把源时序称为源缺陷、越界泄漏
- rule-dd7f37b33287｜常亮和紧凑模式这类前台专属状态，每条退出路径都显式复位｜读到：源端用 WakeLock 或窗口常亮保持亮屏、用系统 PiP，退出 PiP 时回调把标志置 false；规格写明「stop clears flag」；写错：setKeepScreenOn(true) 和紧凑模式标志置 true 之后，回前台、后台交接、后台完成、通知 Stop、页面销毁中有的路径只停服务或重启 ticker，没有对应的 false
- rule-09c576c348d8｜源端画中画自动进入，目标用 PiPWindow.create 加 setAutoStartEnabled｜读到：源端 PictureInPictureParams.Builder().setAutoEnterEnabled(true)、onUserLeaveHint 进入画中画，onPictureInPictureModeChanged 写画中画状态；写错：目标没有 PiPWindow 相关代码，画中画状态写成恒 false，设置里的画中画开关是死键、没有可用性判定
