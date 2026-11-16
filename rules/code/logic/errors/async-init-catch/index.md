# 异步初始化的 Promise 和 catch 分支

agent 会看到什么：读到源端同步读设置（SharedPreferences.getString 带默认值）而目标偏好封装是 async、会 throw，或规格要求在 catch 里有条件地向上抛，产物里是 initialize() 的 try/catch 和已初始化标志、aboutToAppear 里 initialize().then 有没有 .catch，以及 catch 里的 throw error

## 规矩

- rule-d1fb4bf986a2｜同步读设置改成 async load 时，initialize 用 try/catch，失败复位已初始化标志｜读到：源端用 SharedPreferences 的 getString / getInt 带默认值同步读设置（Compose 在 remember 里读）；目标端的偏好封装是 async，内部返回 preferences.getPreferences(...) 的 Promise，未就绪时 throw；写错：initialize() 里先写 `this.initialized = true` 再 await 加载，没有 try/catch；加载 reject 时标志不复位，之后再调用直接返回
- rule-ad1a6602137b｜加载门用 LoadingProgress 切换时，initialize().then 必须配 catch 并离开加载态｜读到：目标端 ViewModel 的 initialize() 返回 Promise，加载链可能 reject（偏好封装里有 throw 或异步读取）；写错：页面在 aboutToAppear 里写 initialize().then(...) 没有 .catch，build 里用已加载标志在正式内容和 LoadingProgress() 之间切换，没有失败分支
- rule-96a5bec3606c｜catch 里重新抛出时先收窄成 Error，不直接 throw catch 变量｜读到：规格或巡检要求区分「过期任务的异常按取消处理、当前任务的异常继续上报」，由上层处理返回的 Promise，需要在 catch 分支里有条件地向上抛；写错：ArkTS 代码里写出 `catch (error) { … throw error; }`，把未定类型的 catch 变量原样抛出；编译报 10605087 `arkts-limited-throw`
- rule-97d886639797｜源端构造期 runBlocking 完成初始化时，目标设显式初始化门禁并让所有入口先 await｜读到：源端客户端在 init { runBlocking { initialize() } } 里同步初始化，业务方法经一个守卫在未就绪时返回错误码；写错：目标逐次守卫在未初始化时自己从数据库解码密钥并照常发请求，没有 `initialized` 门禁；后台同步入口没有先 await initialize()
