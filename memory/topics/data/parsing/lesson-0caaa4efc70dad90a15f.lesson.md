# 以 org.json 构造并输出 JSON（备份、导出）时按库语义序列化：put(null) 删除键、toString 把 “/” 转义为 “\/”；不以 JSON.stringify 直出，也不从 Kotlin 可空字段推出“保留 null 键”

ID：`lesson-0caaa4efc70dad90a15f` · 版本：2 · 阶段：spec/execute · 主题：[data/parsing](index.md)

概要：org.json 输出按库语义：null 删键、转义 /

信号：`JSONObject.put`, `JSONObject.NULL`, `JSONArray`, `toString(indent)`, `JSON.stringify`, `serialize()`

## 何时使用

规格提取与数据层实现阶段，把源端用 JSONObject.put、JSONArray.toString(n) 生成的备份、导出或请求 JSON 写成目标契约与序列化代码时

## 适用情境

源端 serialize() 对可空值直接 put（如 put(key, steps?.serialize())、put(key, time)），再以 JSONObject/JSONArray 的 toString() 或 toString(indent) 写文件；对应 Kotlin 字段声明为可空；目标准备用 DTO 加 JSON.stringify(obj, null, n) 输出，规格可能写“null 字段输出 JSON null（键保留）”。

## 原因

org.json 的 put 值为 null 时删除该键（只有 JSONObject.NULL 才写出 null 值），toString 会把 “/” 转义为 “\/”；JSON.stringify 保留值为 null 的键、不转义 “/”。由 Kotlin 字段可空推出“null 键保留”写进契约后，实现照契约输出，导出文件的键集与字节都与源端不同。

## 做法

1. 规格按库语义写序列化契约：put 的值为 null 时不输出该键，只有显式 put(JSONObject.NULL) 才输出 null 值；toString 转义 “/”；其余值类型照源端 put 的类型输出。不由字段可空性推出“null 键保留”。
2. 实现封装或移植与 org.json 等价的序列化工具（跳过 null 值、转义 “/”、缩进照源端 toString(n)），模型 toJson 与导出服务统一调用，不直接用 JSON.stringify。

## 可选检查

- 用含 null 字段与 “/” 的样例，与源端输出逐字节比对

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [源端可观察缺陷照迁并核次数，修正走待批决策](../../process/unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md)（共享 1 张卡）
- [JSON 取值的空值与类型规则按 org.json 定](lesson-5034b56be6fd828164c9.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../../app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7e6984a7fa6d5845737b](../../../../store/cases/case-7e6984a7fa6d5845737b/28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba.json) · 结论：diagnosis, rec-b9e6a2835c, rec-31a14d260e
  卡片版本：`28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba`
