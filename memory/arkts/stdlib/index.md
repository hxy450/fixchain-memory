# arkts/stdlib

Java 标准库与语言语义到 ArkTS 的等价实现：读行、split/trim、BOM、String.format 与 Locale、Calendar 周规则，HashSet/HashMap 迭代序、有符号 byte 比较与 switch 返回码；DecimalFormat、BigDecimal 舍入与 Float.toString 的数值转文本，位置参数的字面插入（避开 String.replace 替换模式）

[上一级](../index.md)

## 本级经验

- [DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN，小数点与数字符号取应用偏好语言（Locale.getDefault 跟随应用语言，不是系统区域），Float.toString 的十进制串与“.0”；不用 Math.round、toFixed、无参 intl.NumberFormat 或模板串顶替](lesson-ae093dedda604fddf17e.lesson.md)
  - 时机：实现阶段把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、Float.toBigDecimal().setScale、Float 的 toString 或字符串模板）翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些格式化函数写映射与验收判例时；修改已有共享数值工具时
  - 情境：源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）生成显示文本且未传 Locale，用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN).toFloat() 舍入，或把 Float 值直接 toString、写进字符串模板或字符串资源参数；应用可单独设置应用语言；目标 number 为双精度，准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板字符串实现；共享数值工具与页面可能各有一份同名函数。
- [Java 文本读行、split/trim、BOM、String.format、SimpleDateFormat/Calendar 的时区与周规则不用同名 JS API 近似：按 Java 语义集中实现兼容函数，未 setTimeZone 的格式化按构造时默认时区取本地字段](lesson-237091b9b04bc4cd340b.lesson.md)
  - 时机：页面转换和服务/VM 抽取阶段，把 Java 标准库的读行、切分、去空白、解码、数值格式化与日历计算翻译成 ArkTS 时；把 SimpleDateFormat 格式化毫秒值（含语义像时长的值）或格式化固定 epoch 的偏移探测翻译成显式算术时
  - 情境：源码用 BufferedReader.readLine、String.split/trim、FileReader/InputStreamReader、String.format("%.2f", float) 或 Calendar.getInstance() 的 WEEK_OF_YEAR 处理文件行、编辑框文本、百分比与日期；目标准备用 JS 的 split/trim/toFixed、TextDecoder 或手写 ISO 周换算；派工可能写“与 readFileLineByLine 等价”“数值域同 Android”。 也包括 new SimpleDateFormat(pattern, Locale) 或 Calendar 未调用 setTimeZone 就格式化一个毫秒值（变量语义像时长，如 gameTime + hourOffset×3600000），或格式化 1970-01-01T00:01Z 按本地小时位探测偏移；目标准备“不经 Date/Intl”按 UTC 手工拆 h/m/s。
- [Java 集合迭代序、有符号 byte 比较与 switch 返回码按 Java 语义复刻：HashSet/HashMap 决定顺序时用桶序，byte 先换回 -128..127，只把源 case 列出的码判失败](lesson-1f4747c81f16e9529787.lesson.md)
  - 时机：规格提取与切片实现阶段，转写依赖 Java 集合迭代序（keySet、toArray、new ArrayList&lt;&gt;(set)）、byte 与 int 字面量比较、按返回码 switch 分支的逻辑时
  - 情境：源端用 HashSet/HashMap 的迭代序决定输出文件、尝试顺序、写入顺序或问题清单顺序；用 byte 变量与 0x81 一类 int 字面量比较；switch 只把部分返回码（如 2、-1）判为失败；目标准备用 JS Set/Map（插入序）、0–255 的 number 与相邻方法的 result !== 0 判定。
  - 例外：规格或决策明确不要求复刻集合迭代序，并在验收中写明
- [平台库调用不以形似 JS 内建加“等价”注释收口：ICU 正则字符类、码点切分、List.remove、Base64/Uri 逐项按源语义移植](lesson-5e3ba83ebfe5bbdf9278.lesson.md)
  - 时机：实现阶段把 Java/Android 平台库调用（正则、字符串切分与比较、集合删除、Base64、Uri、MIME 查询）替换为 JS 内建或自写简化函数，准备在注释里写“等价/直迁”时；规格提取阶段描述这类调用的契约时
  - 情境：源码调用 Pattern/String.matches/replaceAll（Android 上由 ICU 执行）、split("")、compareToIgnoreCase、List.remove(Object)、android.util.Base64.decode、Uri.parse(path).getPath()、ContentResolver.getType；目标准备用 JS RegExp 字符类或手写 ASCII 空白集、charCodeAt 逐单元计数、整串 toLowerCase 比较、filter、自写宽松解码、对原始串直接处理或静态扩展名表替代；规格对这些调用只有口语描述（如“非空白字符数”“拒绝 /data 前缀”）。
  - 例外：决策记录明确批准某项语义差异，并写明用户可见影响
- [手写 getString/String.format 的位置参数插入时，不把用户数据作为 String.replace 的替换串：用 split/join 或替换回调字面插入](lesson-ecbaa1723e2beb9b1aec.lesson.md)
  - 时机：实现阶段，把 Android getString(resId, args) 或 String.format 的 %1$s、%s 位置参数改写为 ArkTS 字符串拼装（自写 formatRes 一类 helper）时
  - 情境：源端 getString(R.string.x, name) 把用户输入的名称、标题插入格式串（如克隆名后缀）；目标取到格式串后准备用 s.replace('%1$s', arg) 替换占位，或复用兄弟页面已有的同类 helper。
