# 源端阻塞到完成才返回的 void 方法（排空队列、关闭设备、停录）改为 Promise 签名并逐层 await，销毁、重启、重开排在完成之后

ID：`lesson-b1991f633e5307abdc4d` · 版本：1

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-b1991f633e5307abdc4d.json` 改了 0 句，后面接了 10 条已核实的平台事实。原文、来源和证据卡见 [memory/arkts/async/lesson-b1991f633e5307abdc4d.lesson.md](../../../../memory/arkts/async/lesson-b1991f633e5307abdc4d.lesson.md)。

## 何时使用

规格提取写接口清单、跨切片 seam 设计、实现与接线阶段，把源端阻塞式等待或同步关闭/停止映射为 ArkTS 异步实现，并决定签名与调用方是否 await 时

## 适用情境

源端 void 方法内部阻塞到工作完成（waitUntilDone 排空保存队列、后台线程同步 stop+release 后才置 CLOSED、MediaRecorder 同步 stop/release），验收要求“X 先于 Y”（保存先于销毁或重启、关闭完成才回调或重开）；目标对应接口返回 Promise，规格接口表或占位 seam 照搬 Java 的 void 签名，页面生命周期回调（aboutToDisappear）不能 await。

## 例外与边界

- 源端本身就是异步完成且调用方不等待（回调、未 join 的 Future）时，按源端时序迁移，不额外补等待或取消

## 原因

void 签名承载不了等待：调用方只能 fire-and-forget（void promise、只接 .catch、Promise.resolve().then 包裹同步调用），后续的销毁、重启、置 CLOSED 或重开在实际完成前发生。源端同步完成时不存在的“进行中”窗口在目标出现，重复停止、启动中的停止、关闭中的打开都会落进这个窗口。

## 做法

1. 规格接口表与 seam 类型把这类方法写成 Promise<void>（回调类型定为 () => Promise<void>，当前只是桩也如此），验收写明调用方需 await；实现与接线时从被等待的方法到每一层调用方都 await，完成态（如 CLOSING→CLOSED）、完成回调、销毁、重启与重开写在 await 之后。
2. 不能 await 的生命周期回调只发起一个 async 序列（如 void this.vm.destroySequence()），引擎销毁放在该序列的 await 之后，页面不再另行同步销毁；成对的挂接与拆卸 hook 都返回 Promise。
3. 为异步窗口写明请求语义：关闭进行中到来的打开记为待重开，关闭完成后执行；重复停止返回同一个共享的停止任务；启动链每个 await 之后检查是否已请求停止，已请求则不再启动。

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔适用情境〕MediaRecorder.stop() 是同步 native 调用，返回即已停止；没收到有效音视频数据时故意抛 RuntimeException，让应用清理不完整的输出文件（出处：android.media.MediaRecorder#stop）
- 〔适用情境〕BlockingQueue.take() 取队头，必要时一直等到有元素（出处：java.util.concurrent.BlockingQueue#take）
- 〔适用情境〕AVRecorder 的 prepare(config)、start()、pause()、stop()、reset()、release() 都返回 Promise<void>；状态 AVRecorderState = 'idle' | 'prepared' | 'started' | 'paused' | 'stopped' | 'released' | 'error'，经 state 读取（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder、AVRecorderState）
  写法：import { media } from '@kit.MediaKit'
        const rec: media.AVRecorder = await media.createAVRecorder()
        await rec.prepare(config); await rec.start(); await rec.stop(); await rec.release()  // config: media.AVRecorderConfig
        rec.state: media.AVRecorderState
- 〔适用情境〕相机关闭链都是异步：Session.stop()、Session.release()、CameraOutput.release()、CameraInput.close() 均返回 Promise<void>（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.stop、Session.release、CameraOutput.release、CameraInput.close）
  写法：import { camera } from '@kit.CameraKit'
        await session.stop(); await videoOutput.release(); await session.release(); await cameraInput.close()
        // 类型 camera.Session、camera.CameraOutput（VideoOutput 等）、camera.CameraInput
- 〔做法第 2 步〕aboutToDisappear?(): void 返回 void，框架不等待其中的 Promise；声明注释要求不在其中修改状态变量（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToDisappear）
  写法：@Component struct Index { aboutToDisappear(): void { … }  build() { … } }
- 〔做法第 2 步〕UIAbility.onDestroy(): void | Promise<void>：返回 Promise 时后续生命周期等它完成（注释：onDestroy 执行完应用可能退出，其中的异步操作可能来不及）；onWindowStageDestroy、onBackground 只返回 void（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onDestroy、onWindowStageDestroy、onBackground）
  写法：import { UIAbility } from '@kit.AbilityKit'
        // 入口 UIAbility 的子类里：async onDestroy(): Promise<void> { … }
- 〔做法第 3 步〕AVRecorder.stop() 只能在 start() 或 pause() 之后调用，否则以 5400102（AVERR_OPERATE_NOT_PERMIT）拒绝，另可能 5400103（IO）、5400105（服务死亡）；start() 纯音频在 prepare() 之后、视频在 getInputSurface() 之后（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.stop、AVRecorder.start、media.AVErrorCode）
  写法：import { BusinessError } from '@kit.BasicServicesKit'
        rec.stop().catch((e: BusinessError) => { if (e.code === media.AVErrorCode.AVERR_OPERATE_NOT_PERMIT) { … } })
- 〔做法第 3 步〕AVRecorder 每个状态方法都同时有 AsyncCallback 重载和 Promise 重载；pause() 的成对方法是 resume(): Promise<void>（只能在 pause() 之后调，回到 started）；状态监听 on('stateChange', callback: OnAVRecorderStateChangeHandler) 回调 (state: AVRecorderState, reason: StateChangeReason)，一个实例只保留最后一次订阅，off('stateChange', callback?) 注销；另有 on/off('error', callback: ErrorCallback)。StateChangeReason：USER = 1、BACKGROUND = 2（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.resume、AVRecorder.on、AVRecorder.off、OnAVRecorderStateChangeHandler、StateChangeReason）
  写法：import { media } from '@kit.MediaKit'; import { BusinessError } from '@kit.BasicServicesKit'
        await rec.pause(); await rec.resume()  // rec: media.AVRecorder
        rec.on('stateChange', (state: media.AVRecorderState, reason: media.StateChangeReason) => { })；rec.off('stateChange')
        rec.on('error', (err: BusinessError) => { })；rec.off('error')
- 〔做法第 3 步〕相机的打开链与关闭链成对、同样异步：CameraInput.open(): Promise<void>（另有 open(isSecureEnabled: boolean): Promise<bigint>）；Session.beginConfig(): void 是同步的，commitConfig()、start() 返回 Promise<void>；VideoOutput.start()、stop() 返回 Promise<void>；它们都另有 AsyncCallback 重载（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraInput.open、Session.beginConfig、Session.commitConfig、Session.start、VideoOutput.start、VideoOutput.stop）
  写法：import { camera } from '@kit.CameraKit'
        await input.open(); session.beginConfig(); session.addInput(input); session.addOutput(out)
        await session.commitConfig(); await session.start(); await out.start()
        // input: camera.CameraInput；session: camera.VideoSession（extends camera.Session）；out: camera.VideoOutput
- 〔适用情境 / 例外与边界〕源端 Camera2 的 CameraDevice.close() 不等关闭完成就返回：调用后设备与会话接口立即抛 IllegalStateException，设备完全关闭时才回调 StateCallback.onClosed，此后相机才可重开；源端在 close() 后不等 onClosed 就置 CLOSED 或重开时，源端本身并没有阻塞到关闭完成（出处：android.hardware.camera2.CameraDevice#close、#onClosed）
