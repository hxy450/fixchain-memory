# 源端拍照带完成和失败回调时，桥接契约要回传完成 / 失败，编排器在入口里复位状态和续拍

审的是：代码
触发（任一种）：
- 读到：源端以 takePicture(pictureCallback, errorCallback) 发起拍照：完成回调里复位拍照状态、续拍剩余的重复张数、按偏好暂停预览，失败回调重启预览；写错的样子：桥接接口把拍照定义成无参无回调的 takePicture: () => void；编排器没有完成 / 失败入口，拍照中的状态没有复位点，续拍函数没有调用者，暂停预览没实现
适用范围：目标端把拍照编排和相机拍照图元拆到不同模块、经桥接接口连接时
做法：
- 桥接的拍照图元返回完成 / 失败（回调或 Promise），编排器提供完成入口和失败入口，两处都统一复位拍照状态
- 完成入口里续拍剩余的重复张数、按「拍照后暂停预览」偏好暂停预览；失败入口里重启预览
- 加最小检查：重复 3 张的桩在完成回调后再触发 2 次拍照；失败桩之后拍照状态回到常态、结束拍照的通知被调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- capture(): Promise<void>：PhotoOutput 发起拍照，只表示请求已下发（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.capture）
- on(type: 'photoAvailable', callback: AsyncCallback<Photo>): void：PhotoOutput 拿到照片的事件，完成入口从这里接（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.on('photoAvailable')）
- on(type: 'error', callback: ErrorCallback): void：PhotoOutput 的错误事件，失败入口从这里接（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.on('error')）
- on(type: 'captureEnd', callback: AsyncCallback<CaptureEndInfo>): void：PhotoOutput 拍照结束事件（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.on('captureEnd')）
未核实：卡里记的鸿蒙 SDK 是 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-c44827a6995fcd17b82f（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
