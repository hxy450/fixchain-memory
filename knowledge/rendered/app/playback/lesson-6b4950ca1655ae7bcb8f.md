# 视频页按对应源 Activity 绑定 surface，源端等比适配时 XComponent 按视频宽高比内接

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 androidx.media3:media3-ui 1.9.3。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕AVPlayer.surfaceId 可在 initialized 状态设置；在 initialized 状态设置过之后，prepared、playing、paused、completed、stopped 状态下可再次设置
- 〔原因 / 做法第 2 步〕应用没有设置 AVPlayer.videoScaleType 时取 VIDEO_SCALE_TYPE_FIT：内容拉伸铺满显示区域，视频宽高比与区域不同时不保持比例
- 〔做法第 2 步〕AVPlayer.on('videoSizeChange') 只在视频播放场景支持，默认只在 prepared 状态上报一次，HLS 码流分辨率变化时也会上报
- 〔做法第 2 步〕AVPlayer.width、height 单位为 px，prepared 之后有效，可在 prepared、playing、paused、completed 状态查询
- 〔适用情境 / 做法第 2 步〕media3-ui 1.9.3 的 PlayerView 在布局里没写 app:resize_mode 时取 0（fit，按视频宽高比内接）；resize_mode 的取值为 fit=0、fixed_width=1、fixed_height=2、fill=3、zoom=4
- 〔原因〕XComponent 宽高直接写成 100%×100% 铺满、视频宽高比与区域不同时（如横屏），画面被拉伸
