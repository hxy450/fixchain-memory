# 交回报告与完成说法

交回的回执、交付说明、收口报告、转换报告、slice notes 里写着「已实现」「已补齐」「已对齐」「全部完成」「resolved」「均保留」这类完成说法时

## 触发族

- [交付报告里的交互和入口](report-interactions/index.md)（4 条）：交付报告、转换报告里的「已实现交互」、按决策留成占位的入口、跳板 Activity（onCreate 里 startActivity 再 finish）的写法
- [不可用能力的完成说法](unavailable-capability-claims/index.md)（3 条）：台账或决策里关于能力不可用、降级、「不得伪造成功」的条目，和回执、迁移报告、修复单对这项写的完成或放行说法（已完成、WIRED+VERIFIED、do not navigate）
- [没接上的 AC 在交回里的记法](unwired-ac-reporting/index.md)（10 条）：规格 AC 要求的字段、数据、失败态、分享渠道或目标符号还没接上时，交回报告、slice notes、占位登记、verify 报告里写的完成说法（全部完成、已实现、N/N、scope 外）
- [交付和收口报告里的已补齐、已验证说法](delivery-claims/index.md)（8 条）：交付说明、收口报告、impl_claims 或自检写「已补齐」「编译通过」「已实现」「符合 P-05」，没有逐项对照实现文件或运行结果，也没把没验证到的项登记出来
- [回执和 marker 里的已实现、已解决标记](resolved-without-source/index.md)（4 条）：回执、巡检报告或接线 marker 标「已实现」「已补齐」「resolved」，而源布局没读到、没对照任何源端文件，或目标只是静态占位、通用确认弹窗代替
- [收口报告里的 BLOCKER 和验收条目](closing-item-check/index.md)（2 条）：巡检报告列出多个 BLOCKER，或功能规格的 AC 源锚点写着 onEventMainThread / @Subscribe，收口报告只写修了几项、「已清除全部自身占位」，没有逐项的落地或核对记录
- [回执里识别了但没实现的源端行为](unimplemented-behaviors/index.md)（2 条）：写前已读到源端有某项行为（如左右滚动联动、程序滚动保护），子任务回执写「……均保留」，没列出识别到却没实现的行为
- [交付记录里的「已对齐」结论](plan-items-aligned/index.md)（1 条）：实施计划里写了逐面板的对齐条目，实施记录或交付报告写「设置面板已对齐」「改为深色外观并补齐文案」，而计划要求的容器、锚点或步骤在代码里没有落实
