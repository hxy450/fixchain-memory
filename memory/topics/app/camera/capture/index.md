# app/camera/capture

拍照触发与结果链：完成/失败回传与多帧交付、前屏补光、照片缓冲释放与资产回调

[上一级](../index.md)

## 本级经验

- [Photo 字节先复制或用完再 release，不释放后用](lesson-c81407857f6e70183c27.lesson.md) · 阶段：spec/execute · 信号：photoAvailable, Photo.release, getComponent, byteBuffer
- [前屏补光保留控制器判定出口与回退等待](lesson-b20eaa8108cae9476ca3.lesson.md) · 阶段：execute/repair · 信号：CONTROL_AE_PRECAPTURE_TRIGGER, CONTROL_AE_STATE, LENS_FACING_FRONT, FLASH_MODE_CLOSE
- [拍照桥接保留完成失败回传，多帧模式整组交付](lesson-91d254bb9a5187884b4b.lesson.md) · 阶段：spec/execute · 信号：takePicture, captureBurst, CaptureCallback, onCaptureCompleted
- [资产回调无请求 ID 时一拍一输出，超时退役不串帧](lesson-8a1d50b9fdcdee8a5752.lesson.md) · 阶段：execute/repair · 信号：photoAssetAvailable, PhotoOutput, captureStartWithInfo, captureEnd
