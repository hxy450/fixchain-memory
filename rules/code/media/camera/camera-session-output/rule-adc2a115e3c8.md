# 源端用数值 JPEG 质量时，以 QUALITY_LEVEL_HIGH 拍摄，保存时按数值质量重编码

审的是：代码
触发（任一种）：
- 读到：源端拍照按偏好里的数值 JPEG 质量（0–100）出图；写错的样子：拍照路径只调 photoOutput.capture()，不带 PhotoCaptureSetting，数值质量没有任何地方生效；规格没写 CameraKit 只有三档质量
适用范围：把源端数值 JPEG 质量迁到鸿蒙相机拍照和保存时
做法：
- 拍照写 photoOutput.capture({ quality: camera.QualityLevel.QUALITY_LEVEL_HIGH, … })
- 保存时按源端的数值质量重编码：packer.packToData(源图, { format: 'image/jpeg', quality: <数值质量> })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- QualityLevel：QUALITY_LEVEL_HIGH = 0、QUALITY_LEVEL_MEDIUM = 1、QUALITY_LEVEL_LOW = 2：相机拍照只有三档质量，没有数值质量（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.QualityLevel）
- PhotoCaptureSetting.quality?: QualityLevel：拍照设置里的质量字段（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.PhotoCaptureSetting.quality）
- capture(setting: PhotoCaptureSetting): Promise<void>：带设置拍照（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.PhotoOutput.capture）
- PackingOption.quality: number，0–100 的整数，越大越好；PackingOption.format: string，MIME 如 image/jpeg：重编码时数值质量写在这里（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，image.PackingOption）
- packToData(source: PixelMap, options: PackingOption): Promise<ArrayBuffer>：ImagePacker 按 PackingOption 编码（另有 ImageSource 作源的重载）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，image.ImagePacker.packToData）
未核实：卡里把这一项列在未单独成链的目标里，修好后的画质没有单独复测记录；卡里上机看到的行为出自 HarmonyOS API 24，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-91084f18203ecc5e7036（opencamera-hmos）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断
