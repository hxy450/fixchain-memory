# 录音监听服务分 create 与 start 时，调用方在创建成功后调 start 并发启动回调

审的是：代码
触发（任一种）：
- 读到：源端监听类在构造里建 `AudioRecord` 并 `startRecording()`，调用方另调 `start()` 起采样线程，线程退出时 `release()`；调用方在启动成功后切换图标、释放后再切回；写错的样子：目标在异步 `create()` 成功后只赋字段、置标志、弹 toast，没调 `start()`，也没发启动成功的状态回调；释放处不发已停止回调
适用范围：把安卓录音、声控监听迁成 ArkTS 服务类（AudioCapturer 封装成 create()/status()/start()/release()），由别的切片的 VM 调用时
做法：
- 按源调用方的顺序写：await create() 成功 → start() 起采样循环 → 发「已启动」状态回调；释放监听后发「已停止」回调
- 调用跨切片服务前先读它的公开方法（create、status、start、release 各做什么），和源调用方的方法体逐步对齐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- start(): Promise<void>：AudioCapturer 开始采集；只启动录音器，读数据要另外订阅（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioCapturer.start）
- on(type: 'readData', callback: Callback<ArrayBuffer>): void：有数据可读时回调；read(size, isBlockingRead) 自 API 11 起废弃，改用这个事件（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioCapturer.on('readData')、AudioCapturer.read）
- release(): Promise<void>：释放采集器；没有采样循环时也要有路径调到它（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.audio.d.ts，AudioCapturer.release）
- AudioRecord#startRecording()、AudioRecord#read(short[], int, int)、AudioRecord#release()：源端开始录音、读数据、释放原生资源的三步（出处：android.media.AudioRecord#startRecording、android.media.AudioRecord#read、android.media.AudioRecord#release）
- create() 已启动原生录音器，不调 start() 时读数为 0、原生释放为 0：修复前复现到的行为；修复后创建成功即 start 并发启动回调（出处：卡里修好并验证过）
未核实：卡里的行为出自鸿蒙 SDK API 24，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-7d9a07a6b9ead03f55b6（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断
