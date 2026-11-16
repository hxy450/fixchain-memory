# 应用层定时器替代 setMaxDuration 时，按不含暂停的已录时长计，暂停清表、恢复按余量重排

审的是：代码
触发（任一种）：
- 读到：源端 MediaRecorder.setMaxDuration(上限 − 已累计时长)，pause 只把已录区间累加进累计时长；写错的样子：启动后设一次性 setTimeout(上限毫秒数) 触发到达上限，暂停、恢复时既不清除也不重排；或删掉 AVRecorderConfig.maxDuration 只留这个墙钟定时器
适用范围：用应用层定时器承接录制器原生时长上限、且录制可以暂停时
做法：
- 暂停时 clearTimeout；恢复时按「上限 − 已录时长」重新 setTimeout；已录时长只累计 start/resume 到 pause/stop 之间的区间
- pause/resume 加防重入标志，暂停或恢复进行中时不再重排定时器
- 写单测核对「暂停 5s 不消耗 1s 上限」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setMaxDuration(int max_duration_ms)：单位毫秒；到达后 OnInfoListener 收到 MEDIA_RECORDER_INFO_MAX_DURATION_REACHED，录制被停止：源端由录制器自己计时并停止（出处：android.media.MediaRecorder#setMaxDuration）
- maxDuration?: number：单位秒，到达后自动停止，经 stateChange 通知 AVRecorderState = 'stopped'、StateChangeReason = BACKGROUND（@since 18）：目标录制器的原生时长上限，单位和源端不同（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorderConfig.maxDuration）
- pause(): Promise<void>；resume(): Promise<void>：AVRecorder 的暂停、恢复是异步的，清表和重排挂在这两处（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.pause / AVRecorder.resume）
- 暂停时清除计时、恢复后按「上限 − 已录时长」重排、pause/resume 防重入后，时长上限按已录时长生效：修好的写法（出处：卡里修好并验证过）
未核实：卡里的行为出自鸿蒙 SDK API 24，本机核对用 API 23
来源：1 张卡，1 个应用
- case-be892688a05d8782271e（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 1；取值 4 ← 诊断
