# 目标代码对毫秒值直接拆时分秒时，先保存 i18n.getTimeZone() 再加 getOffset(时刻)

审的是：代码
触发（任一种）：
- 读到：源端 new SimpleDateFormat(pattern, Locale) 或 GregorianCalendar 没有 setTimeZone，format 作用在毫秒值上；或规格写着「纯时长格式化」「不经 Date/Intl」；写错的样子：目标代码对毫秒值直接取模（% 86400000、/ 3600000）拆 h/m/s 补零，没有加 TimeZone.getOffset(...)，等于按 UTC 显示
适用范围：源端格式化未设时区的毫秒值、目标端改用手写算术格式化时
做法：
- 在源端 formatter 构造对应的时机保存 tz = i18n.getTimeZone()（import { i18n } from '@kit.LocalizationKit'）
- 格式化时先算 local = ms + tz.getOffset(ms)，再对 local 拆 HH/mm/ss 补零；规格写成纯时长的，按源端实现写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getTimeZone(zoneID?: string): TimeZone：不传 zoneID 取系统时区（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，i18n.getTimeZone）
- getOffset(date?: number): number：date 是毫秒时刻；返回该时刻的偏移，单位毫秒，含夏令时（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，TimeZone.getOffset）
- export { i18n, intl, resourceManager, sendableResourceManager }：i18n 从 @kit.LocalizationKit 导入（出处：鸿蒙 SDK 的 ets/kits/@kit.LocalizationKit.d.ts）
- calendar = Calendar.getInstance(loc)（the calendar should use the current default TimeZone）：源端 SimpleDateFormat 构造时绑定默认时区（出处：java.text.SimpleDateFormat#initializeCalendar）
- 构造时保存 i18n.getTimeZone()，显示前加 timeZone.getOffset(时刻) 再拆时分秒，UTC+8 下两端一致：返修后的写法（出处：卡里修好并验证过）
未核实：卡里上机只对照了 UTC+8
来源：1 张卡，1 个应用
- case-4f72f9527ef62209097d（Blockinger）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 3；取值 5 ← 诊断
