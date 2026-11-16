# 拍照前 setRotation 的 JPEG 角度，目标用 getPhotoRotation 填 rotation

审的是：代码
触发（任一种）：
- 读到：源端拍照函数本体里先 `setRotation(getImageVideoRotation())` 或给 `CaptureRequest.JPEG_ORIENTATION` 设值，再拍照；写错的样子：目标端 `photoOutput.capture(...)` 的 `PhotoCaptureSetting` 里没有 `rotation`，拍照前不下发旋转
- 读到：源端拍照前 `setRotation(getImageVideoRotation())` 或设 `CaptureRequest.JPEG_ORIENTATION`；写错的样子：`PhotoCaptureSetting.rotation` 直接填源端算出的 JPEG 角度换成的 `ImageRotation`，没有经过 `getPhotoRotation`
适用范围：把安卓相机拍照的 JPEG 旋转迁到鸿蒙 CameraKit 的 PhotoOutput 时
做法：
- 移植拍照函数时定位并读完源函数本体，逐行对照它的副作用，拍照前的 setRotation 不能只凭调用方或函数名漏掉
- 按前后摄换算出设备角度 deviceDegree，`const r = photoOutput.getPhotoRotation(deviceDegree)`，再 `photoOutput.capture({ rotation: r, … })`；单拍和连拍前都要做
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getPhotoRotation(deviceDegree?: number): ImageRotation：PhotoOutput 按设备当前旋转角度算照片旋转角（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.getPhotoRotation）
- rotation?: ImageRotation：PhotoCaptureSetting 的照片旋转字段（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoCaptureSetting.rotation）
- ImageRotation.ROTATION_0 = 0、ROTATION_90 = 90、ROTATION_180 = 180、ROTATION_270 = 270：旋转枚举的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，ImageRotation）
- capture(setting: PhotoCaptureSetting): Promise<void>：带设置拍照（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.capture）
- jpegOrientation = (sensorOrientation + deviceOrientation + 360) % 360：源端 JPEG 角度已经含传感器角度，不能直接当鸿蒙的 rotation（出处：android.hardware.camera2.CaptureRequest#JPEG_ORIENTATION）
- 未调 getPhotoRotation、直接填绝对角度时，原生层再叠加传感器角度，照片侧转：改成 getPhotoRotation(deviceDegree) 后方向正确（出处：卡里修好并验证过）
- getVideoRotation(deviceDegree?: number): ImageRotation：同族接口：VideoOutput 的录像旋转角（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，VideoOutput.getVideoRotation）
- getPreviewRotation(displayRotation?: number): ImageRotation：同族接口：PreviewOutput 的预览旋转角（参数是屏幕旋转角）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PreviewOutput.getPreviewRotation）
针对本应用要查的：
- 设备角度 deviceDegree 怎么得到、前后摄怎么处理：源工程里计算拍照旋转角的方法（读方向监听的值、区分前后摄的那段）；取其中设备方向的部分（不含传感器角度）作为 deviceDegree 传给 getPhotoRotation
未核实：前后摄换算 deviceDegree 的具体公式卡里没写；卡里的行为出自鸿蒙 SDK API 24（6.1.1），本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-ef167da8e80990c31714（opencamera-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 4、诊断；取值 6 ← 诊断
