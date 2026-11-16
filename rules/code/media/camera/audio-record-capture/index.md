# AudioRecord 录音采集的创建和启动

agent 会看到什么：读到源端监听类在构造里建 AudioRecord 并 startRecording()、调用方另调 start() 起采样线程、线程退出时 release()；产物里 AudioCapturer 的异步 create() 成功后有没有调 start()、发启动和停止的状态回调

## 规矩

- rule-eb696e012cb3｜录音监听服务分 create 与 start 时，调用方在创建成功后调 start 并发启动回调｜读到：源端监听类在构造里建 `AudioRecord` 并 `startRecording()`，调用方另调 `start()` 起采样线程，线程退出时 `release()`；调用方在启动成功后切换图标、释放后再切回；写错：目标在异步 `create()` 成功后只赋字段、置标志、弹 toast，没调 `start()`，也没发启动成功的状态回调；释放处不发已停止回调
