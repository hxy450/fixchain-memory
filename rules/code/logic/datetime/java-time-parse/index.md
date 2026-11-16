# java.time 的 Instant / ZonedDateTime 解析和日期比较

agent 会看到什么：读到源端用 Instant.parse、ZonedDateTime.parse 严格解析 ISO 时间串并捕获 DateTimeParseException 走失败分支，或用 withZoneSameInstant(…).toLocalDate() >= today 选格式；产物里写成宽松的 Date.parse / new Date(str) 只判 NaN，或用 getFullYear / getMonth / getDate 三项相等判「今天」

## 规矩

- rule-4694c6071111｜源端 Instant.parse 的严格 ISO 解析，不用宽松的 Date.parse 代替｜读到：源端用 Instant.parse(text) 解析时间串，并捕获 DateTimeParseException 走失败分支；写错：目标用 Date.parse(...) 或 new Date(str) 宽松解析，非 ISO 的串也被接受，源端的失败分支没了
- rule-773662a44402｜ZonedDateTime.parse 先校验带偏移的 ISO 串再 Date.parse，不裸用｜读到：Kotlin 源里 ZonedDateTime.parse(text)，catch 后保留旧值或取 now；规格写「日期字符串非法 → 保留旧值」；写错：目标直接 Date.parse(raw)（注释还写着源为 ZonedDateTime.parse），只判 NaN，纯日期 '2024-01-02' 这类源函数会拒绝的串也被接受、覆盖旧值
- rule-9e13cb6ff75f｜源端用 toLocalDate() >= today 选格式时，目标在日期轴上比较 >=，不用年月日相等｜读到：源端 `withZoneSameInstant(zoneId).toLocalDate() >= today` 时用时间格式，否则用中等日期格式；写错：目标用 getFullYear() / getMonth() / getDate() 三项相等判断「今天」，未来日期落进 toLocaleDateString 分支；注释抄的是规格短句
