# 相机能力位与可选值按已提交会话的 isXxxSupported/getXxxRange 查询填写，SDK 声明了枚举或 setter 不等于支持

ID：`lesson-1c175988beebe0d7c4dc` · 版本：1

[本主题](index.md)

## 何时使用

相机能力探测实现阶段，为曝光/白平衡锁、色温、白平衡预设、录像中拍照、RAW 等支持位与可选值列表填值时；规格提取阶段把源端能力位规则写进目标契约时

## 适用情境

源端能力位来自 Camera2 CameraCharacteristics（可用 AE/AWB 模式、硬件等级、RAW_SENSOR 输出尺寸），或由源码硬编码为常量；目标 @ohos.multimedia.camera 的 d.ts 里可见 ExposureMode、WhiteBalanceMode 的 LOCKED、MANUAL 等枚举与对应 setter，会话接口以 interface Xxx extends XxxQuery 分出查询方法；规格可能给出条件式能力规则（多个条件缺一即 false、按硬件等级、尺寸只列 JPEG），也可能把源端常量写成“恒为 true”。

## 原因

枚举值和 setter 只说明接口形状，当前设备与会话是否支持要由查询方法回答；按声明存在置 true、用固定数值范围或把所有 profile 计入尺寸列表，会在不支持的设备上暴露不可用的锁、预设与色温，或把无法保存的格式列为可选。源码里的硬编码能力位是源平台上的事实，原样写成跨平台契约后，下游会照抄常量。

## 做法

1. 每个支持位与可选值列表都对应一条运行期查询：在已提交配置的会话上调用查询接口（遇到 interface X extends XQuery 先展开 XQuery 找 isXxxSupported/getXxxRange），例如锁定位用 isExposureModeSupported(EXPOSURE_MODE_LOCKED)、isWhiteBalanceModeSupported(LOCKED)，色温支持与范围用 isWhiteBalanceModeSupported(MANUAL) 与 getWhiteBalanceRange()；随模式而定的能力（录像中拍照、可拍格式与尺寸）查对应 SceneMode 输出能力里的 photoProfiles 等。
2. 规格给出条件式能力时逐条找到目标查询再写；找不到等价查询就置为不支持并登记差异，不写常量 true 或固定范围。可选值列表（如白平衡预设）逐个模式查询后再暴露，解锁或会话重建时恢复用户所选模式与数值，不固定回到 AUTO。
3. 规格提取时，源码里硬编码的能力位写成“源端常量，目标端按会话查询”并给出目标查询 API，不写成跨平台恒定判定。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-168300edfa3644b0f14a](../../../../store/cases/case-168300edfa3644b0f14a/79e3a447504de5357a4bc6ac0687a348e9214a503b0e3ef26e892f4d596ce8b3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`79e3a447504de5357a4bc6ac0687a348e9214a503b0e3ef26e892f4d596ce8b3`
