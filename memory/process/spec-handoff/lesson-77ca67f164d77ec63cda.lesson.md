# 规格需要的值在上游清单或数据源里取不到时，回源码补全或标“待核”，不用端点计数、枚举举例或自拟值收口

ID：`lesson-77ca67f164d77ec63cda` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，依赖 API 清单等上游产物写网络层、鉴权、服务地址等小节时；上游产物缺失、结果被截断，或所指数据源里没有所需值时

## 适用情境

规格模板要求某小节取自上游工具的最终产物（如 api-inventory.json 的 auth_model、common.md），该产物没有落盘，只剩中间文件（如 raw_apis.json）；中间文件只给出键名、标签或计数，没有 host、请求头、错误码等具体值。

## 原因

用手头的中间文件填模板，小节看起来完整，下游会当成已核事实照写；中间文件里没有的值被计数、枚举举例或脚手架注释顶替。来源中这四处都出自同一个规格作者：它已确认最终清单未生成，仍把网络层标为“数据源已就绪”并删掉待补标记；认证小节没列拦截器注入的公共头，没写凭证取自响应头，把错误码枚举里的一句举例写成踢登条件，只看到地址键名就写下自拟的环境名。下游实现者全部照规格落地，直到用户实机调试才逐项暴露。

## 做法

1. 上游约定产物不在磁盘上时，对应小节保留“待补”标记并在报告里列为阻塞，不以中间文件已就绪收口。
2. 中间文件只给出指针（拦截器路径加 header_write 标签、地址键名、枚举名）时，沿指针读源码，把具体值（头名与格式、各环境 host、码与动作）写进规格；读不到就写“未解析，待核”并注明源文件。
3. 规格写“见某数据源”之前，确认该数据源确实含这些值；查不到就写未核和源码位置，不保留推断值。

来源支持：4 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-31852e28af4327a408a3](../../../store/cases/case-31852e28af4327a408a3/7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b.json) · 结论：diagnosis, recommendation:1
  卡片版本：`7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b`
- [case-69bfbfee5841bf8c60cf](../../../store/cases/case-69bfbfee5841bf8c60cf/2798032985b4b2364eb1764bb0a269cda08617887fbebf8f07e1a8d025e06f7f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`2798032985b4b2364eb1764bb0a269cda08617887fbebf8f07e1a8d025e06f7f`
- [case-7478183bbcfea10865d1](../../../store/cases/case-7478183bbcfea10865d1/6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d.json) · 结论：diagnosis, recommendation:2
  卡片版本：`6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d`
- [case-b000698af8cbbc664b87](../../../store/cases/case-b000698af8cbbc664b87/acc888ff43f4b5d71e80aba0739c35c15dd80e7fa4ad95bf37aeb8acebfc619b.json) · 结论：diagnosis, recommendation:1
  卡片版本：`acc888ff43f4b5d71e80aba0739c35c15dd80e7fa4ad95bf37aeb8acebfc619b`
