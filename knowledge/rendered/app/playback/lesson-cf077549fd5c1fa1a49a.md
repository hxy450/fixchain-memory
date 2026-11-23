# 源端依赖缓冲态、缓冲位或多卡共享播放器时用 AVPlayer + XComponent，不选 ArkUI Video 组件

## 何时使用

规格提取与界面、功能实现阶段，为视频查看器与列表内嵌视频选定播放器路线，并映射缓冲状态、缓冲位置、共享播放器与前后台暂停时

## 适用情境

源端用 ExoPlayer/media3：Player.Listener 区分 BUFFERING/READY、轮询 bufferedPosition、Lifecycle ON_PAUSE/ON_RESUME 暂停恢复，列表内多张卡共享一个播放器；目标决策基线写 AVPlayer，但页面规格或先生成的页面把 Video 组件列为可选或先例。

## 例外与边界

- AVPlayer 的 on('bufferingUpdate') 只在网络播放场景上报；源端播放的是本地文件或本地 fd 时，第 2 步的缓冲态、缓冲位映射拿不到数据，不能单凭它选路线，按共享实例、前后台暂停恢复等其余能力判断；源端这些能力都没用到时，原有的 Video 组件实现不必改。

## 原因

Video 组件没有缓冲事件与缓冲位置，每张卡各自一个解码器；选了它就只能把缓冲位写成播放位、缓冲态缺失，并以“与先前页面一致”为由保留到交付。规格写成“Video 组件（或 AVPlayer）”时，实现者会选更省事的一边。

## 做法

1. 写播放器决策前列出源端用到的播放器能力（缓冲态、缓冲位、共享实例、前后台暂停恢复），逐项核对候选组件的公开 API；需要这些能力时把 AVPlayer + XComponent(SURFACE) 写成唯一路线。
2. 实现时把 on(bufferingUpdate) 的 BUFFERING_START/END 映射为加载与就绪，CACHED_DURATION 加 currentTime 得缓冲位；占位注明“缓冲回调可用则升级”的，条件成立就升级，并一并改造先前页面。
3. 多卡共享一个播放器时，在全局状态保留一个 AVPlayer 会话，按 owner 绑定或解绑当前卡的 surface，暴露 getOrCreate 与 release。
4. ON_PAUSE/ON_RESUME 同时覆盖应用切后台与页面被覆盖：接 applicationStateChange，以及 NavDestination onHidden/onShown（或 navDestinationSwitch）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕AVPlayer.on('bufferingUpdate') 只在网络播放场景支持
- 〔做法第 2 步〕BufferingInfoType 用于网络播放：BUFFERING_START=1、BUFFERING_END=2、BUFFERING_PERCENT=3、CACHED_DURATION=4，CACHED_DURATION 上报的缓存时长单位是毫秒
- 〔做法第 2 步〕AVPlayer.currentTime 是当前播放位置，单位毫秒，可在 prepared、playing、paused、completed 状态查询；-1 表示无效值，直播模式下默认返回 -1
- 〔做法第 3 步〕AVPlayer.surfaceId 在 initialized 状态设置过之后，prepared、playing、paused、completed、stopped 状态下可再次设置
- 〔原因 / 做法第 1 步〕ArkUI Video 组件的事件只有 onStart、onPause、onFinish、onFullscreenChange、onPrepared、onSeeking、onSeeked、onUpdate、onError、onStop，没有缓冲事件，也拿不到缓冲位置
- 〔做法第 4 步〕从 API 21 起 NavDestination 的 onShown、onHidden 回调带 VisibilityChangeReason：TRANSITION=0 为页面跳转，CONTENT_COVER=1 为全模态开关，APP_STATE=2 为前后台切换引起的可见性变化
