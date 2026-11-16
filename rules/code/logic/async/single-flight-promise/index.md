# 单飞缓存的 Promise 入口

agent 会看到什么：读到规格给出返回 Promise<T> 的一次性入口、AC 要求「防重守卫：连续两次调用仅执行一次」；产物里入口写成 static async 方法、方法体 return 缓存在字段里的 Promise

## 规矩

- rule-ece27b5dce75｜单飞缓存 Promise 的入口方法不声明 async，直接返回缓存的同一 Promise 实例｜读到：规格给出返回 `Promise<T>` 的一次性入口，AC 要求「防重守卫：连续两次调用仅执行一次、只写一次」；写错：入口写成 `static async` 方法，方法体 `return` 缓存在字段里的 Promise，注释却写「重入共享同一 Promise」
