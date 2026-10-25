# 录制器原生时长/文件大小上限改由应用层定时器或轮询承接时，按不含暂停的已录时长计时，并照源端 onInfo 各分支停止或续录

ID：`lesson-1ba734fe6ef196518f9c` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与录像功能实现阶段，用应用层定时器、文件大小轮询替代 MediaRecorder.setMaxDuration/setMaxFileSize 及其 onInfo 回调时

## 适用情境

源端由录制器自行计时计量并回调 onInfo（MAX_DURATION_REACHED、MAX_FILESIZE_APPROACHING/REACHED、NEXT_OUTPUT_FILE_STARTED），pause/resume 只累计已录时长，按偏好决定到达上限后续录还是停止；目标 AVRecorder 启停为异步 Promise，上限改由 setTimeout 或 statSize 轮询合成事件。

## 原因

一次性墙钟定时器把暂停区间计入时长上限；合成的文件上限事件只在“自动续录”分支处理时，未开续录到达上限仍继续录制。替代机制只换了检测方式，源端每个事件分支的后果仍要保留。

## 做法

1. 时长预算用不含暂停的已录时长：开始或恢复时按“上限 − 已录时长”安排定时器，暂停时清除定时器并累计已录区间，pause/resume 防重入；保留原生时长上限时，先在 d.ts 或文档确认它对暂停的计时语义再决定是否另设定时器。
2. 合成上限事件后，按源端 onInfo 完整的 if/else 链分派：开启续录走重启，未开启则停止录制；读源端事件分发函数时读完整个分支链。规格映射表登记替代方式及其暂停、停止语义，每个 what 分支写验收或写明跳过理由。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-be892688a05d8782271e](../../../../store/cases/case-be892688a05d8782271e/0ae36d4e4a546c82b4b5f7f45cbb7e9843fceab665aabf81d810a3236c2985c6.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`0ae36d4e4a546c82b4b5f7f45cbb7e9843fceab665aabf81d810a3236c2985c6`
