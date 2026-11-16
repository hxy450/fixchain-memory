# 源端 catch 里的 HTTP 失败和目标的失败信封

agent 会看到什么：读到源端请求包在 try/catch 或错误回调里，catch 中 error instanceof HttpErrorResponse 时设错误并 return false、成功路径才改 hasMore / 游标；产物里目标客户端永不 reject、返回失败信封，调用方有没有 res.status !== 200 分支，单测有没有注入失败信封

## 规矩

- rule-7930d84550da｜源 catch 承载 HTTP 失败而目标客户端永不 reject 时，先写 status!==200 分支｜读到：源端请求包在 try/catch（或 Promise/Observable 的错误回调）里，catch 中 `error instanceof HttpErrorResponse` 时取 error.error?.message 设错误并 return false，成功路径才改 hasMore/游标；写错：目标端请求返回后直接取 res.data 走成功路径，没有 res.status !== 200 分支，只留了一个 catch
- rule-3b0a098d12fe｜分页加载的单元测试要注入失败信封，断言返回 false 且 hasMore、游标不变｜读到：源端分页方法失败时设错误、return false，成功路径才改 hasMore/游标；写错：测试里 mock 的 HttpClient 只返回 status 200 的信封，没有用例覆盖 status !== 200 时 loadMore 的返回值和状态
