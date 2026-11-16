# 源端 Calendar 按 WEEK_OF_YEAR 推日期时，目标按区域周规则算，不用 ISO 周

审的是：代码
触发（任一种）：
- 读到：`Calendar.getInstance()` 后 set(Calendar.WEEK_OF_YEAR, week)、set(Calendar.YEAR, …) 推算日期；写错的样子：目标按 ISO 8601（1 月 4 日所在周的周一）写死周规则，注释写「取确定性 ISO 语义」
适用范围：Java 用默认区域的 Calendar 按年内周序号推算日期，迁成 ArkTS 时
做法：
- 取区域日历 i18n.getCalendar(i18n.System.getSystemLocaleInstance().toString())，读 getFirstDayOfWeek()（1 是周日，7 是周六）和 getMinimalDaysInFirstWeek()
- 第 1 周是从 firstDayOfWeek 开始、在该年里至少含 minimalDaysInFirstWeek 天的最早 7 天；第 N 周起点 = 第 1 周起点 + (N-1)×7 天
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 第一周是从 getFirstDayOfWeek() 开始、至少含 getMinimalDaysInFirstWeek() 天的最早 7 天；两个值都随区域变化：源端 WEEK_OF_YEAR 的定义（出处：java.util.Calendar（类说明，firstDayOfWeek、minimalDaysInFirstWeek））
- export function getCalendar(locale: string, type?: string): Calendar：按区域取日历对象（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，i18n.getCalendar）
- getFirstDayOfWeek(): number，1 表示周日，7 表示周六：区域的周首日（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，Calendar.getFirstDayOfWeek）
- getMinimalDaysInFirstWeek(): number：区域的首周最少天数（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，Calendar.getMinimalDaysInFirstWeek）
- 改按 i18n Calendar 的 firstDayOfWeek / minimalDaysInFirstWeek 计算周起点后与源端一致；ISO 周在 en-US 等区域起止日期偏移：卡里的修法（出处：卡里修好并验证过）
未核实：卡的环境是 API 24，本机按 API 23 的声明核实；Java 默认区域与系统区域不同（应用单独设了语言）时取哪一个没有核实
来源：1 张卡，1 个应用
- case-526d6b56241863d015dd（MifareClassicTool）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
