# 图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时；把 GridView/ListView 适配器条目或 LinearLayout 权重行里的 wrap_content 位图确定盒尺寸时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。 也包括多个列表页共用的推广卡片里，角标 ImageView 为 wrap_content 加 centerInside，位图在 drawable-xxhdpi，媒体留给后续批次拷贝。也包括 ImageView 用 padding 缩小可见图形（如圆形垫底），目标准备换成纯色形状。也包括轮播标题图一类 wrap_content ImageView，位图只在 drawable-xhdpi，目标 Image 只设 objectFit、未设宽高，映射参考写“wrap_content → 无需设置，自动适应”。 也包括 GridView/ListView 适配器条目里 wrap_content 的 ImageView，或纵向 LinearLayout 里 wrap_content 加 layout_weight 的 ImageView：未设 adjustViewBounds，位图只在低密度目录（如 drawable-ldpi），按设备密度放大后宽于列宽或父宽。

## 例外与边界

- 图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：只在父级给出上限的那一轴夹紧图片盒，位图在盒内等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置。ImageView 未设 adjustViewBounds（默认 false）时 onMeasure 对宽、高分别 resolveSize，未超限的轴仍是密度缩放后的固有尺寸，盒子不等比收缩，这个尺寸也是 LinearLayout 量子项、分余量所用的自然尺寸；GridView 只把条目宽限在列宽内（条目 lp.width 为 match_parent 或没设 LayoutParams 时恰为列宽；wrap_content 时不超过列宽，比列宽窄就按 GridView 的 android:gravity 在列内摆放，没写时靠起始边），ListView 按列表宽度和条目 lp.width 定宽，条目高按 UNSPECIFIED 测得（固有高加条目 padding），不为套用本例外给格子补宽高比（如 aspectRatio(1)）。只有 adjustViewBounds=true 时盒子才按位图比例收缩。固有像素按四舍五入取整：(px×设备dpi+目录dpi/2)/目录dpi（Bitmap.scaleFromDensity；资源经 Resources 加载时 API 28 起由 ImageDecoder 解码，缩小时按 (int)(px×设备dpi/目录dpi+0.5)，targetSdk≥28 放大时不在解码时放大、按上式算固有尺寸，同为四舍五入）；不带密度限定的 drawable/ 按 160 计，drawable-nodpi 里的位图不随密度缩放

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。另一应用中写者复刻绑定手机号弹窗时，同轮已按 hdpi 换算了两张插图，输入行的 drawableLeft 图标却照抄仓内同族页面的 24×24，源图标实为 20×29px、24×28px@hdpi（约 13×19、16×19vp）。 ArkUI 同一组件后设的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 把 72px 的 xxhdpi 图标放大到约 40vp。另一应用的漫画阅读顶栏如此，写者已读到原图 72×72px 与 xxhdpi 来源，仍按未换算的 32vp 加槽位宽高写出。 父格往往只在一个轴上定尺寸：ImageView 未设 adjustViewBounds 时只有超限的轴被夹紧，centerInside/FIT_CENTER 只让位图在盒内缩小绘制，盒子本身不等比收缩；把盒子按宽高比缩小，或给列表格子补方形比例，会改变行高、行距与一屏可见行数。

## 做法

1. 先定参照设备选中哪一份资源：同名资源分在多个限定词目录时按限定词优先级逐个淘汰，最小宽度排在屏幕方向、密度之前；sw<N>dp 只在 N ≤ 设备最小宽度时匹配，多份匹配取 N 最大的（如最小宽度 411dp 的设备在 sw360dp、sw600dp 两份里选 sw360dp），land/port 等其余限定词同样先定；不拿已拷进目标工程的那份代替。再按选中目录的密度限定换算固有 dp：xhdpi 为 px/2；没有密度限定（drawable/、drawable-sw<N>dp/ 等）按 mdpi（160），即 px 数就是 dp 数；drawable-nodpi 不随密度缩放，按物理像素显示，目标写 'Npx' 或 this.getUIContext().px2vp(N)，不写成 N vp；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。仓内同族页面已有的图标尺寸本身也是迁移产物，不能代替对源资源的换算。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
5. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row，Image 只设图标尺寸，不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。源 ImageView 是 wrap_content（或 centerInside 且图标小于槽位）时，xxhdpi 资源按 px/3 换算（72×72px → 24×24vp，74×72px → 约 25×24vp）；源 ImageView 自身定成槽位尺寸又没写 scaleType 时，默认 FIT_CENTER 会把图标等比放大到槽位，这时 Image 按槽位尺寸配 Contain（源是 ImageButton 且没写 scaleType 时，默认样式给的是 center，不缩放，仍按固有 dp 显示），换资源后重新核对；槽宽取源布局的承载区宽度，与图标绘制尺寸分开核对。
6. 媒体留给后续批次拷贝时，尺寸仍在本页按源资源像素写定，或登记成可机械校验的交接，不只记“待资源 sweep”。
7. 带 padding 的 ImageView 背景图换成纯色形状时，图形是 android:src 的，可见尺寸取布局尺寸减 padding（src 画在 padding 以内；写在 android:background 上的图铺满整个 View，可见尺寸就是布局尺寸），padding 并入外边距，与同位的热区或进度环保持同心。
8. 多张位图像素不同时逐项换算，或取统一外框配合 Contain；自检已测得位图像素时回到对应 Image 核对宽高是否写入，不只检查 objectFit。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：12 张卡 · 10 次迁移 · 10 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码（另取 AOSP main 的 libs/hwui/jni/BitmapFactory.cpp）；androidx.compose.foundation:foundation-android 1.12.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔标题 / 适用情境 / 原因〕ImageView 没写 scaleType（布局、style 都没写）时为 FIT_CENTER，对应 Matrix.ScaleToFit.CENTER：等比缩放到至少一轴恰好填满内容区并居中，小于内容区的图会被放大；ImageButton 的默认样式 Widget.ImageButton 写 scaleType=center（Widget.Material.ImageButton、Widget.Holo.ImageButton 和 appcompat 的 Widget.AppCompat.ImageButton 都继承它），没另设时按固有尺寸居中、不缩放，大于内容区的部分被裁掉。不论 scaleType，drawable 没有固有尺寸（固有宽或高 ≤ 0，如纯色、不带 size 的 shape）时铺满内容区（FIT_XY 同样铺满）
- 〔标题 / 原因 / 做法第 2 步〕ScaleType.CENTER_INSIDE：图的宽、高都不超过内容区时 scale 为 1（按固有尺寸居中），否则取 min(内容宽/图宽, 内容高/图高) 等比缩小再居中，只缩不放；内容区是 View 宽高减去 padding
- 〔标题 / 原因 / 做法第 1、2 步〕Image 的 objectFit 未设置时为 ImageFit.Cover（保持宽高比缩放到两边都不小于显示边界，居中裁切）；ImageFit.Contain 保持宽高比缩小或放大，使图片完全显示在显示边界内，小于边界的图会被放大到边界；objectFit 设的是图片在组件显示边界内的填充效果
- 〔标题 / 适用情境 / 做法第 3 步〕Image 加载成功且组件不设置宽高时，显示大小自适应父组件；fitOriginalSize 未设置时为 false，组件显示大小不跟随图源大小，设了 width、height 时 fitOriginalSize 不生效；CommonMethod.width 的声明注释写不设宽时取能完整容纳内容的宽度、超过父容器时画到父容器外
- 〔适用情境 / 做法第 3、6 步〕设备上 Image 只写 objectFit、没写宽高时：drawable-xhdpi 486×136px 的轮播标题图显示得比 243×68vp 大，左右越出可视区；放在 xxldpi/media、高 57px 的角标图显示过大
- 〔做法第 1、3、5 步 / 例外与边界〕资源位图按所在目录的密度换算：目录密度为源密度（不带密度限定的 drawable/ 按 DENSITY_DEFAULT 160，drawable-nodpi 为 DENSITY_NONE、不缩放），设备 densityDpi 为目标密度。布局里的 android:src、background 和 getDrawable 走 Resources 加载，API 28 起由 ImageDecoder 解码：缩小时按 (int)(px×设备dpi/目录dpi+0.5) 解码；放大时 targetSdk ≥ 28 的应用不在解码时放大，位图保留源像素和目录密度、绘制时再缩放（targetSdk < 28 照旧解码时放大）；九宫格图不在解码时缩放。应用自己调 BitmapFactory.decodeResource 时走 decodeResourceStream，inScaled 没另设时为 true，原生层按 (int)(px×设备dpi/目录dpi+0.5) 缩放。BitmapDrawable 的固有宽高取 bitmap.getScaledWidth/Height(设备密度)，即 Bitmap.scaleFromDensity 的 (px×目标dpi+目录dpi/2)/目录dpi，上面几种情况都是四舍五入，所以固有 dp ≈ px×160÷目录dpi
- 〔做法第 1、5 步〕DisplayMetrics 的 DENSITY_LOW=120、DENSITY_MEDIUM=160（DENSITY_DEFAULT）、DENSITY_HIGH=240、DENSITY_XHIGH=320、DENSITY_XXHIGH=480、DENSITY_XXXHIGH=640，对应 drawable-ldpi、mdpi、hdpi、xhdpi、xxhdpi、xxxhdpi；像素换 dp 的除数依次为 0.75、1、1.5、2、3、4
- 〔适用情境 / 做法第 1、5 步〕鸿蒙资源的屏幕密度限定词与安卓目录名错位：sdpi 为 (0,120]，mdpi 为 (120,160]，ldpi 为 (160,240]，xldpi 为 (240,320]，xxldpi 为 (320,480]，xxxldpi 为 (480,640]，即鸿蒙 ldpi、xldpi、xxldpi 分别是安卓 hdpi、xhdpi、xxhdpi 那一档；设备状态匹配不到限定词目录或目录里没有该资源时才取 base 目录，有多个密度目录时优先向上匹配最接近的
- 〔做法第 1、3、5 步〕Length 写 number 时单位为 vp；写 string 不带单位也按 vp，'10px' 才按 px
- 〔例外与边界〕display.getDefaultDisplaySync() 返回的 Display.densityDPI 是设备每英寸像素数，即上面公式里的设备 dpi
- 〔适用情境 / 做法第 3 步〕TextView 的 drawableLeft/Right/Top/Bottom 在构造时经 setCompoundDrawablesWithIntrinsicBounds 把 bounds 设成 drawable 的固有宽高，drawableStart/End 经 setRelativeDrawablesIfNeeded 同样取固有宽高
- 〔做法第 3 步〕ImageView 量出的期望宽高 = drawable 固有宽高 + 对应方向的 padding（再与最小宽高取大），wrap_content 时按这个值在父约束内解算；没有 drawable 时固有尺寸按 0 算，drawable 固有宽或高 ≤ 0（纯色、不带 size 的 shape）时该方向按 1px 算
- 〔例外与边界〕没写 android:adjustViewBounds 时 mAdjustViewBounds 为 false：onMeasure 对宽、高分别 resolveSizeAndState，只有超出父约束的那一轴被夹紧，另一轴保持固有尺寸加 padding；adjustViewBounds 为 true 且该轴不是 EXACTLY 时才按图片宽高比调整
- 〔例外与边界〕GridView 量条目时，宽以「列宽 EXACTLY」为父规格、按条目 lp.width 解算（getChildMeasureSpec：match_parent 恰为列宽，wrap_content 不超过列宽，写死的尺寸按该值），高用 getChildMeasureSpec(UNSPECIFIED, 0, lp.height)；条目比列宽窄时按 GridView 的 android:gravity（没写时为 START）在列内摆放；ListView 的条目宽按列表宽度规格和 lp.width 解算，lp.height>0 时高为 EXACTLY，否则为 UNSPECIFIED；getView 没设 LayoutParams（如 inflate 时没传 parent）时 AbsListView 给默认的 (MATCH_PARENT, WRAP_CONTENT)
- 〔例外与边界〕LinearLayout 分余量：剩余权重和起始取 weightSum（没写 weightSum 时取各权重之和），每个带权子项 share=(int)(权重×剩余余量/剩余权重和)，再从余量和权重和里扣掉；主轴尺寸不为 0 的带权子项最终尺寸为自然尺寸+share（下限 0），主轴尺寸为 0 时只取 share；例外：应用 targetSdk ≤ 23 且 LinearLayout 本身主轴不是 EXACTLY 时，主轴尺寸为 0 的子项也按自然尺寸+share，measureWithLargestChild=true 且主轴不是 EXACTLY 时带权子项取最大子项尺寸；余量可为负
- 〔例外与边界〕ArkUI layoutWeight 大于 0 的子组件从主轴剩余空间按权重比分配尺寸，分配时忽略子组件本身的 width/height 设置（保留 minWidth/minHeight）；容器里有子组件设了大于 0 的 layoutWeight 时，所有子组件不再按 flexShrink、flexGrow 布局
- 〔例外与边界〕安卓参照机（440dpi）上，GridView 条目为 wrap_content+centerInside 的 ImageView（位图只在 drawable-ldpi、150×150px，放大后宽于列宽）加上下各 8px padding、getView 没设 LayoutParams 时，格高为 566px（(150×440+60)/120 取整得 550，加 16），行距 593px，一屏只放三行半、需要滚动，格子不是按列宽的方格
- 〔例外与边界〕安卓参照机（440dpi）上，纵向 LinearLayout 里 wrap_content、centerInside、没写 adjustViewBounds 的 ImageView（位图只在 drawable-ldpi、950×154px，放大后宽于父宽）：宽被夹到父宽，参与分余量的自然高仍是 565px（按密度放大后的固有高），不按宽的缩放比例收缩
- 〔适用情境 / 原因 / 做法第 4 步〕VectorDrawable 的 android:width、android:height 是 dimension 类型的固有宽高，按 dp 写；inflate 时密度取当前资源的屏幕密度，固有像素是 dp×屏幕密度换算，不按所在 drawable 目录的密度档再缩放
- 〔适用情境 / 做法第 4 步〕Compose foundation 的 Image(painter, contentDescription, modifier, …) 没传 alignment、contentScale 时取 Alignment.Center、ContentScale.Fit（foundation-android 1.10.3、1.12.0 相同）
- 〔做法第 4 步〕constraintSize 不设时为 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}，写 maxWidth 限制最大宽度；aspectRatio(value: number) 指定组件宽高比
- 〔标题 / 原因 / 做法第 5 步〕同一个 Image 的修饰链里先写 .width(32).height(32)、后面又写 .width(40).height(48) 时，后写的宽高生效，Image 按 40×48 的框 Contain 绘制，72×72px 的 xxhdpi 图标显示约 40vp，设备上顶部图标明显偏大
- 〔标题 / 原因 / 做法第 1、2 步〕Image 设成触摸盒尺寸（60×60、29×29）并配 ImageFit.Contain 时，固有 17–20dp 的图标被等比放大到盒子尺寸
- 〔做法第 3 步〕Image 写成 34×34 固定框再加 padding(10) 时，图片只在去掉 padding 后约 14×14vp 的区域里绘制，可视图形明显变小
- 〔做法第 7 步〕View 的背景 drawable 的 bounds 设为 (0, 0, 宽, 高)，不受 padding 影响；ImageView 的 src 画在去掉 padding 的内容区内
