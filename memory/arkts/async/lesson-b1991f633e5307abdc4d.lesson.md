# 源端阻塞到完成才返回的 void 方法（排空队列、关闭设备、停录）改为 Promise 签名并逐层 await，销毁、重启、重开排在完成之后

ID：`lesson-b1991f633e5307abdc4d` · 版本：1

[本主题](index.md)

## 何时使用

规格提取写接口清单、跨切片 seam 设计、实现与接线阶段，把源端阻塞式等待或同步关闭/停止映射为 ArkTS 异步实现，并决定签名与调用方是否 await 时

## 适用情境

源端 void 方法内部阻塞到工作完成（waitUntilDone 排空保存队列、后台线程同步 stop+release 后才置 CLOSED、MediaRecorder 同步 stop/release），验收要求“X 先于 Y”（保存先于销毁或重启、关闭完成才回调或重开）；目标对应接口返回 Promise，规格接口表或占位 seam 照搬 Java 的 void 签名，页面生命周期回调（aboutToDisappear）不能 await。

## 例外与边界

- 源端本身就是异步完成且调用方不等待（回调、未 join 的 Future）时，按源端时序迁移，不额外补等待或取消

## 原因

void 签名承载不了等待：调用方只能 fire-and-forget（void promise、只接 .catch、Promise.resolve().then 包裹同步调用），后续的销毁、重启、置 CLOSED 或重开在实际完成前发生。源端同步完成时不存在的“进行中”窗口在目标出现，重复停止、启动中的停止、关闭中的打开都会落进这个窗口。

## 做法

1. 规格接口表与 seam 类型把这类方法写成 Promise<void>（回调类型定为 () => Promise<void>，当前只是桩也如此），验收写明调用方需 await；实现与接线时从被等待的方法到每一层调用方都 await，完成态（如 CLOSING→CLOSED）、完成回调、销毁、重启与重开写在 await 之后。
2. 不能 await 的生命周期回调只发起一个 async 序列（如 void this.vm.destroySequence()），引擎销毁放在该序列的 await 之后，页面不再另行同步销毁；成对的挂接与拆卸 hook 都返回 Promise。
3. 为异步窗口写明请求语义：关闭进行中到来的打开记为待重开，关闭完成后执行；重复停止返回同一个共享的停止任务；启动链每个 await 之后检查是否已请求停止，已请求则不再启动。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-742303a1abdd7ba274ec](../../../store/cases/case-742303a1abdd7ba274ec/bb4fea0563908b2101928fcc8630ef98856d69a3735bcd6f529508fc118b6b55.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`bb4fea0563908b2101928fcc8630ef98856d69a3735bcd6f529508fc118b6b55`
- [case-b89cd099bfa87829fd2d](../../../store/cases/case-b89cd099bfa87829fd2d/063e8bf906db6adb5fae0a419989e043b3d8f5f8f5679ae18a2371e50e26fb54.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`063e8bf906db6adb5fae0a419989e043b3d8f5f8f5679ae18a2371e50e26fb54`
