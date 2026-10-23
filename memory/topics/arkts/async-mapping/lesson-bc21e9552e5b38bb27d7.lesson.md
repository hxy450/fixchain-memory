# 源端同步“提交后清空挂起对象”改成含 await 的异步实现时，先摘下挂起对象并置空再 await 提交，不在 await 之后清空

ID：`lesson-bc21e9552e5b38bb27d7` · 版本：1 · 阶段：execute · 主题：[arkts/async-mapping](index.md)

概要：挂起对象先摘下置空，再 await 提交

信号：`Promise`, `BlockingQueue.put`, `synchronized`

## 何时使用

实现阶段，把源端在单线程里同步执行的“入队或保存 → 清空挂起字段”改写为含 await 的异步方法时

## 适用情境

源端在 UI 线程同步调用入队或保存，随后把挂起的批次或请求字段置空；目标的入队在队列满时 await 让出事件循环，挂起字段在 await 返回后才置空；等待期间其他回调（新一帧、新一次拍照）会读写同一字段。

## 原因

await 让出后，其他回调可能新建挂起对象，或继续向旧对象追加；await 返回后的置空会清掉新对象，或让旧对象在提交后继续收数据。源端同步执行时不存在这段交错窗口。

## 做法

1. 在第一个 await 之前把挂起对象存进局部变量并把字段置空，再 await 提交这个局部对象。
2. 移植源端同步方法时列出 await 两侧读写的共享字段；await 之后的写入先确认不会覆盖等待期间别处的修改。

## 可选检查

- 对交错有疑问时写测试：提交等待期间新建一个批次，提交返回后新批次仍在，旧批次不再收数据。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [ViewModel 每步须有 feature 认领或跨契约](../../process/enumeration-gaps/lesson-431a65808f9b46b95974.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [下“不存在”结论前确认检索覆盖完整声明与范围](../../process/unverified-as-fact/lesson-8b7a50eeb92fc3bdb1e7.lesson.md)（共享 1 张卡）
- [规格常量分应用参数与源平台取值，后者写目标取法](../../process/unverified-as-fact/lesson-d280d90bb76be18536f6.lesson.md)（共享 1 张卡）
- [解前向占位按触发文本逐项兑现，写常量不算闭合](../../process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-4171cd43bbb420b4ee40](../../../../store/cases/case-4171cd43bbb420b4ee40/0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa.json) · 结论：diagnosis, rec-0b472c0686
  卡片版本：`0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa`
