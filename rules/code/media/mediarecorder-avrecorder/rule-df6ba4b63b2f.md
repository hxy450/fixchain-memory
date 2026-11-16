# AVRecorder 的错误按 BusinessError.code 数值分档，不按 message 字符串匹配

审的是：代码
触发（任一种）：
- 读到：规格或源端把服务崩溃（SERVER_DIED）与其余录像错误分档提示；写错的样子：on('error', (error: Error) => …) 里用 error.message.includes('5400105') 判定服务崩溃
适用范围：目标用 AVRecorder 录像并按错误类型分档处理时
做法：
- 错误回调参数按 BusinessError 取 code 数值：err.code === media.AVErrorCode.AVERR_SERVICE_DIED（5400105）为服务崩溃档，其余为普通错误档
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- on(type: 'error', callback: ErrorCallback): void：AVRecorder 的错误事件；码值有 5400101–5400107（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVRecorder.on('error')）
- ErrorCallback<T extends Error = BusinessError>；BusinessError 的 code: number：回调参数默认是 BusinessError，错误码在 code 上（出处：鸿蒙 SDK 的 ets/api/@ohos.base.d.ts，ErrorCallback / BusinessError.code）
- AVErrorCode.AVERR_SERVICE_DIED = 5400105：服务进程崩溃（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVErrorCode.AVERR_SERVICE_DIED）
- on(type: 'error', callback: ErrorCallback): void（AVPlayer）：同族接口：AVPlayer 的错误事件同样按 BusinessError.code 判（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.media.d.ts，AVPlayer.on('error')）
未核实：message 文案里是否带码值声明没写；卡里只写了改成按 code 判定
来源：1 张卡，1 个应用
- case-b89cd099bfa87829fd2d（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断
