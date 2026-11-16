# 会话重建要复用同一 CameraInput 时，释放旧会话前先 beginConfig 再 removeInput

审的是：代码
触发（任一种）：
- 写错的样子：拆旧会话时直接 await session.stop() 再 await session.release()，没有先 session.beginConfig() + session.removeInput(cameraInput)，随后新会话又 addInput 同一个 cameraInput
适用范围：鸿蒙相机实现里探测会话、拍照会话、录像会话之间切换并复用同一个 CameraInput 时
做法：
- 释放旧会话按 await session.stop() → session.beginConfig() → session.removeInput(cameraInput) → await session.release() 的顺序，再给新会话 beginConfig、addInput(同一个 cameraInput)、addOutput、commitConfig、start
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Session.release 会关闭仍挂载在会话上的 CameraInput；先 removeInput 再 release 后输入可被下一会话复用：不先移除 input 时，下一会话的预览无法启动（出处：卡里修好并验证过）
- removeInput(cameraInput: CameraInput): void，只在 beginConfig() 与 commitConfig() 之间有效：所以 removeInput 前要先 beginConfig（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.removeInput）
- beginConfig(): void；stop(): Promise<void>；release(): Promise<void>：Session 上的配置、停止和释放（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.beginConfig、Session.stop、Session.release）
- removeInput(cameraInput: CameraInput): void：同族接口：旧的 CaptureSession 上的同名方法（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CaptureSession.removeInput）
未核实：声明只写 Release capture session instance.，release 会关闭已挂载 input 出自卡里的设备日志；卡里的环境是 HarmonyOS SDK 6.1.1(24)，签名按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-9284c0c57d1d9b75b702（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断；取值 1 ← 诊断
