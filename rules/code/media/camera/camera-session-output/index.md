# Camera2 会话的输出配置和拍照数据

agent 会看到什么：读到 CameraDevice.createCaptureSession 一次带的预览、ImageReader、MediaRecorder surface，onImageAvailable 里复制 JPEG 后 image.close()，DngCreator 写 RAW；产物里 beginConfig / addInput / addOutput / commitConfig 的次序、photoAvailable 里 getComponent 后的 byteBuffer 和 photo.release()、.dng 媒体资产

## 规矩

- rule-9b6ea7c9cdac｜源端会话一次带齐预览和 JPEG 输出时，目标在同一次 beginConfig 里加齐再 commitConfig｜读到：源端 CameraDevice.createCaptureSession 一次传入预览 surface 和 ImageReader（JPEG）的 surface，录像态再加 MediaRecorder 的 surface；写错：只 addInput 就 commitConfig，之后在同一会话上再 beginConfig、重复 addInput 并只加 previewOutput；或拍照时才惰性 addOutput(photoOutput) 重配会话
- rule-e0d0d55f8c92｜photoAvailable 的 byteBuffer 要异步消费时，先 slice(0) 复制再释放 Photo｜读到：源端 onImageAvailable 里先把 JPEG 复制成 byte[] 再 image.close()；目标的保存服务把字节排进后台队列异步保存；写错：photoAvailable 回调里 getComponent 之后立即 photo.release()，再把同一个 component.byteBuffer 交给异步保存，中间没有复制
- rule-61157202cf64｜目标端缺 DNG 封装时，RAW 保存在建媒体资产前返回失败，RAW 能力位置 false｜读到：源端用 DngCreator 把 RAW_SENSOR 数据写成 DNG；规格把 DngCreator 映射为「RAW 流 + DNG 封装自实现」并列为平台缺口候选；写错：把传感器原始缓冲直接写成 .dng / image/dng 媒体资产并返回成功；能力探测因有 DNG profile 就上报支持 RAW，图片尺寸列表混进 DNG 尺寸
- rule-adc2a115e3c8｜源端用数值 JPEG 质量时，以 QUALITY_LEVEL_HIGH 拍摄，保存时按数值质量重编码｜读到：源端拍照按偏好里的数值 JPEG 质量（0–100）出图；写错：拍照路径只调 photoOutput.capture()，不带 PhotoCaptureSetting，数值质量没有任何地方生效；规格没写 CameraKit 只有三档质量
