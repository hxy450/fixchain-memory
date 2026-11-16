# sw 限定符译成运行期条件时，用 display 宽高较小者比阈值，不用 mediaquery min-width

审的是：代码
触发（任一种）：
- 读到：源工程 `values-sw<N>dp-land` / `values-sw<N>dp` 里的覆盖值，或规格写“最小宽度≥N”；写错的样子：目标用 mediaquery.matchMediaSync('(min-width: Nvp) and (orientation: landscape)') 或按窗口 width 判断，手机横屏也命中
适用范围：把最小宽度限定目录的覆盖落成 ArkTS 运行期分支时
做法：
- const d = display.getDefaultDisplaySync(); const swVp = Math.min(d.width, d.height) / d.densityPixels; 条件写成 swVp >= N，-land 目录再 && 横屏
- 不用 mediaquery 的 min-width / width 做 sw 判定，它们比的是当前窗口宽
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getDefaultDisplaySync(): Display：同步取默认屏幕（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，display.getDefaultDisplaySync）
- Display.width、Display.height 单位是 px：取较小者再除以 densityPixels 得 vp（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，Display.width / Display.height）
- Display.densityPixels：物理像素与逻辑像素之间的缩放系数：px ÷ densityPixels = vp（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，Display.densityPixels）
- mediaquery 的 min-width：应用页面可绘制区域的最小宽度：按当前窗口宽判定，不是短边（出处：arkts-layout-development-media-query.md，媒体特征（media-feature））
- smallestScreenWidthDp 是两种方向下 screenWidthDp、screenHeightDp 的最小值：源端 sw 限定符的判定量（出处：android.content.res.Configuration#smallestScreenWidthDp）
- 判定改成“横屏且 display 宽高较小者（vp）≥ 阈值”后，手机横屏不再命中平板覆盖值：卡里修好的做法（出处：卡里修好并验证过）
未核实：安卓 screenWidthDp/screenHeightDp 是扣除系统栏后的可用尺寸，display 宽高是整屏，阈值附近可能有出入
来源：1 张卡，1 个应用
- case-db3da49c14f06085f3b8（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 6 ← 诊断
