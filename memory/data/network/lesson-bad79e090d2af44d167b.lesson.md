# 鉴权失效判定按源响应拦截器实际分支的错误码与动作迁移，不把错误码枚举里的举例成员当触发条件

ID：`lesson-bad79e090d2af44d167b` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与网络层实现阶段，写 token 失效判定、踢登与刷新策略时

## 适用情境

源端由响应拦截器按响应体 reasonCode 分支踢登，错误码枚举里同时有多个登录/token 相关成员（LoginExpired、TokenEmpty、TokenExpired、TokenInvalid、RemotingLoginExpired 等）；刷新 token 可能在进入主页的初始化请求里调用，不在拦截器里。

## 原因

枚举成员名看上去都像“登录过期”，只有拦截器里的分支才说明哪些码触发哪个动作。把一句“1001 登录过期”的举例写成判定条件，真正的失效码（来源中是 2012/2013/2082，另有异地登录 5006）就都不会踢登。来源中规格作者只凭参考文档通知里的枚举举例写下“401/1001 刷新”，并让读者去一个没有业务码的数据源查值；实现者查不到，就当“规格已明确”写成 TOKEN_EXPIRED=1001。

## 做法

1. 写失效策略前读响应拦截器（如 HandleErrorInterceptor、TokenInterceptor）实际分支的 reasonCode 和后续动作，写成“码 → 动作”表（踢登、异地登录提示、刷新），实现按表判定。
2. 写“自动刷新”前确认源端的刷新调用在哪里（拦截器里还是某个页面的初始化请求里），按源端位置迁移。

## 来源（按需复核）

- [case-7478183bbcfea10865d1](../../../store/cases/case-7478183bbcfea10865d1/6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d`
