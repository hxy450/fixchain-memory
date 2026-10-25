# Camera2 手动曝光、ISO、对焦迁到 CameraKit 时按 d.ts 注释换单位与值域，能力读回与设定下发对称换算

ID：`lesson-f260fb566ed3ae1d0dd4` · 版本：1

[本主题](index.md)

## 何时使用

相机控制器实现与规格提取阶段，把源端 Camera2 的曝光时长、曝光补偿、ISO 与对焦距离的能力范围和设定映射到 CameraKit 会话接口时

## 适用情境

源端能力结构以 ns 记曝光时长、以整数档位加步长记曝光补偿、以上下限记 ISO、以屈光度记对焦距离（0 为无限远）；目标使用 HarmonyOS CameraKit 的 ManualExposure、AutoExposure、ManualIso、ManualFocus 接口，查 d.ts 时 grep 可能只返回方法签名、过滤掉方法上方的注释。

## 原因

两端同名概念的单位、值域和前置条件都不同：只按签名移植时，换算只做在下发一侧、能力读回原样写进源单位字段，范围、默认值与滑杆刻度整体错位；把 EV 当档位、把离散 ISO 列表当连续范围、不锁曝光就设 ISO、按源端 0 下发无限远，设定会静默无效或方向相反。

## 做法

1. 读目标相机 d.ts 时连同方法上方注释一起读（grep 带前文行，或按接口整段读），逐项确认单位、值域与前置条件。HarmonyOS 6.1.1(24) 的 @ohos.multimedia.camera.d.ts 中：曝光时长单位为 µs；getExposureBiasRange 返回 EV 值；getSupportedIsoRange 返回离散的标准 ISO 值；setIso 只在 EXPOSURE_MODE_LOCKED 下生效；setFocusDistance 取 0.0（最近）到 1.0（最远）。
2. 能力范围、捕获结果读回与设定下发经同一接口时用同一换算，两侧对称：源字段以 ns 计时，读回 ×1000、下发 ÷1000。
3. 曝光补偿：档位范围取 ceil(最小 EV/step) 到 floor(最大 EV/step)（step 取 getExposureBiasStep），下发 setExposureBias(档位 × step)。ISO：过滤正值、排序后取首尾作上下限；设 ISO 前切到 EXPOSURE_MODE_LOCKED，恢复自动用 EXPOSURE_MODE_CONTINUOUS_AUTO。对焦：源端屈光度越大越近、0 为无限远，目标方向相反，无限远下发 1.0。
4. 规格提取时，实现映射表为每个手动参数写出源端与目标端的单位、值域、换算点和模式前置条件，不只抄源端字面值（如“无限远 → 0”）。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-aa27ff1b39767c02b1ec](../../../../store/cases/case-aa27ff1b39767c02b1ec/906e11a6d4db8499a201fa89399af8ef69da0775c2f68d23df299780adb7c59b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`906e11a6d4db8499a201fa89399af8ef69da0775c2f68d23df299780adb7c59b`
