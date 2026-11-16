# 选图兼容层为提速去掉解码时，AssetEntity 宽高不写 0，改读文件头尺寸并给非零兜底

审的是：代码
触发（任一种）：
- 读到：被替代的选图插件（wechat_assets_picker 的 AssetPicker.pickAssets）返回 AssetEntity，兼容层原先用 ui.instantiateImageCodec 解码出宽高再传给 AssetEntity，类注释写明保持既有调用方期望的公开 API；写错的样子：兼容层构造 AssetEntity 时 width / height 写成字面量 0 或别的占位，注释说不必为读尺寸解码原图
适用范围：Flutter 应用迁到 OHOS 时用本地兼容包替代选图插件、返回的 AssetEntity 经共享选图入口交给多个页面，修复里要去掉 UI 线程上的全尺寸解码时
做法：
- 删兼容层里看似多余的计算前，在整个 lib 下搜这个字段的全部消费方（`.width` / `.height`、imageWidth、选图结果 first.width 这类），不只搜报告的那条流程；有消费方就保留字段的原语义
- 宽高改用轻量方式取：预缩放之后用 image_size_getter 读文件头尺寸，needRotate 为真时交换宽高（插件的 pubspec.yaml 加上这个依赖）；读不出或值非法时退为 1×1 这类非零值，不用 0 占位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 预缩放之后用 image_size_getter 读文件头尺寸，needRotate 时交换宽高，异常时退为 1×1：修好后的取尺寸方式，依赖宽高的文字、涂鸦页在真机上恢复（出处：卡里修好并验证过）
- 宽高为 0 时下游按 0/0 算比例得到 NaN，触发 BoxConstraints 错误：写 0 的后果（出处：卡里修好并验证过）
针对本应用要查的：
- 选图结果的宽高被哪些页面用到：目标工程 lib 下的 Dart 文件：搜 `.width`、`.height`、imageWidth、imageHeight，以及选图结果变量上的宽高读取；每个命中看是否用来算宽高比、约束或缩放；有一个就必须给真实的非零宽高
- 所用 image_size_getter 版本读尺寸的入口和表示 EXIF 旋转的字段：pub 缓存里 image_size_getter 包的 lib 源码，按读尺寸的公开函数和它返回的对象找；读出返回对象里宽、高和旋转标志（卡里用的是 needRotate）的名字，照它写交换逻辑
未核实：image_size_getter 的读尺寸接口和 needRotate 字段没在本机来源里核实，按卡写
来源：1 张卡，1 个应用
- case-64090e208edc24d57300（app-photo-shop-flutter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断；取值 2 ← 诊断
