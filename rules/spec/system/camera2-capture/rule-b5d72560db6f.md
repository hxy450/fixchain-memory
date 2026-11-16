# 规格的实现映射表为每个手动相机参数写出两端单位、值域、换算点和读回接口

审的是：规格
触发（任一种）：
- 读到：源端用 Camera2 的 SENSOR_EXPOSURE_TIME、CONTROL_AE_COMPENSATION_RANGE、SENSOR_INFO_SENSITIVITY_RANGE、LENS_FOCUS_DISTANCE 表达手动参数；写错的样子：映射表只列接口名，没写目标单位和值域（曝光时长微秒、补偿 EV、ISO 离散列表、对焦 0.0 最近），验收条目只写源端字面值（如无限远 → 距离 0）；没列捕获结果读回接口
适用范围：规格提取阶段写相机手动参数的实现映射表和验收条目时
做法：
- 每个手动参数写出源端与目标端单位、值域和换算点：ns↔µs、档位↔EV、屈光度↔归一化反向距离、范围↔离散列表，以及模式前置条件
- 下游需要的捕获结果读回（ISO、曝光时长）列出控制器接口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 曝光时长：getSupportedExposureDurationRange / getExposureDuration / setExposureDuration 单位微秒：映射表里曝光时长那一行的目标单位（出处：arkts-apis-camera-ManualExposure.md，setExposureDuration）
- 曝光补偿：setExposureBias 的参数是 EV 值：补偿那一行的目标单位（出处：arkts-apis-camera-AutoExposure.md，setExposureBias）
- ISO：getSupportedIsoRange 返回标准 ISO 值数组：ISO 那一行的目标值域（出处：arkts-apis-camera-ManualIsoQuery.md，getSupportedIsoRange）
- 对焦：setFocusDistance 取值 [0.0, 1.0]，0.0 最近、1.0 最远：对焦那一行的目标值域（出处：arkts-apis-camera-ManualFocus.md，setFocusDistance）
未核实：本机 SDK 是 API 23，ManualExposure、ManualIso、ManualFocus 按文档副本核
来源：1 张卡，1 个应用
- case-aa27ff1b39767c02b1ec（opencamera-hmos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
