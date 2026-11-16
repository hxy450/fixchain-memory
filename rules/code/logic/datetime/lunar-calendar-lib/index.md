# 农历算法库（com.nlf.calendar）按日期实时计算的字段

agent 会看到什么：读到源端用 lunar-java 的 Lunar.fromDate 等按任意日期实时算农历、宜忌，assets 下另有只覆盖少量日期的静态 json；产物里数据层只查 rawfile 的预置 json，或用 Intl 的 chinese 历法补算

## 规矩

- rule-768e03da8094｜源端字段由算法库对任意日期实时计算时，不改绑弃用的静态资产，移植算法或上报阻塞｜读到：源端用算法库按日期实时算字段（如 lunar-java 的 `Lunar.fromDate(date)` 取 `dayYi` / `dayJi`），模型里另有标了 `@Deprecated` 的字段，assets 下有只覆盖少量日期的静态 json 表；写错：目标仓储把这些字段只绑定到 rawfile 里的静态 json，`loadDate` 查不到日期就返回 `null`；或降级用 `Intl` 只补了部分字段，其余字段仍为空
- rule-1df9b9853436｜规格要求农历库同输入同输出适配时，用 Intl 的 chinese 历法生成，不以静态资产为唯一来源｜读到：规格 HARD 映射写「com.nlf.calendar.Lunar → 传统历法适配器，同输入同输出」或「任意合法日期可转换」；源码调 Lunar.fromDate / lunarToLunarDate；写错：数据层只按 rawfile 里的预置 JSON 查行，查不到就返回 null 或空网格 []；完成报告的 generated_placeholders 是 []
