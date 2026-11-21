# 图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时；把 GridView/ListView 适配器条目或 LinearLayout 权重行里的 wrap_content 位图确定盒尺寸时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。 也包括多个列表页共用的推广卡片里，角标 ImageView 为 wrap_content 加 centerInside，位图在 drawable-xxhdpi，媒体留给后续批次拷贝。也包括 ImageView 用 padding 缩小可见图形（如圆形垫底），目标准备换成纯色形状。也包括轮播标题图一类 wrap_content ImageView，位图只在 drawable-xhdpi，目标 Image 只设 objectFit、未设宽高，映射参考写“wrap_content → 无需设置，自动适应”。 也包括 GridView/ListView 适配器条目里 wrap_content 的 ImageView，或纵向 LinearLayout 里 wrap_content 加 layout_weight 的 ImageView：未设 adjustViewBounds，位图只在低密度目录（如 drawable-ldpi），按设备密度放大后宽于列宽或父宽。

## 例外与边界

- 图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：只在父级给出上限的那一轴夹紧图片盒，位图在盒内等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置。ImageView 未设 adjustViewBounds（默认 false）时 onMeasure 对宽、高分别 resolveSize，未超限的轴仍是密度缩放后的固有尺寸，盒子不等比收缩，这个尺寸也是 LinearLayout 量子项、分余量所用的自然尺寸；GridView/ListView 只把条目宽定为列宽，条目高按 UNSPECIFIED 测得（固有高加条目 padding），不为套用本例外给格子补宽高比（如 aspectRatio(1)）。只有 adjustViewBounds=true 时盒子才按位图比例收缩。固有像素按 Bitmap.scaleFromDensity 取整：(px×设备dpi+目录dpi/2)/目录dpi（本机 android-36.1 源码 Bitmap.java）

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。另一应用中写者复刻绑定手机号弹窗时，同轮已按 hdpi 换算了两张插图，输入行的 drawableLeft 图标却照抄仓内同族页面的 24×24，源图标实为 20×29px、24×28px@hdpi（约 13×19、16×19vp）。 ArkUI 同一组件后设的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 把 72px 的 xxhdpi 图标放大到约 40vp。另一应用的漫画阅读顶栏如此，写者已读到原图 72×72px 与 xxhdpi 来源，仍按未换算的 32vp 加槽位宽高写出。 父格往往只在一个轴上定尺寸：ImageView 未设 adjustViewBounds 时只有超限的轴被夹紧，centerInside/FIT_CENTER 只让位图在盒内缩小绘制，盒子本身不等比收缩；把盒子按宽高比缩小，或给列表格子补方形比例，会改变行高、行距与一屏可见行数。

## 做法

1. 先定参照设备选中哪一份资源：同名资源分在多个限定词目录时按限定词优先级逐个淘汰，最小宽度排在屏幕方向、密度之前；sw<N>dp 只在 N ≤ 设备最小宽度时匹配，多份匹配取 N 最大的（如最小宽度 411dp 的设备在 sw360dp、sw600dp 两份里选 sw360dp），land/port 等其余限定词同样先定；不拿已拷进目标工程的那份代替。再按选中目录的密度限定换算固有 dp：xhdpi 为 px/2；没有密度限定（drawable/、drawable-sw<N>dp/ 等）按 mdpi（160），即 px 数就是 dp 数；drawable-nodpi 不随密度缩放，按物理像素显示，目标写 'Npx' 或 this.getUIContext().px2vp(N)，不写成 N vp；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。仓内同族页面已有的图标尺寸本身也是迁移产物，不能代替对源资源的换算。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
5. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row，Image 只设图标尺寸，不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。xxhdpi 资源按 px/3 换算（72×72px → 24×24vp，74×72px → 约 25×24vp），换资源后重新核对；槽宽取源布局的承载区宽度，与图标绘制尺寸分开核对。
6. 媒体留给后续批次拷贝时，尺寸仍在本页按源资源像素写定，或登记成可机械校验的交接，不只记“待资源 sweep”。
7. 带 padding 的 ImageView 背景图换成纯色形状时，可见尺寸取布局尺寸减 padding，padding 并入外边距，与同位的热区或进度环保持同心。
8. 多张位图像素不同时逐项换算，或取统一外框配合 Contain；自检已测得位图像素时回到对应 Image 核对宽高是否写入，不只检查 objectFit。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：12 张卡 · 10 次迁移 · 10 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕安卓目录 dpi：ldpi 120、mdpi 160（DENSITY_DEFAULT）、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640；固有 dp = px × 160 ÷ 目录 dpi（xhdpi ÷2、xxhdpi ÷3、ldpi ×4/3）
- 〔做法第 1 步〕位图 drawable 的固有尺寸取 bitmap.getScaledWidth/Height(设备密度)，换算式 (px × 设备dpi + 目录dpi/2) / 目录dpi（整数除法，四舍五入）；折成 dp 就是 px × 160 ÷ 目录 dpi
- 〔做法第 1 步〕资源位图经 ImageDecoder 解码：目录 dpi 高于设备时解码成 (int)(px × 设备dpi/目录dpi + 0.5)；低于设备且 targetSdk ≥ 28 时解码期不放大，固有尺寸由 BitmapDrawable 按上式换算。两种取整都是四舍五入
- 〔做法第 1 步〕鸿蒙密度限定词与安卓同名不同义：sdpi (0,120]、mdpi (120,160]、ldpi (160,240]、xldpi (240,320]、xxldpi (320,480]、xxxldpi (480,640]；安卓 drawable-ldpi(120) 对应 sdpi，安卓 hdpi 对应鸿蒙 ldpi
- 〔做法第 1 步〕Length 写 number 或不带单位的字符串时按 vp，'10px' 才按 px
- 〔做法第 1 步〕Stack 的 alignContent 默认 Alignment.Center：不写对齐时子组件在 Stack 内居中
- 〔做法第 1 步〕Image 不设宽高：文档写“加载成功且组件不设置宽高时，其显示大小自适应父组件”；CommonMethod.width 注释写缺省用内容所需宽度、超出父容器时画到外面。两处都不等于按安卓固有 dp 显示
- 〔做法第 1 步〕ArkUI Image 只设 objectFit、不设宽高时，从安卓密度目录搬来、放在 base/media 或 xldpi、xxldpi/media 的位图，在设备上显示得比源端固有 dp 大，可越出容器
- 〔做法第 1 步〕资源选哪一份（工具链 sdk-common 的实现，27.0.2 与 32.4.1 相同；设备运行时的原生匹配代码未核）：限定词按固定顺序逐个淘汰，最小宽度排在可用宽高、屏幕方向、夜间模式、密度之前；sw<N>dp 只在 N ≤ 设备最小宽度（dp）时匹配，多份匹配时 N 越大（越接近设备值）越优先；没有 sw 限定的那份对任何设备都匹配，排在匹配上的 sw 目录之后
- 〔做法第 1 步〕资源位图的密度取自所在目录：目录没有密度限定时资源密度为 TypedValue.DENSITY_DEFAULT（0），解码按 DisplayMetrics.DENSITY_DEFAULT（160，mdpi）处理；drawable-nodpi 为 DENSITY_NONE（0xffff，Configuration 里对应 nodpi），ImageDecoder 的资源源把它记成 Bitmap.DENSITY_NONE，BitmapFactory.decodeResourceStream 也不设 inDensity，Bitmap.scaleFromDensity 遇 DENSITY_NONE 原样返回：nodpi 位图按物理像素显示，不随设备密度缩放
- 〔做法第 1 步〕长度单位 px 是屏幕物理像素、不随密度换算（不带单位时按 vp）；UIContext.px2vp(value: number): number 把 px 换成 vp；全局 px2vp 自 API 18 废弃，改用 this.getUIContext().px2vp
- 〔做法第 2 步〕ImageView 在布局和所用 style 都没写 scaleType 时（应用没有另设）为 FIT_CENTER；CENTER_INSIDE 在图宽高都不超过视图内区时 scale = 1，否则 scale = min(vw/dw, vh/dh)，再居中（只缩不放）
- 〔做法第 2 步〕ImageFit.Contain 保持宽高比缩小或放大到完整显示（小图会被放大）；ImageFit.ScaleDown 保持宽高比缩小或保持不变（只缩不放，与 centerInside 同义）；ImageFit.None 原尺寸居中
- 〔做法第 2 步〕Image.objectFit 不设时默认 ImageFit.Cover（保持宽高比缩放、居中裁切）
- 〔做法第 2 步〕Image 宽高等于触摸盒、objectFit 为 Contain 时，小于盒子的位图在设备上被等比放大到盒子大小
- 〔做法第 3 步〕TextView 的 XML drawableLeft/Start 等复合图经 setCompoundDrawablesWithIntrinsicBounds 设边界，即 drawable 固有宽高（位图按上面的密度换算）
- 〔做法第 3 步〕ImageView 的 mAdjustViewBounds 默认 false；此时测量宽 = 固有宽 + 左右 padding、高 = 固有高 + 上下 padding，两轴各自 resolveSizeAndState，只有超限的轴被夹紧
- 〔做法第 3 步〕ArkUI 组件设了固定 width/height 时，内容大小 = 设置的宽高减 padding 和 border：固定方框再叠 padding 会压缩可视图形
- 〔做法第 4 步〕VectorDrawable 的 android:width/height 以 getDimensionPixelSize 读入（dp 按设备密度换成 px），getIntrinsicWidth/Height 返回它：固有尺寸就是 XML 里写的 dp 值
- 〔做法第 4 步〕Compose Image 的 contentScale 默认 ContentScale.Fit，用 Modifier.paint（sizeToIntrinsics 默认 true）按 painter 固有尺寸测量；painterResource 读 vector XML 的 android:width/height（getDimension ÷ density）作 dp 默认尺寸
- 〔做法第 4 步〕aspectRatio(value: number) 即 width/height，只设 width 时 height = width/aspectRatio，受父内容区限制；constraintSize 优先级高于 aspectRatio，默认 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}
- 〔做法第 5 步〕同一组件的修饰链上 width/height 写两次时后写的生效（文档：属性覆盖原则，后设置的生效）；Image 于是按后写的尺寸成盒，Contain 把图标放大到这个盒子
- 〔做法第 7 步〕View 背景按整个视图边界绘制、不扣 padding；ImageView 的 src 画在 padding 以内：被 padding 缩小的是 src 图形，可见尺寸 = 布局尺寸 − padding
- 〔例外与边界〕LinearLayout 分余量：share = (int)(权重 × remainingExcess / remainingWeightSum)，起始 remainingWeightSum = weightSum > 0 ? weightSum : 权重和；带权子项主轴为 0 时取 share，否则 = 自然尺寸 + share（下限 0）
- 〔例外与边界〕layoutWeight 从主轴剩余空间按权重分配，分配时忽略元素自身尺寸设置；只在 Row/Column/Flex 中生效；有子元素设了大于 0 的 layoutWeight 时，所有子元素不再按 flexShrink/flexGrow 布局
- 〔例外与边界〕GridView 条目：宽 getChildMeasureSpec(makeMeasureSpec(列宽, EXACTLY), 0, lp.width)，高 getChildMeasureSpec(makeMeasureSpec(0, UNSPECIFIED), 0, lp.height)；getView 没设 LayoutParams 时默认 (MATCH_PARENT, WRAP_CONTENT)
- 〔例外与边界〕ListView 条目：宽取 ListView 宽度约束，lp.height > 0 时高为 EXACTLY，否则 UNSPECIFIED（按内容量高）
