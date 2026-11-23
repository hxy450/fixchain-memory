# Coil 全局 ImageLoader 的占位、错误图与解码器写进图片契约：没装 GIF 解码器时只显示动图首帧

## 何时使用

规格提取阶段整理图片加载管线与设置位归属时；界面实现阶段把经应用自定义全局 ImageLoader 加载的 Coil AsyncImage 映射为 ArkUI Image 时

## 适用情境

Android 图片组件经应用的 ImageLoaderFactory 或 Coil.setImageLoader 加载，默认 loader 设 placeholder、error、crossfade 并只装部分解码器，autoPlayGifs 一类设置位切换到带 GIF 解码器的 loader；目标用 ArkUI Image（默认播放动图）与 alt 实现。

## 例外与边界

- 只对动图源取首帧，静态图照常用 Image；设置位打开、或界面本来就用带 GIF 解码器的 loader 时，直接用 Image 播放，Image 会在节点不可见时自行停止动画，不需要另写暂停逻辑
- 用 ImageSource 取首帧时 DecodingOptions.index 不写就是第 0 帧，不需要另设

## 原因

Coil 默认 loader 没装 GIF 解码器时动图只出首帧；ArkUI Image 默认播放动图，按“与 Android 一样播放”写进规格或直接用 Image，设置位就失效。占位与错误图来自全局 loader 而不在组件调用处，只看调用点会漏掉；设置位行为在两个 feature 规格之间互相推给对方时，没有人实现。

## 做法

1. 规格先读 ImageLoaderFactory 与 setImageLoader 调用点，把默认 loader 的 placeholder、error、crossfade、已装解码器及切换 loader 的设置位写进图片管线验收；只有用带 GIF 解码器的 loader 的界面才写“动图播放”。
2. 设置位关闭时（如 autoPlayGifs=false），目标对动图源解码首帧显示（如取首帧 PixelMap），不让 Image 直接播放。
3. 规格把设置位行为推给另一 feature 时，先在对方规格核到对应的行为验收（不只是持久化），没有就由本 feature 认领。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕Image 显示动图时，播放跟随节点可见性：节点可见（onVisibleAreaChange 判定的可见比例大于 0）时启动动画，不可见时停止；GIF 各帧时长取文件里的 delay time，小于等于 0 的按 100ms
- 〔做法第 2 步〕ImageSource 解码的 DecodingOptions.index 在应用没有另设时为 0，即第一帧；多帧动图取值范围为 [0, 帧数-1]
