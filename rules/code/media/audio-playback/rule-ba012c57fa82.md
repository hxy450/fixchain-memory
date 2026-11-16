# rawfile 的 getRawFd 描述符只经 AVPlayer.fdSrc 设源，不在 url 上拼 offset

审的是：代码
触发（任一种）：
- 读到：安卓源端 SoundPool.load(context, R.raw.x) 或 MediaPlayer.create(context, R.raw.x)；规格写「getRawFd → url=fd://」；写错的样子：代码写 player.url = `fd://${fd}?offset=${offset}&length=${length}`，或 getRawFd / getRawFdSync 的结果流向 .url
适用范围：目标用 AVPlayer 播应用包 resources/rawfile 里的音频、视频时
做法：
- 写成 const rf = context.resourceManager.getRawFdSync(name); player.fdSrc = { fd: rf.fd, offset: rf.offset, length: rf.length }，在 AVPlayer 处于 idle 时设
- url 的 fd:// 形式只用于整文件的 fd://<数字>（如沙箱文件打开得到的 fd）；不在 url 上拼 d.ts 未记载的 ?offset=&length=
- 规格写法和写前读到的 d.ts 注释冲突时按 d.ts 写，并在源码笔记或回报里登记规格那一行有误，不以「规格明确要求」覆盖查到的 API 语义
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fdSrc?: AVFileDescriptor，只能在 idle 状态设；资源在同一个文件里连续存放时必须用它：AVPlayer 按文件段设源（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.fdSrc）
- AVFileDescriptor { fd: number; offset?: number; length?: number }，offset 默认 0、单位字节；length 默认从 offset 到文件末尾：rawfile 必须把 offset、length 都传上，否则会从 HAP 开头读整包（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVFileDescriptor）
- getRawFdSync(path: string): RawFileDescriptor：同步取 rawfile 描述符；fd 是整个 HAP，offset、length 是资源在 HAP 内的段（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getRawFdSync；ets/api/global/rawFileDescriptor.d.ts，RawFileDescriptor）
- url 的 fd 类型播放写 fd://xx；独立的媒体文件才用它：url 只收整文件句柄（出处：arkts-apis-media-AVPlayer.md，属性 url / fdSrc）
- url 上拼 ?offset=&length= 后播放器建好即报 401，系统日志「not a fd://+numeric string」；改成 fdSrc = { fd, offset, length } 后正常：改前改后的现象（出处：卡里修好并验证过）
- fdSrc?: AVFileDescriptor（AVMetadataExtractor）：同族接口：取媒体元数据时 rawfile 段同样经 fdSrc 传（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVMetadataExtractor.fdSrc）
- fdSrc?: AVFileDescriptor（AVImageGenerator）：同族接口：取视频帧时 rawfile 段同样经 fdSrc 传（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVImageGenerator.fdSrc）
未核实：多个 AVPlayer 共用 getRawFd 得到的 HAP fd 时，是否会遇到声明里所说的同一句柄竞争、能否逐个 closeRawFd，卡里没验证
来源：1 张卡，1 个应用
- case-1299a79fcb5958688d9d（Blockinger）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2；取值 5 ← 诊断
