# 阶段规则要跳过身份字段时，先对照下游验证门的模板值判定：冲突就安排验证前的落地步骤，或让验证门对已登记延后项给出 DEFERRED

ID：`lesson-60d5b35c4ca9c2ccce3b` · 版本：1

[本主题](index.md)

## 何时使用

维护迁移流水线的阶段规则与身份技能范围时；执行编排以受限范围（如开发期身份）派发身份步骤、决定跳过某个字段时

## 适用情境

执行规则或身份技能以“部署期再落地”为由跳过 bundleName、vendor 等字段并保留脚手架值；下游验证门对 com.example.* 包名、vendor=example 等模板默认值直接判失败；流水线在该阶段之后没有安排落地步骤。

## 原因

跳过规则与验证门分属不同阶段，各自看都成立；被跳过的字段正是验证门的失败项、中间又没有落地步骤时，产物必然在验证期失败，而执行者照规则保留模板值，自检还会写“preserved”通过。

## 做法

1. 跳过某个身份字段前，逐项比对下游验证门的模板默认值规则（如 vendor=example、bundleName 匹配 com.example.* 判失败）；冲突时在输出中指出，不静默保留脚手架值。
2. 维护流水线时让两者一致：跳过规则只在工程台账确有已批准的部署期身份决策且已有签名配置时生效；进入验证前安排落地步骤，或让验证门对已登记延后的字段给出 DEFERRED。
3. 确需延后时，在决策台账登记例外、落地时点与复检条件，在迁移报告列出保留的模板值及理由，并把相关技术项标为未完成。

来源支持：5 张卡 · 5 次迁移 · 5 个应用

## 来源（按需复核）

- [case-15465539e78d3d899b47](../../../store/cases/case-15465539e78d3d899b47/7e465462489dec7c4a8da20521c360bfd41a34281bf8e6ad032c54ab4c6d0e32.json) · 结论：diagnosis, recommendation:1
  卡片版本：`7e465462489dec7c4a8da20521c360bfd41a34281bf8e6ad032c54ab4c6d0e32`
- [case-5da0c8596ac49217f162](../../../store/cases/case-5da0c8596ac49217f162/5723bb386ebff8505f8b14d9dd0eeb50e6649ce727be6bc488d4af37484b7058.json) · 结论：recommendation:2
  卡片版本：`5723bb386ebff8505f8b14d9dd0eeb50e6649ce727be6bc488d4af37484b7058`
- [case-c164fb6e384f47fb7ecf](../../../store/cases/case-c164fb6e384f47fb7ecf/48b99b6ec8e2e71e4367568b6230e60b45600f2f613293cf861ab8ddbde09d02.json) · 结论：diagnosis, recommendation:2
  卡片版本：`48b99b6ec8e2e71e4367568b6230e60b45600f2f613293cf861ab8ddbde09d02`
- [case-e6f851fe0dda3d49dc04](../../../store/cases/case-e6f851fe0dda3d49dc04/ef3331bf3ff46ad917f984ee7ea057ba8e0400dc9221dc6fda83486ac3a402f6.json) · 结论：recommendation:3
  卡片版本：`ef3331bf3ff46ad917f984ee7ea057ba8e0400dc9221dc6fda83486ac3a402f6`
- [case-f935850c669c48f05a00](../../../store/cases/case-f935850c669c48f05a00/69dfa72ef88368edd0415d1e9f4e42348abeb6abd342525bb8b208074d2011a3.json) · 结论：diagnosis, recommendation:2
  卡片版本：`69dfa72ef88368edd0415d1e9f4e42348abeb6abd342525bb8b208074d2011a3`
