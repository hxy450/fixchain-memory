# 手动 ISO 时先切曝光模式 LOCKED 再 setIso，恢复自动用 CONTINUOUS_AUTO

审的是：代码
触发（任一种）：
- 写错的样子：setIso(...) 前没有 setExposureMode(EXPOSURE_MODE_LOCKED)；退出手动 ISO 或 AE 解锁时写 setExposureMode(EXPOSURE_MODE_AUTO)
适用范围：把 Camera2 手动 ISO、AE 锁迁到 HarmonyOS 相机会话时的曝光模式切换
做法：
- 手动 ISO 或 AE 锁定时 setExposureMode(camera.ExposureMode.EXPOSURE_MODE_LOCKED) 再 setIso(iso)；否则 setExposureMode(camera.ExposureMode.EXPOSURE_MODE_CONTINUOUS_AUTO)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setExposureMode(aeMode: ExposureMode): void：AutoExposure 切曝光模式（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.AutoExposure.setExposureMode）
- EXPOSURE_MODE_LOCKED = 0、EXPOSURE_MODE_AUTO = 1、EXPOSURE_MODE_CONTINUOUS_AUTO = 2：曝光模式取值（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，camera.ExposureMode）
- EXPOSURE_MODE_AUTO 仅设置后的首次拍照生效；EXPOSURE_MODE_CONTINUOUS_AUTO 随环境变化持续调整：恢复自动曝光要用 CONTINUOUS_AUTO（出处：arkts-apis-camera-e.md，ExposureMode）
- 手动 ISO 或 AE 锁时切 LOCKED，否则 CONTINUOUS_AUTO：修好的写法（出处：卡里修好并验证过）
未核实：文档副本写 EXPOSURE_MODE_LOCKED 时不支持设置 ISO，与卡里做法相反；按卡里修好的做法写
来源：1 张卡，1 个应用
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
