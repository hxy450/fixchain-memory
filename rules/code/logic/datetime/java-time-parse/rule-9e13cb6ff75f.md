# 源端用 toLocalDate() >= today 选格式时，目标在日期轴上比较 >=，不用年月日相等

审的是：代码
触发（任一种）：
- 读到：源端 `withZoneSameInstant(zoneId).toLocalDate() >= today` 时用时间格式，否则用中等日期格式；写错的样子：目标用 getFullYear() / getMonth() / getDate() 三项相等判断「今天」，未来日期落进 toLocaleDateString 分支；注释抄的是规格短句
适用范围：把源端按日期比较选显示格式的逻辑迁成 ArkTS 时
做法：
- 两边先换成本地日的零点毫秒（日期轴），再写 `pubDayMs >= todayMs` 选时间格式，否则用中等日期格式
- 以源码表达式为准，注释引用源码条件原文（`toLocalDate() >= today`），不抄规格里的短句
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LocalDate#compareTo 依次比较年、月、日：Kotlin 的 >= 走 compareTo，今天和未来日期都算满足（出处：java.time.LocalDate#compareTo）
- publicationDayMs >= todayMs：修好后的比较写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端比较时用的时区：源工程里调用 withZoneSameInstant 的那段 Kotlin 代码，看传入的 zoneId 从哪来；是系统默认时区时，目标用本地时间的年月日取零点；是固定时区时按那个时区换算
来源：1 张卡，1 个应用
- case-3f05228d17f878067234（com.nononsenseapps.feeder）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
