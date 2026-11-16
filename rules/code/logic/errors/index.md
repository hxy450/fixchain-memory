# 异常与日志

源端有 try/catch 按异常类或消息分流、Log.e / Log.w、会抛错的异步初始化，目标端有 catch 的范围、Promise 的 .catch、console.error / hilog 时

## 触发族

- [新写或改写的日志调用](log-calls/index.md)（2 条）：源端 Log.e / Log.w 或静默吞错的 catch，工程已有 hilog 写法；产物里 catch 和边界处新写的 console.error / hilog 调用缺定位字段或带了敏感内容
- [异步初始化的 Promise 和 catch 分支](async-init-catch/index.md)（4 条）：读到源端同步读设置（SharedPreferences.getString 带默认值）而目标偏好封装是 async、会 throw，或规格要求在 catch 里有条件地向上抛，产物里是 initialize() 的 try/catch 和已初始化标志、aboutToAppear 里 initialize().then 有没有 .catch，以及 catch 里的 throw error
- [Java 异常的捕获和分流](java-exception-catch/index.md)（7 条）：读过的 Java 源码里有 try/catch、按异常类或 getMessage() 分流；交回的代码里 catch 的范围、取消息和按错误分类的写法
- [主体加载和辅助请求共用的 try](aux-request-try/index.md)（1 条）：产物里辅助接口的 await 赋值写在主体加载同一个 try 的末尾：失败时用 [] 覆盖已有列表，或异常落进主 catch 把整次加载置成错误
- [源函数的失败处理范围：try/catch 和 Either 的 Left](failure-handling-scope/index.md)（2 条）：读到源端辅助函数内部自带 try/catch 只记日志、循环里不逐条 catch、chunked(N).forEach 忽略单批失败，或调用链用 .onLeft { Log.e(…) } 消费 Either / Result 的失败；产物里 catch 包的范围、continue / return 和对返回值的处理和源端不同
- [BusinessError.code 的错误码判别](businesserror-code-compare/index.md)（1 条）：读到 d.ts 里接口写着 @throws { BusinessError } 加数值错误码（如 geoLocationManager 的 3301100）；产物里 catch 中用 (error as BusinessError).code === 某个常量分派错误分支
