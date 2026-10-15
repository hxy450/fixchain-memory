# app/media

媒体与文件的用户可见性：SaveButton 安全控件的样式与授权时序、picker 导入导出、沙箱产物的导出、本地文件的播放 URI，以及按序浏览媒体时后续项的图片预取，以及长内容保存为图片时的快照尺寸限制与分段渲染

[上一级](../index.md)

## 本级经验

- [SaveButton 授权后的回调里只做快速写入：下载等耗时准备放在点击之前](lesson-089bb378b1ec034a3e84.lesson.md)
  - 时机：实现或改造 SaveButton 保存链（如把多步流程改成主按钮直接保存）时
  - 情境：页面用 SaveButton 临时授权经 photoAccessHelper 写系统相册；保存前需要下载或缓存网络文件；原链路先准备好文件再显示或启用 SaveButton。
- [SaveButton 的底色与圆角设在控件自身，不设透明底再靠外层容器画外观](lesson-e1211056a34f58403e3a.lesson.md)
  - 时机：界面实现阶段，用 SaveButton 等安全控件替代源端自绘样式按钮（渐变、半透明胶囊、圆角描边）时
  - 情境：源端主操作按钮带渐变或半透明底、圆角或描边；迁移要求改成 SaveButton 安全控件（文案只能用系统预设，样式能力受限，如不支持渐变），实现者打算让外层容器画外观、控件自身设 Color.Transparent。
- [从图库选图用系统 PhotoViewPicker 并复制进应用目录：一次性处理放缓存，要写进持久配置的复制到 filesDir 并校验非空；不以申请 READ_IMAGEVIDEO 读媒体库或经权限未接通的自建相册页实现](lesson-ad1db0aa0434c2e766fd.lesson.md)
  - 时机：平台能力映射与实现阶段，为“从相册选择图片导入”选择 HarmonyOS 读取方式与权限声明时，包括在 Flutter 本地兼容插件中实现选图时；为背景等持久配置接入“从相册选一张图”并保存结果时
  - 情境：源端经媒体库查询（MediaStore，或 photo_manager 一类插件）列出并读取相册图片，依赖媒体库读写权限；目标应用为普通应用，功能只需用户主动选择的图片。 也包括选出的图片要作为背景等持久配置反复读取，而工程里另有依赖 getAlbums 全量查询、带未完成权限或相册绑定 TODO 的自建选择页。
  - 例外：应用已确认具备申请 READ_IMAGEVIDEO 所需的签名等级与权限审批，且功能确需浏览整个媒体库
- [把任意长度内容保存为图片时不靠单次离屏快照：先查快照尺寸限制，内容可能超过一屏就按视口分段渲染再拼接，并校验输出高度](lesson-e0f3b5b744e6b0518814.lesson.md)
  - 时机：界面实现阶段，为“保存完整长内容为图片”或分享长图选择截图、离屏渲染方案时
  - 情境：源端按内容总高度创建 Bitmap 后整体绘制（如 getBitmapFromView、Canvas.draw），高度随文本无上限增长；目标拟用 componentSnapshot.createFromBuilder 等单次快照，Builder 根组件只定宽、高度随内容撑开。
  - 例外：内容高度有明确上限且不超过一屏时，可以单次快照
- [本地文件路径接到 ArkUI Video 前规范成 file:// URI，并分清缓存接口返回的是路径还是播放地址](lesson-2b3d45c1a89dc1ead7e3.lesson.md)
  - 时机：页面转换与跨页接线阶段，把路由参数或缓存/预载接口给出的本地文件接到 Video src 时
  - 情境：源端把缓存文件路径交给第三方播放器 setUrl(path)（其内部把本地文件转成 Uri）；目标用 ArkUI Video；工程缓存单例可能同时提供返回裸沙箱路径和返回 file:// 播放地址的两个方法。
- [本地音频导入用 AudioViewPicker 并复制进沙箱；photoAccessHelper 只覆盖图片和视频，不作为音频来源](lesson-62ac5e65ac4aa51128bd.lesson.md)
  - 时机：平台能力映射与实现阶段，为 Android MediaStore 本地音频扫描选择 HarmonyOS 读取方式与权限链时；编译修复遇到缺失的媒体类型枚举时
  - 情境：源端申请 READ_EXTERNAL_STORAGE/READ_MEDIA_AUDIO 后查询 MediaStore.Audio 列出本地音频；目标受“不申请图片/视频媒体权限、优先 picker”约束，候选方案涉及 photoAccessHelper(MediaLibraryKit)、READ_AUDIO 与 AudioViewPicker。
- [源端写公共目录并做媒体扫描的产物，目标改落沙箱后每条链路都要写出用户可见的导出步骤](lesson-b59097ee968fe827f70d.lesson.md)
  - 时机：规格提取阶段，把源端下载或导出产物的落点及“沙箱 + picker 导出”替代方案映射到各条业务链时；实现者把公共目录换成沙箱路径时
  - 情境：源端申请 WRITE_EXTERNAL_STORAGE 写公共目录并发 ACTION_MEDIA_SCANNER_SCAN_FILE，使产物在文件管理或媒体库中可见；目标不申请媒体权限，改为下载到应用沙箱；同一功能中可能只有某一条链写了 DocumentViewPicker 导出。
- [源端推进后主动预取后续图片时，目标用图片解码真实预取并限定缓存，不以 Image 组件缓存替代或只在差异清单里注销](lesson-cde53c6eab199d1262b2.lesson.md)
  - 时机：ViewModel 或页面逻辑迁移阶段，处理源端图片预加载、缓存预热等性能行为，决定实现、平台替代还是登记缺口时
  - 情境：源端 ViewModel 在加载或每次推进后按规则挑出后续若干项（如跳过已处理、已跳过项和视频）并主动预取（如 Coil imageLoader.enqueue），规格含对应的性能验收项；目标页面只用 Image 组件按需显示当前项，没有独立的预加载服务。
  - 例外：已有批准的决策放弃该性能行为，并在迁移报告或占位登记中留有记录
