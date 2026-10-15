# 源端由 Gson 默认适配器填充 Bean 时，显式解码器保留数字与字符串互转，并按源数据实际类型选解码函数

ID：`lesson-871d3751cadde6dda1dc` · 版本：3

[本主题](index.md)

## 何时使用

数据层与网络层实现阶段，把 Retrofit+Gson 的 Bean、响应壳或预置 JSON 资产的读取翻译成 ArkTS 显式解码器时

## 适用情境

源端由 Gson 把 JSON 填进 Int/String 字段，或预置资产用字符串存放数值（"id": "43831"）；目标仓库提供只接受单一 typeof 的严格解码函数（string()/number() 类型不符即抛错），真实响应样例尚未采集，规格只写了“Gson → 显式 decoder、显式校验字段”。

## 例外与边界

- 源端对该字段确实以类型不符为错误（例如源码显式校验并走失败分支），此时保留严格校验
- GsonBuilder 注册了 TypeAdapter/JsonDeserializer 或字段带 @JsonAdapter 时，按该适配器的实现转换，不套默认标量规则

## 原因

Gson 默认适配器会把 JSON 数字填入 String 字段、把数字字符串填入 Int 字段；目标按声明类型写 typeof 硬校验，就丢掉了这层容忍，HTTP 200 的响应和预置资产在解码边界整体失败、页面报错。网络层另写一份与共享模型不一致的响应壳类型，同一字段会在两处按不同类型解码。

## 做法

1. 写 decoder 前先核对 GsonBuilder 注册的适配器与字段注解；只用默认适配器时按其标量规则（出处：Gson 2.11.0 源码 TypeAdapters.STRING 把布尔转为字符串、对数字取原文，INTEGER 等用 nextInt 读数字字符串）：String 字段接受数字、布尔并转为字符串，Int/Long 字段接受数字字符串并转为数字（非数字或超出范围仍失败）；目标的 string/number 读取接受这些等价形态并转换，其余类型仍报错。
2. 数值 token 填入 String 字段且取值可能超过 2^53 时，按同库大整数 id 经验在 JSON.parse 之前保真，不在解析后再 String(value)。
3. 预置资产和接口样本按实际 JSON 类型选择解码函数，不按目标模型字段类型；调用共享解码工具前先读其实现，确认它接受哪些类型。
4. 响应壳等共享类型从模型规格表或 Android Bean 取字段类型并复用已有定义，不在网络层另写一份。

## 可选检查

- 可用一组与字段名无关的最小样例核对：String 字段收 123 得 '123'，Int 字段收 '42' 得 42。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-853ca988d9a2683b1c8d](../../../store/cases/case-853ca988d9a2683b1c8d/9481017a4a478ff69e2b3212fc23467ff3598149ba121d6de3e300271444d53d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`9481017a4a478ff69e2b3212fc23467ff3598149ba121d6de3e300271444d53d`
- [case-c9f068102d7b9057938e](../../../store/cases/case-c9f068102d7b9057938e/dfe948af75e0f1c102fa7d2444c640253b28a02af635ad7f4efaaf9e01ef20ed.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`dfe948af75e0f1c102fa7d2444c640253b28a02af635ad7f4efaaf9e01ef20ed`
