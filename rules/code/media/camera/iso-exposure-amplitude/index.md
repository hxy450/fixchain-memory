# 手动 ISO、曝光、捕获结果和录音振幅

agent 会看到什么：读到源端 Camera2 的 CaptureResult（SENSOR_SENSITIVITY、SENSOR_EXPOSURE_TIME，在 onCaptureCompleted 里写入）、CONTROL_AE_MODE 手动曝光，或 MediaRecorder.getMaxAmplitude 采样；产物里 PhotoSession 的 setIso / setExposureMode、getIso / getExposureDuration / onIsoInfoChange，AVRecorder 的振幅读取，或这些数据源留着恒 0 的基类默认

## 规矩

- rule-458e1518530e｜源端读录音振幅和捕获结果 ISO/曝光时，目标接 AVRecorder 和 PhotoSession 的读接口｜读到：源端用 MediaRecorder.getMaxAmplitude() 采样录音振幅画振幅表；写错：目标振幅源保留基类默认（恒 0），注释写「AVRecorder 无 getMaxAmplitude 等价 API」
- rule-b849f1bde737｜capture result 字段由 onCaptureCompleted 写入时，目标订阅 ISO 和曝光事件写缓存｜读到：源端 getter 返回的字段在 CameraCaptureSession.CaptureCallback#onCaptureCompleted 里从 TotalCaptureResult 的 CaptureResult.SENSOR_SENSITIVITY / SENSOR_EXPOSURE_TIME 写入；写错：目标 getter 写成 this.session?.getIso() 或 getExposureDuration() 即时同步查询，名字还叫 CaptureResult
- rule-6a4d37668aed｜手动 ISO 时先切曝光模式 LOCKED 再 setIso，恢复自动用 CONTINUOUS_AUTO｜写错：setIso(...) 前没有 setExposureMode(EXPOSURE_MODE_LOCKED)；退出手动 ISO 或 AE 解锁时写 setExposureMode(EXPOSURE_MODE_AUTO)
