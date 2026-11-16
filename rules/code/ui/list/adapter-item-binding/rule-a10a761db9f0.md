# 返修重写界面时，列数按 Adapter 实际绑定项、背景按源码选图逻辑、尺寸按源布局

审的是：代码
触发（任一种）：
- 读到：RecyclerView Adapter 的绑定方法只把列表第 1、2 项绑到两列控件；背景由按状态选图的方法设置；布局里 ImageView 写着 `android:scaleType="fitXY"` 和固定 dp 高度；写错的样子：ArkTS 按截图写成 slice(1, 4) 三列概览，或把按状态切换的背景写成一张固定 Image(...)，高度和 ImageFit 与源布局不同
适用范围：返修阶段按截图对照重做界面时
做法：
- 列数和取哪几项照 Adapter 实际绑定的数据项写（只绑第 1、2 项就是 slice(1, 3) 两列）
- 背景照源码的状态选图逻辑按状态切换，不固定成截图里那一张；高度取源布局的 dp 值，fitXY 写成 .objectFit(ImageFit.Fill)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- objectFit(value: ImageFit): ImageAttribute：Image 的缩放方式（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- ImageFit.Fill：不保持宽高比缩放填满显示区，对应 fitXY（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Fill）
- scaleType 的 fitXY = 1，对应 ScaleType.FIT_XY（Matrix.ScaleToFit#FILL）：源端 X、Y 各自缩放填满（出处：Android SDK 平台资源 data/res/values/attrs.xml，ImageView 的 scaleType（按应用的 compileSdk 取对应平台）；android.widget.ImageView.ScaleType#FIT_XY）
来源：1 张卡，1 个应用
- case-0dd25455d592a77ed652（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断
