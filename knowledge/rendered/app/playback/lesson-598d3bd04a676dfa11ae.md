# 源端退后台不停播时，AVPlayer 接入 AVSession 与音频长时任务，并声明后台模式与权限

## 何时使用

规格提取阶段为 MediaPlayer/ExoPlayer 写 AVPlayer 映射行与生命周期验收时；服务实现阶段接入 AVPlayer，并向配置写者交接 module.json5 声明时

## 适用情境

源端在页面或宿主里内联播放音频（录音附件等），宿主 onPause/onStop 不调用 pause/stop/release，只有显式停止、播完或退出才停，退后台后继续播到结束；目标 AVPlayer 未接 AVSession、未申请长时任务，module.json5 也没有 backgroundModes 与 KEEP_BACKGROUND_RUNNING。

## 例外与边界

- AVPlayer 没有另设 audioRendererInfo 时，纯音频源的 usage 默认是 STREAM_USAGE_MUSIC（含视频的源默认 STREAM_USAGE_MOVIE），都属于媒体类，第 2 步的 AVSession 不能省；只有工程已把 usage 设成媒体类、游戏类以外的类型时，才只需音频播放类长时任务、不必接 AVSession。不要为省掉 AVSession 去改原有的 usage。

## 原因

HarmonyOS 在后台播放媒体类（流类型 STREAM_USAGE_MUSIC、STREAM_USAGE_MOVIE、STREAM_USAGE_AUDIOBOOK）和游戏类音频时，要同时具备 AVSession 与音频播放类长时任务（含 module.json5 的 backgroundModes 与 KEEP_BACKGROUND_RUNNING 权限），缺一项退后台就被系统静音挂起，切回前台才恢复；其他用户可感知的播放只需音频播放类长时任务。映射行不看宿主生命周期就写成“行为等价”，源端跨后台的播放在目标成了缺失功能。

## 做法

1. 写映射行前查宿主 onPause/onStop/onDestroy 与 stop/release 的全部调用方：生命周期里不停播，就在验收中写明“切后台继续播放至结束”，接入方式按后台播放设计。
2. 进入播放时 avSession.createAVSession(context, tag, 'audio') 并 setAVPlaybackState、activate，同时 backgroundTaskManager.startBackgroundRunning(context, BackgroundMode.AUDIO_PLAYBACK, wantAgent)；停止、播完、出错与宿主销毁时 stopBackgroundRunning 并销毁会话。
3. 在承载的 UIAbility 写 backgroundModes: ['audioPlayback']，requestPermissions 加 ohos.permission.KEEP_BACKGROUND_RUNNING；本任务不能改 module.json5 时，把这两项连同运行时权限按所用 skill 的配置清单逐项写进移交，由配置写者按同一清单落地。
4. 接入后系统播控中心出现会话卡片是后台播放的平台形态，不作为不接入的理由；确要不同取舍时先在真机比对源端与目标退后台的表现，再作为差异决策登记。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕应用在后台播放媒体类（流类型 STREAM_USAGE_MUSIC、STREAM_USAGE_MOVIE、STREAM_USAGE_AUDIOBOOK）和游戏类（STREAM_USAGE_GAME）音频时，必须接入 AVSession 并申请 AUDIO_PLAYBACK 类型长时任务；其他用户可感知的播放任务要在后台长时间运行时，只需申请 AUDIO_PLAYBACK 类型长时任务，无需接入 AVSession
- 〔原因〕不满足上述接入规范时，应用退至后台播放会被系统静音并挂起，直到切回前台才解除静音并恢复播放
- 〔做法第 2 步〕申请了 AUDIO_PLAYBACK 类型长时任务的应用退至后台时，如果设备上没有有效的音频播放，应用可能被系统挂起
- 〔做法第 2 步〕backgroundTaskManager.startBackgroundRunning 需要 ohos.permission.KEEP_BACKGROUND_RUNNING 权限
- 〔做法第 2 步〕AVSession 的 activate() 激活会话，激活后可设置元数据、播放状态、接收控制命令；文档的接入示例在注册元数据、控制命令之后调用 activate
- 〔做法第 3 步〕使用长时任务的 UIAbility 要在 module.json5 abilities 的 backgroundModes 里声明长时任务类型（字符串数组，可缺省，缺省为空），AUDIO_PLAYBACK 对应的配置项是 audioPlayback；同时要申请 ohos.permission.KEEP_BACKGROUND_RUNNING
- 〔做法第 3 步〕ohos.permission.KEEP_BACKGROUND_RUNNING 的权限级别是 normal，授权方式是系统授权（system_grant）
- 〔做法第 4 步〕从 API 20 开始，申请 AUDIO_PLAYBACK 长时任务但不接入 AVSession 时，后台任务模块在通知栏显示通知；接入 AVSession 后后台任务模块不发通知栏通知，由 AVSession 发送通知；API 19 及之前后台任务模块不在通知栏显示通知
- 〔原因〕只接前台 AVPlayer、未接 AVSession 和长时任务时，设备上应用退后台后播放被系统（AudioBackgroundManager）静音暂停，同一场景下安卓参照机继续播放
