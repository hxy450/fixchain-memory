# 源码调用项目自定义图片组件时，打开其定义把形状、裁剪和 contentScale 一起翻译

审的是：代码
触发（任一种）：
- 读到：调用点是从项目 ui/components 包 import 的自定义图片组件，只传 imageRes 和 Modifier.size(...)；`CircleShape`、`ContentScale.Crop` 在组件定义里；写错的样子：ArkTS 写成 Image(...).objectFit(ImageFit.Contain)，没有 borderRadius 和 clip
- 读到：父级 Layout { measurables, constraints -> … } 用 Constraints.fixed / placeRelative 放置共享 composable，它的定义是 Surface(shape = CircleShape) 包 AsyncImage(ContentScale.Crop)；写错的样子：对应 Image 只有 width / height、objectFit(ImageFit.Cover)、position，没有 .borderRadius(...) 或 .clipShape(...)
适用范围：源端图片由项目自定义组件渲染（含被父级自定义 Layout 放置）而不是平台 Image 时
做法：
- 打开该组件定义，把 shape/clip 和 contentScale 一起翻：CircleShape + ContentScale.Crop 写成 .objectFit(ImageFit.Cover).borderRadius(边长 / 2).clip(true)；父 Layout 只给尺寸位置
- 没读定义时不以 ImageFit.Contain 作默认
- 写完按组件名搜源页面所有调用点，逐个核对对应 Image 都带同样裁切
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ImageFit.Cover：保持宽高比缩放，使图片两边都大于或等于显示边界：对应 ContentScale.Crop；也是 Image.objectFit 的默认值（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Cover；ets/component/image.d.ts，ImageAttribute.objectFit）
- ImageFit.Contain：保持宽高比缩放，使图片完整显示在边界内：会留白，不是 Crop（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Contain）
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T，半径最大为组件宽或高的一半：圆角，边长 / 2 即圆形（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- clip(value: boolean): T，默认 false：按边缘轮廓裁剪（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.clip）
- 分类图加 .borderRadius(边长 / 2) 后与源端圆形一致：返修的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 自定义组件的形状和填充方式：源工程里按调用点的 import 或函数名（搜 fun 名字(）找到该组件的 @Composable 定义；读最外层 Surface / Box 的 shape 和 Modifier.clip(shape)，以及内部 Image 的 contentScale，分别翻成 borderRadius/clip 和 objectFit
来源：2 张卡，1 个应用
- case-2298d8bb5582e74fe497（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2；取值 5 ← 诊断
- case-5adfa1aabec5f52b2744（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 3
