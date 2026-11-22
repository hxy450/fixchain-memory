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

1. 按短边判定：从 display.getDefaultDisplaySync() 取宽高（px 换成 vp），取较小者与阈值 N 比较，再按限定目录与当前方向组合（-land 即横屏且短边≥N，横屏包括 Display.orientation 为 LANDSCAPE 和 LANDSCAPE_INVERTED 两种）；方向或窗口变化时重算（display.on('change') 在显示方向改变时回调）。不用 mediaquery 的 min-width/width 代替短边条件。
2. 规格登记 sw 覆盖时写明判定量是设备短边、与方向无关，再写方向条件，并给出手机横屏不命中的样例；不只写“最小宽度”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码（android.content.res.Configuration）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Configuration.smallestScreenWidthDp 是应用正常运行时在竖屏、横屏两种方向下 screenWidthDp 和 screenHeightDp 的最小值，对应 sw<N>dp（smallest width）资源限定符，与当前方向无关
- 〔原因〕Configuration.screenWidthDp、screenHeightDp 随应用 targetSdk 不同：targetSdk 为 35（VANILLA_ICE_CREAM）及以上时等于 WindowMetrics（含窗口 insets），按 dp 四舍五入；低于 35 时不含状态栏、导航栏等窗口 insets，应用用 setDecorFitsSystemWindows(false) 画到系统栏下也照样扣掉；多窗口下是应用窗口的可用区域，嵌入的 Activity 取各自 Activity 的尺寸
- 〔做法第 1 步〕display.getDefaultDisplaySync()（API 9 起）同步返回应用所在屏幕的 Display；Display.width、Display.height 是显示设备的屏幕宽高，单位 px，整数
- 〔做法第 1 步〕Display.densityPixels 是物理像素与逻辑像素之间的缩放系数（取值范围 [0.5, 4.0]），px 除以它得到 vp
- 〔原因 / 做法第 1 步〕mediaquery 的 width、min-width 比较的是应用页面可绘制区域的宽度，不是屏幕短边；比较数值型媒体特征时支持 vp 和 px，不写单位时按 px
- 〔做法第 1 步〕Display.orientation（API 10 起）的 Orientation 取值为 PORTRAIT 0、LANDSCAPE 1、PORTRAIT_INVERTED 2、LANDSCAPE_INVERTED 3，横屏对应 LANDSCAPE 和 LANDSCAPE_INVERTED 两个值
- 〔做法第 1 步〕display.on('change', callback) 监听显示设备变化，文档举的例子包括显示器方向改变，回调参数是屏幕 ID
