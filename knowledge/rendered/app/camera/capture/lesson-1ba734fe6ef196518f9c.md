# 录制器原生时长/文件大小上限改由应用层定时器或轮询承接时，按不含暂停的已录时长计时，并照源端 onInfo 各分支停止或续录

## 何时使用

规格提取与录像功能实现阶段，用应用层定时器、文件大小轮询替代 MediaRecorder.setMaxDuration/setMaxFileSize 及其 onInfo 回调时

## 适用情境

源端由录制器自行计时计量并回调 onInfo（MAX_DURATION_REACHED、MAX_FILESIZE_APPROACHING/REACHED、NEXT_OUTPUT_FILE_STARTED），pause/resume 只累计已录时长，按偏好决定到达上限后续录还是停止；目标 AVRecorder 启停为异步 Promise，上限改由 setTimeout 或 statSize 轮询合成事件。

## 例外与边界

- 源端把时长或文件大小上限设为 0 或负数（即关闭上限，常见于偏好里的“不限”）时，目标对应地不安排定时器、不做大小轮询，不要换成某个默认上限。

## 原因

一次性墙钟定时器把暂停区间计入时长上限；合成的文件上限事件只在“自动续录”分支处理时，未开续录到达上限仍继续录制。替代机制只换了检测方式，源端每个事件分支的后果仍要保留。

## 做法

1. 时长预算用不含暂停的已录时长：开始或恢复时按“上限 − 已录时长”安排定时器，暂停时清除定时器并累计已录区间，pause/resume 防重入；保留原生时长上限（AVRecorderConfig.maxDuration，单位秒）时，声明和文档都没写明它是否计入暂停区间，同样按上面的已录时长另设定时器。
2. 合成上限事件后，按源端 onInfo 完整的 if/else 链分派：开启续录走重启，未开启则停止录制；读源端事件分发函数时读完整个分支链。规格映射表登记替代方式及其暂停、停止语义，每个 what 分支写验收或写明跳过理由。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕MediaRecorder.setMaxDuration 的单位是毫秒（0 或负数关闭上限）；到达上限时 OnInfoListener 收到 MEDIA_RECORDER_INFO_MAX_DURATION_REACHED，录制被停止，停止是异步发生的
- 〔适用情境 / 做法第 2 步〕MediaRecorder.setMaxFileSize 的单位是字节（0 或负数关闭上限）；到达上限时 onInfo 收到 MEDIA_RECORDER_INFO_MAX_FILESIZE_REACHED，录制被停止，停止是异步发生的
- 〔做法第 1 步〕AVRecorderConfig.maxDuration（API 18 起）单位是秒，有效范围 [1, 2^31-1]，无效值重置为最大值；录到设定时长后自动停止，经 stateChange 回调 AVRecorderState 为 'stopped'、StateChangeReason 为 BACKGROUND
- 〔做法第 2 步〕fs 的 Stat.size 是文件大小，单位字节，只对普通文件有效
