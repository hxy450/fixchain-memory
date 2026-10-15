# ui/graphics

图标与图形资源：动画矢量的状态帧、Lottie 动画层的接入、被注释的自定义绘制绑定、系统符号替代、资源迁移中的静态化标注，图标固有尺寸与 scaleType（含 vector 转来的 SVG），整屏背景图的缩放方式，自定义图片组件的形状与裁剪（含被父级自定义 Layout 放置时），自绘图表的坐标原点，按使用场景区分的资源变体映射，自绘视图自适应尺寸公式的参照基数，按产品 flavor 覆盖的 layer-list 根背景逐层落地与位图暂缺时的引用保留，以及多个指标共用的绘制分支按源端通用参数（线宽、描边）统一实现，缺失原图时从 Android 复制且不以近名图标或着色替代，文字字符按钮的字形；自绘 View 移植到 Canvas 的单位、帧循环、位图缓存语义与文字度量见子主题 canvas；自绘角标与圆点按调用分支推导尺寸（半径与直径）；动画矢量（AVD）两态之间的形变过渡

[上一级](../index.md)

## 子主题

- [canvas](canvas/index.md) — 自绘 View（onDraw、Paint）移植到 ArkUI Canvas：上下文单位域与跨域换算，invalidate 与帧循环，每帧起始画面（清屏），预烘焙位图改每帧绘制时的取值时机与缩放语义，字体串格式与字体就绪，文字基线度量与段落方向

## 本级经验

- [android:background 的整屏背景是普通位图时按拉伸铺满映射，不默认用 ImageFit.Cover 裁切](lesson-7708f650eb4b55dce045.lesson.md)
  - 时机：界面实现阶段，把源根布局的 android:background 背景图转换为 ArkUI 背景 Image 或背景图属性时
  - 情境：源根容器以 android:background=@drawable/xxx 铺设整屏背景，该 drawable 是普通位图（png/jpg，或未设 gravity/tileMode 的 &lt;bitmap&gt;，BitmapDrawable.java 默认 gravity=FILL），背景上画有需要完整显示的图文；目标用 Stack 底层 Image 或背景图属性重建。
  - 例外：源端是 ImageView 且显式 scaleType=centerCrop 一类裁切语义，按该 scaleType 映射；背景是设了 gravity 或 tileMode 的 &lt;bitmap&gt;：按其定位或平铺映射（common.d.ts 的 backgroundImagePosition、backgroundImage 的 ImageRepeat）；背景是 .9.png：按九宫格拉伸，用 Image.resizable（image.d.ts）或 backgroundImageResizable（common.d.ts）按源 .9 的拉伸区设 slice；背景是 layer-list 或按产品 flavor 覆盖：按生效版本逐层落成组件
- [animated-vector 按 atEnd 在起止帧之间实现过渡；同名静态 SVG 只是起始帧，不当作完整实现](lesson-e6b1f9094ec3b905cab5.lesson.md)
  - 时机：规格提取与界面实现阶段，为 AnimatedImageVector/animated-vector 图标确定实现方案、各状态显示的帧与状态切换时的过渡时；以及资源迁移阶段遇到 animated-vector 时
  - 情境：源码用 AnimatedImageVector.animatedVectorResource 与 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定，animated-vector 的 objectAnimator 以 pathData 的 valueFrom/valueTo 描述两态之间的形变，带 duration 与 interpolator；目标没有直接等价组件，资源目录里的同名媒体可能是资源迁移从起始帧导出的静态 SVG；规格可能允许资源动画或等价符号，或写“图标态切换即可满足”。
  - 例外：决策记录以编号批准省略形变过渡、差异验收与之一致时，按批准的两态静态帧或等价符号实现，仍按状态分别给出起止帧；objectAnimator 的 propertyName 不是 pathData（AnimatedVectorDrawable.java 列出的 rotation、fillAlpha、trimPathEnd 等）：不按本条在两组 pathData 间逐数值插值，按该属性另行映射；atEnd 两态与源 duration、插值器仍照源保留
- [从源端自绘角标、圆点控件推导目标固定尺寸时，按调用实际进入的分支取尺寸函数，drawCircle 的半径换成直径，密度分支写明所取档](lesson-99fe69fc59afa886750d.lesson.md)
  - 时机：界面实现阶段（含补齐遗漏元素的返修），把 Android 自定义 BadgeView、红点 View 等按计数与屏幕密度分支计算尺寸的控件改写为固定 vp 的 Circle 或 Text 时
  - 情境：源端以自定义计数接口（如 setBadgeCount）显示红点或角标，尺寸由 dp 半径基数、计数分支（如无数字、带数字）和密度分支共同决定，绘制用 drawCircle(半径)；目标用固定 vp 的 Circle 复刻，常叠在高度很小的入口 chip 或图标上；协调者可能转述或改写尺寸。
- [位图图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 图标不设成盒子尺寸再 Contain](lesson-bdc493f5950835f9bfcc.lesson.md)
  - 时机：界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时
  - 情境：源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain，或写“wrap_content → 无需设置，自动适应”。也包括工具栏按钮原本在组件上链式设置点击区宽高，替换成位图后又在同一 Image 上写图标宽高；多个列表页共用的推广角标；媒体留给后续批次拷贝；ImageView 用 padding 缩小可见图形、目标准备换成纯色形状。
  - 例外：图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：按父级给出的上限夹紧图片盒并等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置；资源是 vector drawable 转来的 SVG：固有尺寸取源 drawable 的 android:width/height（dp），不按密度目录换算
- [修共享绘制分支里某一指标的显示差异时，按源端通用规则统一实现，不写单 key 特判；先列出落入该分支的全部指标](lesson-17d6e4c04764983be25a.lesson.md)
  - 时机：界面绘制修复阶段，按用户对某一指标的视觉反馈，调整多个指标共用的 Canvas 绘制分支（线宽、描边、填充样式）时
  - 情境：源端同类图形由通用 helper 按统一规则绘制（如按 Paint.Style 与默认 strokeWidth 统一绘制），不区分指标 key；目标多个指标经分派落到同一绘制分支，用户只报告其中一个与源端粗细不一致。
- [无来源、无数据的兜底预览不添加源端没有的装饰：边框、选中态等可选视觉属性在未选择时不由兜底层伪造](lesson-c8909c3cb5f925913407.lesson.md)
  - 时机：界面实现或返修阶段，为编辑页、详情页的预览补无预览源、无数据时的兜底态时
  - 情境：源端预览容器本身是空容器，由运行时填入组件视图；可选视觉属性（如边框）默认未选择，选择后才绘制；目标要为没有预览源的状态写占位，并在其上叠加真实的选中层。
- [根背景是按产品 flavor 覆盖的 layer-list 时按生效版本逐层落成组件；位图暂缺也保留 Image 引用并申报，不降成纯色底](lesson-0da8733ee0a6c52924da.lesson.md)
  - 时机：页面界面转换阶段，迁移根布局的背景 drawable，尤其所需位图尚未进入目标 media 时
  - 情境：源页面根背景是 layer-list（纯色底、全屏位图、定位的品牌图），main 与产品 flavor 的 sourceSet 各有一份，flavor 版覆盖 main；规格要求 Stack 加全屏 Image 背景；目标工程缺失的资源由后续批次统一补源，转换期不编译。
  - 例外：背景是单张位图（不是 layer-list）且没有 flavor 覆盖：按背景位图的拉伸、gravity 或九宫格规则映射
- [源布局引用的 @drawable 图标在目标判缺失前检索全部限定词目录，缺图从源仓或主题提供方复制原图，不用近名图、符号或纯色底替代](lesson-943544ce27bf04f9faf8.lesson.md)
  - 时机：页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时
  - 情境：资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里有外观相近、名称相近的其他模块图标。也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标，现有代码用 SymbolGlyph 或 Unicode 字形占位。也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者准备用 Polyline、Circle 或字形自绘。
  - 例外：源端用文字字符或 emoji 充当图形（Text 或 TextView 显示的字符）：按源字面字符用 Text 实现，不属资源查找；主题 parent 链不止于 android:Theme.*（如 AppCompat、MaterialComponents 主题）：本条的 SDK 平台 drawable 路径不适用，按该主题实际所在的依赖库资源查找原图
- [源布局有按状态切换的 Lottie 动画层时接入 @ohos/lottie 并迁移动画 JSON，不以静态兜底图静默替代](lesson-ea55fe23fea47c1cfca3.lesson.md)
  - 时机：界面实现阶段，转换含 LottieAnimationView 或 setAnimation("json/...") 的页面头图、背景等动画层时
  - 情境：Android 页面在静态背景 ImageView 之上叠加 LottieAnimationView，代码按业务状态（如天气、昼夜）调用 setAnimation 选择 assets/json 中的动画文件；目标工程尚无 lottie 依赖，静态兜底图已迁移。
- [源端按使用场景返回不同资源变体时，按取值字段分别映射，不用一个映射覆盖所有场景](lesson-c65e8e59008a5e31bcad.lesson.md)
  - 时机：界面实现与返修阶段，把源端“编码 → 资源”的映射函数（如状态编码到图标）迁移为 $r 资源映射，并为各使用处选择资源时
  - 情境：源端一个编码对应多种资源（白色图标、背景图、另一色系图标等），经不同的映射函数或字段分别取用，页面不同位置（顶部、卡片、选中/非选中、列表）绑定不同字段。也包括同一选项在列表与主预览分别取自固定 drawable 和按尺寸挑选的素材。
- [源端用文字字符或 emoji 充当图形时，按原字符用 Text 实现，不换成外形不同的系统符号](lesson-f280dea78bb77f84ddba.lesson.md)
  - 时机：规格提取与界面实现阶段，为源端以 TextView/Text 字符（粗体“-”“+”、emoji）表现的按钮或图形写转换决策并选择目标组件时
  - 情境：源端用 TextView 或 Compose Text 显示字面字符充当按钮图形（加减号），或 Text 直接显示 emoji（如星标、咖啡杯）；工程 skill 或规格有“图标优先用已验证的系统 symbol”“不把 emoji 塞进 Text 当图标”一类规则，写者准备改成 SymbolGlyph 或带圆圈的近似符号。
  - 例外：源端该处引用的是 drawable 或矢量图标资源：按源资源复制原图，不属本条
- [由 vector drawable 转来的 SVG 图标按源 android:width/height 的 dp 取固有尺寸，不再按密度目录换算](lesson-aefa093c4e662d53c2d1.lesson.md)
  - 时机：界面实现阶段，为不设尺寸的 Compose Image(painterResource(vector drawable)) 或 ImageView 引用的矢量图确定目标 Image 尺寸时；收口阶段按密度自动校正图标尺寸时
  - 情境：源端 Image(painterResource(R.drawable.x)) 不设尺寸、按 drawable 声明的 dp 固有尺寸显示，或 ImageView 引用 vector drawable；源 drawable 是 &lt;vector android:width="…dp" android:height="…dp"&gt;，常在无密度限定的 drawable 目录；目标 SVG 由它转换而来。
  - 例外：资源是位图（png/webp/jpg）：按所在密度目录把像素换算成 dp
- [移植自适应尺寸公式时把源端的固定参照量写成独立常量，不用目标布局中会变化的实际量替换](lesson-f395cbdf6742a7f4c761.lesson.md)
  - 时机：界面实现阶段，把源端自绘视图或布局代码里的自适应行高、格高等尺寸公式移植到目标时
  - 情境：源公式以固定参照量（常量分母、固定行数或周数）反推尺寸，并保证最少可见量；目标布局中对应的实际量会变化（例：月视图按固定 6 周反推行高，而当月实际可能是 5 周）。
- [自绘图表的折线点与节点标签共用同一坐标原点：点坐标已含顶部留白时，不再给图形节点加同向 position 偏移](lesson-dca31bed776aaf7cb328.lesson.md)
  - 时机：界面实现阶段，把 Android 自定义 ItemDecoration/Canvas 图表（温度折线、趋势图）转换为 ArkUI Canvas、Polyline 或 Shape 时
  - 情境：源端在同一画布坐标里用 valToY 一类函数（已含 paddingTop 与文字高度）画折线和节点标签；目标把折线画在 Polyline/Shape 上并用 position 定位，标签另用 Text 定位。
- [调用项目自定义图片组件时先读其定义：CircleShape + Crop 写成 ImageFit.Cover + 半边长圆角 + clip(true)](lesson-9dcd69d2824702310959.lesson.md)
  - 时机：页面转换与巡检修复阶段，把 Compose 页面里的自定义图片组件调用翻译为 ArkUI Image，确定形状、裁剪与填充方式时；把 Compose 自定义 Layout（measurables、Constraints.fixed、placeRelative）转写为 ArkUI Stack/position，为被放置的子组件落定形状时
  - 情境：Compose 页面通过项目自定义组件（ui/components 下的 XxxImage 一类）渲染图片，shape = CircleShape、contentScale = Crop 写在组件定义里，调用点只传资源与 size/modifier；页面规格只写图片尺寸；目标端的共享组件可能尚未生成，或页面选择内联 Image。也包括父级自定义 Layout 以 Constraints.fixed 给共享图片组件指定尺寸和位置、容器再裁掉溢出，形状写在子组件定义里，同页另一处也调用同一组件。
