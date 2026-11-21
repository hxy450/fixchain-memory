# 源端阻塞到完成才返回的 void 方法（排空队列、关闭设备、停录）改为 Promise 签名并逐层 await，销毁、重启、重开排在完成之后

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

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕MediaRecorder.stop() 是同步 native 调用，返回即已停止；没收到有效音视频数据时故意抛 RuntimeException，让应用清理不完整的输出文件
- 〔适用情境〕BlockingQueue.take() 取队头，必要时一直等到有元素
- 〔适用情境〕AVRecorder 的 prepare(config)、start()、pause()、stop()、reset()、release() 都返回 Promise<void>；状态 AVRecorderState = 'idle' | 'prepared' | 'started' | 'paused' | 'stopped' | 'released' | 'error'，经 state 读取
- 〔适用情境〕相机关闭链都是异步：Session.stop()、Session.release()、CameraOutput.release()、CameraInput.close() 均返回 Promise<void>
- 〔做法第 2 步〕aboutToDisappear?(): void 返回 void，框架不等待其中的 Promise；声明注释要求不在其中修改状态变量
- 〔做法第 2 步〕UIAbility.onDestroy(): void | Promise<void>：返回 Promise 时后续生命周期等它完成（注释：onDestroy 执行完应用可能退出，其中的异步操作可能来不及）；onWindowStageDestroy、onBackground 只返回 void
- 〔做法第 3 步〕AVRecorder.stop() 只能在 start() 或 pause() 之后调用，否则以 5400102（AVERR_OPERATE_NOT_PERMIT）拒绝，另可能 5400103（IO）、5400105（服务死亡）；start() 纯音频在 prepare() 之后、视频在 getInputSurface() 之后
