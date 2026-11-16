# 规格引用的上游清单和台账条目（api-inventory、接口清单、skip-list）

agent 会看到什么：读到模板或派工要求取 api-inventory.json 的 auth_type、接口清单的常量表、上游 skip-list 里「无 X API」的条目，而磁盘上只有 raw_apis.json、查出来是 0 条或作者自己没检索过 d.ts；交回的规格照样写「见某数据源」「已就绪」或照抄「无 X API」

## 规矩

- rule-9ec821759a02｜规格把取值写成「见某数据源」时，先确认那里真有值，查不到写「未核」并给源码位置｜读到：查询接口清单的结果显示某类常量（如业务状态码）为 0 条；写错：规格仍写「业务状态码：见接口清单的常量表（某码 登录过期…）」，指向的数据源里没有这些值，括号里留着推断出的码
- rule-63bf36d6254b｜API 清单的鉴权摘要还没落盘时，规格的网络层认证小节保留待补标记，不以 raw_apis 收口｜读到：feature-base 模板要求认证和拦截器取自 api-inventory.json 的 auth_type / auth_detail 和 common.md，但磁盘上只有 raw_apis.json；写错：规格网络层写「数据源 raw_apis.json（已就绪）」，删掉了「待 api-inventory.json（含 auth_type）」这类待补标记，认证只写「统一 token 注入」一句
- rule-bcee1f53a0ce｜规格的依据列只引用自己查过的 d.ts，上游「无 API」补查后再落笔｜读到：派工要求引用上游 skip-list / 决策台账里「无 X API」的既有条目；写错：规格映射行的依据写成「skip-list … 行——无 X API；d.ts 无对应能力条款」，规格作者自己没有检索过 d.ts
