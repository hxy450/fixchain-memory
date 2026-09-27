# 显式 JSON 解码器按源解析器的接受范围和源数据的实际类型定规则：Gson 的数字与字符串互转要保留

ID：`lesson-871d3751cadde6dda1dc` · 版本：1

[本主题](index.md)

## 何时使用

数据层与网络层实现阶段，把 Retrofit+Gson 的 Bean、响应壳或预置 JSON 资产的读取翻译成 ArkTS 显式解码器时

## 适用情境

源端由 Gson 把 JSON 填进 Int/String 字段，或预置资产用字符串存放数值（"id": "43831"）；目标仓库提供只接受单一 typeof 的严格解码函数（string()/number() 类型不符即抛错），真实响应样例尚未采集，规格只写了“Gson → 显式 decoder、显式校验字段”。

## 例外与边界

- 源端对该字段确实以类型不符为错误（例如源码显式校验并走失败分支），此时保留严格校验

## 原因

Gson 会把 JSON 数字填入 String 字段、把数字字符串填入 Int 字段；目标按声明类型写 typeof 硬校验，就丢掉了这层容忍，HTTP 200 的响应和预置资产在解码边界整体失败，常被上层包装成“网络错误”或整页报错。来源为同一应用：模型层对 id、aqi，网络层对响应壳 code/time 都做硬校验，而服务端实际 code 为字符串、time 与 id 为数字、aqi 为数字字符串；网络层还另写了一份与共享模型不一致的响应壳类型。黄历仓储读到的资产样本 id 是字符串，仍按目标字段类型用 number 解码。

## 做法

1. 写 decoder 前先写出源解析器的标量规则：Gson 下 String 字段接受数字、布尔并转为字符串，Int 字段接受数字字符串并转为数字；目标的 string/number 读取接受这些等价形态并转换，其余类型仍报错。
2. 预置资产和接口样本按实际 JSON 类型选择解码函数，不按目标模型字段类型；调用共享解码工具前先读其实现，确认它接受哪些类型。
3. 响应壳等共享类型从模型规格表或 Android Bean 取字段类型并复用已有定义，不在网络层另写一份。
4. 可用一组最小样例核对：{code:'200', msg:'ok', time:1723456789} 解析为 code=200、time='1723456789'；{id:123, aqi:'42'} 得到 id='123'、aqi=42。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-853ca988d9a2683b1c8d · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`bdd87c7f5a351594fdf08ee333cadf73c21beb381c1121e2bc09fe9056955e2f`
- case-c9f068102d7b9057938e · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`e8a368c96d0b621df1d5defddc5022cd7f61860ef3df07fcaa62704a8782728f`
