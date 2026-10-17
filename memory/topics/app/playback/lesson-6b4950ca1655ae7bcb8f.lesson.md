# 视频页按对应源 Activity 绑定 surface，XComponent 按视频宽高比内接

ID：`lesson-6b4950ca1655ae7bcb8f` · 版本：2 · 阶段：execute · 主题：[app/playback](index.md)

概要：surface 按对应源页绑定，画面等比内接

信号：`XComponent`, `SURFACE`, `surfaceId`, `AVPlayer`, `PLAYING`

## 何时使用

功能实现阶段，移植视频播放页的 surface 绑定时机与画面尺寸时

## 适用情境

源新版播放视图在控制器就绪后即挂接播放器、默认等比适配，旧版页另有“surface 就绪且 PLAYING”双守卫；目标用 XComponent(SURFACE) 加共享 AVPlayer 引擎。

## 原因

套用旧页的双守卫、又不在 PLAYING 边沿补挂时，页面先于播放进入就只有声音黑屏；XComponent 直接写满宽高会拉伸画面。

## 做法

1. 以目标页对应的源 Activity 为准绑定 surface；保留状态门时在状态回调的 PLAYING 边沿补挂，并先确认引擎能否在非 PLAYING 状态接收 surfaceId。
2. 按视频宽高比在根区域内接计算 XComponent 宽高。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [新旧两套实现并存时以当前构建启用的为基准](../../process/inferred-not-traced/lesson-2e8ffecce25935dda502.lesson.md)（共享 1 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](../../ui/layout/constraints/lesson-92aee54a305ea0bde363.lesson.md)（共享 1 张卡）
- [manifest 未声明的窗口缺省解析成目标值并指派](../entry/lesson-c1d7ec16bb02aa152c33.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5e35bb283520acf3bd35](../../../../store/cases/case-5e35bb283520acf3bd35/954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f.json) · 结论：diagnosis, rec-8297527649, rec-e810f7dda3
  卡片版本：`954c420a6eb53234d9a40e9851863e13e6a2b9e3e2195abc6f71fcfe048dcf4f`
