# 源端相机能力 getter 读打开期缓存时，目标在会话 commit 后快照一次，getter 只读内存

审的是：代码
触发（任一种）：
- 读到：源端打开相机时调一次 CameraManager#getCameraCharacteristics（或包它的能力枚举）存进字段，能力 getter 只返回这个字段；写错的样子：目标的能力 getter 每次调用都执行 cameraManager.getSupportedOutputCapability(...) 和 session.isFocusModeSupported(...)、getExposureBiasRange() 等同步查询，只在注释里说有缓存
- 读到：UI 访问器、定时绘制（setInterval、onDraw 回调）或会话切换的代码里调用控制器的能力 getter；写错的样子：被调用的 getter 实现里含 session.isFocusModeSupported(...) 或 cameraManager.getSupportedOutputCapability(...) 这类同步相机服务调用
适用范围：把安卓相机控制器里读打开期缓存的能力 getter 迁成 HarmonyOS 相机实现时
做法：
- 在初次 photo 会话 await session.commitConfig() 之后，调一次 getSupportedOutputCapability 和会话上的各项能力查询，存成能力快照；公开 getter 只返回快照
- 显示尺寸、zoom 这类派生值在内存里更新；快照未就绪时 throw 明确的错误，不返回部分结果
- UI 绘制、定时器、访问器消费控制器值前，看 getter 里有没有 session. 或 manager. 的调用；有就改读快照或缓存
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getSupportedOutputCapability(camera: CameraDevice, mode: SceneMode): CameraOutputCapability：同步返回的能力查询（返回值不是 Promise）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraManager.getSupportedOutputCapability）
- isFocusModeSupported(afMode: FocusMode): boolean；会话没配置时抛 7400103 Session not config：会话上的能力查询是同步的，并依赖会话已 commit（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，FocusQuery.isFocusModeSupported）
- getExposureBiasRange(): Array<number>；同样在会话没配置时抛 7400103：同类的会话能力查询（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，AutoExposureQuery.getExposureBiasRange）
- commitConfig(): Promise<void>：会话配置提交，快照在它完成之后读（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.commitConfig）
- 初次 photo 会话 commit 后读一次能力快照、派生值在内存派生、未就绪抛异常；关闭期间旧 UI 引用读取要兼容：返修后的做法（出处：卡里修好并验证过）
未核实：卡里的上机行为出自 HarmonyOS 6.1.1(24)，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-d160173a312daca7fc69（opencamera-hmos）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 4；取值 5 ← 诊断
