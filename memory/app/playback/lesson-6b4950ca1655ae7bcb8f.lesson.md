# 视频页按对应源 Activity 绑定 surface，源端等比适配时 XComponent 按视频宽高比内接

ID：`lesson-6b4950ca1655ae7bcb8f` · 版本：2

[本主题](index.md)

## 何时使用

功能实现阶段，移植视频播放页的 surface 绑定时机与画面尺寸时

## 适用情境

源新版播放视图在控制器就绪后即挂接播放器、默认等比适配，旧版页另有“surface 就绪且 PLAYING”双守卫；目标用 XComponent(SURFACE) 加共享 AVPlayer 引擎。

## 例外与边界

- 源端 PlayerView 设了 resize_mode（fill、zoom、fixed_width、fixed_height）或源页本来就铺满拉伸时，按源端那一种映射，不一律改成内接；裁切铺满对应 AVPlayer 的 VIDEO_SCALE_TYPE_FIT_CROP。
- 工程已把 AVPlayer.videoScaleType 设为 VIDEO_SCALE_TYPE_SCALED_ASPECT（API 20 起，等比缩放、短边居中）时，平台已经按宽高比内接，XComponent 可以铺满根区域，不必再按宽高比计算尺寸。

## 原因

套用旧页的双守卫、又不在 PLAYING 边沿补挂时，页面先于播放进入就只有声音黑屏；XComponent 直接写满宽高会拉伸画面。

## 做法

1. 以目标页对应的源 Activity 为准绑定 surface；保留状态门时在状态回调的 PLAYING 边沿补挂，并先确认引擎能否在非 PLAYING 状态接收 surfaceId。
2. 按视频宽高比在根区域内接计算 XComponent 宽高。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：diagnosis, recommendation:4, recommendation:5
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
