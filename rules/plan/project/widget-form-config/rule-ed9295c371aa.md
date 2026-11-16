# 派工定 form_config 规格时按源 appwidget-provider 换算，写上 resizable 和预览

审的是：计划与派工
触发（任一种）：
- 读到：源 res/xml 的 appwidget-provider 写了 targetCellWidth / targetCellHeight、minResizeWidth、maxResizeWidth、resizeMode；写错的样子：台账或派工里写默认假设的 supportDimensions（如 1*2/2*2/2*4）和 defaultDimension，没写出自源的哪一项；没有 resizable；台账已批的静态预览没带进派工
适用范围：编排者给服务卡片的资源或界面转换派工、写 form_config 具体值时
做法：
- 派工里逐项写出 form_config 的值和源头：defaultDimension ← targetCellWidth×targetCellHeight，supportDimensions ← minResize 到 maxResize 覆盖的各档，resizable ← resizeMode，updateEnabled ← 有没有 updatePeriodMillis
- 台账里已批的预览决策（静态预览）写成派工里的 previewImages 一项（每档一张）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- targetCellWidth / targetCellHeight 是以桌面格为单位的默认宽高；minResizeWidth、maxResizeWidth 是 dimension：源端给出默认格数和拉伸范围的属性（出处：Android SDK 平台资源 data/res/values/attrs.xml，AppWidgetProviderInfo 的 targetCellWidth、minResizeWidth（按应用的 compileSdk 取对应平台））
- resizable：是否可以拖拽调整大小，调整值必须在 supportDimensions 里，API 20 起支持，缺省 false：派工里要写明的一项（出处：arkts-ui-widget-configuration.md，配置文件字段说明）
针对本应用要查的：
- 源端小部件的默认格数、拉伸范围、刷新周期和预览：源工程 res/xml 下的 appwidget-provider 文件，以及它引用的 dimens；读 android:targetCellWidth/Height、minResizeWidth/Height、maxResizeWidth/Height、resizeMode、updatePeriodMillis、previewImage / previewLayout 的取值写进派工
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5
