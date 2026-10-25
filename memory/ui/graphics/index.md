# ui/graphics

图标与图形资源：动画矢量的状态帧、Lottie 动画层的接入、被注释的自定义绘制绑定、系统符号替代、资源迁移中的静态化标注，图标固有尺寸与 scaleType（含 vector 转来的 SVG），整屏背景图的缩放方式，自定义图片组件的形状与裁剪（含被父级自定义 Layout 放置时），自绘图表的坐标原点，按使用场景区分的资源变体映射，自绘视图自适应尺寸公式的参照基数，按产品 flavor 覆盖的 layer-list 根背景逐层落地与位图暂缺时的引用保留，以及多个指标共用的绘制分支按源端通用参数（线宽、描边）统一实现，缺失原图时从 Android 复制且不以近名图标或着色替代，文字字符按钮的字形；自绘 View 移植到 Canvas 的单位、帧循环、位图缓存语义与文字度量见子主题 canvas；自绘角标与圆点按调用分支推导尺寸（半径与直径）；动画矢量（AVD）两态之间的形变过渡；Coil 全局 ImageLoader 的默认占位、错误图与解码器（动图是否播放）写进图片契约

[上一级](../index.md)

## 子主题

- [canvas](canvas/index.md) — 自绘 View（onDraw、Paint）移植到 ArkUI Canvas：上下文单位域与跨域换算，invalidate 与帧循环，每帧起始画面（清屏），预烘焙位图改每帧绘制时的取值时机与缩放语义，字体串格式与字体就绪，文字基线度量与段落方向，SurfaceView 自建线程渲染循环的实例结构、vsync 驱动与 surface 失效，位图按密度解码与预缩放采样

## 本级经验

- [AnimatedImageVector/animated-vector 按 atEnd 在起止帧之间实现形变过渡；同名静态 SVG 只是起始帧，两态静态帧或符号切换只在已批准降级时使用](lesson-e6b1f9094ec3b905cab5.lesson.md)
  - 时机：规格提取与界面实现阶段，为 AnimatedImageVector/animated-vector 图标确定实现方案、各状态显示的帧与状态切换时的过渡时；以及资源迁移阶段遇到 animated-vector 时
  - 情境：源码用 AnimatedImageVector.animatedVectorResource 与 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定，animated-vector 的 objectAnimator 以 pathData 的 valueFrom/valueTo、duration 与 interpolator 描述两态形变；目标没有直接等价组件，资源目录里的同名媒体是资源迁移从起始帧导出的静态 SVG；规格可能允许资源动画或等价符号，或写“图标态切换即可满足”。
  - 例外：决策记录以编号批准省略形变过渡、差异验收与之一致时，按批准的两态静态帧或等价符号实现，仍按状态分别给出起止帧
- [Coil 全局 ImageLoader 的占位、错误图与解码器写进图片契约：没装 GIF 解码器时只显示动图首帧](lesson-544f9fa8eff09aca5f52.lesson.md)
  - 时机：规格提取阶段整理图片加载管线与设置位归属时；界面实现阶段把 Coil AsyncImage 映射为 ArkUI Image 时
  - 情境：Android 图片组件经应用的 ImageLoaderFactory 或 Coil.setImageLoader 加载，默认 loader 设 placeholder、error、crossfade 并只装部分解码器，autoPlayGifs 一类设置位切换到带 GIF 解码器的 loader；目标用 ArkUI Image（默认播放动图）与 alt 实现。
- [android:background 的整屏背景位图按拉伸铺满映射，不默认用 ImageFit.Cover 裁切；被铺满且未置顶的 SurfaceView 盖住时不建背景层](lesson-7708f650eb4b55dce045.lesson.md)
  - 时机：界面实现阶段，把源根布局的 android:background 背景图转换为 ArkUI 背景 Image 或背景图属性时；规格提取阶段为承载自绘游戏视图的页面确定背景层与画布叠放关系时
  - 情境：源根容器以 android:background=@drawable/xxx 铺设整屏背景位图，背景上画有需要完整显示的图文；目标用 Stack 底层 Image 或背景图属性重建。 也包括根容器内 addView 或布局了铺满的 SurfaceView/GLSurfaceView 子类（未调用 setZOrderOnTop(true)，绘制时 drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR) 清屏或不画底色），目标准备用 Stack 叠放背景 Image 与透明 Canvas。
  - 例外：源端是 ImageView 且显式 scaleType=centerCrop 一类裁切语义，按该 scaleType 映射；源容器内铺满的 SurfaceView/GLSurfaceView/VideoView 未 setZOrderOnTop(true)：该区域的父容器背景在源端不可见，不建背景层，按做法第 1 步取可见底色
- [从源端自绘角标、圆点控件推导目标固定尺寸时，按调用实际进入的分支取尺寸函数，drawCircle 的半径换成直径，密度分支写明所取档](lesson-99fe69fc59afa886750d.lesson.md)
  - 时机：界面实现阶段（含补齐遗漏元素的返修），把 Android 自定义 BadgeView、红点 View 等按计数与屏幕密度分支计算尺寸的控件改写为固定 vp 的 Circle 或 Text 时
  - 情境：源端以 setBadgeCount(0) 一类调用显示无数字红点，尺寸由 dp 半径基数、计数分支（无数字、个位数、更多）和密度分支共同决定，绘制用 drawCircle(半径)；目标用固定 vp 的 Circle 复刻，常叠在高度很小的入口 chip 或图标上；协调者可能转述或改写尺寸。
- [修共享绘制分支里某一指标的显示差异时，按源端通用规则统一实现，不写单 key 特判；先列出落入该分支的全部指标](lesson-17d6e4c04764983be25a.lesson.md)
  - 时机：界面绘制修复阶段，按用户对某一指标的视觉反馈，调整多个指标共用的 Canvas 绘制分支（线宽、描边、填充样式）时
  - 情境：源端同类图形由通用 helper 按统一规则绘制（如 drawBars 中 STROKE/FILL_AND_STROKE 与 strokeWidth ?: 3f 像素），不区分指标 key；目标多个指标经分派落到同一绘制分支，用户只报告其中一个与源端粗细不一致。
- [图标按源端原始资源落实：缺失时从 Android 密度目录、SDK 平台或依赖库 AAR 复制原图，不用字形、近名图标、系统符号或二次着色替代](lesson-943544ce27bf04f9faf8.lesson.md)
  - 时机：页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时；规格提取阶段为源端图标与界面字符写转换决策时
  - 情境：资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。 也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标（如带 1/2 后缀的阅读器图标），现有代码用 SymbolGlyph 或 Unicode 字形占位，或工程 skill 要求图标优先用已验证的系统 symbol；以及源端用粗体文字字符（“-”“+”）充当按钮图形。也包括源端 Text 直接显示 emoji 字符（如 ⭐、☕️），规格或写者按“不把 emoji 塞进 Text 当图标”一类 symbol 规则改成 SymbolGlyph。 也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者以“平台 chrome、应用无源图”为由用 Polyline、Circle 或字形自绘。 也包括 AppCompat Activity 调 setDisplayHomeAsUpEnabled(true)，返回箭头由 appcompat 库主题提供，已迁移的 media 目录里找不到，目标准备改用系统符号。
- [图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸](lesson-bdc493f5950835f9bfcc.lesson.md)
  - 时机：界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时；把 GridView/ListView 适配器条目或 LinearLayout 权重行里的 wrap_content 位图确定盒尺寸时
  - 情境：源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。 也包括多个列表页共用的推广卡片里，角标 ImageView 为 wrap_content 加 centerInside，位图在 drawable-xxhdpi，媒体留给后续批次拷贝。也包括 ImageView 用 padding 缩小可见图形（如圆形垫底），目标准备换成纯色形状。也包括轮播标题图一类 wrap_content ImageView，位图只在 drawable-xhdpi，目标 Image 只设 objectFit、未设宽高，映射参考写“wrap_content → 无需设置，自动适应”。 也包括 GridView/ListView 适配器条目里 wrap_content 的 ImageView，或纵向 LinearLayout 里 wrap_content 加 layout_weight 的 ImageView：未设 adjustViewBounds，位图只在低密度目录（如 drawable-ldpi），按设备密度放大后宽于列宽或父宽。
  - 例外：图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：只在父级给出上限的那一轴夹紧图片盒，位图在盒内等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置。ImageView 未设 adjustViewBounds（默认 false）时 onMeasure 对宽、高分别 resolveSize，未超限的轴仍是密度缩放后的固有尺寸，盒子不等比收缩，这个尺寸也是 LinearLayout 量子项、分余量所用的自然尺寸；GridView/ListView 只把条目宽定为列宽，条目高按 UNSPECIFIED 测得（固有高加条目 padding），不为套用本例外给格子补宽高比（如 aspectRatio(1)）。只有 adjustViewBounds=true 时盒子才按位图比例收缩。固有像素按 Bitmap.scaleFromDensity 取整：(px×设备dpi+目录dpi/2)/目录dpi（本机 android-36.1 源码 Bitmap.java）
- [无来源、无数据的兜底预览不添加源端没有的装饰：边框、选中态等可选视觉属性在未选择时不由兜底层伪造](lesson-c8909c3cb5f925913407.lesson.md)
  - 时机：界面实现或返修阶段，为编辑页、详情页的预览补无预览源、无数据时的兜底态时
  - 情境：源端预览容器本身是空容器，由运行时填入组件视图；可选视觉属性（如边框）默认未选择，选择后才绘制；目标要为没有预览源的状态写占位，并在其上叠加真实的选中层。
- [根背景是按产品 flavor 覆盖的 layer-list 时按生效版本逐层落成组件；位图暂缺也保留 Image 引用并申报，不降成纯色底](lesson-0da8733ee0a6c52924da.lesson.md)
  - 时机：页面界面转换阶段，迁移根布局的背景 drawable，尤其所需位图尚未进入目标 media 时
  - 情境：源页面根背景是 layer-list（纯色底、全屏位图、定位的品牌图），main 与产品 flavor 的 sourceSet 各有一份，flavor 版覆盖 main；规格要求 Stack 加全屏 Image 背景；目标工程缺失的资源由后续批次统一补源，转换期不编译。
- [源布局有按状态切换的 Lottie 动画层时接入 @ohos/lottie 并迁移动画 JSON，不以静态兜底图静默替代](lesson-ea55fe23fea47c1cfca3.lesson.md)
  - 时机：界面实现阶段，转换含 LottieAnimationView 或 setAnimation("json/...") 的页面头图、背景等动画层时
  - 情境：Android 页面在静态背景 ImageView 之上叠加 LottieAnimationView，代码按天气、昼夜等状态选择 assets/json 中的动画文件；目标工程尚无 lottie 依赖，静态兜底图已迁移。
- [源码调用项目自定义图片组件时先读组件定义（含被父级自定义 Layout 放置时）：CircleShape + Crop 译为 Cover + borderRadius(边长/2) 并确认裁剪生效，不以裸 Image + Contain 代替](lesson-9dcd69d2824702310959.lesson.md)
  - 时机：页面转换与巡检修复阶段，把 Compose 页面里的自定义图片组件调用翻译为 ArkUI Image，确定形状、裁剪与填充方式时；把 Compose 自定义 Layout（measurables、Constraints.fixed、placeRelative）转写为 ArkUI Stack/position，为被放置的子组件落定形状时
  - 情境：Compose 页面通过项目自定义组件（ui/components 下的 XxxImage 一类）渲染图片，shape = CircleShape、contentScale = Crop 写在组件定义里，调用点只传资源与 size/modifier；页面规格只写图片尺寸；目标端的共享组件可能尚未生成，或页面选择内联 Image。也包括父级自定义 Layout 以 Constraints.fixed 给共享图片组件指定尺寸和位置、容器再裁掉溢出，形状写在子组件定义里，同页另一处也调用同一组件。
- [源端 Adapter 中被注释掉的数据绑定视为未启用行为：按 XML 的静态属性实现，不据注释代码或 ViewModel 重建动态效果](lesson-cd87ec49e06af8e6459a.lesson.md)
  - 时机：界面实现阶段，转换 item 布局中的自定义绘制 View（曲线、进度、图表）并决定其数据绑定时
  - 情境：源 Adapter 对自定义 View 的数据绑定整段被注释，只剩 XML 中的静态属性（颜色、点色、尺寸）；ViewModel 仍计算着可能用于绑定的值（如 maxTop/minTop）；决策账本规定注释和死代码不迁移。
- [源端按使用场景返回不同资源变体时，按取值字段分别映射，不用一个映射覆盖所有场景](lesson-c65e8e59008a5e31bcad.lesson.md)
  - 时机：界面实现与返修阶段，把源端“编码 → 资源”的映射函数（如天气编码到图标）迁移为 $r 资源映射，并为各使用处选择资源时
  - 情境：源端一个编码对应多种资源（白色图标、背景图、另一色系图标等），经 iconEx/bgEx/icon2Ex 一类字段分别取用，页面不同位置（顶部、小时卡、选中/非选中、列表）绑定不同字段。 也包括同一编辑选项在选择列表与主预览取自不同资源族：列表 Holder 用固定 drawable（setBackgroundResource），主预览按组件尺寸加载 cover/&lt;尺寸&gt;/&lt;id&gt;.webp。
- [移植自适应尺寸公式时把参照基数（如按 6 周计算的参考格高）写成独立常量，不用当前布局的实际值替换](lesson-f395cbdf6742a7f4c761.lesson.md)
  - 时机：界面实现阶段，把源端自绘视图的自适应行高、字号等公式移植到目标 Canvas 时
  - 情境：源端在自动行高模式下用固定参考值（如 6 周月份的格高）反推每格事件区高度并保证最少可见行数；目标按当月实际周数（5 或 6 周）平分格高，同一行高在 5 周月份应多显示行。
- [自绘图表的折线点与节点标签共用同一坐标原点：点坐标已含顶部留白时，不再给图形节点加同向 position 偏移](lesson-dca31bed776aaf7cb328.lesson.md)
  - 时机：界面实现阶段，把 Android 自定义 ItemDecoration/Canvas 图表（温度折线、趋势图）转换为 ArkUI Canvas、Polyline 或 Shape 时
  - 情境：源端在同一画布坐标里用 valToY 一类函数（已含 paddingTop 与文字高度）画折线和节点标签；目标把折线画在 Polyline/Shape 上并用 position 定位，标签另用 Text 定位。
