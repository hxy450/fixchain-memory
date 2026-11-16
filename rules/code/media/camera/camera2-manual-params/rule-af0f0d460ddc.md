# Camera2 ISO 上下限迁到 getSupportedIsoRange 时过滤正值排序取首尾

审的是：代码
触发（任一种）：
- 读到：源端 CameraCharacteristics.SENSOR_INFO_SENSITIVITY_RANGE（Range<Integer> 上下限）；写错的样子：把 getSupportedIsoRange() 返回值的 iso[0]、iso[1] 当最小、最大 ISO
适用范围：把 Camera2 ISO 能力迁到 HarmonyOS 相机会话的 ManualIso（文档标 API 24+）时
做法：
- getSupportedIsoRange() 的结果过滤出正值、升序排序，取第一个作最小 ISO、最后一个作最大 ISO；setIso 的值取自这个列表
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getSupportedIsoRange(): number[]：获取支持的标准ISO感光度值数组：返回离散的标准值列表，不是 [min, max]（出处：arkts-apis-camera-ManualIsoQuery.md，getSupportedIsoRange）
- setIso(iso: number): void，设置的值需在 getSupportedIsoRange 范围内：ManualIso 下发 ISO（出处：arkts-apis-camera-ManualIso.md，setIso）
- SENSOR_INFO_SENSITIVITY_RANGE: Range<Integer>，取值是标准 ISO 感光度：源端是上下限（出处：android.hardware.camera2.CameraCharacteristics#SENSOR_INFO_SENSITIVITY_RANGE）
- ISO 取正值排序后的首尾：修好的写法（出处：卡里修好并验证过）
未核实：本机 SDK 是 API 23，没有 ManualIso 的声明，按文档副本核
来源：1 张卡，1 个应用
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
