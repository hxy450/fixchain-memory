# arkts/stdlib

Java 标准库与语言语义到 ArkTS 的等价实现：读行、split/trim、BOM、String.format 与 Locale、Calendar 周规则，HashSet/HashMap 迭代序、有符号 byte 比较与 switch 返回码；DecimalFormat、BigDecimal 舍入与 Float.toString 的数值转文本，位置参数的字面插入（避开 String.replace 替换模式）

[上一级](../index.md)

## 本级经验

- [DecimalFormat、String.format、BigDecimal 舍入生成数值文本时，按源 API 复刻舍入模式与默认 Locale](lesson-ae093dedda604fddf17e.lesson.md)
  - 时机：实现阶段把 DecimalFormat 模式串、String.format("%.Nf")、Float.toBigDecimal().setScale 等数值转文本函数翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些函数写映射与验收判例时；修改已有共享数值工具时
  - 情境：源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）且未传 Locale，用 String.format("%.2f", f) 输出小数，或用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN) 舍入；应用可能单独设置应用语言；目标准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板串实现；共享数值工具与页面可能各有一份同名函数。
  - 例外：源端显式传入 Locale 或调用了 setRoundingMode：按显式设置实现
- [Java 读行、split、trim 与文本解码迁到 ArkTS 时按 Java 语义集中实现兼容函数，不用同名 JS API 近似](lesson-237091b9b04bc4cd340b.lesson.md)
  - 时机：页面转换和服务/VM 抽取阶段，把 Java 的 BufferedReader.readLine、String.split、String.trim 与 FileReader/InputStreamReader 解码翻译成 ArkTS 时
  - 情境：源码用 readLine 循环读文件行，用 split/trim 处理编辑框或文件文本，用 Reader 解码文件；目标准备用 JS 的 split/trim、按 \\n 断行或 TextDecoder；派工可能写“与源端读行函数等价”。多个页面与服务都要用这些调用。
- [实现源端按返回码 switch 的分支时逐值对照源 case，只把源码列出的码判失败，不套用相邻方法的 result !== 0](lesson-9d56a6bbc436ff262d13.lesson.md)
  - 时机：切片实现阶段，转写源端按返回码 switch/case 判定成功或失败的逻辑时
  - 情境：源端 switch 只把部分返回码列为失败分支，其余落入 default 视为成功；同一文件的相邻方法用“非 0 即失败”判定，写者准备照搬。
- [手写 %1$s 位置参数插入时字面插入，不把用户数据作为 String.replace 的替换串](lesson-ecbaa1723e2beb9b1aec.lesson.md)
  - 时机：实现阶段，把 Android getString(resId, args) 或 String.format 的 %1$s、%s 位置参数改写为 ArkTS 字符串拼装（自写 formatRes 一类 helper）时
  - 情境：源端 getString(R.string.x, name) 把用户输入的名称、标题插入格式串（如克隆名后缀）；目标取到格式串后准备用 s.replace('%1$s', arg) 替换占位，或复用兄弟页面已有的同类 helper。
- [源端 HashSet/HashMap 的迭代序决定输出文件、尝试或写入顺序时，按 Java 桶序复刻，不用 JS Set/Map 插入序](lesson-1f4747c81f16e9529787.lesson.md)
  - 时机：规格提取与切片实现阶段，转写依赖 Java 集合迭代序（keySet、values、toArray、new ArrayList&lt;&gt;(set)）的逻辑时
  - 情境：源端用 HashSet/HashMap 的迭代序决定输出文件、尝试顺序、写入顺序或问题清单顺序；目标准备用 JS Set/Map（插入序）或 indexOf 保序替代。
  - 例外：规格或决策明确不要求复刻集合迭代序，并在验收中写明；源端用 LinkedHashSet/LinkedHashMap 或 TreeMap 等有序集合时，按其插入序或键序实现，不套桶序
- [源端 SimpleDateFormat/Calendar 未指定时区或区域时，按默认时区与区域语义复刻：时刻取本地字段，周规则随区域](lesson-91c60cb726d59b315d33.lesson.md)
  - 时机：规格提取与实现阶段，把 SimpleDateFormat/DateFormat、GregorianCalendar 或 Calendar.getInstance() 的格式化、字段读取与周计算翻译成 ArkTS 显式算术或 i18n 调用时
  - 情境：源码 new SimpleDateFormat(pattern\[, Locale\]) 或 Calendar.getInstance() 后没有调用 setTimeZone，就格式化一个毫秒值（变量语义可能像时长，如“已用时间 + 偏移小时×3600000”）、读 HOUR_OF_DAY，或格式化固定 epoch 时刻、按本地小时位探测偏移；也包括用 Calendar 的 WEEK_OF_YEAR、firstDayOfWeek 计算周起止。目标准备“不经 Date/Intl”按 UTC 手工拆 h/m/s，或手写 ISO 周换算。
  - 例外：源端显式 setTimeZone 或传入固定时区、固定 Locale：按该显式配置实现
- [源端把 Float 直接转字符串（toString、模板、资源参数）时按 Float.toString 规则输出，不用 JS 数字串](lesson-98896db85687113ce58f.lesson.md)
  - 时机：实现阶段把 Float 值的 toString()、"$f" 字符串模板、String.valueOf(f) 或作为字符串资源参数的显示翻译成 ArkTS 时；规格为这类显示写判例时
  - 情境：源端变量为 Kotlin Float/Java float，不经格式化器直接转成文本显示（倍率、重量、滑杆标签、资源占位符参数）；目标 number 为双精度，准备用模板串、String(v) 或 toString()。
  - 例外：源端显示前已经过 DecimalFormat、String.format 等格式化：按对应格式化 API 实现
- [转写 Java byte 与 int 字面量的比较（如 b &lt; 0x81）时，先把 0–255 的值换回 -128..127 再比较](lesson-cebf3a8b27e177a86601.lesson.md)
  - 时机：规格提取与实现阶段，转写 Java byte 变量与 int 字面量的比较、范围判断时
  - 情境：源端把字节读入 byte 变量后与 0x81、0xFE 一类 int 字面量比较；目标从 Uint8Array 或 number 数组取到 0–255 的无符号值。
  - 例外：源端先做 b &amp; 0xFF 再比较时，本来就是无符号语义，直接比较
