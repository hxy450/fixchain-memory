# 停录视频缩略图取末帧后按实测画廊按钮宽等比缩放，不借用媒体库缩略图的固定尺寸

审的是：代码
触发（任一种）：
- 写错的样子：停录缩略图用 PixelMapParams { width: 512, height: 384 } 这类媒体库缩略图常量取帧，并直接写共享状态里的画廊位图，绕过画廊服务和覆盖层
适用范围：录像停止后生成画廊缩略图、规格写「取末帧，宽度按画廊按钮宽等比缩放」时
做法：
- AVImageGenerator.fetchFrameByTime 取末帧的自然尺寸，再按实测画廊按钮宽（px）等比缩放：pixelMap.scaleSync(按钮宽 / 帧宽, 按钮宽 / 帧宽)
- 经画廊服务或 VM 统一发布，发布前校验 URI 与前台状态，不直接写共享状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fetchFrameByTime(timeUs: number, options: AVImageQueryOptions, param: PixelMapParams): Promise<image.PixelMap>：按时间取视频帧（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVImageGenerator.fetchFrameByTime）
- PixelMapParams.width / height 必须大于 0 且不超过原视频宽高，否则返回的缩略图不缩放：取帧时指定尺寸的限制（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，PixelMapParams）
- scaleSync(x: number, y: number): void：按宽高比例缩放 PixelMap（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.scaleSync）
- 取自然帧按实测画廊宽缩放、经 VM 校验 URI / 前台后发布，停录缩略图与源端一致：返修的落法（出处：卡里修好并验证过）
- fetchFrameByTime(timeUs: number, options: AVImageQueryOptions, param: PixelMapParams): Promise<image.PixelMap>（AVMetadataExtractor）：同族接口：AVMetadataExtractor 上的同名取帧方法（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVMetadataExtractor.fetchFrameByTime）
针对本应用要查的：
- 画廊按钮的实测宽度：目标页面里画廊按钮组件的 onAreaChange 回调；记下 newValue.width（vp），换成 px 后作为缩放基准
未核实：卡里环境是 API 24，声明按本机 API 23 核对
来源：1 张卡，1 个应用
- case-d5c3514ada560cb5134d（opencamera-hmos）：做法第 1 步 ← 建议 5、诊断；做法第 2 步 ← 建议 5；取值 4 ← 诊断
