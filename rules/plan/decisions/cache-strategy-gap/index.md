# decision_gaps 里的缓存或重绘选型

agent 会看到什么：规格的跨栈映射允许「OffscreenCanvas 缓存或每帧矢量重绘」二选一，worker 交回的 decision_gaps 只报选型，没写取值时机和源端的差异

## 规矩

- rule-241c1afa96f9｜交回的 decision_gaps 写明缓存策略改写带来的取值时机差异｜读到：规格的跨栈映射允许「OffscreenCanvas 缓存或每帧矢量重绘」二选一，要求行为等价；写错：worker 交回的 decision_gaps 只报缓存选型，没写选了每帧重绘后状态取值时机和源端不同、靠快照补齐
