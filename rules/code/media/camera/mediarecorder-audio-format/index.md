# MediaRecorder 的音源、封装格式和音频参数

agent 会看到什么：读到源端 MediaRecorder 的 setAudioSource(AudioSource.CAMCORDER / UNPROCESSED)、setOutputFormat(THREE_GPP / WEBM)、只在录音开关打开时才调的 setAudioEncoder；产物里 AVRecorderConfig 的 audioSourceType、fileFormat 和 AVRecorderProfile 的音频字段

## 通用查法

### MediaRecorder 的录像选项逐项查 media 声明，有对应项照写，没有就报错

审的是：代码
触发（任一种）：
- 读到：源端 MediaRecorder 的 setAudioSource、setOutputFormat 传入 AudioSource.*、OutputFormat.* 常量；写错的样子：audioSourceType、fileFormat 换成相邻的枚举（AUDIO_SOURCE_TYPE_MIC、CFT_MPEG_4）或只改扩展名，注释写「无对应枚举」
适用范围：MediaRecorder 录像迁到 AVRecorder 时各选项常量的映射
做法：
- 在 android.media.MediaRecorder 的 AudioSource、OutputFormat 里读常量注释的含义，到鸿蒙 SDK 的 @ohos.multimedia.media.d.ts 按同一场景找 AudioSourceType、ContainerFormatType 的成员
- 找到的照写（例：录像场景的 AudioSource.CAMCORDER 对应 AUDIO_SOURCE_TYPE_CAMCORDER）；确认没有的，在创建录制资产前抛错并提示用户，不换成相邻选项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- audioSourceType?: AudioSourceType：AVRecorderConfig 上设音源的字段，录音时必填（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.AVRecorderConfig.audioSourceType）
针对本应用要查的：
- 源端实际会传给 MediaRecorder 的录像选项：源工程 Java / Kotlin 里 MediaRecorder 的 setAudioSource、setOutputFormat、setCaptureRate 调用，以及给它们传值的录像设置（偏好键和可选项数组）；把每个可能传入的常量都列出来，逐个按上面的做法找对应项
未核实：卡的环境是 API 24，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-9d3828c851006d29fc06（opencamera-hmos）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 3、诊断

## 规矩

- rule-07bd217128ef｜源端音源 CAMCORDER 映射成 AUDIO_SOURCE_TYPE_CAMCORDER，不回落成 MIC｜读到：源端 setAudioSource(MediaRecorder.AudioSource.CAMCORDER)，或规格的音源映射写「默认/camcorder → CAMCORDER」；写错：camcorder 和默认值被映射成 AudioSourceType.AUDIO_SOURCE_TYPE_MIC，文件头注释写「CAMCORDER 无对应枚举」
- rule-b161bceaf37c｜录像关闭录音时不设 audioSourceType，AVRecorderProfile 省略音频四个字段｜读到：源端只在录音开关打开时调用 setAudioSource / setAudioEncoder（录像设置里有是否录音的开关）；写错：不论录音开关，AVRecorderProfile 都下发 audioBitrate、audioChannels、audioCodec、audioSampleRate
- rule-6c897a52513c｜录像选项在目标确实不支持时，创建资产前明确报错，不静默换成别的选项｜读到：源端 setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP) 或 OutputFormat.WEBM；写错：3gp/webm 只改了文件扩展名，fileFormat 仍是 ContainerFormatType.CFT_MPEG_4，没有提示
