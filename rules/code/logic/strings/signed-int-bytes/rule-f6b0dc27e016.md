# Java byte 与 0x80 以上的 int 字面量比较时，先换成有符号值再照写

审的是：代码
触发（任一种）：
- 读到：Java 源码里 `byte` 变量与大于 0x7F 的 int 字面量（如 0x81、0xFE）做 `<`、`>` 比较；写错的样子：ArkTS 直接拿 Uint8Array 或 number[] 里 0–255 的字节和同一字面量比较，注释称与 Java 有符号位模式一致
适用范围：源端 Java 的 byte（有符号）参与比较或分支、目标端字节是 0–255 的值时
做法：
- 比较前把 0–255 的值换回 -128..127：`const s = v > 0x7F ? v - 0x100 : v`，再照源码写 `s < 0x81 || s > 0xFE`
- 用 0x80–0xFF 的样例核对目标与源码同样恒通过或恒失败
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Byte.MIN_VALUE = -128，Byte.MAX_VALUE = 127：Java byte 的取值范围，与大于 0x7F 的字面量比较时 `<` 恒为 true、`>` 恒为 false（出处：java.lang.Byte#MIN_VALUE、Byte#MAX_VALUE）
- `byte < 0x81 || byte > 0xFE` 对任何字节都成立：按有符号复刻后该检查恒通过；按无符号写会拒掉 0x81–0xFE（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-119e8f2945fd9ff1c0c4（MifareClassicTool）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 2 ← 诊断
