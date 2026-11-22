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
2. 不能 await 的生命周期回调只发起一个 async 序列（如 void this.vm.destroySequence()），引擎销毁放在该序列的 await 之后，页面不再另行同步销毁；这个序列在组件析构之后才跑完，await 之后的步骤不改本组件的状态变量、不再弹窗；成对的挂接与拆卸 hook 都返回 Promise。
3. 为异步窗口写明请求语义：关闭进行中到来的打开记为待重开，关闭完成后执行；重复停止返回同一个共享的停止任务；启动链每个 await 之后检查是否已请求停止，已请求则不再启动。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 2 步〕自定义组件的 aboutToDisappear?(): void 在组件析构销毁时执行，声明为同步、返回 void；文档规定其中不允许改变状态变量，也不建议在它被调用之后触发自定义弹窗创建这类逻辑（组件树信息已丢失）
- 〔适用情境〕安卓 MediaRecorder 的 start()、stop()、release() 都是同步的 native 方法，返回时动作已完成；stop() 在 start() 之前调抛 IllegalStateException，停止时没收到有效音视频数据会抛 RuntimeException；停止后要重新配置才能再录
- 〔适用情境 / 做法第 1 步〕AVRecorder 的 prepare(config)、start()、stop()、release() 都返回 Promise<void>；stop 必须在 start 或 pause 之后调用，状态不允许时以 5400102 拒绝，成功后进入 stopped 状态；release 之后这个实例不能再做任何操作
- 〔做法第 3 步〕AVRecorder.start 必须在 prepare 之后调用，录制视频时还要在 getInputSurface 成功之后；getInputSurface 也必须在 prepare 之后，启动链因此是 prepare → getInputSurface → start 几段先后的 Promise
- 〔做法第 3 步〕AVRecorder stop 之后要重新录：纯音频录制要重新调 prepare，纯视频、音视频录制要重新调 prepare 和 getInputSurface
- 〔适用情境 / 做法第 1 步〕相机侧的 CameraInput.close()、Session.stop()、Session.release()、CameraOutput.release() 都返回 Promise<void>
