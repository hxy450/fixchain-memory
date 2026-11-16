# 兼容层给 AssetEntity 填宽高时从文件头读，不用 instantiateImageCodec 整图解码

审的是：代码
触发（任一种）：
- 读到：源 AssetEntity 带 width / height；写错的样子：兼容层用 ui.instantiateImageCodec 对选中的原图整图解码，只为取宽高
适用范围：Flutter 选图兼容层构造 AssetEntity 的尺寸元数据时
做法：
- 宽高从文件头读：原生侧 image.createImageSource(<路径>).getImageInfo() 取 ImageInfo.size，或用读文件头的库，不整图解码
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getImageInfo(index?: number): Promise<ImageInfo>：从解码源取图片信息，index 默认 0（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageSource.getImageInfo）
- getImageInfoSync(index?: number): ImageInfo：同族接口：同步取图片信息（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageSource.getImageInfoSync）
- ImageInfo.size: Size：图片宽高（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageInfo.size）
未核实：卡里宽高后来改为读文件头的库获取，但上机复测在这次改动之前，卡里没写这一改动验证过
来源：1 张卡，1 个应用
- case-d166fd60d66832c204bc（app-photo-shop-flutter）：做法第 1 步 ← 建议 3、诊断
