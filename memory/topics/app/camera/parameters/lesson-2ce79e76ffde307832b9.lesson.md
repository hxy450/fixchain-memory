# Camera2 手动曝光、补偿、ISO、对焦参数映射到 CameraKit 时，按目标单位、值域与前置模式换算，范围读回与设定下发用同一换算

ID：`lesson-2ce79e76ffde307832b9` · 版本：1 · 阶段：spec/execute · 主题：[app/camera/parameters](index.md)

概要：手动参数按 CameraKit 单位与值域换算，读写同口径

信号：`SENSOR_EXPOSURE_TIME`, `CONTROL_AE_EXPOSURE_COMPENSATION`, `SENSOR_SENSITIVITY`, `LENS_FOCUS_DISTANCE`, `setExposureDuration`, `getSupportedExposureDurationRange`, `getExposureBiasStep`, `setExposureBias`, `getSupportedIsoRange`, `setIso`, `EXPOSURE_MODE_LOCKED`, `setFocusDistance`

## 何时使用

规格提取与相机控制器实现阶段，把源端曝光时长、曝光补偿、ISO、对焦距离的能力范围与设定映射到 CameraKit 会话接口，并写曝光面板的取值范围时

## 适用情境

源端 Camera2 以 ns 表示曝光时长、以整数档位加步长表示曝光补偿、以上下限表示 ISO、以屈光度表示对焦距离（0 为无限远）；目标 PhotoSession 的 ManualExposure、AutoExposure、ManualIso、ManualFocus 接口单位、值域与前置模式不同，同一接口既有范围查询或当前值读回，也有设定。

## 原因

目标方法签名只给 number，单位、值域与生效条件写在紧邻的注释里，grep 只取签名时容易按源端语义直传。只在下发侧换算、读回侧原样写入，会让能力范围与设定相差 1000 倍；把补偿值区间当档位、把离散 ISO 列表当上下限、在非锁定曝光模式下设 ISO、把无限远写成 0，都能编译但效果错误。

## 做法

1. 连同方法上方注释读 @ohos.multimedia.camera.d.ts（如 grep -B12），本条数值据 API 24 该文件。曝光时长：getSupportedExposureDurationRange、setExposureDuration、getExposureDuration 均为 µs（L6582、L6627）；源端 ns 下发时 /1000，范围与当前值读回写入 ns 字段时 ×1000，三处共用同一换算函数。
2. 曝光补偿：getExposureBiasRange（L3091）返回补偿值区间，不是档位索引；步长取 getExposureBiasStep（L6603）。源端档位 i 下发 i×step；把区间换成档位上下限时取 ceil(min/step) 与 floor(max/step)。
3. ISO：getSupportedIsoRange 返回离散的标准 ISO 值数组（L3767），过滤正值排序后取首尾作上下限；setIso 只在 EXPOSURE_MODE_LOCKED 下生效（L3800），先 setExposureMode(EXPOSURE_MODE_LOCKED) 再 setIso，恢复自动曝光用 EXPOSURE_MODE_CONTINUOUS_AUTO。
4. 对焦距离：setFocusDistance 取 0.0（最近可对焦距离）到 1.0（最远），默认 1.0（L3585、L3597），方向与屈光度相反；源端屈光度 0（无限远）下发 1.0，不下发 0。
5. 规格提取时在实现映射表为每个手动参数写出源端与目标端的单位、值域、换算点和模式前置条件，并列出下游需要的当前值读回接口（如当前 ISO、曝光时长）。

## 可选检查

- 能力探测单测：mock 的 getSupportedExposureDurationRange 返回 µs 区间时，写入 ns 字段的范围应为其 1000 倍

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [跨文件补实现的功能登记带负责方与验证的移交项](../../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../../../process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 1 张卡）
- [辅助谓词与 getter 读到定义再翻译，不按名字推断](../../../process/inferred-not-traced/lesson-b3f534eb740a768d95a6.lesson.md)（共享 1 张卡）
- [规格常量分应用参数与源平台取值，后者写目标取法](../../../process/unverified-as-fact/lesson-d280d90bb76be18536f6.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-aa27ff1b39767c02b1ec](../../../../../store/cases/case-aa27ff1b39767c02b1ec/906e11a6d4db8499a201fa89399af8ef69da0775c2f68d23df299780adb7c59b.json) · 结论：diagnosis, rec-c02635505f, rec-d9e998c9c0, rec-f6d5e3fb78
  卡片版本：`906e11a6d4db8499a201fa89399af8ef69da0775c2f68d23df299780adb7c59b`
