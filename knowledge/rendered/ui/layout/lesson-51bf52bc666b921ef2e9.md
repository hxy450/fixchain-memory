# values-sw<N>dp(-land) 覆盖按设备屏幕短边 min(宽,高) 判定再叠加方向，不译成 mediaquery min-width

## 何时使用

规格提取与界面实现阶段，把源端 sw<N>dp 限定目录（可带 -land/-port）的覆盖值落成运行期分支时

## 适用情境

源 res 有 values-sw720dp-land 一类最小宽度限定目录，覆盖尺寸、边距等取值，注释常写“for sw720dp devices (e.g. 10" tablets)”；目标没有对应资源限定词，要在运行期按屏幕配置取值，可用 mediaquery 或 display 查询；规格里写成“横屏 + 最小宽度≥N”。

## 例外与边界

- 源限定目录是 values-w<N>dp、values-h<N>dp（当前可用宽高）：按当前窗口宽高取值，不按短边

## 原因

sw<N>dp 比较的是 smallestScreenWidthDp：两种方向下应用可用宽高的最小值（targetSdk<35 时扣除系统栏等窗口 insets，≥35 时按整窗），约等于设备屏幕短边，与方向无关：手机横屏时当前宽可以超过平板阈值，短边却远小于它。ArkUI mediaquery 的 min-width/width 比较当前窗口宽，把“最小宽度≥N”对译成 (min-width: Nvp) 会让手机横屏也命中平板覆盖值。规格的中文“最小宽度”与媒体特性 min-width 同名，容易被直接对译。

## 做法

1. 按短边判定：从 display.getDefaultDisplaySync() 取宽高（px 换成 vp），取较小者与阈值 N 比较，再按限定目录与当前方向组合（-land 即横屏且短边≥N）；方向或窗口变化时重算。不用 mediaquery 的 min-width/width 代替短边条件。
2. 规格登记 sw 覆盖时写明判定量是设备短边、与方向无关，再写方向条件，并给出手机横屏不命中的样例；不只写“最小宽度”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 API 23（HarmonyOS 6.1.0，SDK ets 6.1.0.105）；文档用 2026-05 的 OpenHarmony 中文文档副本；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 平台资源 android-34；源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Configuration#smallestScreenWidthDp 对应 sw<N>dp 限定词，是竖屏与横屏两种方向下 screenWidthDp、screenHeightDp 的最小值，与当前方向无关
- 〔例外与边界〕Configuration#screenWidthDp 对应 w<N>dp（可用宽）限定词，随横竖屏变化；targetSdk < 35 时不含窗口 insets，targetSdk ≥ 35 等于 WindowMetrics 宽度
- 〔原因〕configChanges 的 smallestScreenSize 表示不论方向的尺寸，只在物理屏尺寸变化（如换到外接显示器）时才变；横竖切换只改变 screenSize
- 〔做法第 1 步〕display.getDefaultDisplaySync(): Display；Display.width、height 为屏幕宽高（px、整数）；densityPixels 为物理与逻辑像素的缩放系数，vp = px / densityPixels（或 UIContext.px2vp）
- 〔做法第 1 步〕mediaquery 的 width、min-width、max-width 比较的是应用页面可绘制区域的宽度；orientation 取 portrait 或 landscape
- 〔做法第 1 步〕方向或尺寸变化时重算：display.on('change', callback: Callback<number>)（如方向改变）或 Window.on('windowSizeChange', callback: Callback<Size>)
- 〔适用情境〕鸿蒙资源限定词只有移动国家码和移动网络码、语言、文字、国家或地区、横竖屏（vertical/horizontal）、设备类型、颜色模式、屏幕密度，没有屏幕宽度维度
