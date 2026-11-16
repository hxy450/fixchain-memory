# 单例数据层的 addListener 订阅

agent 会看到什么：读到源端用 LiveData / Flow 的 observeAsState、collectAsState 观察数据（随生命周期自动结束），交回的代码在应用级单例的数据层上写 addListener / removeListener

## 规矩

- rule-e84dd58ad911｜页面向单例仓库 addListener 时，回调存成字段并在 aboutToDisappear 里移除，不传内联箭头函数｜读到：源端页面用 observeAsState() / collectAsState() / DisposableEffect 观察数据，观察随组合退出自动结束；目标数据层是单例，提供 addListener / removeListener（按回调引用移除）；写错：页面 aboutToAppear 里写 services.preferences.addListener(snapshot => {...}) 内联回调、不存字段；页面没有 aboutToDisappear，或 aboutToDisappear 里没有对应的 removeListener
- rule-c6c676710035｜数据层设计监听接口时，addListener 返回可移除的句柄，让调用方必须持有它｜读到：计划或验收写「订阅可释放」，源端数据层用 LiveData / Flow 给多个页面提供可观察数据，目标数据层是应用级单例；写错：数据层 addListener(cb) 返回 void，只能靠 removeListener(cb) 按回调引用移除
