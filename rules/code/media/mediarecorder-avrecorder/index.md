# MediaRecorder 录像迁成 AVRecorder 的配置、上限和错误

agent 会看到什么：读到源端 MediaRecorder 的 setOutputFile、setVideoEncoder、setMaxFileSize / setMaxDuration、onInfo 和 OnErrorListener；产物里 AVRecorderConfig / AVRecorderProfile 的 fileGenerationMode、url、videoCodec，替代上限的文件大小轮询和 setTimeout，以及 on('error') 里按什么分档

## 规矩

- rule-df799874844f｜相机录像默认用 AUTO_CREATE_CAMERA_SCENE，不用 createAsset 建 fd｜读到：源端 `MediaRecorder` 录像写到输出文件（可能带 `setMaxFileSize`）；决策台账只写「AVRecorder 录制 + photoAccessHelper 媒体库落盘」；写错：`AVRecorderConfig` 没设 `fileGenerationMode`，`url` 用 `helper.createAsset(PhotoType.VIDEO, 'mp4')` + `fileIo.openSync` 得到的 `fd://`，并按 fd 大小轮询 maxFileSize
- rule-05ddfcde4268｜源端编码可选 HEVC 时按配置用 VIDEO_HEVC 并先查可用编码器，不写死 AVC｜读到：源端 setVideoEncoder(MediaRecorder.VideoEncoder.HEVC)，或录像设置里可选 H264/HEVC；写错：AVRecorderProfile 固定写 videoCodec: media.CodecMimeType.VIDEO_AVC，不看所选编码；也没调用 getAvailableEncoder
- rule-0b26229d9548｜轮询文件大小合成到达上限事件时，未开启自动重启的分支要停止录制｜读到：源端 MediaRecorder.setMaxFileSize(...)，onInfo 里未开启自动重启、收到 MEDIA_RECORDER_INFO_MAX_FILESIZE_REACHED 时停止录制；写错：轮询文件大小合成 MAX_FILESIZE_REACHED 后，处理函数只在开启自动重启时处理，未开启时继续录制
- rule-43906cdeefa7｜应用层定时器替代 setMaxDuration 时，按不含暂停的已录时长计，暂停清表、恢复按余量重排｜读到：源端 MediaRecorder.setMaxDuration(上限 − 已累计时长)，pause 只把已录区间累加进累计时长；写错：启动后设一次性 setTimeout(上限毫秒数) 触发到达上限，暂停、恢复时既不清除也不重排；或删掉 AVRecorderConfig.maxDuration 只留这个墙钟定时器
- rule-df6ba4b63b2f｜AVRecorder 的错误按 BusinessError.code 数值分档，不按 message 字符串匹配｜读到：规格或源端把服务崩溃（SERVER_DIED）与其余录像错误分档提示；写错：on('error', (error: Error) => …) 里用 error.message.includes('5400105') 判定服务崩溃
