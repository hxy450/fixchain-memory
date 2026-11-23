# 相机能力位与可选值按已提交会话的 isXxxSupported/getXxxRange 查询填写，SDK 声明了枚举或 setter 不等于支持

## 何时使用

相机能力探测实现阶段，为曝光/白平衡锁、色温、白平衡预设、录像中拍照、RAW 等支持位与可选值列表填值时；规格提取阶段把源端能力位规则写进目标契约时

## 适用情境

源端能力位来自 Camera2 CameraCharacteristics（可用 AE/AWB 模式、硬件等级、RAW_SENSOR 输出尺寸），或由源码硬编码为常量；目标 @ohos.multimedia.camera 的 d.ts 里可见 ExposureMode、WhiteBalanceMode 的 LOCKED、MANUAL 等枚举与对应 setter，会话接口以 interface Xxx extends XxxQuery 分出查询方法；规格可能给出条件式能力规则（多个条件缺一即 false、按硬件等级、尺寸只列 JPEG），也可能把源端常量写成“恒为 true”。

## 例外与边界

- 源端条件式能力里不属于相机特性的那部分（应用自己的开关、偏好、按机型的例外判断）照源端保留，并与目标查询结果相与；“找不到等价查询就置为不支持”只针对相机特性那部分，不要因此丢掉或改写应用侧条件。

## 原因

枚举值和 setter 只说明接口形状，当前设备与会话是否支持要由查询方法回答；按声明存在置 true、用固定数值范围或把所有 profile 计入尺寸列表，会在不支持的设备上暴露不可用的锁、预设与色温，或把无法保存的格式列为可选。源码里的硬编码能力位是源平台上的事实，原样写成跨平台契约后，下游会照抄常量。

## 做法

1. 每个支持位与可选值列表都对应一条运行期查询：在已提交配置的会话上调用查询接口（遇到 interface X extends XQuery 先展开 XQuery 找 isXxxSupported/getXxxRange），例如锁定位用 isExposureModeSupported(EXPOSURE_MODE_LOCKED)、isWhiteBalanceModeSupported(LOCKED)，色温支持与范围用 isWhiteBalanceModeSupported(MANUAL) 与 getWhiteBalanceRange()；随模式而定的能力（录像中拍照、可拍格式与尺寸）查对应 SceneMode 输出能力里的 photoProfiles 等。
2. 规格给出条件式能力时逐条找到目标查询再写；找不到等价查询就置为不支持并登记差异，不写常量 true 或固定范围。可选值列表（如白平衡预设）逐个模式查询后再暴露，解锁或会话重建时恢复用户所选模式与数值，不固定回到 AUTO。
3. 规格提取时，源码里硬编码的能力位写成“源端常量，目标端按会话查询”并给出目标查询 API，不写成跨平台恒定判定。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕AutoExposureQuery.isExposureModeSupported 在会话未配置时抛 7400103（只在会话上使用时抛）
- 〔原因 / 做法第 1、2 步〕WhiteBalanceQuery.isWhiteBalanceModeSupported 检测是否支持传入的白平衡模式，getWhiteBalanceRange 返回手动白平衡模式下白平衡值的范围；两者在会话未配置时抛 7400103
- 〔做法第 1 步〕CameraManager.getSupportedOutputCapability(camera, mode) 按相机设备和场景模式返回该模式下的输出能力（各模式的 profiles 分开给出）
