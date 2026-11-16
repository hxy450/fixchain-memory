# Java 线程和阻塞调用改写成 async

agent 会看到什么：读到源端 Java 的 Thread、Handler、BlockingQueue.take / put 常驻消费、Object.wait / notifyAll 阻塞等待、同步提交后把挂起字段置空，或 new Thread 里成功后才写字段、调用方随即清零；产物里的 Promise 泵、async 方法里 await 和置空、清零的先后、void 前缀丢掉的 Promise 和 (): void 的等待方法

## 规矩

- rule-d12a6f5b374f｜源端阻塞等待接到「X 先于 Y」的验收时，等待链一路 Promise<void> 并逐层 await｜读到：源端 void 方法内部阻塞等待队列、线程完成（Object.wait()、BlockingQueue），规格验收写「排空先于销毁」「先等待再重启」；目标端的等待方法是 async、返回 Promise<void>；写错：调用方用 `void` 前缀丢弃等待方法返回的 Promise，或等待方法、销毁序列仍是 `(): void`，调用后立即销毁、重启
- rule-3c9207648295｜BlockingQueue 常驻消费改写成 Promise 泵时，先入队启动泵，逐请求 try/catch｜读到：源端保存线程 while(true) 里 queue.take() 常驻消费，生产者 put 后按成本追加占位请求；规格写「满队等待空位」「等待入队与计数分离」；写错：按需启动的消费泵：入队方法先 await 全部占位请求才启动泵；泵循环不对单个请求 `try/catch`，运行标志只在循环正常退出时复位
- rule-7302f65fc1fc｜把同步的「提交后清空挂起状态」移植到 async 时，先摘下挂起对象再 await｜读到：源端 Java 在调用线程上同步提交或保存挂起对象后把挂起字段置空（`字段 = null`）；写错：ArkTS 里先 await 提交或保存的调用，之后才把挂起字段置空（this.pending = null）
- rule-a994cf17829a｜源端异步写被同步化后，调用方先取出旧值并写清零，再调用同步方法｜读到：源端调用方先调一个在 new Thread 里成功后才写某字段的方法，紧接着在主线程把同一字段置 0；写错：目标的处理（如 onBackPress 里）照源端书写顺序先调已同步化的方法、再把字段置 0，同步方法里的写被随后的清零覆盖
