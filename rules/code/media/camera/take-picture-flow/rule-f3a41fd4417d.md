# 规格要求布尔参数开启连拍时，编排层自建连拍循环，不用 void 吞掉参数

审的是：代码
触发（任一种）：
- 读到：规格的 AC 写明某个布尔参数为 true 时要「长按后连续多帧 onPictureTaken」，源端长按快门持续出帧、松手停止；写错的样子：拍照编排函数里用 `void 参数名;` 丢弃这个标志，只走一次单拍；编排器里没有连拍循环、在途帧状态和停止连拍的方法
适用范围：目标相机接口没有连续 burst 类型、要在编排层复刻源端长按连拍时
做法：
- 在编排层自建连拍循环：记录在途帧，上一帧回调（PhotoOutput 的 photoAvailable）回来后检查是否仍在连拍再续拍，并提供停止连拍和查询连拍是否进行中的方法
- 做不到时登记 FWD-REF 或 PD，不能静默退化成单拍
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- PhotoOutput.capture(): Promise<void>：一次只拍一张，连拍要在上层循环调用（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.capture）
- PhotoOutput.on(type: 'photoAvailable', callback: AsyncCallback<Photo>): void：一帧出图的回调，续拍放在这里（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.on('photoAvailable')）
- 编排器新增连拍上下文、一帧在途状态机和停止 / 续拍 / 结束三个动作后，长按得到连续多帧：修复后的写法（出处：卡里修好并验证过）
未核实：卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-56249562721f5dc59148（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
