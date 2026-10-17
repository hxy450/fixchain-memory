# 鉴权失效判定按源响应拦截器实际分支的错误码与动作迁移，不把错误码枚举里的举例成员当触发条件

ID：`lesson-bad79e090d2af44d167b` · 版本：2 · 阶段：spec/execute · 主题：[data/network-auth](index.md)

概要：token 失效判定按响应拦截器实际分支的码迁移

信号：`reasonCode`, `HandleErrorInterceptor`, `TokenInterceptor`, `LoginExpired`, `TokenExpired`, `TokenInvalid`, `RemotingLoginExpired`, `refreshToken`

## 何时使用

规格提取与网络层实现阶段，写 token 失效判定、踢登与刷新策略时

## 适用情境

源端由响应拦截器按响应体 reasonCode 分支踢登，错误码枚举里同时有多个登录/token 相关成员（LoginExpired、TokenEmpty、TokenExpired、TokenInvalid、RemotingLoginExpired 等）；刷新 token 可能在进入主页的初始化请求里调用，不在拦截器里。

## 原因

枚举成员名看上去都像“登录过期”，只有拦截器里的分支才说明哪些码触发哪个动作。把一句“1001 登录过期”的举例写成判定条件，真正的失效码（来源中是 2012/2013/2082，另有异地登录 5006）就都不会踢登。来源中规格作者只凭参考文档通知里的枚举举例写下“401/1001 刷新”，并让读者去一个没有业务码的数据源查值；实现者查不到，就当“规格已明确”写成 TOKEN_EXPIRED=1001。

## 做法

1. 写失效策略前读响应拦截器（如 HandleErrorInterceptor、TokenInterceptor）实际分支的 reasonCode 和后续动作，写成“码 → 动作”表（踢登、异地登录提示、刷新），实现按表判定。
2. 写“自动刷新”前确认源端的刷新调用在哪里（拦截器里还是某个页面的初始化请求里），按源端位置迁移。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [规格所需值上游缺失时回源码补或标待核，不自拟](../../process/unverified-as-fact/lesson-77ca67f164d77ec63cda.lesson.md)（共享 1 张卡）
- [迁启动链路时列出各去向页初始化请求与登录态组合](../../app/startup/lesson-8c24f05ec8df45401482.lesson.md)（共享 1 张卡）
- [派工要求按源码确认的值回源码核对，没读到标未核实](../../process/secondary-over-source/lesson-93214f5a49c4d1d82316.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7478183bbcfea10865d1](../../../../store/cases/case-7478183bbcfea10865d1/6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d.json) · 结论：diagnosis, rec-34b333d8e8, rec-0dd208eae1
  卡片版本：`6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d`
