# 背景和进度条引用的 drawable 层

agent 会看到什么：读到 android:background、android:progressDrawable 引用的 @drawable/ layer-list 或 @mipmap/ 位图层；产物里只剩 .backgroundColor(...)、没有出处的 .height(...)，或位图层只留了 FWD-REF 注释

## 通用查法

### 属性引用的 drawable 是 layer-list 时，按生效源集逐层读出颜色、位图和尺寸再写目标

审的是：代码
触发（任一种）：
- 读到：android:background、android:progressDrawable 等属性引用的 @drawable/… 是 <layer-list>（item 里有 <solid>、<bitmap>、<size>，或 @android:id/progress）；flavor 源集里可能有同名 drawable；写错的样子：目标只留 .backgroundColor(...)，或自定了没有出处的 .height(...) 和颜色，位图层、进度层没有落下来
适用范围：控件的背景、进度条等属性引用 layer-list drawable，迁成 ArkUI 组件时
做法：
- 先定生效的那份 drawable：当前构建 flavor 的源集里有同名文件时以它为准，main 版只作回退
- 按 item 顺序逐层读出颜色、位图、android:gravity 和尺寸，每层写成显式写法：纯色 .backgroundColor(...)、位图 Stack 里的 Image($r('app.media.…'))、进度层 Progress 的 .color(...)，高度取 drawable 尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LayerDrawableItem：没写 width/height 时 gravity 默认 fill_horizontal / fill_vertical，写了尺寸时默认 left / top；width、height 默认取该层的固有尺寸：item 没写 gravity 时也要按铺满或左上对齐处理，没写宽高时按位图固有尺寸（出处：Android SDK 平台资源 data/res/values/attrs.xml，LayerDrawableItem 的 gravity、width（按应用的 compileSdk 取对应平台））
- objectFit(value: ImageFit): ImageAttribute，默认 ImageFit.Cover：不写 objectFit 时按 Cover 等比裁切，铺满的位图层要显式写 ImageFit.Fill（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- progressDrawable 的 layer-list 里 @android:id/background 是轨道、@android:id/progress 是进度层：轨道色和进度色分别从这两项读（出处：Android SDK 平台资源 data/res/drawable/progress_horizontal.xml，layer-list 的 @android:id/background 和 @android:id/progress 项（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 生效的那份 drawable：源工程模块构建脚本的 productFlavors 和当前构建变体；src 下各源集的 res/drawable* 里按名找同名文件；当前 flavor 的源集里有就用它，没有才用 main 版
- 每层的颜色、位图和尺寸：生效的 drawable XML 里的各个 <item>，以及它们引用的 @color/、@mipmap/、@drawable/ 资源；顺着引用读出 #AARRGGBB、位图名和 dp 数值（<size android:height>、item 的 android:top / width / height），dp 写成同数值的 vp；例：卡里 progressDrawable 的高度读出来是 12，Progress 写 .height(12)
未核实：定位层宽高未写时按位图固有尺寸折成 vp 的换算，卡里没有写明；selector、inset、clip 等其他 drawable 类型怎么逐层对应，族里的卡没验证
来源：2 张卡，2 个应用
- case-9a108f83b6eca279b883（android-train-ticket-vest7）：做法第 2 步 ← 建议 2
- case-bcb4b234c7b3327e2100（DeepAI全能PPT）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-5ae473cdcc9a｜背景 drawable 是 layer-list 时，按生效 flavor 把每层写成 Stack 里的组件，不只留底色｜读到：根布局的 android:background 引用一个 <layer-list>：纯色 <item> 之外还有 <bitmap android:gravity="fill"> 的全屏位图层、带 android:top / android:gravity 的定位位图 <item>；产品 flavor 的 sourceSet 里有同名 drawable 覆盖 main 版；写错：目标页面的 Stack 只写了 .backgroundColor(...)，没有铺满的 Image 层和定位的 Image；或者照 main 版（只有纯色）写
- rule-b0a3d15f13f2｜位图资产暂缺、编译在补资源后才跑时，照常写 Image($r('app.media.…')) 引用，不降成注释｜读到：规格或转换决策写了全屏 Image 背景或位图层，源端引用 @mipmap/、@drawable/ 位图，而目标 resources/base/media 下还没有这张图；写错：该处没有 Image(...)，只留 `FWD-REF` 注释（带 P-RES-ASSET- 编号）和「资产未迁移，就绪后补 Image 层」一类散文，或用 .backgroundColor(...) 顶替位图层
- rule-b83eb832b1ab｜带 progressDrawable 的 ProgressBar，Progress 高度和颜色取该 drawable｜读到：布局 XML 里 ProgressBar 写 android:progressDrawable="@drawable/…"；写错：对应的 Progress 自定了 .height(4) 一类没有出处的高度，.backgroundColor(...) 沿用工程里已有的、含义不同的颜色资源
