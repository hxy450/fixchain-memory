# arkts/async-mapping

源端同步调用、线程与事件投递改成 Promise/异步 API 后的时序、重入、线程与结果三态

[上一级](../index.md)

## 本级经验

- [EventBus 需同步按引用投递时自建订阅表](lesson-9db967b1941da87f27be.lesson.md) · 阶段：execute · 信号：EventBus, EventBus.getDefault, @ohos.events.emitter, eventHub
- [单线程执行器改 Promise 队列时给重入内部版本](lesson-cdc6de4ebcdeeadc287c.lesson.md) · 阶段：execute · 信号：Executor, runnable.run(), Promise
- [后台拷贝用异步 IO 或 taskpool，不包 *Sync](lesson-c54d1c8af2177b819837.lesson.md) · 阶段：execute · 信号：AsyncTask, doInBackground, THREAD_POOL_EXECUTOR, fileIo.copyFileSync
- [挂起对象先摘下置空，再 await 提交](lesson-bc21e9552e5b38bb27d7.lesson.md) · 阶段：execute · 信号：Promise, BlockingQueue.put, synchronized
- [被拒与故障都 reject 时用单次适配器还原三态](lesson-47faf26b44bb4075b0d2.lesson.md) · 阶段：execute · 信号：BusinessError, Promise&lt;void&gt;, IOException, TagLostException
- [连续同步平台调用改 Promise 时在网关内串行](lesson-ba0cb144aa48f9584060.lesson.md) · 阶段：spec/execute · 信号：Vibrator.cancel, vibrate(pattern), stopVibration, startVibration
- [阻塞等待改 Promise 后签名与调用链一路 await](lesson-c53d56284f178b5ab63f.lesson.md) · 阶段：spec/execute · 信号：Thread.join, Object.wait, CountDownLatch.await, Future.get
- [阻塞队列改 Promise 泵：先启泵，单项失败不卡队](lesson-256f088e149edbcb3e64.lesson.md) · 阶段：execute · 信号：BlockingQueue, ArrayBlockingQueue, LinkedBlockingQueue, take()
