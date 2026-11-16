# capture result 字段由 onCaptureCompleted 写入时，目标订阅 ISO 和曝光事件写缓存

审的是：代码
触发（任一种）：
- 读到：源端 getter 返回的字段在 CameraCaptureSession.CaptureCallback#onCaptureCompleted 里从 TotalCaptureResult 的 CaptureResult.SENSOR_SENSITIVITY / SENSOR_EXPOSURE_TIME 写入；写错的样子：目标 getter 写成 this.session?.getIso() 或 getExposureDuration() 即时同步查询，名字还叫 CaptureResult
适用范围：把安卓逐帧回调写入的 capture result 缓存字段（ISO、曝光时间等）迁成 HarmonyOS 相机实现时
做法：
- 先打开源端赋值点确认值来自 onCaptureCompleted 逐帧回调，再在目标 SDK 里按事件找对应通道（ISO 用 onIsoInfoChange，曝光用 onExposureInfoChange），不只按 getter 名搜
- 会话启动后用 session.onIsoInfoChange((info) => { 缓存 = info.iso }) 和曝光事件写缓存；会话停止、替换、暂停时取消订阅并清空；getter 只读缓存
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onIsoInfoChange(callback: Callback<IsoInfo>): void；offIsoInfoChange(callback?: Callback<IsoInfo>): void（@since 22）：订阅和取消 ISO 变化事件（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，VideoSession.onIsoInfoChange）
- interface IsoInfo { readonly iso?: number }：事件里带的 ISO 值，可能缺省（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，IsoInfo）
- onCaptureCompleted(CameraCaptureSession session, CaptureRequest request, TotalCaptureResult result)：源端每次拍摄完整结束、结果元数据齐全时回调，字段是逐帧写入的缓存（出处：android.hardware.camera2.CameraCaptureSession.CaptureCallback#onCaptureCompleted）
- CaptureResult.SENSOR_SENSITIVITY：Key<Integer>（android.sensor.sensitivity）：源端 ISO 的来源键（出处：android.hardware.camera2.CaptureResult#SENSOR_SENSITIVITY）
- 订阅 onIsoInfoChange / onExposureInfoChange 写缓存，会话停止、替换、暂停清空，getter 只读缓存后，定时绘制不再卡主线程：返修后的做法（出处：卡里修好并验证过）
未核实：本机 API 23 的声明里只有 VideoSession 上的 onIsoInfoChange / offIsoInfoChange；卡里用的 onExposureInfoChange、getIso、getExposureDuration 及其在 photo 会话上的可用性出自 HarmonyOS 6.1.1(24)，本机没核到
来源：1 张卡，1 个应用
- case-d160173a312daca7fc69（opencamera-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 诊断、建议 1；取值 5 ← 诊断
