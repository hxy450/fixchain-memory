# 录像输出的挂接和拆卸 hook 都返回 Promise，调用方先 await 拆卸再释放录制器

审的是：代码
触发（任一种）：
- 写错的样子：挂接 hook 是 async 并被 await，拆卸 hook 却定义成 () => void；拆卸插在 recorder.release() 之后，或拆卸里 session.stop()、output.release() 只发起不等待
适用范围：为异步会话重建接录像输出的挂接、拆卸 hook 并跨文件接线时
做法：
- 挂接和拆卸 hook 都返回 Promise；拆卸里按 videoOutput.stop() → session.stop() → output.release() 等逐步 await
- 调用方顺序：await 拆卸录像输出 → await recorder.release() → 再重开或重连相机
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stop(): Promise<void>：VideoOutput 停止录像输出（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，VideoOutput.stop）
- release(): Promise<void>：CameraOutput 释放输出（VideoOutput 继承它）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraOutput.release）
- release(): Promise<void>：AVRecorder 释放录制资源，之后不能再操作这个实例（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.release）
- 拆卸 hook 改为返回 Promise，先 await 拆卸再释放录制器：改后的做法，保留到最终（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自 HarmonyOS 6.1.1（API 24），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-b89cd099bfa87829fd2d（opencamera-hmos）：做法第 1 步 ← 建议 5、诊断；做法第 2 步 ← 建议 5、诊断；取值 4 ← 诊断
