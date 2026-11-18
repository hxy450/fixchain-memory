# 图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸

ID：`lesson-bdc493f5950835f9bfcc` · 版本：10

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-bdc493f5950835f9bfcc.json` 改了 0 句，后面接了 27 条已核实的平台事实。原文、来源和证据卡见 [memory/ui/graphics/lesson-bdc493f5950835f9bfcc.lesson.md](../../../../memory/ui/graphics/lesson-bdc493f5950835f9bfcc.lesson.md)。

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时；把 GridView/ListView 适配器条目或 LinearLayout 权重行里的 wrap_content 位图确定盒尺寸时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。 也包括多个列表页共用的推广卡片里，角标 ImageView 为 wrap_content 加 centerInside，位图在 drawable-xxhdpi，媒体留给后续批次拷贝。也包括 ImageView 用 padding 缩小可见图形（如圆形垫底），目标准备换成纯色形状。也包括轮播标题图一类 wrap_content ImageView，位图只在 drawable-xhdpi，目标 Image 只设 objectFit、未设宽高，映射参考写“wrap_content → 无需设置，自动适应”。 也包括 GridView/ListView 适配器条目里 wrap_content 的 ImageView，或纵向 LinearLayout 里 wrap_content 加 layout_weight 的 ImageView：未设 adjustViewBounds，位图只在低密度目录（如 drawable-ldpi），按设备密度放大后宽于列宽或父宽。

## 例外与边界

- 图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：只在父级给出上限的那一轴夹紧图片盒，位图在盒内等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置。ImageView 未设 adjustViewBounds（默认 false）时 onMeasure 对宽、高分别 resolveSize，未超限的轴仍是密度缩放后的固有尺寸，盒子不等比收缩，这个尺寸也是 LinearLayout 量子项、分余量所用的自然尺寸；GridView/ListView 只把条目宽定为列宽，条目高按 UNSPECIFIED 测得（固有高加条目 padding），不为套用本例外给格子补宽高比（如 aspectRatio(1)）。只有 adjustViewBounds=true 时盒子才按位图比例收缩。固有像素按 Bitmap.scaleFromDensity 取整：(px×设备dpi+目录dpi/2)/目录dpi（本机 android-36.1 源码 Bitmap.java）

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。另一应用中写者复刻绑定手机号弹窗时，同轮已按 hdpi 换算了两张插图，输入行的 drawableLeft 图标却照抄仓内同族页面的 24×24，源图标实为 20×29px、24×28px@hdpi（约 13×19、16×19vp）。 ArkUI 同一组件后设的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 把 72px 的 xxhdpi 图标放大到约 40vp。另一应用的漫画阅读顶栏如此，写者已读到原图 72×72px 与 xxhdpi 来源，仍按未换算的 32vp 加槽位宽高写出。 父格往往只在一个轴上定尺寸：ImageView 未设 adjustViewBounds 时只有超限的轴被夹紧，centerInside/FIT_CENTER 只让位图在盒内缩小绘制，盒子本身不等比收缩；把盒子按宽高比缩小，或给列表格子补方形比例，会改变行高、行距与一屏可见行数。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。仓内同族页面已有的图标尺寸本身也是迁移产物，不能代替对源资源的换算。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
5. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row，Image 只设图标尺寸，不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。xxhdpi 资源按 px/3 换算（72×72px → 24×24vp，74×72px → 约 25×24vp），换资源后重新核对；槽宽取源布局的承载区宽度，与图标绘制尺寸分开核对。
6. 媒体留给后续批次拷贝时，尺寸仍在本页按源资源像素写定，或登记成可机械校验的交接，不只记“待资源 sweep”。
7. 带 padding 的 ImageView 背景图换成纯色形状时，可见尺寸取布局尺寸减 padding，padding 并入外边距，与同位的热区或进度环保持同心。
8. 多张位图像素不同时逐项换算，或取统一外框配合 Contain；自检已测得位图像素时回到对应 Image 核对宽高是否写入，不只检查 objectFit。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔做法第 1 步〕安卓目录 dpi：ldpi 120、mdpi 160（DENSITY_DEFAULT）、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640；固有 dp = px × 160 ÷ 目录 dpi（xhdpi ÷2、xxhdpi ÷3、ldpi ×4/3）（出处：android.util.DisplayMetrics#DENSITY_LOW、DENSITY_MEDIUM、DENSITY_HIGH、DENSITY_XHIGH、DENSITY_XXHIGH、DENSITY_XXXHIGH）
- 〔做法第 1 步〕位图 drawable 的固有尺寸取 bitmap.getScaledWidth/Height(设备密度)，换算式 (px × 设备dpi + 目录dpi/2) / 目录dpi（整数除法，四舍五入）；折成 dp 就是 px × 160 ÷ 目录 dpi（出处：android.graphics.drawable.BitmapDrawable#computeBitmapSize；android.graphics.Bitmap#scaleFromDensity）
- 〔做法第 1 步〕资源位图经 ImageDecoder 解码：目录 dpi 高于设备时解码成 (int)(px × 设备dpi/目录dpi + 0.5)；低于设备且 targetSdk ≥ 28 时解码期不放大，固有尺寸由 BitmapDrawable 按上式换算。两种取整都是四舍五入（出处：android.content.res.ResourcesImpl#loadDrawableForCookie；android.graphics.ImageDecoder#computeDensity）
- 〔做法第 1 步〕鸿蒙密度限定词与安卓同名不同义：sdpi (0,120]、mdpi (120,160]、ldpi (160,240]、xldpi (240,320]、xxldpi (320,480]、xxxldpi (480,640]；安卓 drawable-ldpi(120) 对应 sdpi，安卓 hdpi 对应鸿蒙 ldpi（出处：文档 resource-categories-and-access.md，限定词目录、sdpi、xxxldpi）
- 〔做法第 1 步〕Length 写 number 或不带单位的字符串时按 vp，'10px' 才按 px（出处：文档 ts-types.md，Length；ts-pixel-units.md）
  写法：全局可用，不用导入：declare type Length = string | number | Resource
        Image($r('app.media.icon')).width(24).height(24)
- 〔做法第 1 步〕Stack 的 alignContent 默认 Alignment.Center：不写对齐时子组件在 Stack 内居中（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent；文档 ts-container-stack.md，alignContent）
  写法：全局可用，不用导入（全局组件）：Stack(options?: StackOptions)，StackOptions { alignContent?: Alignment }；或 .alignContent(value: Alignment): StackAttribute
        Alignment（全局枚举）成员：TopStart、Top、TopEnd、Start、Center、End、BottomStart、Bottom、BottomEnd
- 〔做法第 1 步〕Image 不设宽高：文档写“加载成功且组件不设置宽高时，其显示大小自适应父组件”；CommonMethod.width 注释写缺省用内容所需宽度、超出父容器时画到外面。两处都不等于按安卓固有 dp 显示（出处：文档 ts-basic-components-image.md，组件不设置宽高时；鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width）
  写法：全局可用，不用导入（全局组件）：Image(src: PixelMap | ResourceStr | DrawableDescriptor): ImageAttribute
        通用属性 width(value: Length): T、height(value: Length): T；API 15 起另有 width(widthValue: Length | LayoutPolicy): T
- 〔做法第 1 步〕ArkUI Image 只设 objectFit、不设宽高时，从安卓密度目录搬来、放在 base/media 或 xldpi、xxldpi/media 的位图，在设备上显示得比源端固有 dp 大，可越出容器（出处：卡里上机实测）
  写法：Image(src).objectFit(value: ImageFit): ImageAttribute；尺寸属性 .width(value: Length).height(value: Length)
- 〔做法第 2 步〕ImageView 在布局和所用 style 都没写 scaleType 时（应用没有另设）为 FIT_CENTER；CENTER_INSIDE 在图宽高都不超过视图内区时 scale = 1，否则 scale = min(vw/dw, vh/dh)，再居中（只缩不放）（出处：android.widget.ImageView#initImageView；android.widget.ImageView#configureBounds）
- 〔做法第 2 步〕ImageFit.Contain 保持宽高比缩小或放大到完整显示（小图会被放大）；ImageFit.ScaleDown 保持宽高比缩小或保持不变（只缩不放，与 centerInside 同义）；ImageFit.None 原尺寸居中；Image.objectFit 不设时默认 ImageFit.Cover（保持宽高比缩放、居中裁切）（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Contain、ImageFit.ScaleDown、ImageFit.None；文档 ts-basic-components-image.md，objectFit）
  写法：全局可用，不用导入：Image(src).objectFit(value: ImageFit): ImageAttribute
        ImageFit（全局枚举）成员：Contain、Cover、Auto、Fill、ScaleDown、None；API 12 起 TOP_START、TOP、TOP_END、START、CENTER、END、BOTTOM_START、BOTTOM、BOTTOM_END；API 15 起 MATRIX
- 〔做法第 2 步〕Image 宽高等于触摸盒、objectFit 为 Contain 时，小于盒子的位图在设备上被等比放大到盒子大小（出处：卡里上机实测）
  写法：Image(src).width(盒宽).height(盒高).objectFit(ImageFit.Contain)
- 〔做法第 3 步〕TextView 的 XML drawableLeft/Start 等复合图经 setCompoundDrawablesWithIntrinsicBounds 设边界，即 drawable 固有宽高（位图按上面的密度换算）（出处：android.widget.TextView#TextView(Context, AttributeSet, int, int)；android.widget.TextView#setCompoundDrawablesWithIntrinsicBounds）
- 〔做法第 3 步〕ImageView 的 mAdjustViewBounds 默认 false；此时测量宽 = 固有宽 + 左右 padding、高 = 固有高 + 上下 padding，两轴各自 resolveSizeAndState，只有超限的轴被夹紧（出处：android.widget.ImageView#mAdjustViewBounds；android.widget.ImageView#onMeasure）
- 〔做法第 3 步〕ArkUI 组件设了固定 width/height 时，内容大小 = 设置的宽高减 padding 和 border：固定方框再叠 padding 会压缩可视图形（出处：文档 arkts-layout-development-overview.md，布局元素的组成）
  写法：全局可用，不用导入（通用属性）：padding(value: Padding | Length | LocalizedPadding): T，Padding = { top?, right?, bottom?, left?: Length }
        margin(value: Margin | Length | LocalizedMargin): T，Margin 即 Padding 同结构；number 单位 vp
- 〔做法第 4 步〕VectorDrawable 的 android:width/height 以 getDimensionPixelSize 读入（dp 按设备密度换成 px），getIntrinsicWidth/Height 返回它：固有尺寸就是 XML 里写的 dp 值（出处：android.graphics.drawable.VectorDrawable#updateStateFromTypedArray、#getIntrinsicWidth）
- 〔做法第 4 步〕Compose Image 的 contentScale 默认 ContentScale.Fit，用 Modifier.paint（sizeToIntrinsics 默认 true）按 painter 固有尺寸测量；painterResource 读 vector XML 的 android:width/height（getDimension ÷ density）作 dp 默认尺寸（出处：androidx.compose.foundation:foundation 1.10.3，ImageKt#Image；androidx.compose.ui:ui 1.10.3，androidx.compose.ui.draw.PainterModifierKt#paint、androidx.compose.ui.graphics.vector.compat.XmlVectorParser_androidKt）
- 〔做法第 4 步〕aspectRatio(value: number) 即 width/height，只设 width 时 height = width/aspectRatio，受父内容区限制；constraintSize 优先级高于 aspectRatio，默认 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}（出处：文档 ts-universal-attributes-layout-constraints.md，aspectRatio；鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.aspectRatio、CommonMethod.constraintSize）
  写法：全局可用，不用导入（通用属性）：aspectRatio(value: number): T；constraintSize(value: ConstraintSizeOptions): T
        ConstraintSizeOptions { minWidth?: Length; maxWidth?: Length; minHeight?: Length; maxHeight?: Length }
        Image(src).width('100%').constraintSize({ maxWidth: 48 }).aspectRatio(48 / 32)
- 〔做法第 5 步〕同一组件的修饰链上 width/height 写两次时后写的生效（文档：属性覆盖原则，后设置的生效）；Image 于是按后写的尺寸成盒，Contain 把图标放大到这个盒子（出处：卡里上机实测；文档 arkts-user-defined-extension-attributeModifier.md（属性覆盖原则））
  写法：全局可用，不用导入（通用属性）：width(value: Length): T、height(value: Length): T
        Stack() { Image(src).width(24).height(24) }.width(40).height(48)
- 〔做法第 5 步〕Row 的 alignItems 默认 VerticalAlign.Center、justifyContent 默认 FlexAlign.Start：不另设时子组件在 Row 内竖直居中、水平贴起始边（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowInterface、RowAttribute.alignItems、RowAttribute.justifyContent；文档 ts-container-row.md）
  写法：全局可用，不用导入（全局组件）：Row(options?: RowOptions)；.alignItems(value: VerticalAlign): RowAttribute；.justifyContent(value: FlexAlign): RowAttribute
        VerticalAlign：Top、Center、Bottom；FlexAlign：Start、Center、End、SpaceBetween、SpaceAround、SpaceEvenly
- 〔做法第 7 步〕View 背景按整个视图边界绘制、不扣 padding；ImageView 的 src 画在 padding 以内：被 padding 缩小的是 src 图形，可见尺寸 = 布局尺寸 − padding（出处：android.view.View#setBackgroundBounds；android.widget.ImageView#configureBounds、#onDraw）
- 〔例外与边界〕LinearLayout 分余量：share = (int)(权重 × remainingExcess / remainingWeightSum)，起始 remainingWeightSum = weightSum > 0 ? weightSum : 权重和；带权子项主轴为 0 时取 share，否则 = 自然尺寸 + share（下限 0）（出处：android.widget.LinearLayout#measureVertical（横向见 measureHorizontal））
- 〔例外与边界〕layoutWeight 从主轴剩余空间按权重分配，分配时忽略元素自身尺寸设置；只在 Row/Column/Flex 中生效；有子元素设了大于 0 的 layoutWeight 时，所有子元素不再按 flexShrink/flexGrow 布局（出处：文档 ts-universal-attributes-size.md，layoutWeight）
  写法：全局可用，不用导入（通用属性）：layoutWeight(value: number | string): T
- 〔例外与边界〕GridView 条目：宽 getChildMeasureSpec(makeMeasureSpec(列宽, EXACTLY), 0, lp.width)，高 getChildMeasureSpec(makeMeasureSpec(0, UNSPECIFIED), 0, lp.height)；getView 没设 LayoutParams 时默认 (MATCH_PARENT, WRAP_CONTENT)（出处：android.widget.GridView#setupChild；android.widget.AbsListView#generateDefaultLayoutParams）
- 〔例外与边界〕ListView 条目：宽取 ListView 宽度约束，lp.height > 0 时高为 EXACTLY，否则 UNSPECIFIED（按内容量高）（出处：android.widget.ListView#setupChild）
- 〔适用情境〕ImageButton 在布局和 style 都没写 scaleType 时（应用没有另设 imageButtonStyle）是 CENTER，不是 ImageView 的 FIT_CENTER：图标按固有尺寸居中、不缩不放，超出视图的部分被裁掉（cropToPadding 默认 false，可画进 padding 区）；默认 clickable、focusable 为 true。各标准主题的 imageButtonStyle 最终都继承平台 Widget.ImageButton 的 scaleType=center：Theme.Holo、Theme.Holo.Light、Theme.Material、Theme.Material.Light、Theme.Material.Light.DarkActionBar、Theme.DeviceDefault；Theme.AppCompat、.Light、.Light.DarkActionBar、.DayNight（appcompat 1.1.0–1.8.0，Widget.AppCompat.ImageButton）；Theme.MaterialComponents、.Light、.Light.DarkActionBar、.DayNight（material 1.4.0–1.14.0，同样取 Widget.AppCompat.ImageButton）（平台资源 android-30、34、36 相同）（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.ImageButton；android.widget.ImageView#mCropToPadding；android.widget.ImageView#mCropToPadding；Android SDK 平台资源 data/res/values/themes.xml，imageButtonStyle；Android SDK 平台资源 data/res/values/themes_holo.xml，imageButtonStyle；Android SDK 平台资源 data/res/values/themes_material.xml，imageButtonStyle；Android SDK 平台资源 data/res/values/themes_device_defaults.xml，imageButtonStyle；androidx.appcompat:appcompat 1.1.0、1.8.0，Base.V7.Theme.AppCompat、Base.Widget.AppCompat.ImageButton；com.google.android.material:material 1.4.0、1.14.0，Theme.MaterialComponents（imageButtonStyle 沿用 AppCompat））
- 〔做法第 1 步〕ImageButton 的默认背景自带 padding，src 只画在 padding 以内（布局没写 android:padding 时；写了的边以布局为准）：Theme.Material、Theme.Material.Light、Theme.Material.Light.DarkActionBar、Theme.DeviceDefault，以及 API 21 起的 Theme.AppCompat 全系（appcompat 1.1.0–1.8.0，Base.Widget.AppCompat.ImageButton 的父是 android:Widget.Material.ImageButton）和 Theme.MaterialComponents 全系（material 1.4.0–1.14.0），背景都是 btn_default_material：inset 左右 4dp、上下 6dp 加 shape padding 左右 8dp、上下 4dp，合计左右各 12dp、上下各 10dp；Theme.Holo、Theme.Holo.Light 是 9-patch 背景 btn_default_holo_dark / _light，padding 左右 12dp、上下 8dp，最小 26×32dp（平台资源 android-30、34、36 相同）（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.ImageButton；Android SDK 平台资源 data/res/drawable/btn_default_mtrl_shape.xml，button_inset_horizontal_material；Android SDK 平台资源 data/res/values/dimens_material.xml，control_inset_material、button_inset_vertical_material、button_padding_horizontal_material、control_padding_material；Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.ImageButton、Widget.Holo.Light.ImageButton；Android SDK 平台资源 drawable-xhdpi/btn_default_normal_holo_dark.9.png（9-patch 内容区，mdpi 同比）；android.graphics.drawable.InsetDrawable#getPadding；android.view.View#View(Context, AttributeSet, int, int)（布局 padding 优先于背景 padding））
- 〔做法第 8 步〕Image 的 onComplete 回调给出图源像素和组件尺寸，单位都是 px：width、height 是图片的宽高，componentWidth、componentHeight 是组件宽高，contentWidth、contentHeight、contentOffsetX、contentOffsetY（API 10 起）是实际绘制区域；可用来核对写定的 vp 尺寸（px ÷ 屏幕密度）（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.onComplete；文档 ts-basic-components-image.md，onComplete）
  写法：全局组件，全局可用，不用导入
        Image(src).onComplete((event?: { width: number, height: number, componentWidth: number, componentHeight: number, loadingStatus: number, contentWidth: number, contentHeight: number, contentOffsetX: number, contentOffsetY: number }) => void): ImageAttribute
