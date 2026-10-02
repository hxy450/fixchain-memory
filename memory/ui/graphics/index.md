# ui/graphics

图标与图形资源：动画矢量的状态帧、Lottie 动画层的接入、被注释的自定义绘制绑定、系统符号替代、资源迁移中的静态化标注，图标固有尺寸与 scaleType（含 vector 转来的 SVG），整屏背景图的缩放方式，自定义图片组件的形状与裁剪（含被父级自定义 Layout 放置时），自绘图表的坐标原点，按使用场景区分的资源变体映射，自绘视图自适应尺寸公式的参照基数，按产品 flavor 覆盖的 layer-list 根背景逐层落地与位图暂缺时的引用保留

[上一级](../index.md)

## 本级经验

- [AnimatedImageVector/animated-vector 按状态分别给出起点帧和终点帧；同名静态 SVG 只是起始帧](lesson-e6b1f9094ec3b905cab5.lesson.md)
  - 时机：界面实现阶段转换 AnimatedImageVector/animated-vector 图标、决定各状态显示哪一帧时；以及资源迁移阶段遇到 animated-vector 时
  - 情境：源码用 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定；目标资源目录里的同名媒体是资源迁移从 animated-vector 起始帧导出的静态 SVG；页面规格允许资源动画或等价符号，并要求保持可见的状态切换。
- [android:background 的整屏背景位图按拉伸铺满映射，不默认用 ImageFit.Cover 裁切](lesson-7708f650eb4b55dce045.lesson.md)
  - 时机：界面实现阶段，把源根布局的 android:background 背景图转换为 ArkUI 背景 Image 或背景图属性时
  - 情境：源根容器以 android:background=@drawable/xxx 铺设整屏背景位图，背景上画有需要完整显示的图文；目标用 Stack 底层 Image 或背景图属性重建。
  - 例外：源端是 ImageView 且显式 scaleType=centerCrop 一类裁切语义，按该 scaleType 映射
- [centerInside、wrap_content 或未设尺寸的图片按资源固有 dp 显示，外层保留触摸盒；ImageFit.Contain 会放大小图标](lesson-bdc493f5950835f9bfcc.lesson.md)
  - 时机：界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时
  - 情境：源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。
- [判定 $r('app.media.X') 是否可用时检索全部限定词目录，按源布局的 drawable 名取图；确认缺失才登记缺口，不用文字字形、纯色底或近似图标替代](lesson-943544ce27bf04f9faf8.lesson.md)
  - 时机：页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时
  - 情境：资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。
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
  - 情境：源端一个编码对应多种资源（白色图标、背景图、另一色系图标等），经 iconEx/bgEx/icon2Ex 一类字段分别取用，页面不同位置（顶部、小时卡、选中/非选中、列表）绑定不同字段。
- [移植自适应尺寸公式时把参照基数（如按 6 周计算的参考格高）写成独立常量，不用当前布局的实际值替换](lesson-f395cbdf6742a7f4c761.lesson.md)
  - 时机：界面实现阶段，把源端自绘视图的自适应行高、字号等公式移植到目标 Canvas 时
  - 情境：源端在自动行高模式下用固定参考值（如 6 周月份的格高）反推每格事件区高度并保证最少可见行数；目标按当月实际周数（5 或 6 周）平分格高，同一行高在 5 周月份应多显示行。
- [自绘图表的折线点与节点标签共用同一坐标原点：点坐标已含顶部留白时，不再给图形节点加同向 position 偏移](lesson-dca31bed776aaf7cb328.lesson.md)
  - 时机：界面实现阶段，把 Android 自定义 ItemDecoration/Canvas 图表（温度折线、趋势图）转换为 ArkUI Canvas、Polyline 或 Shape 时
  - 情境：源端在同一画布坐标里用 valToY 一类函数（已含 paddingTop 与文字高度）画折线和节点标签；目标把折线画在 Polyline/Shape 上并用 position 定位，标签另用 Text 定位。
