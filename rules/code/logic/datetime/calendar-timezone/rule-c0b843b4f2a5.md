# 目标代码用 getRawOffset() 复刻 1970 时刻的偏移探测时，改成 getOffset(该时刻)

审的是：代码
触发（任一种）：
- 读到：源码在 SimpleDateFormat 构造后格式化固定的 epoch 时刻（如 60000 ms），按小时位前缀判定偏移；写错的样子：目标代码用 i18n.getTimeZone().getRawOffset() 求这个偏移
适用范围：源端用格式化固定历史时刻探测时区偏移、目标端写显式算术时
做法：
- 写成 tz.getOffset(同一时刻的毫秒值)（如 tz.getOffset(60000)），用它算出该时刻的本地小时位，再照源端的前缀判定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getOffset(date?: number): number：按指定毫秒时刻求偏移（毫秒），含夏令时（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，TimeZone.getOffset）
- getRawOffset(): number：原始偏移（毫秒），不随时刻变（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，TimeZone.getRawOffset）
- 探测改为 getOffset(60000) 后两端对照一致：返修后的写法（出处：卡里修好并验证过）
未核实：Europe/London 下未上机对照
来源：1 张卡，1 个应用
- case-4f72f9527ef62209097d（Blockinger）：做法第 1 步 ← 诊断、建议 1；取值 3 ← 诊断
