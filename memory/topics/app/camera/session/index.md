# app/camera/session

CameraKit 会话的输入输出组成、提交时机、拍照 profile、拆卸重建顺序与相机就绪时机

[上一级](../index.md)

## 本级经验

- [一次性拍照请求在相机就绪回调消费，不用页面显示](lesson-e3bf30ce225c1c8964aa.lesson.md) · 阶段：spec/execute · 信号：StateCallback.onOpened, onConfigured, CameraInput.open, aboutToAppear
- [会话一次配齐输出再提交，拍照档不硬限 JPEG](lesson-05cd365740c0003662a4.lesson.md) · 阶段：execute/repair · 信号：createCaptureSession, ImageReader, beginConfig, addInput
- [会话拆卸逐步 await，复用输入先 removeInput](lesson-50b1ee39a9ff2d60174e.lesson.md) · 阶段：execute · 信号：CameraDevice.close, CameraCaptureSession.close, Session.stop, Session.release
