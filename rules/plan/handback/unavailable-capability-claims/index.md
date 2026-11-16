# 不可用能力的完成说法

agent 会看到什么：台账或决策里关于能力不可用、降级、「不得伪造成功」的条目，和回执、迁移报告、修复单对这项写的完成或放行说法（已完成、WIRED+VERIFIED、do not navigate）

## 规矩

- rule-03727d96b3c5｜核心能力只有不可用实现时，回执写明未接入并登记占位或决策缺口，不报完成｜读到：规格和台账留桩范围要求真实实现，台账汇总行却写降级，输入互相矛盾；写错：切片回执称功能已完成，而核心能力只有不可用实现；没有登记 thirdparty-sdk 占位，migration-report 的「决策缺口」里也没有这一项
- rule-6b66723da998｜迁移报告把功能记为已接线已验证前，与账本里 approved 的实现类决策逐条对照｜读到：决策账本里该功能的实现类决策为 approved（选定等价实现，未选仅前台）；写错：迁移报告把功能记为 WIRED+VERIFIED，并以决策编号为由写成「前台常亮 + 显式不可后台」之类，实际代码是桩
- rule-c9af95ff0da6｜修复单描述奖励门结果时分三类给期望，台账没批准阻断就不把「不伪造成功」写成「不导航」｜读到：台账写「核心流程全部真实跑通；仅平台或三方能力不可用时返回明确 unavailable，不得伪造成功」，广告输出 closed|rewarded|failed|unavailable；源端入口只在奖励回调后导航；写错：修复单写「return true only for REWARDED; dismissed/failed/unavailable … do not navigate」，把能力不可用和用户未获奖励并列为不放行
