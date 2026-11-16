# Calendar 和 SimpleDateFormat 的日期、周与时区计算

agent 会看到什么：读到源端 SimpleDateFormat / GregorianCalendar 对毫秒值格式化、Calendar 按 WEEK_OF_YEAR 或 firstDayOfWeek 推日期；产物里手写的时分秒拆分、时区偏移（getRawOffset / getOffset）、ISO 周规则和月历查询范围

## 规矩

- rule-89d01f64af4a｜目标代码对毫秒值直接拆时分秒时，先保存 i18n.getTimeZone() 再加 getOffset(时刻)｜读到：源端 new SimpleDateFormat(pattern, Locale) 或 GregorianCalendar 没有 setTimeZone，format 作用在毫秒值上；或规格写着「纯时长格式化」「不经 Date/Intl」；写错：目标代码对毫秒值直接取模（% 86400000、/ 3600000）拆 h/m/s 补零，没有加 TimeZone.getOffset(...)，等于按 UTC 显示
- rule-c0b843b4f2a5｜目标代码用 getRawOffset() 复刻 1970 时刻的偏移探测时，改成 getOffset(该时刻)｜读到：源码在 SimpleDateFormat 构造后格式化固定的 epoch 时刻（如 60000 ms），按小时位前缀判定偏移；写错：目标代码用 i18n.getTimeZone().getRawOffset() 求这个偏移
- rule-1f0e2f3ae7d2｜源端 Calendar 按 WEEK_OF_YEAR 推日期时，目标按区域周规则算，不用 ISO 周｜读到：`Calendar.getInstance()` 后 set(Calendar.WEEK_OF_YEAR, week)、set(Calendar.YEAR, …) 推算日期；写错：目标按 ISO 8601（1 月 4 日所在周的周一）写死周规则，注释写「取确定性 ISO 语义」
- rule-67c6e894eee1｜月历查询范围按页面实际格子的首尾日期计算，不按自然月 1 日到月底截断｜写错：ArkTS 月历的查询范围写成自然月 1 日到月底（如 new Date(y, m, 1) 到 new Date(y, m + 1, 0)），月格里补位的上月尾、下月头没有数据
