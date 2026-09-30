# 只为源端实际存在的 values-<语言> 目录生成目标语言限定字符串；单语源不合成 zh_CN 等译文

ID：`lesson-b58df29f032cc6a8c9d6` · 版本：1

[本主题](index.md)

## 何时使用

资源迁移阶段，决定目标工程生成哪些语言限定字符串目录（base、zh_CN 等）及各键取值时

## 适用情境

Android 源只有默认 res/values/strings.xml（常为英文），没有 values-zh 等语言限定目录；规格要求与源应用逐屏对齐或写明“不擅自翻译”；资源转换 skill 带有“至少生成两套语言、默认英文则补 zh_CN”一类通用规则；设备可能使用中文系统语言。

## 例外与边界

- 规格或决策明确要求本轮新增本地化语言；此时按批准的译文来源生成，并在报告中注明源端没有该语言

## 原因

HarmonyOS 在中文系统语言下优先取 zh_CN，合成的中文译文让界面显示中文或中英混排，而同一设备上的 Android 源应用显示默认英文；按键集合一致的检查发现不了取值差异。来源中资源代理已读到规格“默认文案为英文、迁移不擅自翻译”和只有 values/ 的源清单，仍按 skill 的双语规则用脚本写出整张中文译表；后续写者按键一致继续补中文值，直到视觉验收在 zh-Hans 设备上逐页发现文案不符。

## 做法

1. 先盘点源 res 下实际存在的 values-<locale> 目录（values-night、values-sw600dp 等不是语言目录），只为这些语言生成目标限定目录；源只有默认 values/ 时只写 base。
2. 通用 skill 的默认语言规则与项目规格或源码单语事实冲突时，以规格和源码为准，并在资源映射报告写明冲突与取舍。
3. 流程确需保留第二语言目录（例如只放脚手架的 app/ability 键）时，业务键省略以回落 base，或取值与 base 完全一致。

## 可选检查

- 对非 base 语言目录对账：取值与 base 不同的业务字符串，都应能追溯到源端对应的 values-<locale> 条目。

## 来源（按需复核）

- [case-311b8c323b04022b2a04](../../../store/cases/case-311b8c323b04022b2a04/ab46ecccf22e52f446c55f852f10ee3fea2a941b95c71c7a416d4e85f7cd2f06.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ab46ecccf22e52f446c55f852f10ee3fea2a941b95c71c7a416d4e85f7cd2f06`
