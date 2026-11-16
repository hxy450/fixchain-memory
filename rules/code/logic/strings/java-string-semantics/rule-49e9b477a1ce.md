# 源端 String.split 切分文本时，目标切分后去掉结果末尾的空串

审的是：代码
触发（任一种）：
- 读到：`getText().split(System.getProperty("line.separator"))` 或其他单参数 String.split(regex) 调用；写错的样子：目标写 text.split('\n') 后直接用结果数组，以分隔符结尾的文本多出末尾空串，行数判定因此出错
适用范围：Java 单参数 String.split 迁成 ArkTS 字符串切分时
做法：
- JS split 之后从末尾起删掉连续的空串，得到与 Java split(regex) 相同的数组；源端分隔符是 System.getProperty("line.separator") 时，在 Android 上就是 "\n"
- 自检：以换行结尾的文本切分后不应多出末尾空串，按行数做的判定（如固定 4 行、16 行）不应因此失败
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- split(regex) 等于 split(regex, 0)，结果里不含末尾的空串：源端切分语义（出处：java.lang.String#split）
- line.separator 在 Android 上是 \n：源端分隔符的实际值（出处：java.lang.System#getProperties）
- JS split('\n') 保留末尾空串，以换行结尾的扇区文本被判成多一行而返回错误码：直接用 JS split 的后果（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-526d6b56241863d015dd（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3；取值 3 ← 诊断
