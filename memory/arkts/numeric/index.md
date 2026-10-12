# arkts/numeric

数值语义：ArkTS number 与 Kotlin 在除法、零分母与范围钳制上的差异，迁移比值和进度计算时要保留的保护，以及 Java long 常量超出安全整数范围时的拼接；Kotlin Float 相等比较的 float32 对齐

[上一级](../index.md)

## 本级经验

- [Java long 常量进入 SQL 或字符串时检查 JS 安全整数范围](lesson-5f669c379cfcdb14ad10.lesson.md)
  - 时机：实现阶段，把 Long.MAX_VALUE 等 Java long 哨兵移植到 SQL 拼接、比较或字符串时
  - 情境：源把 long 常量拼进 SQL；目标准备以 number 常量声明再拼接。
- [Kotlin Float 的 == 比较迁到 ArkTS 时保持精确相等：两侧对齐到 float32（Math.fround）后用 ===，不自加容差；选中、存在判断与删除共用同一比较](lesson-0deb51172ebdd2e056a9.lesson.md)
  - 时机：实现阶段，把 Kotlin 中对 Float 值的 ==/!= 比较（选项选中判断、列表去重、删除过滤）翻译成 ArkTS 时
  - 情境：源端用 value.toFloat() == state 一类写法比较 Float（如倍率、刻度选项与当前值），值来自字符串解析或滑杆；目标 number 为双精度，写者担心浮点误差，准备用 Math.abs(a - b) &lt; ε 容差比较，或在不同位置各写一套比较。
  - 例外：源端本身就用容差或先舍入再比较
- [迁移比值与进度计算时保留源端的零分母分支与范围钳制：ArkTS number 除法不抛错，0/0 得 NaN](lesson-52d7edb9042110e30eb4.lesson.md)
  - 时机：服务或业务逻辑实现阶段，把源端带保护的比值、进度计算改写或内联到目标回调并写入共享状态时
  - 情境：源端用辅助方法计算 completed/total，其中含 total==0 分支与 coerceIn(0,1) 一类钳制；目标把计算内联进进度回调，直接以 current/total 写入 0..1 语义的共享状态。
