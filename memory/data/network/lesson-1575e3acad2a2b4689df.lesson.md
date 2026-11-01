# 源端靠 catch 处理 HTTP 失败、目标客户端永不 reject 时，在消费 res.data 前写 status 失败分支还原 catch 语义

ID：`lesson-1575e3acad2a2b4689df` · 版本：1

[本主题](index.md)

## 何时使用

服务层实现阶段，把源端请求的 try/catch 失败处理翻译到“永不 reject、以信封 status 表示失败”的 HTTP 客户端时

## 适用情境

源端 HTTP 调用在非 2xx 时抛错（如 Angular HttpClient 的 HttpErrorResponse），由 catch 设置错误文案并返回失败；目标网络层契约把非 2xx、传输异常和解析失败都归一为失败信封、不 reject，调用方按 status 判成功；方法还维护 hasMore、游标或已加载标记等分页状态。

## 例外与边界

- 目标客户端契约或实现对失败确实 reject，此时源 catch 可原样承接

## 原因

照搬源端 try/catch 结构时，失败信封走进成功路径：空的 res.data 被当成空页或“无更多”，错误文案不设、分页状态被错误推进并返回成功；catch 在契约下不可达，编译和正常路径测试都发现不了。

## 做法

1. 翻译 catch 前先列出哪些失败会进入它（非 2xx、超时、解析错误），再按目标网络层契约映射到实际失败信号；客户端不 reject 时，在消费 res.data 前写 status 非成功分支：错误文案取信封 message（为空时用源端兜底文案），返回源 catch 的返回值，不改 hasMore、游标与首拉完成标记。
2. 写出“此 catch 在契约下不可达、仅作防御”一类注释时，回查源 catch 的语义是否已迁到信封分支；同一服务里已有 status 判定的方法与分页、列表方法逐个对齐。

## 可选检查

- 注入一个带 message 的失败信封，断言返回值、错误文案、hasMore 与游标保持调用前的值

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7cb7554a3696dcbc7647](../../../store/cases/case-7cb7554a3696dcbc7647/d845c4c998696388b5fa4e1a08c0e411b71b4211e20396da3d5a142be7558e87.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d845c4c998696388b5fa4e1a08c0e411b71b4211e20396da3d5a142be7558e87`
