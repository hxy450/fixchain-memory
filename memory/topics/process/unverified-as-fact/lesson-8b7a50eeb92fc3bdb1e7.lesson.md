# 据检索回执下“不存在”结论（SDK 无此成员或枚举值、工程未导出、资源未迁移）前，确认检索覆盖了完整范围：截断窗口和只查一处只能证明看到的部分

ID：`lesson-8b7a50eeb92fc3bdb1e7` · 版本：1 · 阶段：spec/execute/converge · 主题：[process/unverified-as-fact](index.md)

概要：下“不存在”结论前确认检索覆盖完整声明与范围

信号：`.d.ts`, `sed -n`, `head -n`, `grep -n`, `ets/api`, `base/media`

## 何时使用

规格提取、切片实现与接线收口阶段，准备依据检索结果写下“平台无此 API/枚举值”“公开面未导出”“资源未迁移”“无入口”，并据此改映射、写死取值、静默替换选项或登记平台缺口时

## 适用情境

检索回执来自按行号或固定字符数截取的 d.ts 片段（sed 前 N 行、head、脚本固定窗口），或只查了预想的一个类、一个文件、base 资源目录；要找的成员可能在同一声明更靠后的位置、在并行切片的产物里，或在限定资源目录里。也包括当前工程确实没有某个 getter 或入口，写者直接推定平台没有对应 API；以及检索结论与规格 AC、登记行要求的映射相矛盾。

## 原因

回执只能证明看到了哪些成员，不能证明缺了哪些；截断窗口和只查一处的检索常恰好漏掉要找的项。否定结论随后变成写死的取值、静默替换的选项、恒定返回或“平台缺口”登记，编译照常通过，后续阶段把它当成已查证事实。工程里没有某个 getter 只说明工程尚未暴露，不说明平台不支持。

## 做法

1. 查 SDK 成员或枚举值是否存在时，按成员名直接 grep（如 grep -n 'NAME_A\|NAME_B' 对应 d.ts），或从 interface/enum 声明起读到闭合括号；固定行数、固定字符窗口和 head 截出的回执只说明看到了哪些成员，不作为否定依据。
2. 查工程内是否已有某方法、判断或入口时，按源函数名与语义在全部上游产物和并行切片中检索，不只查预想的类；查资源时连同全部限定目录（各密度、各语言）一起列出。
3. 工程检索落空只记“工程未暴露”：平台有对应 API 就补实现，或回派拥有该文件的切片；写“平台无此能力”前在本机 SDK d.ts 检索，把文件与行号写进登记理由，没有 d.ts 依据不登记平台缺口。
4. 检索结论与规格 AC、登记行或同工程已有写法矛盾时，先按成员名定向复查，再决定是否改映射；确认确实缺失后按平台差异登记。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [跨文件补实现的功能登记带负责方与验证的移交项](../handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 3 张卡）
- [解前向占位按触发文本逐项兑现，写常量不算闭合](../deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md)（共享 3 张卡）
- [必读 skill 与源码逐份读全，截断即重读再写码](../unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 2 张卡）
- [功能对齐以代码落点为准，空回调不算实现](../claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md)（共享 2 张卡）
- [偏好契约按源全部读写点定格式、缺键与持久性](../../data/preferences/lesson-bf7a5ff24d5ae4193eb4.lesson.md)（共享 2 张卡）

来源支持：8 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-4171cd43bbb420b4ee40](../../../../store/cases/case-4171cd43bbb420b4ee40/0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa.json) · 结论：rec-54ca256d72
  卡片版本：`0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa`
- [case-76fcde297f6a5406e58f](../../../../store/cases/case-76fcde297f6a5406e58f/4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d.json) · 结论：rec-50093589aa
  卡片版本：`4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d`
- [case-775c2298a494ebceb71c](../../../../store/cases/case-775c2298a494ebceb71c/d711688bb4178570fd5e418ae31c04b00870fc4ee4045447542f4db47b2c685f.json) · 结论：rec-cd0a3ac391
  卡片版本：`d711688bb4178570fd5e418ae31c04b00870fc4ee4045447542f4db47b2c685f`
- [case-91084f18203ecc5e7036](../../../../store/cases/case-91084f18203ecc5e7036/b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561.json) · 结论：rec-bd997b39d3
  卡片版本：`b2ef3d93c321f92d42c3adeb2614a39fc4a1d58051f93808ce0ad907fbc2e561`
- [case-9d3828c851006d29fc06](../../../../store/cases/case-9d3828c851006d29fc06/c198fe473f6d3c9d774f95de74c649d6542ab966ab417df2dcb1881819cb4366.json) · 结论：diagnosis, rec-bafb55f00f, rec-cdc5be4c36
  卡片版本：`c198fe473f6d3c9d774f95de74c649d6542ab966ab417df2dcb1881819cb4366`
- [case-a0ce76f2b62e29f7e625](../../../../store/cases/case-a0ce76f2b62e29f7e625/685a7008b68cbb1654bdc78ced08355677ac078b506b6128ce591e666fef9692.json) · 结论：rec-55cc953c14
  卡片版本：`685a7008b68cbb1654bdc78ced08355677ac078b506b6128ce591e666fef9692`
- [case-d5698429a34c85664785](../../../../store/cases/case-d5698429a34c85664785/7ab31e28c5c952c7e5c7b20548bde4e7bd5dbfb464237ece26dfb1b81c2cebe0.json) · 结论：diagnosis
  卡片版本：`7ab31e28c5c952c7e5c7b20548bde4e7bd5dbfb464237ece26dfb1b81c2cebe0`
- [case-ef167da8e80990c31714](../../../../store/cases/case-ef167da8e80990c31714/b0741045842d4ef96db79c2bd8c9a99425324ad7612422a92bb274517b7f68a8.json) · 结论：rec-63e620a5f5
  卡片版本：`b0741045842d4ef96db79c2bd8c9a99425324ad7612422a92bb274517b7f68a8`
