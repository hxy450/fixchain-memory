# 相机能力位取自会话查询，不因有某枚举或 setter 就置 true

审的是：代码
触发（任一种）：
- 读到：源端能力位来自 CameraCharacteristics（CONTROL_AWB_AVAILABLE_MODES、INFO_SUPPORTED_HARDWARE_LEVEL），规格给出条件式能力规则；写错的样子：因 WhiteBalanceMode 等枚举有 LOCKED、MANUAL 或有 setWhiteBalance 就把能力位写成常量 true，色温范围写死
- 读到：SDK 声明里 interface WhiteBalance extends WhiteBalanceQuery 这类写法；写错的样子：没有调用 isExposureModeSupported / isWhiteBalanceModeSupported / getWhiteBalanceRange
适用范围：Camera2 能力探测迁到 @ohos.multimedia.camera 时（白平衡查询 @since 20，出自声明）
做法：
- 支持位取自会话或模式输出能力的查询：曝光锁 isExposureModeSupported(ExposureMode.EXPOSURE_MODE_LOCKED)，白平衡锁 isWhiteBalanceModeSupported(WhiteBalanceMode.LOCKED)，色温 isWhiteBalanceModeSupported(WhiteBalanceMode.MANUAL) + getWhiteBalanceRange()，录像中拍照看 NORMAL_VIDEO 模式有没有 JPEG photoProfiles
- 遇到 X extends XQuery 时先展开 Query 接口找查询方法
- 规格的条件式能力逐条找目标端等价查询；找不到就置 false 并在差异记录里登记，不写常量 true 或固定范围
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- isExposureModeSupported(aeMode: ExposureMode): boolean，会话未配置时抛 7400103：AutoExposureQuery 上的曝光模式查询，要在已提交的会话上调（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，AutoExposureQuery.isExposureModeSupported）
- ExposureMode.EXPOSURE_MODE_LOCKED = 0：曝光锁对应的模式（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，ExposureMode.EXPOSURE_MODE_LOCKED）
- isWhiteBalanceModeSupported(mode: WhiteBalanceMode): boolean；getWhiteBalanceRange(): Array<number>：WhiteBalanceQuery 上的白平衡模式查询和色温范围（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，WhiteBalanceQuery）
- WhiteBalanceMode：AUTO = 0、CLOUDY = 1、INCANDESCENT = 2、FLUORESCENT = 3、DAYLIGHT = 4、MANUAL = 5、LOCKED = 6（@since 20）：枚举里有不等于设备支持，要逐个查询（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，WhiteBalanceMode）
- getSupportedOutputCapability(camera: CameraDevice, mode: SceneMode): CameraOutputCapability；SceneMode.NORMAL_VIDEO = 2：按模式取输出能力，录像模式下看 photoProfiles 里有没有 JPEG（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，CameraManager.getSupportedOutputCapability、SceneMode.NORMAL_VIDEO）
- 改用 isExposureModeSupported / isWhiteBalanceModeSupported、getWhiteBalanceRange 和录像模式的 JPEG photoProfiles 得到能力位：修好后的写法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK 6.1.1(24)，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-168300edfa3644b0f14a（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 6 ← 诊断
