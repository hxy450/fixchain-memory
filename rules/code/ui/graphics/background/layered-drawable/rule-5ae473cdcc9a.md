# 背景 drawable 是 layer-list 时，按生效 flavor 把每层写成 Stack 里的组件，不只留底色

审的是：代码
触发（任一种）：
- 读到：根布局的 android:background 引用一个 <layer-list>：纯色 <item> 之外还有 <bitmap android:gravity="fill"> 的全屏位图层、带 android:top / android:gravity 的定位位图 <item>；产品 flavor 的 sourceSet 里有同名 drawable 覆盖 main 版；写错的样子：目标页面的 Stack 只写了 .backgroundColor(...)，没有铺满的 Image 层和定位的 Image；或者照 main 版（只有纯色）写
适用范围：安卓页面根布局或容器的背景是 layer-list（含被 flavor 覆盖的版本）、迁成 ArkUI 页面背景时
做法：
- 先定生效的 drawable：当前构建 flavor 的 sourceSet 里有同名文件时以它为准，main 版只是回退
- 按 item 顺序在 Stack 里自下而上写：纯色层写成 .backgroundColor(...)；gravity=fill 的位图层写成 Image($r('app.media.<位图名>')).width('100%').height('100%').objectFit(ImageFit.Fill)
- 带 gravity / top 的位图层另写一个 Image：对齐照 gravity（top|center_horizontal 即顶部水平居中），android:top 的 dp 数值写成同数值的上边距（vp），宽高照该层尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- objectFit(value: ImageFit): ImageAttribute，默认 ImageFit.Cover：不写 objectFit 时按 Cover 等比放大裁切，不是 gravity=fill 的拉伸铺满（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- ImageFit.Fill：不保持宽高比缩放，让图片填满显示边界，对应位图层的 gravity=fill（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Fill）
- gravity 的 fill = 0x77：横纵两个方向都放大到完全填满容器（出处：Android SDK 平台资源 data/res/values/attrs.xml，gravity 的 flag fill（按应用的 compileSdk 取对应平台））
- LayerDrawableItem：没写 width/height 时 gravity 默认 fill_horizontal / fill_vertical，写了尺寸时默认 left / top；width、height 默认取该层的固有尺寸：源 item 没写 gravity 时也要按铺满或左上对齐处理，定位层的宽高未写时按位图固有尺寸（出处：Android SDK 平台资源 data/res/values/attrs.xml，LayerDrawableItem 的 gravity、width（按应用的 compileSdk 取对应平台））
- StackOptions.alignContent 默认 Alignment.Center：Stack 的子组件默认居中，顶部定位的层要显式写对齐（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- Stack 首层 Image 100%×100% 加 ImageFit.Fill，其上品牌 Image 以 android:top 的数值作顶部内边距：修好后的写法，启动背景和品牌图恢复显示（出处：卡里修好并验证过）
- objectFit(value: ImageFit): ImageSpanAttribute：同族接口：ImageSpan 的缩放方式，同样用 ImageFit（出处：鸿蒙 SDK 的 ets/component/image_span.d.ts，ImageSpanAttribute.objectFit）
针对本应用要查的：
- 生效的 flavor 和它覆盖的 drawable：源工程模块构建脚本的 productFlavors 和当前构建变体；src 下该 flavor 目录的 res/drawable* 里与 main 同名的 drawable；flavor 版存在就按它的 item 列表逐层落组件，main 版只作回退
- 每个位图层引用的位图和它的尺寸：layer-list item 的 android:drawable 或 <bitmap android:src> 指向的 @mipmap/、@drawable/ 资源，在对应 sourceSet 的 res/mipmap-*、drawable-* 下按名找；位图名作目标 media 资源名；item 没写 android:width/height 时读位图固有尺寸作该层宽高
未核实：卡里上机看到的行为出自 HarmonyOS API 21/24，本机声明按 API 23 核实；定位层宽高未写时按位图固有尺寸折成 vp 的换算，卡里没有写明
来源：1 张卡，1 个应用
- case-bcb4b234c7b3327e2100（DeepAI全能PPT）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1、诊断；取值 6 ← 诊断
