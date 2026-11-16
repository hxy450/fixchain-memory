# FlutterBoost 宿主页的事件通道

agent 会看到什么：读过的源码里宿主挂 FlutterBoostFragment 子类或有事件通道常量表，用 addEventListener / sendEventToFlutter 收发事件；交回的宿主页只挂 FlutterUIComponent、没有对应的监听和推送

## 规矩

- rule-1429db088366｜Flutter 宿主挂的是自定义 FlutterBoostFragment 子类时，目标页逐项实现它的事件通道｜读到：源宿主挂的是 `FlutterBoostFragment` 子类（如经 `CachedEngineFragmentBuilder(<子类>::class.java)` 构造），子类里 `addEventListener(通道名, …)` 分发事件、`sendEventToFlutter(...)` 推数据；写错：目标宿主页只挂 `FlutterUIComponent({ uri: … })`，没有 `addEventListener` 监听和 `sendEventToFlutter` 推送，也没标缺口
