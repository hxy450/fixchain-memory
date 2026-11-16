# 用系统 i18n / intl 替代有自有阈值和模板的库时，移植算法和资源，不自定阈值冒充库默认

审的是：代码
触发（任一种）：
- 读到：源端 new PrettyTime(); pt.setLocale(locale); pt.format(date)；写错的样子：目标用 intl.RelativeTimeFormat(…, { numeric: 'auto' }) 配自定阈值（秒、天、周、月、Math.round），注释写「prettytime 默认粒度」
- 读到：源端 DateUtils.formatDateTime(context, t, FORMAT_ABBREV_WEEKDAY | FORMAT_SHOW_WEEKDAY | FORMAT_ABBREV_MONTH | FORMAT_SHOW_DATE) 再拼 FORMAT_SHOW_TIME；写错的样子：目标用 intl.DateTimeFormat({ weekday: 'short', month: 'short', day, hour, minute }) 直接格式化，没有「不是本年才带年份」的规则
适用范围：服务实现阶段用系统国际化接口替代相对时间、日期格式类库时
做法：
- 只有库本身是系统接口的薄封装时才直接换成系统接口；PrettyTime、重复文案格式化器、DateUtils 的 skeleton 这类有自有阈值、模板和资源表的，移植算法和资源
- 暂时做不到移植时，把自定阈值与库默认值逐项对照写进注释并登记差异，不标「库默认粒度」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- format(value: number, unit: string): string；unit 只能是 year、quarter、month、week、day、hour、minute、second：只按调用方给的数值和单位格式化，换单位的阈值和取整要调用方自己定；@deprecated since 20，改用 Intl.RelativeTimeFormat（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，RelativeTimeFormat.format）
- skeleton 依次拼 [y] + MMM（ABBREV_MONTH）+ d + EEE（ABBREV_WEEKDAY）+ 时间（j / H / h 加 m）；不在同一年或不是今年时才加 y：源端短日期的年份规则和字段顺序（出处：android.text.format.DateUtilsBridge#toSkeleton）
- 只给 FORMAT_SHOW_TIME、没给 12 / 24 小时标志时，按 DateFormat.is24HourFormat(context) 补 FORMAT_24HOUR 或 FORMAT_12HOUR：源端时间部分跟随用户的 24 小时制设置（出处：android.text.format.DateUtils#formatDateRange）
- static is24HourClock(): boolean：目标端读系统是否用 24 小时制，对应源端 is24HourFormat（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，System.is24HourClock）
- PrettyTime 3.2.7 的默认：5 分钟内为「moments ago」，按 0.75 容差取整，周、月、年、十年等单位有各自的毫秒阈值，带 44 种语言资源：库默认行为，系统接口给不出（出处：卡里修好并验证过）
- 目标的日期工具类重写为 libcore skeleton + PrettyTime 3.2.7 移植，并补 DateFormat.is24HourFormat 的等价：修复后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 相对时间库的版本、默认阈值和语言资源：源工程依赖里 prettytime 的版本；本机 Gradle 缓存里该版本的 jar；用 JDK 小程序跑一组时间差取真值，对照阈值和取整写进移植代码
来源：1 张卡，1 个应用
- case-d23537ecc4c87801075a（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断；取值 6 ← 诊断
