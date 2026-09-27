# 源端从响应头取 token/refreshToken 时，HTTP 封装把响应头交给调用方，Repository 按源端成功回调取值

ID：`lesson-2a4e6af209308c08aaa6` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-31852e28af4327a408a3 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`740e2dc64c574567257686cdc96a77c90c8d4d3cf95039981c44aafb662531bc`
