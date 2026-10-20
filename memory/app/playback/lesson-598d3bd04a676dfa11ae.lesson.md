# 源端退后台不停播时，AVPlayer 接入 AVSession 与音频长时任务，并声明后台模式与权限

ID：`lesson-598d3bd04a676dfa11ae` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段为 MediaPlayer/ExoPlayer 写 AVPlayer 映射行与生命周期验收时；服务实现阶段接入 AVPlayer，并向配置写者交接 module.json5 声明时

## 适用情境

源端在页面或宿主里内联播放音频（录音附件等），宿主 onPause/onStop 不调用 pause/stop/release，只有显式停止、播完或退出才停，退后台后继续播到结束；目标 AVPlayer 未接 AVSession、未申请长时任务，module.json5 也没有 backgroundModes 与 KEEP_BACKGROUND_RUNNING。

## 原因

HarmonyOS 的后台音频要同时具备 AVSession 与音频播放类长时任务（含 module.json5 的 backgroundModes 与 KEEP_BACKGROUND_RUNNING 权限），缺一项退后台就被系统静音暂停。映射行不看宿主生命周期就写成“行为等价”，源端跨后台的播放在目标成了缺失功能。

## 做法

1. 写映射行前查宿主 onPause/onStop/onDestroy 与 stop/release 的全部调用方：生命周期里不停播，就在验收中写明“切后台继续播放至结束”，接入方式按后台播放设计。
2. 进入播放时 avSession.createAVSession(context, tag, 'audio') 并 setAVPlaybackState、activate，同时 backgroundTaskManager.startBackgroundRunning(context, BackgroundMode.AUDIO_PLAYBACK, wantAgent)；停止、播完、出错与宿主销毁时 stopBackgroundRunning 并销毁会话。
3. 在承载的 UIAbility 写 backgroundModes: ['audioPlayback']，requestPermissions 加 ohos.permission.KEEP_BACKGROUND_RUNNING；本任务不能改 module.json5 时，把这两项连同运行时权限按所用 skill 的配置清单逐项写进移交，由配置写者按同一清单落地。
4. 接入后系统播控中心出现会话卡片是后台播放的平台形态，不作为不接入的理由；确要不同取舍时先在真机比对源端与目标退后台的表现，再作为差异决策登记。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-1dee716aadc97af875f2](../../../store/cases/case-1dee716aadc97af875f2/4cbf9374789dfcc6a399b52446f467b4097a36c7cb3b873e72d9dafb28a6769a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`4cbf9374789dfcc6a399b52446f467b4097a36c7cb3b873e72d9dafb28a6769a`
