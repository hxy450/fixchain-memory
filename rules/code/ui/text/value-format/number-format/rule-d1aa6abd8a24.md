# 源码用 Formatter.formatShortFileSize 时，目标按千进、>900 升级和短格式小数位实现

审的是：代码
触发（任一种）：
- 读到：源码调用 Formatter.formatShortFileSize(context, bytes)（或 Formatter.formatFileSize）显示文件大小；写错的样子：目标自写的格式化函数按 1024 进位、单位写成 KB，或升级阈值写成 999.5、1000 之类不是 900 的值，小数位不按量级取
适用范围：安卓 android.text.format.Formatter 的文件大小格式化迁到 ArkTS 自写函数时；源码注释写明 O 起按 SI 千进，N 及以前是 1024
做法：
- 按 Formatter.RoundedBytesResult#roundBytes 写：进制 1000；值 > 900 就除以 1000 升一级，依次 B → kB → MB → GB → TB → PB
- 小数位：未升级（字节）或值 ≥ 100 取 0 位；值 < 1 取 2 位；短格式下 1 ≤ 值 < 10 取 1 位、10 ≤ 值 < 100 取 0 位；四舍五入，不加千分位
- 数字和单位之间一个空格，字节单位是 B，其余用 SI 短写（kB 的 k 小写）；用已知输入核对：96000 字节应为 96 kB
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- formatShortFileSize(context, sizeBytes) = formatFileSize(context, sizeBytes, FLAG_SI_UNITS | FLAG_SHORTER)：短格式就是 SI 单位加 FLAG_SHORTER（出处：android.text.format.Formatter#formatShortFileSize）
- unit = (flags & FLAG_IEC_UNITS) != 0 ? 1024 : 1000；每次 result > 900 升一级，最多到 PETABYTE：进制和升级阈值（出处：android.text.format.Formatter.RoundedBytesResult#roundBytes）
- mult == 1 或 result >= 100 → 0 位；result < 1 → 2 位；result < 10 → FLAG_SHORTER 时 1 位；10 ≤ result < 100 → FLAG_SHORTER 时 0 位：小数位规则；不带 FLAG_SHORTER（formatFileSize）时后两档都是 2 位（出处：android.text.format.Formatter.RoundedBytesResult#roundBytes）
- setGroupingUsed(false)；setRoundingMode(BigDecimal.ROUND_HALF_UP)：不加千分位，四舍五入（出处：android.text.format.Formatter#getNumberFormatter）
- byteShort = B；fileSizeSuffix = %1$s %2$s：字节级的单位和「数字 空格 单位」的拼法（出处：Android SDK 平台资源 data/res/values/strings.xml，byteShort、fileSizeSuffix（按应用的 compileSdk 取对应平台））
- formatFileSize(context, sizeBytes) = formatFileSize(context, sizeBytes, FLAG_SI_UNITS)：同类方法：长格式，同样千进，只是不带 FLAG_SHORTER（出处：android.text.format.Formatter#formatFileSize）
- 96000 字节 → 96 kB（SI 短格式，> 900 升级）：核对用的已知输入（出处：卡里修好并验证过）
未核实：非英文语言下 kB、MB 等单位串的写法（安卓按 ICU MeasureFormat 的 SHORT 宽度取，随 locale 变）
来源：1 张卡，1 个应用
- case-bdbb705b26462605b1c3（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2、诊断；取值 7 ← 建议 2、诊断
