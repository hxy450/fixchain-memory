# 异步与并发

源端有 viewModelScope.launch、多路请求和缓存、Mutex.withLock、Executors 单线程执行器、Thread 轮询重连循环，目标端有 Promise、async / await、请求取消和排队时

## 触发族

- [ViewModel 多路请求的部分失败和缓存](partial-failure-cache/index.md)（5 条）：读到源 ViewModel 先读缓存再请求、几个请求各自 launch、只在 Result.Success 时替换数据（或规格写「失败读有效缓存、不清空整页」），交回的代码把任一失败映射成整页 ERROR、返回 FAILED 加空模型，或全失败时仍写新时间戳的缓存
- [协程 launch 的并发和排队](launch-concurrency/index.md)（2 条）：读到源端每次触发都 viewModelScope.launch / launch 新任务（不取消在途的前一组、或在 Mutex.withLock 后排队），交回的代码对新调用一律 cancel 上一请求、generation 全局递增，或直接返回在途的 Promise
- [Java 线程、执行器和轮询循环的执行语义](java-thread-loop-semantics/index.md)（2 条）：读到源端 Executors.newSingleThreadExecutor 串行写任务、Thread.currentThread 判重入，或 while (!isConnected()) { sleep; connect(); } 重连循环；交回的 Promise 队列在任务体内 await 同队列方法，或循环里多加了取消出口
- [Java 线程和阻塞调用改写成 async](java-thread-to-async/index.md)（4 条）：读到源端 Java 的 Thread、Handler、BlockingQueue.take / put 常驻消费、Object.wait / notifyAll 阻塞等待、同步提交后把挂起字段置空，或 new Thread 里成功后才写字段、调用方随即清零；产物里的 Promise 泵、async 方法里 await 和置空、清零的先后、void 前缀丢掉的 Promise 和 (): void 的等待方法
- [按键登记的在途任务表](running-task-table/index.md)（1 条）：读到源端 JobService 的 onStartJob / onStopJob 和 jobs.remove(jobId)，或规格写同一 Job ID 先 cancel 旧 handle 再写入；产物里 Map<number, TaskHandle> 运行表在任务 finally 里无条件 running.delete(workId)
- [单飞缓存的 Promise 入口](single-flight-promise/index.md)（1 条）：读到规格给出返回 Promise<T> 的一次性入口、AC 要求「防重守卫：连续两次调用仅执行一次」；产物里入口写成 static async 方法、方法体 return 缓存在字段里的 Promise
