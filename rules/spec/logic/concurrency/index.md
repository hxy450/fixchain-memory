# 线程与调用顺序

读到新开 Thread 后 Handler.post / runOnUiThread、单线程执行器、sleep 重连循环或前后依赖的同步调用，规格里写竞态、异步形态和串行要求时

## 触发族

- [后台线程回投 UI 和单线程执行器](background-thread-post/index.md)（6 条）：读到源码新开 Thread 或循环线程做完后 Handler.post / runOnUiThread 回 UI（不判 isFinishing、每帧都 post 弹窗），或单线程执行器在执行线程内直接内联运行；规格的竞态条目、弹窗状态和验收条目写成丢弃迟到结果、两个布尔旗、只验提交顺序
- [源端同步执行的调用序列和阻塞循环](sync-call-sequences/index.md)（3 条）：读到源码 while (!isConnected()) { sleep(500); connect(); } 这类不查取消的重连循环，或同一方法里先后同步调用两个平台方法且后者依赖前者（如 `Vibrator.cancel()` 后接 `vibrate(...)`）；规格新增了取消出口却没登记偏离，或把目标 API 标成 Promise 形、服务层 void 却没写串行要求
