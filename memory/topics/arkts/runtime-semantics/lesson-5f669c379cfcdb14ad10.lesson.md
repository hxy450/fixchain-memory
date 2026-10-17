# Java long 常量进入 SQL 或字符串时检查 JS 安全整数范围

ID：`lesson-5f669c379cfcdb14ad10` · 版本：2 · 阶段：execute · 主题：[arkts/runtime-semantics](index.md)

概要：超安全整数的 long 常量以字符串拼进 SQL

信号：`Long.MAX_VALUE`, `Number.MAX_SAFE_INTEGER`, `bigint`, `9223372036854775807`, `typeof()`

## 何时使用

实现阶段，把 Long.MAX_VALUE 等 Java long 哨兵移植到 SQL 拼接、比较或字符串时

## 适用情境

源把 long 常量拼进 SQL；目标准备以 number 常量声明再拼接。

## 原因

超出 Number.MAX_SAFE_INTEGER 的 number 字符串化后数值改变（9223372036854775807 变为 9223372036854776000），SQLite 按 REAL 存储，回读与比较出错。

## 做法

1. 超出范围的常量用字符串字面量拼接（或 bigint），不声明成 number。

## 可选检查

- 不确定拼接结果的存储类型时，用 SQLite typeof() 确认仍为 INTEGER

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [辅助谓词与 getter 读到定义再翻译，不按名字推断](../../process/inferred-not-traced/lesson-b3f534eb740a768d95a6.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bdbb705b26462605b1c3](../../../../store/cases/case-bdbb705b26462605b1c3/ad200a78c3c72540d53a93e8cbf6f54f99aa14007e6e209df98a73f3d6837888.json) · 结论：rec-ad5b5eeb56
  卡片版本：`ad200a78c3c72540d53a93e8cbf6f54f99aa14007e6e209df98a73f3d6837888`
