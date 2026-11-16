# 随默认时区和区域变化的日期时间调用

agent 会看到什么：源码里 SimpleDateFormat、GregorianCalendar、Calendar.getInstance() 没 setTimeZone 就 format 毫秒值，或用 Locale.getDefault() 等随区域变化的调用，规格写成「纯时长格式化」、按 getRawOffset 探测、样例只有 UTC 0，或在笔记里写「确定性取舍」

## 规矩

- rule-546d63e283ef｜SimpleDateFormat 未 setTimeZone 格式化毫秒值时，规格按时刻加默认时区偏移写契约｜读到：源码 new SimpleDateFormat(pattern, Locale)、GregorianCalendar 或 Calendar.getInstance() 没有调用 setTimeZone，format(...) 作用在一个毫秒值上（变量名或用途看起来像时长也一样）；写错：规格的实现映射或算法说明写成「纯时长格式化（手工 h/m/s + 补零）」「不经 Date/Intl」，对毫秒值直接拆时分秒，没写时区偏移
- rule-5e9898d23075｜源端格式化固定 epoch 时刻探测偏移时，规格用 getOffset(该时刻)，不用 getRawOffset｜读到：源码在 SimpleDateFormat 构造后格式化一个固定的 epoch 时刻（如 60000 ms，即 1970-01-01T00:01Z），按结果的小时位前缀（如 23、01）判定偏移；写错：规格把这个探测写成当前的 getRawOffset()，或断言 rawOffset 与 1970 年那一刻的本地小时位等价、历史或夏令时差异可以忽略
- rule-b7d8fe953d0d｜时间显示的验收只给 UTC 偏移 0 样例时，补一个非零偏移时区的样例｜读到：源端的时间显示经 SimpleDateFormat、GregorianCalendar 或 Calendar 在默认时区下格式化；写错：验收条目里时间显示的样例只有 UTC 偏移 0 下的（毫秒值 → HH:mm:ss），没写在哪个时区下，也没有非零偏移时区的样例
- rule-f9def8dac686｜偏离源端随区域变化的语义时，登记为待确认决策，不只写在注释或源码笔记里｜读到：源码用 Calendar.getInstance()、Locale.getDefault() 等随区域变化的调用；映射或验收要求「数值域同 Android」「与 Android 同日」；写错：源码笔记或代码注释里写「确定性取舍」「取确定性 ISO 语义」「有意偏差」，决策台账里没有对应的待确认决策
- rule-853dc74a1f13｜平台限制文件名时规格保留源格式、只替换非法字符，改格式要有选择器实测证据｜读到：源码建议文件名用 DateFormat.getDateTimeInstance(SHORT, SHORT, Locale.getDefault()) 格式化；页面规格写「文件名规则保留」；写错：规格或决策台账把建议文件名改成固定格式（如 yyyy-MM-dd_HH-mm）并新开决策项，理由是选择器拒绝某些字符，但没有实测证据
