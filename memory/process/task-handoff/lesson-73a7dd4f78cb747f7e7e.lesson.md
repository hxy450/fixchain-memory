# 派工转述规则或把某任务的局部做法推广为派工规则时，连同原文的替代写法、适用范围与配套要求一起下发；禁止并发构建的 worker 改动汇总后立即全量构建

ID：`lesson-73a7dd4f78cb747f7e7e` · 版本：3

[本主题](index.md)

## 何时使用

编排或返修阶段，把规则清单或上一批子任务回报的做法转述进后续 worker 派工，并决定 worker 能否自行构建时

## 适用情境

编排者收到的规则原文带有替代写法（例如“禁止 Record，改用具名字段或 HashMap”），派给多个并发 worker 时压缩成一句禁令，并要求 worker 不跑全量构建。也包括首批子任务回报了按某参考条目采用的局部做法（如把弹窗写成页内覆盖层），编排者把它写成“全部照此处理”的后续派工规则。也包括禁编译的 worker 写出 TS 习惯写法（implements SDK class、按类名调用顶层函数），而收尾构建因会话中断没有执行。

## 原因

只转述禁令不转述替代写法，worker 会各自找一种看似合规的写法，可能同样被禁止；又因为不能构建，错误要到汇总后才暴露。把局部做法写成总则，会同时丢掉原参考的适用范围与配套条件。来源中返修派工把“No Record<K,V> — use explicit typed fields or HashMap”截成“No Record<K,V>”，两个 worker 都改成了索引签名；另一应用的编排者把首批转换者回报的“页内覆盖层”写成“对话框全部改页内 overlay”，既丢掉原参考“普通确认框不必页面级”的守卫，也没带返回键关闭要求，下游页面照此实现后按返回整页被弹出。

## 做法

1. 转述规则时保留原文的替代写法或示例，不只写禁令；把某任务的做法推广给后续派工前，回读它所依据的参考条目，把适用范围、负向守卫和配套要求一并写进派工。
2. 禁止 worker 并发构建时，限制清单写入与 TS 直觉相反的规则（如 implements 只接受 interface），worker 仍做导入名与导出名的静态对照；收齐改动后立即全量构建，并逐一核对 worker 新引入的类型声明；收尾构建因会话中断未执行时，下一轮先编译再派工。

来源支持：4 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-0fc468c36c3cf09b06bb](../../../store/cases/case-0fc468c36c3cf09b06bb/93efce843b538354c85222f088e9667e495135f3cea4d482a1a80ce9849ccbdd.json) · 结论：recommendation:3
  卡片版本：`93efce843b538354c85222f088e9667e495135f3cea4d482a1a80ce9849ccbdd`
- [case-104a365629bd48069967](../../../store/cases/case-104a365629bd48069967/a1627b0c872858a162cd2b9e32351195aee56ffb8e1323502a880ad30919b798.json) · 结论：recommendation:3
  卡片版本：`a1627b0c872858a162cd2b9e32351195aee56ffb8e1323502a880ad30919b798`
- [case-28990049b25bf1086836](../../../store/cases/case-28990049b25bf1086836/4c3037100e303a3b9a9c78b8d172f92cb23342e0be0d2c8c467948a720e3723f.json) · 结论：recommendation:3
  卡片版本：`4c3037100e303a3b9a9c78b8d172f92cb23342e0be0d2c8c467948a720e3723f`
- [case-98e7bd27bb334db83f51](../../../store/cases/case-98e7bd27bb334db83f51/2bd8a63105c2a86e012e477614f9ed3d54d26dbfc05250b99a797f194a3e1b79.json) · 结论：diagnosis, recommendation:4
  卡片版本：`2bd8a63105c2a86e012e477614f9ed3d54d26dbfc05250b99a797f194a3e1b79`
