# 源端编码可选 HEVC 时按配置用 VIDEO_HEVC 并先查可用编码器，不写死 AVC

审的是：代码
触发（任一种）：
- 读到：源端 setVideoEncoder(MediaRecorder.VideoEncoder.HEVC)，或录像设置里可选 H264/HEVC；写错的样子：AVRecorderProfile 固定写 videoCodec: media.CodecMimeType.VIDEO_AVC，不看所选编码；也没调用 getAvailableEncoder
适用范围：安卓录像的编码选项迁到 AVRecorder、容器为 MP4 时
做法：
- 按配置选 videoCodec：H264 → media.CodecMimeType.VIDEO_AVC，HEVC → media.CodecMimeType.VIDEO_HEVC；fileFormat 为 ContainerFormatType.CFT_MPEG_4
- prepare 前调 avRecorder.getAvailableEncoder()，在返回的 EncoderInfo[] 里找 type 为 'video'、mimeType 等于所选编码的项；找不到按不支持处理，创建资产前明确提示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- VIDEO_AVC = 'video/avc'、VIDEO_HEVC = 'video/hevc'：两种视频编码的 MIME 常量（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.CodecMimeType）
- getAvailableEncoder(): Promise<Array<EncoderInfo>>（@since 11）：AVRecorder 上查可用编码器（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.AVRecorder.getAvailableEncoder）
- EncoderInfo.mimeType: CodecMimeType；EncoderInfo.type: string（audio 或 video）：按这两个字段判断所选编码是否可用（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.EncoderInfo）
- AVRecorder 支持的音视频编码格式含 video/hevc、video/avc：HEVC 录制在文档的支持列表里（出处：media-kit-intro.md，支持的格式）
- MediaRecorder.VideoEncoder.H264 = 2、HEVC = 5：源端编码常量（出处：android.media.MediaRecorder.VideoEncoder）
- MP4 容器下按配置选 AVC 或 HEVC，并用 getAvailableEncoder 校验：修好的写法（出处：卡里修好并验证过）
未核实：卡的环境是 API 24，声明按本机 API 23 核实；HEVC 在具体设备上能否录制要靠运行时 getAvailableEncoder 判断
来源：1 张卡，1 个应用
- case-9d3828c851006d29fc06（opencamera-hmos）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 3；取值 6 ← 诊断
