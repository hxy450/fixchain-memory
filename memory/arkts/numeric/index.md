# arkts/numeric

数值语义：ArkTS number 与 Kotlin 在除法、零分母与范围钳制上的差异，迁移比值和进度计算时要保留的保护，以及 Java long 常量超出安全整数范围时的拼接

[上一级](../index.md)

## 本级经验

- [Java long 常量进入 SQL 或字符串时检查 JS 安全整数范围](lesson-5f669c379cfcdb14ad10.lesson.md)
  - 时机：实现阶段，把 Long.MAX_VALUE 等 Java long 哨兵移植到 SQL 拼接、比较或字符串时
  - 情境：源把 long 常量拼进 SQL；目标准备以 number 常量声明再拼接。
- [迁移比值与进度计算时保留源端的零分母分支与范围钳制：ArkTS number 除法不抛错，0/0 得 NaN](lesson-52d7edb9042110e30eb4.lesson.md)
  - 时机：服务或业务逻辑实现阶段，把源端带保护的比值、进度计算改写或内联到目标回调并写入共享状态时
  - 情境：源端用辅助方法计算 completed/total，其中含 total==0 分支与 coerceIn(0,1) 一类钳制；目标把计算内联进进度回调，直接以 current/total 写入 0..1 语义的共享状态。
