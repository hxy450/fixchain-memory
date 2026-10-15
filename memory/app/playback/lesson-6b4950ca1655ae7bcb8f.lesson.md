# XComponent(SURFACE) 承载 AVPlayer 视频时，surfaceId 在 initialized 状态首次设置，绑定时机按对应源页面

ID：`lesson-6b4950ca1655ae7bcb8f` · 版本：2

[本主题](index.md)

## 何时使用

功能实现阶段，移植视频播放页的 surface 绑定时机时

## 适用情境

目标用 XComponent(SURFACE) 加共享 AVPlayer 引擎播放视频；源端多处播放页的 surface 绑定时机不同：有的在播放控制器就绪后直接挂接播放器，有的另加“surface 已创建且状态为 PLAYING”双守卫；规格可能把其中一页的守卫写成通用规则。

## 原因

AVPlayer 的 surfaceId 只能在 initialized 状态首次设置，之后才可在 prepared、playing 等状态重设（@ohos.multimedia.media.d.ts 的 surfaceId 注释）；套用“等 PLAYING 再挂”的守卫时，PLAYING 边沿已错过首次设置的时机，页面先于播放进入也会一直只有声音、画面黑屏。

## 做法

1. 以目标页对应的源页面为准确定绑定时机；源页面在控制器就绪即挂接时，XComponent onLoad 拿到 surfaceId 后无状态门地交给引擎。
2. surfaceId 须在设源后、prepare 之前（initialized 状态）首次设置；PLAYING 边沿只能重设已设过的 surface，保留状态门时也要先在 initialized 挂上。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：diagnosis, recommendation:4
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
