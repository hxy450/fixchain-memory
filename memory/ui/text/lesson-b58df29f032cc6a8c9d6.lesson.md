# 字符串语言限定目录与键集按源端实际存在的 values-<语言> 镜像：源端有几种语言就迁几种，限定词粒度照源（values-zh→zh），单语源不合成译文，源 locale 缺键保持缺失、回落 base

ID：`lesson-b58df29f032cc6a8c9d6` · 版本：4

[本主题](index.md)

## 何时使用

规格提取与资源迁移阶段，确定要迁移哪些 values-* 语言目录及其目标限定词、目标生成哪些语言限定字符串目录及各键取值、源 locale 缺键如何处理时

## 适用情境

Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。也包括源端有多个 values-xx（如 es/fr/it/pt/ru/zh/zh-rTW）并提供应用内语言切换，规格或主会话却自定“默认只迁 values + values-zh”，并以“项目决策优先”覆盖资源 skill 的“全部转换”硬规则；部分语言目录键集不全，skill 要求键集一致并自动补译。也包括源端只有仅语言限定的 values-zh，skill 正文写“values-zh-rCN 或 values-zh → zh_CN 或 zh”并要求最少生成 zh_CN，而详细映射表写 values-zh→zh、values-zh-rCN→zh_CN。

## 例外与边界

- 规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言
- 源端引用 android.R.string.* 等框架字符串：译文由系统按设备语言提供，按系统字符串的经验为已有语言补框架译文（必要时补地区目录）

## 原因

HarmonyOS 在中文系统语言下优先取 zh_CN，合成的中文译文让界面显示中文或中英混排，而同一设备上的 Android 源应用显示默认英文；按键集合一致的检查发现不了取值差异。限定词改粒度同样改变匹配范围：仅语言的 values-zh 在 Android 服务所有中文 locale，改写成 zh_CN 后只匹配中国大陆地区，其他中文地区的设备取不到这份译文。来源中资源代理已读到规格“默认文案为英文、迁移不擅自翻译”和只有 values/ 的源清单，仍按 skill 的双语规则用脚本写出整张中文译表；后续写者按键一致继续补中文值，直到视觉验收在 zh-Hans 设备上逐页发现文案不符。缩减语言范围后，应用内选择其他语言只显示英文；为源 locale 缺失的键补写译文，目标会显示源端没有的文案，而 Android 对这些键回落默认 values。

## 做法

1. 先盘点源 res 下实际存在的 `values-<locale>` 目录（values-night、values-sw600dp 等不是语言目录），只为这些语言生成目标限定目录；源只有默认 values/ 时只写 base。
2. 通用 skill 的默认语言规则与项目规格或源码单语事实冲突时，以规格和源码为准，并在资源映射报告写明冲突与取舍。
3. 流程确需保留第二语言目录（例如只放脚手架的 app/ability 键）时，业务键省略以回落 base，或取值与 base 完全一致。
4. 按源 res 下全部 `values-<locale>` 登记迁移范围；没有用户或任务明确裁剪时不自设缩减默认值，项目约定与资源 skill 硬规则冲突时先核对约定的来源，无来源按源端全集执行或作为冲突上报。
5. 源 locale 缺少的键保持缺失，让平台回落 base；不按键集一致规则补写机器翻译，除非任务明确要求补译。
6. 目标限定词按源限定词的粒度映射：仅语言的 values-zh → zh/，带地区的 values-zh-rCN → zh_CN/、values-zh-rTW → zh_TW/；skill 的“最少生成 zh_CN”一类规则不用来改写源端已有的限定词；skill 正文与逐项映射表说法不一时以逐项表为准，并在映射报告写明。

## 可选检查

- 对非 base 语言目录对账：取值与 base 不同的业务字符串，都应能追溯到源端对应的 `values-<locale>` 条目。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-311b8c323b04022b2a04](../../../store/cases/case-311b8c323b04022b2a04/ab46ecccf22e52f446c55f852f10ee3fea2a941b95c71c7a416d4e85f7cd2f06.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ab46ecccf22e52f446c55f852f10ee3fea2a941b95c71c7a416d4e85f7cd2f06`
- [case-8a522021d6d10fded125](../../../store/cases/case-8a522021d6d10fded125/695193a757e708a77ef3560a9f73b4caf829f00fdfad9ee70368e51f842a04f9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`695193a757e708a77ef3560a9f73b4caf829f00fdfad9ee70368e51f842a04f9`
- [case-bf53fdebb87671d9eba3](../../../store/cases/case-bf53fdebb87671d9eba3/cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f.json) · 结论：diagnosis, recommendation:3
  卡片版本：`cb56b1662aea796547436b8d3cee96766e78d87283d49a367635d37b39107c2f`
