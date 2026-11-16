# 重复规则库（RRULE）的序列化和文案

agent 会看到什么：读到源端用 RRule / Recur 这类重复规则库 toString、getNextDate，或 EventRecurrenceFormatter.getRepeatString 出重复文案；产物里手拼的 RRULE 串（UNTIL=…Z、换行）、自写的 DAILY / WEEKLY 步进和降级的重复文案

## 规矩

- rule-8c637a064176｜源码用库输出作持久化串或文案时，先取库真值再写序列化，不固定成 UTC Z、不降级文案｜读到：源端 new RRule(recur).toString().replace("RRULE:", "")、EventRecurrenceFormatter.getRepeatString(...)、Recur.getNextDate(...)；派工要求与源端产物逐字段兼容；写错：目标 RRULE 串写成固定 UTC 的 UNTIL=…Z、没有 CRLF；下一次时间自写 DAILY / WEEKLY 步进；重复文案「降级为 FREQ 词 + 原样透传」
