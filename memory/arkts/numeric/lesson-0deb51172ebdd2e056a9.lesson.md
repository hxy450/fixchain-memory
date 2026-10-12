# Kotlin Float 的 == 比较迁到 ArkTS 时保持精确相等：两侧对齐到 float32（Math.fround）后用 ===，不自加容差；选中、存在判断与删除共用同一比较

ID：`lesson-0deb51172ebdd2e056a9` · 版本：1

[本主题](index.md)

## 何时使用

实现阶段，把 Kotlin 中对 Float 值的 ==/!= 比较（选项选中判断、列表去重、删除过滤）翻译成 ArkTS 时

## 适用情境

源端用 value.toFloat() == state 一类写法比较 Float（如倍率、刻度选项与当前值），值来自字符串解析或滑杆；目标 number 为双精度，写者担心浮点误差，准备用 Math.abs(a - b) < ε 容差比较，或在不同位置各写一套比较。

## 例外与边界

- 源端本身就用容差或先舍入再比较

## 原因

容差会把源端判为不同的值当成相同，选中态、是否已存在、删除哪一项随之偏离；只把 == 换成 === 也不完全等价：Kotlin Float 是 32 位，同一个十进制串解析成 double 与解析成 float 的值可能不同，两侧来源不一致时本应相等的值会被判为不等。

## 做法

1. 比较两侧都按 Float 语义归一：解析或计算得到的值用 Math.fround 转成 float32（也可在写入状态时就 fround），再用 ===；不加 ε 容差。
2. 同一组值的选中判断、存在判断与删除过滤调用同一个比较函数。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:3
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
