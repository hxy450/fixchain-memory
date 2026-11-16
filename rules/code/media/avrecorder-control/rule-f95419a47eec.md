# AVRecorder.stop 失败时在 finally 复位录制中标志，删坏片并回传空 URI

审的是：代码
触发（任一种）：
- 读到：源端 MediaRecorder.stop() 抛 RuntimeException 时删掉输出文件（坏片）；写错的样子：stop 失败分支删了坏片仍以原 URI 回调停录结果；录制中标志只在 release() 里复位，recorder.stop() 失败后仍为 true
适用范围：目标用 AVRecorder 停录并把录像文件回传给上层时
做法：
- await recorder.stop() 包在 try/finally 里，finally 复位录制中标志
- stop 抛错时删掉输出文件，并以空 URI 回调停录结果，不回传原 URI
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stop() 没收到有效音视频数据时故意抛 RuntimeException，让应用清理没写完整的输出文件：源端 stop 失败即坏片（出处：android.media.MediaRecorder#stop）
- stop(): Promise<void>，可能以 5400102、5400103、5400105 拒绝：目标端 stop 失败走 Promise 拒绝（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.stop）
未核实：卡里观察到的行为出自 HarmonyOS 6.1.1（API 24），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-b89cd099bfa87829fd2d（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断
