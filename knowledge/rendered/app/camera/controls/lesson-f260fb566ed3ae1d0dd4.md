# Camera2 手动曝光、ISO、对焦迁到 CameraKit 时按 d.ts 注释换单位与值域，能力读回与设定下发对称换算

## 何时使用

相机控制器实现与规格提取阶段，把源端 Camera2 的曝光时长、曝光补偿、ISO 与对焦距离的能力范围和设定映射到 CameraKit 会话接口（手动曝光、ISO、对焦接口自 API 24 起）时

## 适用情境

源端能力结构以 ns 记曝光时长、以整数档位加步长记曝光补偿、以上下限记 ISO、以屈光度记对焦距离（0 为无限远）；目标使用 HarmonyOS CameraKit 的 ManualExposure、AutoExposure、ManualIso、ManualFocus 接口，查 d.ts 时 grep 可能只返回方法签名、过滤掉方法上方的注释。

## 例外与边界

- 手动曝光时长、ISO、对焦距离、曝光偏置步长这些接口自 API 24 起才有：目标最低 API 低于 24 时按运行设备的 API 版本分支，低版本上对应的源端手动能力置为不支持、不下发；对焦距离先用 isFocusDistanceSupported 判断，返回 false 时同样置为不支持。曝光补偿（setExposureBias、getExposureBiasRange）不受此限。

## 原因

两端同名概念的单位、值域和前置条件都不同：只按签名移植时，换算只做在下发一侧、能力读回原样写进源单位字段，范围、默认值与滑杆刻度整体错位；把 EV 当档位、把离散 ISO 列表当连续范围、在 EXPOSURE_MODE_LOCKED 下设 ISO、按源端 0 下发无限远，设定会静默无效或方向相反。

## 做法

1. 读目标相机 d.ts 时连同方法上方注释一起读（grep 带前文行，或按接口整段读），逐项确认单位、值域与前置条件。按 OpenHarmony 文档 master 的 Camera Kit 参考（手动曝光、手动 ISO、手动对焦接口自 API 24 起）：曝光时长单位为 µs，setExposureDuration 只在 EXPOSURE_MODE_MANUAL 下生效；getExposureBiasRange 返回 EV 值，超出范围的补偿自动取就近临界点；getSupportedIsoRange 返回离散的标准 ISO 值；曝光模式为 EXPOSURE_MODE_LOCKED 时不支持 setIso（HarmonyOS 6.1.1(24) 的 d.ts 注释写的是只在 LOCKED 下生效，与文档相反，以文档为准）；setFocusDistance 取 0.0（最近）到 1.0（最远），默认 1.0，超出值域按边界值处理。
2. 能力范围、捕获结果读回与设定下发经同一接口时用同一换算，两侧对称：源字段以 ns 计时，读回 ×1000、下发 ÷1000。
3. 曝光补偿：档位范围取 ceil(最小 EV/step) 到 floor(最大 EV/step)（step 取 getExposureBiasStep），下发 setExposureBias(档位 × step)。ISO：过滤正值、排序后取首尾作上下限；设 ISO 时曝光模式不处于 EXPOSURE_MODE_LOCKED（该模式下不支持设置 ISO），手动曝光时长先切到 EXPOSURE_MODE_MANUAL，恢复自动用 EXPOSURE_MODE_CONTINUOUS_AUTO。对焦：源端屈光度越大越近、0 为无限远，目标方向相反，无限远下发 1.0。
4. 规格提取时，实现映射表为每个手动参数写出源端与目标端的单位、值域、换算点和模式前置条件，不只抄源端字面值（如“无限远 → 0”）。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、2 步〕ManualExposureQuery.getSupportedExposureDurationRange、ManualExposure.getExposureDuration 与 setExposureDuration 的曝光时长单位都是微秒（API 24 起，超出本机 SDK 的 API 23）
- 〔做法第 1、3 步〕setExposureDuration 只在 ExposureMode.EXPOSURE_MODE_MANUAL（手动曝光，API 24 起，超出本机 SDK 的 API 23）下设置生效
- 〔适用情境 / 做法第 2 步〕安卓 SENSOR_EXPOSURE_TIME 与 SENSOR_INFO_EXPOSURE_TIME_RANGE 的单位是纳秒
- 〔做法第 3 步〕AutoExposure.setExposureBias 的参数是曝光补偿值（EV），范围由 getExposureBiasRange 查询，超出范围时自动匹配到就近临界点；补偿存在随设备不同的步长，例如步长 0.5 时设 1.2 实际生效 1.0
- 〔做法第 3 步〕ManualExposureQuery.getExposureBiasStep 返回曝光偏置步长（API 24 起，超出本机 SDK 的 API 23）
- 〔适用情境 / 做法第 3 步〕安卓 CONTROL_AE_COMPENSATION_STEP 是曝光补偿可调的最小步长，单位 EV；CONTROL_AE_EXPOSURE_COMPENSATION 的单位是这个步长的档数
- 〔做法第 3 步〕ManualFocus.setFocusDistance 取值 [0.0, 1.0]，0.0 是镜头能对焦的最短距离，1.0 是最远距离，默认 1.0，超出值域按边界值处理（API 24 起，超出本机 SDK 的 API 23）
- 〔适用情境 / 做法第 3 步〕安卓 LENS_FOCUS_DISTANCE 为 0.0f 表示无限远对焦，设定值被限制在 [0.0f, LENS_INFO_MINIMUM_FOCUS_DISTANCE] 内
- 〔做法第 3 步〕ManualIsoQuery.getSupportedIsoRange 返回支持的标准 ISO 感光度值数组（API 24 起，超出本机 SDK 的 API 23）
- 〔原因 / 做法第 1、3 步〕ManualIso.setIso 的值要在 getSupportedIsoRange 范围内；文档写曝光模式为 EXPOSURE_MODE_LOCKED 时不支持设置 ISO（API 24 起，超出本机 SDK 的 API 23），HarmonyOS 6.1.1(24) 的 d.ts 注释写的是只在 LOCKED 下生效，两者相反，以文档为准
- 〔适用情境 / 做法第 3 步〕安卓 SENSOR_INFO_SENSITIVITY_RANGE 是 Range<Integer>，取值是 ISO 12232:2006 定义的标准 ISO 感光度
- 〔做法第 3 步〕ExposureMode.EXPOSURE_MODE_AUTO 设置后只对设置后的首次拍照生效；EXPOSURE_MODE_CONTINUOUS_AUTO 会随每次环境变化自动调整曝光；EXPOSURE_MODE_LOCKED 每次拍照默认锁定曝光
