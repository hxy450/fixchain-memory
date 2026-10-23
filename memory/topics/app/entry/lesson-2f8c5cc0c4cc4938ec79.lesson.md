# 源端以 setResult(code, data)+finish() 回传外部请求结果时，合并为一次 terminateSelfWithResult

ID：`lesson-2f8c5cc0c4cc4938ec79` · 版本：1 · 阶段：spec/execute · 主题：[app/entry](index.md)

概要：多处 setResult 合并为一次带结果结束

信号：`setResult`, `RESULT_OK`, `RESULT_CANCELED`, `terminateSelfWithResult`, `AbilityResult`, `terminateSelf`, `ACTION_IMAGE_CAPTURE`, `ACTION_VIDEO_CAPTURE`, `EXTRA_OUTPUT`, `EXTRA_DURATION_LIMIT`, `EXTRA_SIZE_LIMIT`, `EXTRA_VIDEO_QUALITY`

## 何时使用

规格提取、功能实现与接线阶段，迁移外部拍摄、选取一类结果型请求的结果回传、输出位置与限制参数时

## 适用情境

源 Activity 响应 ACTION_IMAGE_CAPTURE/ACTION_VIDEO_CAPTURE 等结果型 intent，读 EXTRA_OUTPUT、EXTRA_VIDEO_QUALITY、EXTRA_DURATION_LIMIT、EXTRA_SIZE_LIMIT，在保存或录像完成处 setResult(RESULT_OK/RESULT_CANCELED, data)+finish()，可能有多处 setResult；目标 UIAbility 由 want 拉起，结果经 UIAbilityContext.terminateSelfWithResult 回传 AbilityResult。

## 原因

terminateSelf() 不携带结果，调用方收不到结果码与 uri。Android 中后一次 setResult 覆盖前一次、finish 幂等；把多个调用点照搬到“先到先终止”的一次性出口，会提前以空 uri 报成功或重复结束。请求参数没有从 launch want 注入保存与录像管线时，输出位置与时长、大小、质量限制都被忽略。

## 做法

1. 把 setResult(code, data)+finish() 映射为 terminateSelfWithResult({ resultCode, want: { uri } })（UIAbilityContext.d.ts，API 24）；resultCode 按调用方约定，没有约定时沿用 Android 的 RESULT_OK=-1、RESULT_CANCELED=0（android.app.Activity 常量）；结果函数里的成功标志与 uri 必须写进 AbilityResult。
2. 列出源端全部 setResult/finish 调用点，合并为唯一的最终出口：等保存或录像完成后再结束，空 uri 或失败按取消结束，出口防重入。
3. 按源端逐分支写“写入 → 回传 → 结束”：带 EXTRA_OUTPUT 的分支写入调用方 URI（截断打开，不删除调用方资产）完成后同样回传；调用方要求的数据确实无法经 want 传回（如 inline-data 位图）时按取消结束，不以成功码结束。
4. 从 launch want 读 EXTRA_OUTPUT、EXTRA_VIDEO_QUALITY、EXTRA_DURATION_LIMIT、EXTRA_SIZE_LIMIT 并注入保存与录像管线；为这些参数预留的注入接口要有调用方，不在录像器里留默认空值了事。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [下“不存在”结论前确认检索覆盖完整声明与范围](../../process/unverified-as-fact/lesson-8b7a50eeb92fc3bdb1e7.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-76fcde297f6a5406e58f](../../../../store/cases/case-76fcde297f6a5406e58f/4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d.json) · 结论：diagnosis, rec-14644f84a3, rec-fe58acf0a3, rec-ec1e3e8b64, rec-c6fa6bda54, rec-50093589aa
  卡片版本：`4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d`
