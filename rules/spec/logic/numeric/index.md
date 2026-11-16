# 数值、常量与日期时间

读到 (float) 强转后 (int) 截断、byte[] 协议常量、DecimalFormat / NumberFormat / String.format、SimpleDateFormat / Calendar、System.nanoTime，规格里写公式、常量表、格式化精度、时区和计时 API 时

## 触发族

- [源码里的定长 byte[] 协议常量](byte-array-protocol-constant/index.md)（2 条）：Java 源码用有符号 byte[] 字面量定义定长协议块（如 MIFARE 扇区尾块 KeyA | 访问位 | GPB | KeyB），规格的常量清单、验收条目或伪代码里写的是 hex 片段或几种不一致的简写
- [随默认时区和区域变化的日期时间调用](default-timezone-locale-date/index.md)（5 条）：源码里 SimpleDateFormat、GregorianCalendar、Calendar.getInstance() 没 setTimeZone 就 format 毫秒值，或用 Locale.getDefault() 等随区域变化的调用，规格写成「纯时长格式化」、按 getRawOffset 探测、样例只有 UTC 0，或在笔记里写「确定性取舍」
- [Java 源表达式里的 float 运算和 (int) 截断](float32-arithmetic/index.md)（2 条）：读到 Java 源表达式有 (float) 强转、f 后缀字面量或 float 返回值，结果随后 (int) 截断或比较；验收样例按实数或 double 心算，没有一个 float 与 double 结果不同的样例
- [联动字段的格式化精度](linked-field-precision/index.md)（1 条）：源端十字光标或高亮联动代码里各跟随字段的格式化小数位；源码笔记或对照表里只列了哪些字段跟随
- [数值格式化的舍入模式和区域](number-format-defaults/index.md)（3 条）：源端用 DecimalFormat / NumberFormat / String.format / setScale 生成显示文本，调用里有没有显式写舍入模式和 Locale；规格映射行和验收判例里的舍入、小数点、分组符说法
- [计时 API 的映射](timer-api-mapping/index.md)（1 条）：源端用 System.nanoTime() 做动画或帧计时；规格实现映射里写的目标计时 API（如 performance.now）和「行为等价」「低难度」标注
- [引用别处 const val 符号的默认值](symbolic-constant-defaults/index.md)（1 条）：读到 Room 实体字段的初值、SharedPreferences.getLong / getInt 的缺省值写的是别的文件里 const val 定义的大写常量符号，不是字面量；规格表的默认值、偏好缺省值一栏写成 -1 这类具体数，没注明取自哪个常量
- [直接写在平台或传感器 API 实参里的字面参数](literal-api-arguments/index.md)（1 条）：读到源端调平台或传感器 API 时把字面参数直接写在实参里（如角度乘 0.01745329252f 的度转弧度原式）；规格常量清单里没有这些参数，只写「弧度域」这类单位说明
