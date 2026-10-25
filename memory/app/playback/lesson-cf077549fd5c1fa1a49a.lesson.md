# 源端依赖缓冲态、缓冲位或多卡共享播放器时用 AVPlayer + XComponent，不选 ArkUI Video 组件

ID：`lesson-cf077549fd5c1fa1a49a` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面、功能实现阶段，为视频查看器与列表内嵌视频选定播放器路线，并映射缓冲状态、缓冲位置、共享播放器与前后台暂停时

## 适用情境

源端用 ExoPlayer/media3：Player.Listener 区分 BUFFERING/READY、轮询 bufferedPosition、Lifecycle ON_PAUSE/ON_RESUME 暂停恢复，列表内多张卡共享一个播放器；目标决策基线写 AVPlayer，但页面规格或先生成的页面把 Video 组件列为可选或先例。

## 原因

Video 组件没有缓冲事件与缓冲位置，每张卡各自一个解码器；选了它就只能把缓冲位写成播放位、缓冲态缺失，并以“与先前页面一致”为由保留到交付。规格写成“Video 组件（或 AVPlayer）”时，实现者会选更省事的一边。

## 做法

1. 写播放器决策前列出源端用到的播放器能力（缓冲态、缓冲位、共享实例、前后台暂停恢复），逐项核对候选组件的公开 API；需要这些能力时把 AVPlayer + XComponent(SURFACE) 写成唯一路线。
2. 实现时把 on(bufferingUpdate) 的 BUFFERING_START/END 映射为加载与就绪，CACHED_DURATION 加 currentTime 得缓冲位；占位注明“缓冲回调可用则升级”的，条件成立就升级，并一并改造先前页面。
3. 多卡共享一个播放器时，在全局状态保留一个 AVPlayer 会话，按 owner 绑定或解绑当前卡的 surface，暴露 getOrCreate 与 release。
4. ON_PAUSE/ON_RESUME 同时覆盖应用切后台与页面被覆盖：接 applicationStateChange，以及 NavDestination onHidden/onShown（或 navDestinationSwitch）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-dfd68051bcdcc94eba9f](../../../store/cases/case-dfd68051bcdcc94eba9f/07a5310040b53c84865c2afcdfe94396e276549a1c5ea8d94f07ee774232607a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:6
  卡片版本：`07a5310040b53c84865c2afcdfe94396e276549a1c5ea8d94f07ee774232607a`
