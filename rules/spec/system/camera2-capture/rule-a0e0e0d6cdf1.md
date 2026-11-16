# 源码硬编码的能力位写进目标契约时，注明「源端常量，目标端按会话查询」并给查询 API

审的是：规格
触发（任一种）：
- 读到：源端能力探测里把某些支持位直接写成 true（如曝光锁、白平衡锁支持位）；写错的样子：规格契约写成「曝光锁 / AWB 锁支持位恒为 true」这类跨平台恒真判定，没写目标端怎么查
适用范围：规格里写设备能力位契约和验收条目的那一节
做法：
- 契约写「源端常量，目标端按会话查询」，并给出目标查询 API：曝光锁 isExposureModeSupported(ExposureMode.EXPOSURE_MODE_LOCKED)，白平衡锁 isWhiteBalanceModeSupported(WhiteBalanceMode.LOCKED)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- isExposureModeSupported(aeMode: ExposureMode): boolean；isWhiteBalanceModeSupported(mode: WhiteBalanceMode): boolean：契约里要写的目标查询（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，AutoExposureQuery.isExposureModeSupported、WhiteBalanceQuery.isWhiteBalanceModeSupported）
来源：1 张卡，1 个应用
- case-168300edfa3644b0f14a（opencamera-hmos）：做法第 1 步 ← 建议 3、建议 1
