# 源端会话一次带齐预览和 JPEG 输出时，目标在同一次 beginConfig 里加齐再 commitConfig

审的是：代码
触发（任一种）：
- 读到：源端 CameraDevice.createCaptureSession 一次传入预览 surface 和 ImageReader（JPEG）的 surface，录像态再加 MediaRecorder 的 surface；写错的样子：只 addInput 就 commitConfig，之后在同一会话上再 beginConfig、重复 addInput 并只加 previewOutput；或拍照时才惰性 addOutput(photoOutput) 重配会话
适用范围：Camera2 的拍照预览会话迁成 CameraKit PhotoSession / VideoSession 时
做法：
- 同一次 session.beginConfig() 里 addInput(cameraInput)，按源端 surfaces 清单 addOutput(previewOutput)、addOutput(photoOutput)，再 await session.commitConfig()、await session.start()
- 开流前要取能力时，用带输出的探测会话或 CameraManager.getSupportedOutputCapability 的静态能力；不提交只含输入的会话，不在运行中的会话上惰性 addOutput
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- addOutput(cameraOutput: CameraOutput): void：Session 上加输出，只在 addInput 之后、commitConfig 之前有效（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.addOutput）
- beginConfig(): void；commitConfig(): Promise<void>：Session 的配置开始与提交（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.beginConfig、Session.commitConfig）
- getSupportedOutputCapability(camera: CameraDevice, mode: SceneMode): CameraOutputCapability：CameraManager 上按场景模式取静态输出能力，不用开会话（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraManager.getSupportedOutputCapability）
- 会话由 createCaptureSession 时给出的输出 Surface 集合决定：源端的 surfaces 清单就是目标会话该加齐的输出（出处：android.hardware.camera2.CameraDevice#createCaptureSession）
- 新增带 JPEG PhotoOutput 的探测会话取能力，正式会话 preview 与 photo 一并 commit：修复后的会话配置（出处：卡里修好并验证过）
未核实：commit 失败由只含输入提交还是同会话重复 addInput 触发，卡里没逐项区分；卡里的行为出自目标 SDK 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-7ef1335447ade047f4c7（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
