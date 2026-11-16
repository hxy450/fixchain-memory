# photoAccessHelper 找音频时不写 PhotoType.AUDIO，改用 AudioViewPicker

审的是：代码
触发（任一种）：
- 读到：规格写「MediaLibraryKit 查询音频资产」，而 photoAccessHelper 参考或声明里按类型筛选只有 PhotoType.IMAGE / PhotoType.VIDEO；写错的样子：代码里出现 PhotoType.AUDIO，例如 predicates.equalTo(PHOTO_TYPE, PhotoType.AUDIO)
- 读到：编译报错 Property 'AUDIO' does not exist on type 'typeof PhotoType'；写错的样子：删掉 PhotoType 谓词，改成 getAssets 取全部相册资产再按扩展名、时长过滤当本地音频
适用范围：迁安卓本地音频扫描时，鸿蒙代码里用 photoAccessHelper 查询或筛选音频的地方
做法：
- PhotoType 只有 IMAGE、VIDEO，音频不在相册媒体库里：不自拟枚举成员，也不删掉类型谓词换编译通过
- 改成 new picker.AudioViewPicker(context).select(options) 多选导入 → 把返回 URI 的文件复制进应用沙箱 → media.createAVMetadataExtractor() 设好 fdSrc 后 fetchMetadata() 取 duration；页面进入时扫描沙箱里已导入的文件
- 回执里写明目标平台没有这个能力、原功能链不可达，作为规格问题上报
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- PhotoType 只有 IMAGE = 1、VIDEO = 2：没有 AUDIO 成员，写 PhotoType.AUDIO 编译不过（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，photoAccessHelper.PhotoType）
- PhotoAccessHelper.getAssets 的 @permission 是 ohos.permission.READ_IMAGEVIDEO：扫全部相册资产拿到的只是图片和视频，还要图片/视频读取权限（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoAccessHelper.getAssets）
- select(option?: AudioSelectOptions): Promise<Array<string>>：AudioViewPicker 返回选中音频的 URI；多选设 AudioSelectOptions.maxSelectNumber（默认 1，1 到 500）（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，AudioViewPicker.select）
- select() 返回的 URI 是临时只读权限，退出应用后台后失效：要复制进沙箱才能下次进页还能扫到（出处：select-user-file.md，选择音频类文件）
- function createAVMetadataExtractor(): Promise<AVMetadataExtractor>：创建取元数据的实例（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.createAVMetadataExtractor）
- AVMetadataExtractor.fdSrc?: AVFileDescriptor；fetchMetadata(): Promise<AVMetadata>：取元数据前必须先设 fdSrc 或 dataSrc（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVMetadataExtractor.fdSrc、AVMetadataExtractor.fetchMetadata）
- AVMetadata.duration?: string：媒体时长，类型是字符串（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVMetadata.duration）
未核实：卡里的行为在 target SDK 6.1.1(24) 下观察，本机核实用的声明是 API 23；AVMetadata.duration 的单位声明里没写
来源：1 张卡，1 个应用
- case-1607d055621c41c4c087（免费来电多多）：做法第 1 步 ← 建议 2、建议 3；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2、建议 3
