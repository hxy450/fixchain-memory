# 源端仅调试用的日志迁进 401 刷新链时，取值放在不会抛错的旁路

审的是：代码
触发（任一种）：
- 读到：源端拦截器里的日志包在 `!environment.production` 判断下，如 console.info(request.url)；写错的样子：目标端 401→refresh→retry 主链里无保护地计算日志参数（hilog 的参数里调用可能抛错的 getter 或 toString()）
适用范围：把源端只在调试构建输出的日志迁到目标端拦截器的刷新/重试主链时
做法：
- 日志的取值先在 try/catch 里算好（失败给占位值），再交给 hilog；日志出错不得中断 401→refresh→retry
来源：1 张卡，1 个应用
- case-5fa5586d4aba0a31c0e6（real-estate-hmos）：做法第 1 步 ← 建议 2
