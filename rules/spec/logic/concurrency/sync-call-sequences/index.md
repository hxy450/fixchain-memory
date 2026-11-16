# 源端同步执行的调用序列和阻塞循环

agent 会看到什么：读到源码 while (!isConnected()) { sleep(500); connect(); } 这类不查取消的重连循环，或同一方法里先后同步调用两个平台方法且后者依赖前者（如 `Vibrator.cancel()` 后接 `vibrate(...)`）；规格新增了取消出口却没登记偏离，或把目标 API 标成 Promise 形、服务层 void 却没写串行要求

## 规矩

- rule-b0f7110e515a｜映射表把同步调用换成 Promise 形且服务层是 void 时，规格写明连续调用的串行要求和可单测判据｜读到：源端同一方法里依次同步调用两个平台方法且后者依赖前者生效（如 `Vibrator.cancel()` 后紧接 `vibrate(...)`）；写错：规格的映射表把对应目标 API 标为「Promise 形」、服务层把方法声明为 void，契约里却没写「前一调用完成后才发后一调用」，对应验收条目也没有可单测的判据
- rule-4f49bc2b5d73｜规格描述源码重连循环时保留源码退出条件，新增取消出口要登记为显式偏离并同步 AC｜读到：源码重连循环 while (!isConnected()) { sleep(500); connect(); }，循环内不检查取消；写错：规格附录写「页面销毁必须能终止该循环」「以取消标志为唯一出口」，主规格 AC 却写「循环 connect 直到成功」，决策台账里没有这条偏离
- rule-c2fd0cb63c8b｜规格接口清单不照搬 Java 的 void，阻塞等待的方法写成 Promise<void> 并在验收写明需 await｜读到：源方法是 void 但内部阻塞等待队列、线程或 IO 完成，验收里有「X 先于 Y」的排序要求；写错：规格接口清单照搬 Java 签名写成 xxx(): void，没标出 ArkTS 里它必须是可 await 的 Promise；验收没写调用方需 await
