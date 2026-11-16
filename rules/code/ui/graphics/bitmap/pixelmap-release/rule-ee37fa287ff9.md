# 同一 PixelMap 送给两个接收方时，接收方 cloneSync 后各自持有、各自 release

审的是：代码
触发（任一种）：
- 写错的样子：画廊和 Canvas 覆盖层共用同一个 PixelMap，两边各自 release()，重复释放后另一边画不出来
适用范围：一份缩略图 PixelMap 同时送到画廊和覆盖层等多个接收方时
做法：
- 接收方收到后 pixelMap.cloneSync() 一份自己持有，用完 release 自己的那份；发送方只释放自己的
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- cloneSync(): PixelMap（@since 18）：从当前 PixelMap 克隆一份（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.cloneSync）
- release(): Promise<void>：释放 PixelMap（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.release）
- 接通两路后共用同一 PixelMap 会重复释放；覆盖层 cloneSync 独立持有后正常：返修的落法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-d5c3514ada560cb5134d（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；取值 3 ← 诊断
