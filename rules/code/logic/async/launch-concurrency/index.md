# 协程 launch 的并发和排队

agent 会看到什么：读到源端每次触发都 viewModelScope.launch / launch 新任务（不取消在途的前一组、或在 Mutex.withLock 后排队），交回的代码对新调用一律 cancel 上一请求、generation 全局递增，或直接返回在途的 Promise

## 规矩

- rule-753ca047b8e3｜共享单例 ViewModel 按规格的业务键只丢旧键迟到响应，不让新调用一律取消上一请求｜读到：规格状态段写「以某个业务键（如城市 id）作 generation key，旧键的迟到响应不得覆盖新页面」；安卓源码每次用 viewModelScope.launch / async 发一组请求，后到的调用不取消在途的前一组；写错：单例里的加载方法对任何新调用都先 cancel() 上一请求，generation 计数全局递增，不分键
- rule-e3ccf8c7b1cb｜串行化的同步服务不给全量同步加「返回在途 Promise」捷径，用请求版本号补跑尾随请求｜读到：源端每次同步触发 launch 新任务，在 Mutex.withLock 后排队执行，不合并在途任务；写错：目标端用 Promise 链 / 串行队列统一调度后，全量同步入口在有在途 Promise 时直接 `return await` 它，运行中新到的请求不再获得推送轮次
