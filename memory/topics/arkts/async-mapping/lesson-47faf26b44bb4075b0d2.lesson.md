# 源 API 用返回值表示“被拒”、用异常表示故障，而目标 SDK 两者都 reject 时，用一个单次原语适配器还原三态，所有重试与返回码路径都经它

ID：`lesson-47faf26b44bb4075b0d2` · 版本：2 · 阶段：execute · 主题：[arkts/async-mapping](index.md)

概要：被拒与故障都 reject 时用单次适配器还原三态

信号：`BusinessError`, `Promise<void>`, `IOException`, `TagLostException`, `MIFARE`

## 何时使用

服务或引擎实现阶段，把以 boolean 返回业务结果、以异常表示 I/O 失败或目标丢失的源 API（如 MIFARE 扇区认证）映射到只以 Promise reject 报错的 SDK，并实现带重试或返回码的上层方法时

## 适用情境

源方法返回 false 表示被拒并据此按偏好重试，只有 IOException、TagLostException 等才立即失败；目标方法返回 Promise<void>，被拒与 I/O、状态异常都以 BusinessError reject，d.ts 只列错误码、不说明各码对应哪种情形；同一文件里可能已有区分两者的单次函数，却只被部分路径调用。

## 原因

上层直接 await SDK、任何 reject 都立即返回失败时，“被拒后重试”分支永远走不到，重试偏好在这些路径上失效；自检只核单次函数与源码形状一致时发现不了。错误码语义未经文档说明时，按单个码分流也只是假设。来源中引擎 worker 在笔记里写明“认证失败与 IO 错同为 reject”，也写了区分两者的单次函数，主认证方法仍对所有 reject 直接返回 false，读扇区、写块等路径都失去重试。

## 做法

1. 写一个单次原语适配器：成功返回 true，被拒返回 false，丢失等故障抛出；所有带重试或返回码的上层方法（认证、读扇区、写块等）都经它，不在上层 catch 全部 reject 后直接返回。
2. 按规格判定用例逐条走读：例如“偏好开、重试 2 次、持续失败 → 恰 3 次”，确认持续失败在目标表现为 reject 时代码确实进入后续轮次。
3. 适配器依赖 d.ts 未说明语义的错误码区分被拒与故障时，把码值假设写进真机待验项，并配合连接或在场复核等独立信号，不只靠单个码分流。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [源端可观察缺陷照迁并核次数，修正走待批决策](../../process/unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-68b0d7a44f60b8170647](../../../../store/cases/case-68b0d7a44f60b8170647/1a6362abd01bf2efef12a84518e969b1cc7e4a2a05d94027ccdca22adb072d44.json) · 结论：diagnosis, rec-2ae06c8af5, rec-e65652a212, rec-9eb57b45fc
  卡片版本：`1a6362abd01bf2efef12a84518e969b1cc7e4a2a05d94027ccdca22adb072d44`
