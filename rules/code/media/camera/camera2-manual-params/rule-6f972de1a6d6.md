# Camera2 参数键迁到鸿蒙手动相机控制时，先查齐两端单位和取值形态，下发读回都换算

审的是：代码
触发（任一种）：
- 读到：源端用 CaptureRequest / CameraCharacteristics 的数值键（曝光时长、补偿档位、ISO 范围、对焦距离）下发参数和探测能力；写错的样子：ManualExposure / AutoExposure / ManualIso / ManualFocus 的 set… / getSupported… 原样传源端数值，或把返回值原样存进源端单位的字段
适用范围：Camera2 的手动曝光、曝光补偿、ISO、对焦迁到鸿蒙相机会话时
做法：
- 源端读该键在 CaptureRequest / CameraCharacteristics 里的注释：Units、Range of valid values、Key 的类型（Range<…>、Rational 步长）
- 目标读对应方法的文档或 d.ts：参数和返回值的单位（微秒、EV、归一化 0.0–1.0）、返回的是 [min, max] 还是标准值数组、方向是否相反
- 能力探测、读回、下发三处写同一套显式换算，并用 mock 的能力范围做最小检查
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SENSOR_EXPOSURE_TIME 的 Units 是 Nanoseconds；setExposureDuration 的参数单位是微秒：例：手动曝光时长两端差 1000 倍，下发 /1000、读回 ×1000（出处：android.hardware.camera2.CaptureRequest#SENSOR_EXPOSURE_TIME；arkts-apis-camera-ManualExposure.md，setExposureDuration）
针对本应用要查的：
- 源端每个参数键的单位和取值形态：Android 框架源码 android.hardware.camera2.CaptureRequest / CameraCharacteristics 里该键的注释（按应用的 compileSdk 取对应平台）；读 Units、Range of valid values 和 Key 的泛型类型
- 目标对应方法的单位和返回形态：Camera Kit 参考文档 arkts-apis-camera-*.md 或鸿蒙 SDK 的 @ohos.multimedia.camera.d.ts，按方法名找；读参数和返回值说明里的单位、取值范围，以及返回的是范围还是标准值数组
未核实：ManualExposure、ManualIso、ManualFocus 和 getExposureBiasStep 在本机鸿蒙 SDK（API 23）里没有声明，单位按文档副本核
来源：1 张卡，1 个应用
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 1
