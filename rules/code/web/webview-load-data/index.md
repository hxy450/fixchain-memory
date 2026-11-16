# loadDataWithBaseURL 程序装载的正文

agent 会看到什么：读到 webView.loadDataWithBaseURL(baseUrl, data, "text/html", "utf-8", historyUrl)，常在数据加载完成的回调里调；产物里 controller.loadData 的参数个数、baseUrl 和清洗，以及调用前有没有等 onControllerAttached

## 规矩

- rule-a12831dcb777｜loadDataWithBaseURL 迁移时用五参 loadData 带上 baseUrl，并先清洗｜读到：`loadDataWithBaseURL(baseUrl, data, "text/html", "utf-8", historyUrl)`，data 先经清洗器产出；写错：目标写成三参 loadData(data, 'text/html', 'utf-8')，正文直接装原始文本；baseUrl、historyUrl 和清洗都推到占位说明里「如需再切五参重载」
- rule-02b17be386cc｜异步数据回来后调 controller.loadData 时，以 onControllerAttached 置位为前提｜读到：源端在数据加载完成的回调里直接调 `webView.loadDataWithBaseURL(...)`；写错：目标在异步数据回来后直接调 controller.loadData(...)，Web 上没有 .onControllerAttached(...) 置位守卫，默认「异步加载足够慢、controller 已挂接」
