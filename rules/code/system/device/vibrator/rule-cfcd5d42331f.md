# 源端计时器步骤切换按偏好发声振动时，目标步进分支读偏好并播 rawfile 提示音、调振动

审的是：代码
触发（任一种）：
- 读到：源端计时器在非静默步骤切换时按偏好用 `MediaPlayer` 播本地提示音、调 `Vibrator` 振动封装，长按跳步做重触觉；设置页有提示音、振动两个开关；写错的样子：目标的步进函数只改索引、清进度、停表，不读提示音和振动偏好，不播 rawfile 提示音、不调 vibrator.startVibration；占位的 `FWD-REF` 标记被删掉却没写触觉
适用范围：功能接线阶段实现计时器自动推进下一步和长按跳步、源端带声音和振动反馈时
做法：
- 步骤切换分支读提示音、振动两个偏好，开着才执行：resourceManager.getRawFd('<提示音文件>') 交给 AVPlayer 的 fdSrc 播放；振动调 vibrator.startVibration({ type: 'time', duration: <源端毫秒数> }, { usage: … })
- 把源端振动封装（进度振动、重触觉）移植成目标端的同名封装，长按跳步调重触觉；设置页的两个开关做成运行期可观察的状态，供步进分支读取
- 删 FWD-REF 标记前逐条对照它的 trigger 文本和所属切片 Step 3c/3d 的 scope；写了 heavy-click haptic 或 feedback services 的，不能只重置进度、推进索引
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- startVibration(effect: VibrateEffect, attribute: VibrateAttribute): Promise<void>，需 ohos.permission.VIBRATE：触发振动（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，vibrator.startVibration）
- VibrateTime { type: 'time'; duration: number }，duration 单位 ms：按时长振动，源端毫秒数照搬（出处：鸿蒙 SDK 的 ets/api/@ohos.vibrator.d.ts，vibrator.VibrateTime）
- getRawFd(path: string): Promise<RawFileDescriptor>：取 rawfile 里提示音的文件描述符（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getRawFd）
- fdSrc?: AVFileDescriptor：AVPlayer 以文件描述符作播放源（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.fdSrc）
- getRawFd 取提示音交 AVPlayer，在非静默步骤切换时播放；按振动偏好调进度振动，长按跳步调重触觉；两项偏好做成 @ObservedV2/@Trace 运行期状态：修好后的接法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端振动时长、重触觉方式和提示音文件：源工程里振动封装类（调 Vibrator / VibrationEffect 的那个）和计时器步骤切换处的 MediaPlayer 调用；记下每种振动的毫秒数或效果、提示音的资源名，目标按同样的值写；提示音要已迁入目标的 rawfile
未核实：卡里的环境是 API 21，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-290eac71ee43fe336138（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 1；取值 5 ← 诊断
