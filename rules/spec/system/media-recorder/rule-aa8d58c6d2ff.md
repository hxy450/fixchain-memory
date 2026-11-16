# 规格把同步停录、关相机映射到 AVRecorder/CameraKit 时，写 Promise 签名和串行化契约

审的是：规格
触发（任一种）：
- 读到：源端 MediaRecorder.stop() / release() 同步完成并置空录制器，再重连相机；相机在后台线程阻塞 stopPreview + release 后才置为已关闭；写错的样子：规格接口表写 stopRecording(...): void、release(): void，映射表写「MediaRecorder → AVRecorder 状态机等价·低风险」，没写重复停止、准备期间停止、关相机等停录、拆输出与释放录制器的先后
适用范围：规格阶段把安卓同步的录制器、相机关闭接口映射到 AVRecorder、CameraKit 时
做法：
- 写接口表前查目标 d.ts 的返回类型：AVRecorder 的 prepare / start / stop / release 和 CameraKit 的 close / stop / release 都返回 Promise<void>，接口表里 stop、release、detach 一律写成返回 Promise
- 写串行化契约四条：重复 stop 共享同一个停止任务；准备期间 stop 要取消启动；关闭相机先等停录且不再重连；先拆录像输出再释放录制器
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stop(): Promise<void>，只能在 start() 或 pause() 之后调：AVRecorder 停录是异步的，准备期间不能直接 stop（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.stop）
- prepare(config: AVRecorderConfig): Promise<void>；start(): Promise<void>；release(): Promise<void>：AVRecorder 其余步骤也都返回 Promise（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.prepare / start / release）
- close(): Promise<void>：CameraInput 关闭相机是异步的（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraInput.close）
- public native void stop() throws IllegalStateException：源端 MediaRecorder.stop 是同步调用，返回即已停止（出处：android.media.MediaRecorder#stop）
来源：1 张卡，1 个应用
- case-b89cd099bfa87829fd2d（opencamera-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
