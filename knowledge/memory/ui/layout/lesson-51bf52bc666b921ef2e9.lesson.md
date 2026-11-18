# values-sw<N>dp(-land) 覆盖按设备屏幕短边 min(宽,高) 判定再叠加方向，不译成 mediaquery min-width

ID：`lesson-51bf52bc666b921ef2e9` · 版本：2

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-51bf52bc666b921ef2e9.json` 改了 1 句，后面接了 9 条已核实的平台事实。原文、来源和证据卡见 [memory/ui/layout/lesson-51bf52bc666b921ef2e9.lesson.md](../../../../memory/ui/layout/lesson-51bf52bc666b921ef2e9.lesson.md)。

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

## 已核实的平台事实

核实时用的是 API 23（HarmonyOS 6.1.0，SDK ets 6.1.0.105）；文档用 2026-05 的 OpenHarmony 中文文档副本；安卓 平台资源 android-34；源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔原因 / 做法第 1 步〕Configuration#smallestScreenWidthDp 对应 sw<N>dp 限定词，是竖屏与横屏两种方向下 screenWidthDp、screenHeightDp 的最小值，与当前方向无关（出处：android.content.res.Configuration#smallestScreenWidthDp）
- 〔例外与边界〕Configuration#screenWidthDp 对应 w<N>dp（可用宽）限定词，随横竖屏变化；targetSdk < 35 时不含窗口 insets，targetSdk ≥ 35 等于 WindowMetrics 宽度（出处：android.content.res.Configuration#screenWidthDp）
- 〔原因〕configChanges 的 smallestScreenSize 表示不论方向的尺寸，只在物理屏尺寸变化（如换到外接显示器）时才变；横竖切换只改变 screenSize（出处：Android SDK 平台资源 data/res/values/attrs_manifest.xml，configChanges 的 smallestScreenSize、screenSize）
- 〔做法第 1 步〕display.getDefaultDisplaySync(): Display；Display.width、height 为屏幕宽高（px、整数）；densityPixels 为物理与逻辑像素的缩放系数，vp = px / densityPixels（或 UIContext.px2vp）（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.getDefaultDisplaySync、Display；文档 js-apis-display.md，Display）
  写法：import { display } from '@kit.ArkUI';
        const d: display.Display = display.getDefaultDisplaySync();  // API 9
        const vp: number = Math.min(d.width, d.height) / d.densityPixels;
        d.orientation: display.Orientation  // PORTRAIT | LANDSCAPE | PORTRAIT_INVERTED | LANDSCAPE_INVERTED（API 10）
- 〔做法第 1 步〕mediaquery 的 width、min-width、max-width 比较的是应用页面可绘制区域的宽度；orientation 取 portrait 或 landscape（出处：文档 arkts-layout-development-media-query.md，媒体特征（media-feature））
  写法：import { mediaquery } from '@kit.ArkUI';
        const l: mediaquery.MediaQueryListener = this.getUIContext().getMediaQuery().matchMediaSync('(orientation: landscape)');
        l.matches: boolean；l.on('change', (r: mediaquery.MediaQueryResult) => { r.matches; })；模块函数 mediaquery.matchMediaSync 自 API 18 废弃
- 〔做法第 1 步〕方向或尺寸变化时重算：display.on('change', callback: Callback<number>)（如方向改变）或 Window.on('windowSizeChange', callback: Callback<Size>)（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.on；ets/api/@ohos.window.d.ts，Window.on('windowSizeChange')）
  写法：import { display, window } from '@kit.ArkUI';
        display.on('change', (displayId: number) => { })
        win.on('windowSizeChange', (size: window.Size) => { })  // win 为 window.Window；window.Size = { width: number; height: number }（px）
- 〔适用情境〕鸿蒙资源限定词只有移动国家码和移动网络码、语言、文字、国家或地区、横竖屏（vertical/horizontal）、设备类型、颜色模式、屏幕密度，没有屏幕宽度维度（出处：文档 resource-categories-and-access.md，限定词目录）
  写法：目录：resources/base/（回落）、resources/horizontal/、resources/vertical/、resources/dark/ 等；组合顺序 移动国家码_移动网络码-语言_文字_国家或地区-横竖屏-设备类型-颜色模式-屏幕密度，如 'en_GB-vertical-car-mdpi'
- 〔做法第 1 步〕监听要成对注销：display.off('add' | 'remove' | 'change', callback?: Callback<number>) 不传 callback 时注销该类型的全部回调；Window.off('windowSizeChange', callback?: Callback<Size>) 同理，只在主线程调用。Display.availableWidth、availableHeight（API 12，px）只在 2in1、Tablet 设备可用，其他设备文档要求用 width、height（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.off、Display.availableWidth、Display.availableHeight；ets/api/@ohos.window.d.ts，Window.off；文档 js-apis-display.md，display.off；文档 arkts-apis-window-Window.md，off('windowSizeChange')）
  写法：import { display, window } from '@kit.ArkUI';
        const cb = (id: number): void => { };  display.on('change', cb);  display.off('change', cb)  // 在 aboutToDisappear 里注销
        win.off('windowSizeChange')  // win 为 window.Window；不传回调时注销全部
        d.availableWidth、d.availableHeight: number  // d 为 display.Display，API 12，仅 2in1、Tablet
- 〔原因 / 做法第 1 步〕mediaquery 另有 device-width、device-height（及 min-、max- 前缀）按设备宽高比较，文档注明 device-width 只在应用初始化时保存一次、不随设备宽度变化（如折叠屏折叠展开）实时更新；width、min-width 比较页面可绘制区域宽。宽高条件支持 vp 和 px，不写单位按 px（出处：文档 arkts-layout-development-media-query.md，device-width、device-height、min-width）
  写法：import { mediaquery } from '@kit.ArkUI';
        const l: mediaquery.MediaQueryListener = this.getUIContext().getMediaQuery().matchMediaSync('(orientation: landscape)')  // 只用方向条件；短边按 display 宽高取小者计算
