# 规格的依据列只引用自己查过的 d.ts，上游「无 API」补查后再落笔

审的是：规格
触发（任一种）：
- 读到：派工要求引用上游 skip-list / 决策台账里「无 X API」的既有条目；写错的样子：规格映射行的依据写成「skip-list … 行——无 X API；d.ts 无对应能力条款」，规格作者自己没有检索过 d.ts
适用范围：feature 规格在契约或依据列写平台能力结论时
做法：
- 依据列只写自己实际查过的 d.ts 段落、arkts-knowledge-verifier 结论或 references 条目；上游的「无 API」先补查一次，查到接口就按接口写，不能改写成「d.ts 无对应能力条款」
针对本应用要查的：
- 上游结论对应的鸿蒙接口：鸿蒙 SDK 的 openharmony/ets/api、hms/ets/api 下的 .d.ts 和 ets/kits 导出，按能力关键词搜；把命中的文件、符号和标注写进依据列；为空写检索词
来源：1 张卡，1 个应用
- case-33b4b9ce51ba471ee770（Cofi）：做法第 1 步 ← 建议 4、诊断
