# 录像关闭录音时不设 audioSourceType，AVRecorderProfile 省略音频四个字段

审的是：代码
触发（任一种）：
- 读到：源端只在录音开关打开时调用 setAudioSource / setAudioEncoder（录像设置里有是否录音的开关）；写错的样子：不论录音开关，AVRecorderProfile 都下发 audioBitrate、audioChannels、audioCodec、audioSampleRate
适用范围：安卓录像迁到 AVRecorder、录音可关的情形
做法：
- 录音关闭时，AVRecorderConfig 不设 audioSourceType，AVRecorderProfile 省略 audioBitrate / audioChannels / audioCodec / audioSampleRate；打开时四个字段和音源一起设
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- avConfig 中仅设置视频相关参数是纯视频录制；添加了音频参数，系统认为是「音频+视频录制」：关闭录音就不能带音频字段（出处：video-recording.md，开发步骤及注意事项）
- audioBitrate?: number、audioChannels?: number、audioCodec?: CodecMimeType、audioSampleRate?: number，注释都写 This parameter is mandatory for audio recording：四个都是可选字段，只在录音时必填（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，media.AVRecorderProfile）
- 关闭音频时省略音频字段：修好的写法（出处：卡里修好并验证过）
未核实：带着音频字段而关闭录音时设备上的具体表现，卡里没写
来源：1 张卡，1 个应用
- case-9d3828c851006d29fc06（opencamera-hmos）：做法第 1 步 ← 诊断；取值 3 ← 诊断
