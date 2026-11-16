# 源端后台阻塞关相机时，目标释放返回 Promise，按输出、会话、输入逐步 await

审的是：代码
触发（任一种）：
- 读到：源端在后台线程（AsyncTask 等）里阻塞执行 Camera.stopPreview() 和 Camera.release()，完成后才置为已关闭并回调或重开；规格写「异步关闭完成后回调，reopen 时重开」；写错的样子：session.release()、cameraInput.close()、各 output 的 release() 只接 .catch( 不 await，释放方法签名是 void；或用 Promise.resolve().then(...) 包住 void 的释放调用冒充后台任务
适用范围：把安卓后台线程阻塞式关闭相机迁成 CameraKit 的 Promise 调用时
做法：
- 释放方法返回 Promise，按「录像输出 → session.stop() → 各 output.release() → session.release() → cameraInput.close()」逐步 await，每步单独 try/catch 记错后继续下一步
- 置为已关闭、关闭完成回调和 reopen 都放在这些 await 全部完成之后；关相机时先 await 停录（停录后不再重连相机），再走释放
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- close(): Promise<void>：CameraInput 关闭相机（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraInput.close）
- stop(): Promise<void>；release(): Promise<void>：Session 停止和释放会话（PhotoSession、VideoSession 继承 Session）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，Session.stop / Session.release）
- release(): Promise<void>：CameraOutput 释放输出；PreviewOutput、PhotoOutput、VideoOutput 都继承它（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraOutput.release）
- stop(): Promise<void>：VideoOutput 停止录像输出，拆录像输出时先调（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，VideoOutput.stop）
- 按「录像 → session.stop → outputs → session → input」串行 await 拆卸、全部完成后才置已关闭：改后的做法，保留到最终（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自 HarmonyOS 6.1.1（API 24），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-b89cd099bfa87829fd2d（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
