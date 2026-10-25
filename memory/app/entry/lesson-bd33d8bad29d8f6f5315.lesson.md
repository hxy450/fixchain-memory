# 被第三方拉起并回传结果的入口：setResult+finish 映射为一次 terminateSelfWithResult，最终状态确定后从唯一出口回传

ID：`lesson-bd33d8bad29d8f6f5315` · 版本：1

[本主题](index.md)

## 何时使用

功能实现与接线阶段，移植源 Activity 响应第三方带结果请求（如 ACTION_IMAGE_CAPTURE、ACTION_VIDEO_CAPTURE）的结果回传、输出位置与限制参数时；判定这类入口的平台缺口时

## 适用情境

源端以 setResult(RESULT_OK/RESULT_CANCELED, data)+finish() 回传，可能在多处调用 setResult（后一次覆盖前一次，finish 幂等），并按 EXTRA_OUTPUT、时长/大小/质量限制或内联数据分支处理；目标由 Want 拉起，结果经 UIAbilityContext.terminateSelfWithResult 以 AbilityResult 一次性返回。

## 原因

只调用 terminateSelf 时调用方收不到结果码与数据；把多处 setResult 直译成一次性终止回调会先到先终止，结果回传两次或空结果先以成功结束；写入分支各自收尾时，带调用方输出位置的分支写完不回传。以上游临时实现推断“平台无数据通道”，还会把没有回传数据的请求报成成功。

## 做法

1. 结果出口写成 terminateSelfWithResult({ resultCode, want: { uri, parameters } })；resultCode 取当前契约约定的成功与取消值，规格未另定时沿用源端 RESULT_OK=-1、RESULT_CANCELED=0 并写进契约。
2. 列出源端全部 setResult/finish 调用点，合并为一个在最终状态确定后调用的出口；空输出或失败按取消返回。
3. 每个请求分支按“写入完成 → 回传 → 结束”串起，先等保存完成再结束，带调用方输出位置的分支写完也走结果出口；结果通道经查证确实无法携带的数据（如内联位图）按取消返回并释放资源，不报成功。
4. 启动 Want 里的输出位置与时长、大小、质量限制注入到实际执行写入或录制的组件；写调用方提供的 URI 时打开其 fd 写入，失败清理不删除调用方的资产。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-76fcde297f6a5406e58f](../../../store/cases/case-76fcde297f6a5406e58f/4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d`
