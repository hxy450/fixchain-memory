# 源端 Camera2 相机的能力位、手动参数和采集回调

agent 会看到什么：读到源端 Camera2 相机代码：能力探测里写死为 true 的支持位、SENSOR_EXPOSURE_TIME 这类手动参数、靠 AE 状态驱动的前屏补光、onImageAvailable 里先复制字节再 image.close()；规格的契约、映射表或 AC 写成恒真判定、只列接口名、只写「AE 状态不可观测 → 近似」或只抽出「立即 close」，没写目标端的查询接口、单位值域、回退时序和释放顺序

## 通用查法

### 源端 Camera2 的能力键和手动参数键，规格写目标会话上的查询接口、单位和值域

审的是：规格
触发（任一种）：
- 读到：源端用 Camera2 的 CameraCharacteristics 能力键（CONTROL_AE_LOCK_AVAILABLE、SENSOR_INFO_SENSITIVITY_RANGE）或 CaptureRequest 的手动参数键（SENSOR_EXPOSURE_TIME、LENS_FOCUS_DISTANCE），或在能力探测里把支持位直接写成 true；写错的样子：规格的映射表、能力契约或验收条目只列接口名、照搬源端字面值或常量，没写目标端按会话查询的接口、目标单位和值域
适用范围：规格里写相机能力位、手动参数映射表和对应验收条目时
做法：
- 每个源端键在鸿蒙 Camera Kit 里找同一功能的会话接口：能力位找 …Query 上的 is…Supported 或 getSupported…Range，手动参数找 set… / get…；契约写「源端常量，目标端按会话查询」并给出这个接口
- 从目标接口的参数说明读出单位和值域，映射行写两端单位、值域和换算点，下游要读回的值列出控制器接口
针对本应用要查的：
- 源端相机键在目标端对应的查询或设置接口，以及它的单位和值域：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，按功能名（Exposure、Iso、Focus、WhiteBalance）找会话上的 …Query 和 set / get 方法；Camera Kit 文档 apis-camera-kit 目录下同名接口的 arkts-apis-camera-*.md；读方法签名和参数表里写的单位、取值范围，逐项写进映射行。例：曝光锁是否支持查 AutoExposureQuery.isExposureModeSupported(ExposureMode.EXPOSURE_MODE_LOCKED)；ManualExposure.setExposureDuration 的单位是微秒
未核实：Camera2 其余能力键（对焦模式、闪光灯等）在目标端是否都有对应的 …Query 查询，族里规矩没有核实
来源：2 张卡，1 个应用
- case-168300edfa3644b0f14a（opencamera-hmos）：做法第 1 步 ← 建议 3
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 2 步 ← 建议 3

## 规矩

- rule-a0e0e0d6cdf1｜源码硬编码的能力位写进目标契约时，注明「源端常量，目标端按会话查询」并给查询 API｜读到：源端能力探测里把某些支持位直接写成 true（如曝光锁、白平衡锁支持位）；写错：规格契约写成「曝光锁 / AWB 锁支持位恒为 true」这类跨平台恒真判定，没写目标端怎么查
- rule-9f00adf098f9｜CameraKit 没有 AE 状态事件时，规格写明前屏补光等待的回退时序和触发方｜写错：规格或源码理解笔记只写「AE 状态不可观测 → 走 fake-precapture 近似」，没写补光等待的回退时长、与 AE 驱动时序的差异，也没说由谁触发
- rule-b5d72560db6f｜规格的实现映射表为每个手动相机参数写出两端单位、值域、换算点和读回接口｜读到：源端用 Camera2 的 SENSOR_EXPOSURE_TIME、CONTROL_AE_COMPENSATION_RANGE、SENSOR_INFO_SENSITIVITY_RANGE、LENS_FOCUS_DISTANCE 表达手动参数；写错：映射表只列接口名，没写目标单位和值域（曝光时长微秒、补偿 EV、ISO 离散列表、对焦 0.0 最近），验收条目只写源端字面值（如无限远 → 距离 0）；没列捕获结果读回接口
- rule-bfd0d8a29030｜抽取原生图像回调时，规格把「先复制字节再 close」写成验收条目｜读到：源端 onImageAvailable 里先把 JPEG 复制到 byte[] 再 image.close()；写错：规格只抽出「无回调时立即 close」，没有「先复制字节再 close / release」的验收条目
