# 跨文件接线时把视频档的尺寸和帧率、捕获率一路传到配置 VideoOutput 的地方

审的是：代码
触发（任一种）：
- 读到：上游接口收到整份视频档（含 videoFrameWidth、videoFrameHeight、videoFrameRate 和捕获率）；写错的样子：中间层挂视频输出的接口只收 surfaceId 和宽高，binder 只传 videoFrameWidth / videoFrameHeight，帧率在中间层被丢掉
适用范围：录像参数从上游控制器经引擎层、控制器层传到底层相机会话的接线
做法：
- 接线的每一层都带上帧率（和捕获率）参数，一直传到配置 VideoOutput 的地方，用于 frameRateRange 匹配和 videoOutput.setFrameRate(min, max)
- 释放视频输出的 detach 接口写成 async 返回 Promise，调用方 await
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setFrameRate(minFps: number, maxFps: number): void：VideoOutput 设帧率范围，传下来的帧率最终落在这里（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，VideoOutput.setFrameRate）
- attach 接口追加帧率参数串到配置视频输出处，binder 追加捕获率，detach 改为 async：修复后的接线（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-7ef1335447ade047f4c7（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 诊断；取值 2 ← 诊断
