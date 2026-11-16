# Camera2 无限远对焦（距离 0）迁到 setFocusDistance 时下发 1.0

审的是：代码
触发（任一种）：
- 读到：源端无限远对焦下发 CaptureRequest.LENS_FOCUS_DISTANCE = 0（屈光度，0.0f 为无限远）；写错的样子：无限远对焦写成 setFocusDistance(0)，或读回时把 0 当无限远
适用范围：把 Camera2 手动对焦距离迁到 HarmonyOS 相机会话的 ManualFocus（文档标 API 24+）时
做法：
- 无限远下发 setFocusDistance(1.0)，读回 1.0 时识别为无限远；其他手动距离按「0.0 最近、1.0 最远」反向对应源端屈光度（源端 0 是最远）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setFocusDistance(distance: number): void，取值 [0.0, 1.0]，0.0 是最短对焦距离，1.0 是最远，默认 1.0：目标对焦距离是归一化、方向与屈光度相反（出处：arkts-apis-camera-ManualFocus.md，setFocusDistance）
- LENS_FOCUS_DISTANCE：A value of 0.0f means infinity focus：源端 0 是无限远（出处：android.hardware.camera2.CaptureRequest#LENS_FOCUS_DISTANCE）
- 无限远对焦下发 1.0，读回时区分无限远：修好的写法（出处：卡里修好并验证过）
未核实：本机 SDK 是 API 23，没有 ManualFocus 的声明，按文档副本核；屈光度到 0..1 的具体换算公式卡里没写
来源：1 张卡，1 个应用
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；取值 3 ← 诊断
