# Coil 全局 ImageLoader 的占位、错误图与解码器写进图片契约：没装 GIF 解码器时只显示动图首帧

ID：`lesson-544f9fa8eff09aca5f52` · 版本：2

[本主题](index.md)

## 何时使用

规格提取阶段整理图片加载管线与设置位归属时；界面实现阶段把 Coil AsyncImage 映射为 ArkUI Image 时

## 适用情境

Android 图片组件经应用的 ImageLoaderFactory 或 Coil.setImageLoader 加载，默认 loader 设 placeholder、error、crossfade 并只装部分解码器，autoPlayGifs 一类设置位切换到带 GIF 解码器的 loader；目标用 ArkUI Image（默认播放动图）与 alt 实现。

## 原因

Coil 默认 loader 没装 GIF 解码器时动图只出首帧；ArkUI Image 默认播放动图，按“与 Android 一样播放”写进规格或直接用 Image，设置位就失效。占位与错误图来自全局 loader 而不在组件调用处，只看调用点会漏掉；设置位行为在两个 feature 规格之间互相推给对方时，没有人实现。

## 做法

1. 规格先读 ImageLoaderFactory 与 setImageLoader 调用点，把默认 loader 的 placeholder、error、crossfade、已装解码器及切换 loader 的设置位写进图片管线验收；只有用带 GIF 解码器的 loader 的界面才写“动图播放”。
2. 设置位关闭时（如 autoPlayGifs=false），目标对动图源解码首帧显示（如取首帧 PixelMap），不让 Image 直接播放。
3. 规格把设置位行为推给另一 feature 时，先在对方规格核到对应的行为验收（不只是持久化），没有就由本 feature 认领。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-af4252d474c172e093fc](../../../store/cases/case-af4252d474c172e093fc/cbb8ea02978ec26f3c0634ccd8741583db0582686b51cc563af4b5a5325614d1.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`cbb8ea02978ec26f3c0634ccd8741583db0582686b51cc563af4b5a5325614d1`
