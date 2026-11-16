# d.ts 里带 @throws 801 的接口变体

agent 会看到什么：读到 d.ts 里同一能力的几个变体（同步、Promise、带 ID 参数）中某个单独写了 @throws { BusinessError } 801 - Capability not supported；产物里所有调用方共用的封装选了这个变体（如 RdbStore.beginTrans）

## 规矩

- rule-079d06fe05c6｜共享封装在 d.ts 同名变体间选接口时，对比 @throws，带 801 的不用作共享封装｜读到：d.ts 里同一能力有几个变体（同步、Promise、带 ID 参数），其中某个变体的注释单独写了 @throws { BusinessError } 801 - Capability not supported；写错：所有调用方共用的封装选了带 801 的变体（如 RdbStore.beginTrans），理由只是「签名存在、异步写法更简洁」
