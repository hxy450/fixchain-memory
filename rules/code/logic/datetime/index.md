# 日期和时间

源端有 Calendar、SimpleDateFormat、时区和周的计算、System.nanoTime、农历算法库，目标端有手写的日期拆分、时区偏移和时钟函数时

## 触发族

- [农历算法库（com.nlf.calendar）按日期实时计算的字段](lunar-calendar-lib/index.md)（2 条）：读到源端用 lunar-java 的 Lunar.fromDate 等按任意日期实时算农历、宜忌，assets 下另有只覆盖少量日期的静态 json；产物里数据层只查 rawfile 的预置 json，或用 Intl 的 chinese 历法补算
- [Calendar 和 SimpleDateFormat 的日期、周与时区计算](calendar-timezone/index.md)（4 条）：读到源端 SimpleDateFormat / GregorianCalendar 对毫秒值格式化、Calendar 按 WEEK_OF_YEAR 或 firstDayOfWeek 推日期；产物里手写的时分秒拆分、时区偏移（getRawOffset / getOffset）、ISO 周规则和月历查询范围
- [System.nanoTime 一类的单调时钟计时](monotonic-clock/index.md)（1 条）：读到源端用 System.nanoTime() 求帧间隔、推进动画进度或重置计时基线；产物里的时钟函数写成 performance.now()、Date.now() 或 systemDateTime.getTime()，注释写「ms 墙钟」
- [java.time 的 Instant / ZonedDateTime 解析和日期比较](java-time-parse/index.md)（3 条）：读到源端用 Instant.parse、ZonedDateTime.parse 严格解析 ISO 时间串并捕获 DateTimeParseException 走失败分支，或用 withZoneSameInstant(…).toLocalDate() >= today 选格式；产物里写成宽松的 Date.parse / new Date(str) 只判 NaN，或用 getFullYear / getMonth / getDate 三项相等判「今天」
- [重复规则库（RRULE）的序列化和文案](rrule-recurrence/index.md)（1 条）：读到源端用 RRule / Recur 这类重复规则库 toString、getNextDate，或 EventRecurrenceFormatter.getRepeatString 出重复文案；产物里手拼的 RRULE 串（UNTIL=…Z、换行）、自写的 DAILY / WEEKLY 步进和降级的重复文案
