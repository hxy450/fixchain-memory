# 媒体 URI 交给外部查看或分享的 Want：type 取该条媒体的精确 MIME，并附 FLAG_AUTH_READ_URI_PERMISSION

ID：`lesson-c78d27d0ebcb9885f3a0` · 版本：1

[本主题](index.md)

## 何时使用

系统集成实现阶段，把 Android 打开或分享媒体的 Intent（ACTION_VIEW、REVIEW、ACTION_SEND）翻译为 startAbility 的 Want，确定 uri、type、flags 与无媒体分支时

## 适用情境

源端用 MediaStore URI 打开最近的照片或视频，不设 MIME、由 URI 决定查看器，无媒体时回落到图库；分享依赖 ACTION_SEND 启动时把 EXTRA_STREAM 迁入 ClipData 并附读授权，源码里看不到显式授权标志。目标的媒体查询结果已能区分照片与视频（photoType、文件名）。

## 原因

写死 image/* 会把视频当图片打开，修复期日志还显示系统查看器拒绝通配 MIME、要求精确类型；只传 URI 会丢掉已查到的视频标记。目标不会像 ACTION_SEND 那样隐式授予接收方读权限，缺少授权标志时查看器或分享接收方读不到该 URI。

## 做法

1. 从当前媒体记录取类型（photoType，或扩展名经 UTD 推得的精确 MIME，如 image/jpeg、video/mp4），随 uri 一起交给拉起网关，不只传 URI。
2. 查看与分享的 Want 加 wantConstant.Flags.FLAG_AUTH_READ_URI_PERMISSION；规格映射 ACTION_SEND/ACTION_VIEW 时写明源端隐式授予的 URI 读权限。
3. 源端无 URI 或打开失败时的回落（如打开图库）照迁为等价入口（拉起系统图库或 PhotoViewPicker），不改成直接返回。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-3d6568f13ae09eb5090d](../../../store/cases/case-3d6568f13ae09eb5090d/5b4001738169878d739ff6bd72c53837c9acf050eccc463cd5ec04292cc96963.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`5b4001738169878d739ff6bd72c53837c9acf050eccc463cd5ec04292cc96963`
