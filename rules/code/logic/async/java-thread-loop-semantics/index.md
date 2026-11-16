# Java 线程、执行器和轮询循环的执行语义

agent 会看到什么：读到源端 Executors.newSingleThreadExecutor 串行写任务、Thread.currentThread 判重入，或 while (!isConnected()) { sleep; connect(); } 重连循环；交回的 Promise 队列在任务体内 await 同队列方法，或循环里多加了取消出口

## 规矩

- rule-5a04fb83b1db｜单线程写执行器改成 Promise 队列时，任务体内嵌套写调内部版本，不 await 同队列方法｜读到：源端用 Executors.newSingleThreadExecutor() 串行执行写任务，提交方法按 Thread.currentThread().getName() 判断已在执行线程就 runnable.run() 内联、否则 submit；任务体内还会调用同类的公开写方法；写错：目标端执行器只有 tail = tail.then(task) 的链式 Promise，没有重入判断；入队的任务体内 await 同一队列的公开写方法；注释声称单线程事件循环下重入天然成立
- rule-edc87a49c35e｜源码重连循环只在连上后退出时，目标循环内不加取消出口，取消留到下一轮检点｜读到：源码 while (!isConnected()) { sleep(500); connect(); }，循环内不检查取消，取消只在外层每一轮的检点生效；写错：目标的重连 while (!….isConnected()) 循环里加了 if (<取消标志>) return -1 这类出口
