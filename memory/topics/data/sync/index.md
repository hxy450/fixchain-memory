# data/sync

同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤

[上一级](../index.md)

## 本级经验

- [同步终态只在最后一轮后发一次，开始进度保留源门控](lesson-34f35851208470602570.lesson.md) · 阶段：execute/verify · 信号：SyncCoordinator, EventBus, onComplete
- [同步调度合并在途任务要补跑尾随请求，失败项重推](lesson-cfe552e1b20080212ce9.lesson.md) · 阶段：spec/execute/verify · 信号：Mutex.withLock, Promise
- [多路聚合缓存至少一路成功才写，命中校验时效和载荷](lesson-c6379cfcbee86500f91f.lesson.md) · 阶段：execute · 信号：refreshTime, Promise.all, Promise.allSettled, TTL
- [异步落库完成后再广播触发重查的事件](lesson-1d3ab8b9d39bd8f6e24d.lesson.md) · 阶段：execute · 信号：Promise
- [替代作业聚合器时结束作业写显式终态不删键](lesson-d18e6e019cad3d26839b.lesson.md) · 阶段：execute · 信号：WorkManager, LiveData, COMPLETED
- [重写多阶段数据流程时保留缓存写入等副作用步骤](lesson-686bbe76f7c2c783f2bd.lesson.md) · 阶段：spec/execute/verify · 信号：DAO, currentId, Repository
