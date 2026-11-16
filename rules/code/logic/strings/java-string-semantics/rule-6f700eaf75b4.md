# 多处要用 Java 字符串和读行语义时，集中实现一组兼容函数，各处统一调用

审的是：代码
触发（任一种）：
- 读到：源端多个类都用 readLine、String.split、String.trim、String.format 处理文本；写错的样子：两个以上服务、VM 或页面各自写读行、切分、去空白、解码的近似实现（各自的 split('\n')、.trim()、TextDecoder）
适用范围：同一工程里多处要按 Java 语义处理字符串、读行、解码时
做法：
- 在服务层建一组 Java 兼容函数（readLines、split、trim、decodeUtf8、formatFixed 等），所有服务、VM 和页面统一调用，删掉各自的近似实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 新建一组读行、切分、去空白、解码、定点格式化、float 换算、本地数字的兼容函数，各服务改用后问题消失：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-526d6b56241863d015dd（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；取值 1 ← 诊断
