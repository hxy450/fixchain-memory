# 媒体 URI 交给外部查看或分享的 Want：type 取该条媒体的精确 MIME，并附 FLAG_AUTH_READ_URI_PERMISSION

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕系统查看器收到 type 为 image/* 的 Want 时拒绝打开，要求 image/jpeg 这样的精确 MIME
- 〔做法第 2 步〕wantConstant.Flags.FLAG_AUTH_READ_URI_PERMISSION 表示授予对方对 Want 里 URI 的读权限
- 〔适用情境 / 原因〕android-36.1 源码中，ACTION_SEND 带 EXTRA_STREAM 启动时框架把它迁入 ClipData，Intent 没带 FLAG_GRANT_READ_URI_PERMISSION 时自动加上；系统开关 implicitUriGrantsRestrictedForSendAction 打开时跳过这次隐式授权
