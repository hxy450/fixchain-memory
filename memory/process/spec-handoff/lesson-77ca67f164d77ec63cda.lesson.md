# 上游清单、规格或指定数据源里取不到所需的具体值时，规格作者与写码者都沿指针回源码取值，不用计数、举例或自拟值收口

ID：`lesson-77ca67f164d77ec63cda` · 版本：4

[本主题](index.md)

## 何时使用

规格提取阶段依赖 API 清单等上游产物写网络层、鉴权、服务地址等小节时；写码者开工、派工要求按源码确认字段、请求体或响应处理，而手头的规格、锚点或上游产物看似已给全，或规格指定的数据源里查不到具体值时

## 适用情境

规格模板要求某小节取自上游工具的最终产物（如 api-inventory.json 的 auth_model、common.md），该产物没有落盘、只剩中间文件（如 raw_apis.json），或中间文件只给键名、header_write 标签与计数，没有 host、请求头、错误码等具体值。写码阶段则是规格只给接口签名与源码锚点，没写字段类型、请求体字段、凭证来源或码值；Kotlin 可以在一个 .kt 文件里定义多个类，kapt stub 按类拆分。

## 原因

规格是源码的摘要，中间文件只是指针；用它们填模板，小节看起来完整，下游会当成已核事实照写，缺的值被计数、枚举举例、脚手架注释、空对象或同文件另一个类的字段顶替，编译照样通过。“锚点已给出完整签名”“规格已明确”这类判断又让写码者跳过源码。

## 做法

1. 规格作者：上游约定产物不在磁盘上时，先按 skill 补跑该工具，或直接沿源码取值；两者都做不到才把对应小节列为阻塞并写明缺哪个产物，不以中间文件已就绪收口。
2. 规格作者：中间文件只给出指针（拦截器路径加 header_write 标签、地址键名、枚举名）时，沿指针读源码，把具体值（头名与格式、各环境 host、码与对应动作）写进规格；写“见某数据源”之前确认该数据源确实含这些值。
3. 写码者：开工前为每个要输出的字段、请求体、凭证和码值列出出处（源文件与行号）；有一项出处为空就读源码，不因规格或锚点看似完整而跳过；规格指定的数据源里查不到时，回源码读定义和使用处（枚举定义与使用它的拦截器、地址常量与取址函数）。
4. 找类定义时按类名 grep 源 .kt 文件，不只读同名的 kapt stub；不用其他类的字段填占位，没读到定义时不声称已核实。
5. 沿符号追到定义所在的源文件，跨模块的追到所属模块（如公共库模块里的 Repository 或同一 .kt 中的其他类）；读过定义与使用处仍取不到值时，在规格或回报里写明“未核”并列出已查的源文件位置，作为阻塞项上报，不写推测值。

来源支持：7 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-2c1f292dab668274366a](../../../store/cases/case-2c1f292dab668274366a/8c984c0d9f97cf54d6be55cd26b3b6970d0ee3325f5cddd2d1156632f23e3689.json) · 结论：diagnosis, recommendation:2
  卡片版本：`8c984c0d9f97cf54d6be55cd26b3b6970d0ee3325f5cddd2d1156632f23e3689`
- [case-31852e28af4327a408a3](../../../store/cases/case-31852e28af4327a408a3/7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b`
- [case-69bfbfee5841bf8c60cf](../../../store/cases/case-69bfbfee5841bf8c60cf/2798032985b4b2364eb1764bb0a269cda08617887fbebf8f07e1a8d025e06f7f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`2798032985b4b2364eb1764bb0a269cda08617887fbebf8f07e1a8d025e06f7f`
- [case-6be1461999c00a7fe781](../../../store/cases/case-6be1461999c00a7fe781/6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7.json) · 结论：diagnosis, recommendation:1
  卡片版本：`6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7`
- [case-7478183bbcfea10865d1](../../../store/cases/case-7478183bbcfea10865d1/6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:1
  卡片版本：`6a67c10c5843039d9605d2674ad05a8fd93aeb449ce5b1925b68e23389947a5d`
- [case-b000698af8cbbc664b87](../../../store/cases/case-b000698af8cbbc664b87/acc888ff43f4b5d71e80aba0739c35c15dd80e7fa4ad95bf37aeb8acebfc619b.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`acc888ff43f4b5d71e80aba0739c35c15dd80e7fa4ad95bf37aeb8acebfc619b`
- [case-b98aad1336d85a238cd7](../../../store/cases/case-b98aad1336d85a238cd7/1b1048f7aeb0b8a70838ac7223c8c31fd0564271f85a608b01cd3b70ad02eb69.json) · 结论：recommendation:4
  卡片版本：`1b1048f7aeb0b8a70838ac7223c8c31fd0564271f85a608b01cd3b70ad02eb69`
