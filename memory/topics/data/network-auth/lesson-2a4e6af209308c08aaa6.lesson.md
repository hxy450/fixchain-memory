# 源端从响应头取 token/refreshToken 时，HTTP 封装把响应头交给调用方，Repository 按源端成功回调取值

ID：`lesson-2a4e6af209308c08aaa6` · 版本：2 · 阶段：spec/execute · 主题：[data/network-auth](index.md)

概要：响应头携带 token 时 HTTP 封装连头一起返回

信号：`headers()["Authorization"]`, `RefreshToken`, `Response<BaseResponse`, `TokenManager`, `headers()`, `refreshToken`, `Authorization`

## 何时使用

网络与登录数据层的规格提取和实现阶段，确定登录类接口凭证的取值来源与 HTTP 封装的返回结构时

## 适用情境

源端 Retrofit 登录接口返回 Response<BaseResponse<T>>，Repository 在成功回调里用 headers()["Authorization"]、headers()["RefreshToken"] 写 TokenManager，body 的 data 只含用户信息；目标端 HTTP 封装统一返回解析后的响应体。

## 原因

封装层只返回 body 时，响应头在最底层就被丢掉，上层怎么写都拿不到凭证；照“登录返回用户与 token”这类规格措辞去 body 里找，只能取到空值，refreshToken 也一直是空串，持久化和刷新随之失效。来源中规格从未写明凭证来源，封装层实现者只读到 body 结构；Repository 实现者跳过源码，只从 data 取 token，给保存函数传空串。

## 做法

1. 规格整理鉴权模型时，列出返回 Response<BaseResponse<T>> 的端点，逐个查调用方是否读取 headers()，把头名和写入点写进网络层与登录功能规格。
2. 源接口有 Response<> 包裹的端点时，HTTP 封装把响应头随结果返回（例如在响应对象上加 header 字段）；读取时兼容头名大小写。
3. 实现登录 Repository 前读源 Repository 的成功回调，核对 token 与 refreshToken 各自来源；源端写了 refreshToken 时，不向保存函数传空串。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [规格所需值上游缺失时回源码补或标待核，不自拟](../../process/unverified-as-fact/lesson-77ca67f164d77ec63cda.lesson.md)（共享 1 张卡）
- [派工要求按源码确认的值回源码核对，没读到标未核实](../../process/secondary-over-source/lesson-93214f5a49c4d1d82316.lesson.md)（共享 1 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-31852e28af4327a408a3](../../../../store/cases/case-31852e28af4327a408a3/7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b.json) · 结论：diagnosis, rec-05992b7d58, rec-a583bac8fb, rec-900bcadda5
  卡片版本：`7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b`
