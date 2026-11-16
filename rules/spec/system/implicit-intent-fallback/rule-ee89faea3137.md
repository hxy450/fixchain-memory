# 把源 helper 翻成服务契约时，动作和可用性探测要有目标符号承接，不只留分类函数

审的是：规格
触发（任一种）：
- 读到：源 helper 按 scheme 分发：tel → ACTION_DIAL、mailto → ACTION_SENDTO、其他 ACTION_VIEW；可用性检查为真才 startActivity，否则抛异常，页面提示没有应用可处理；写错的样子：服务层契约只定义一个分类函数（返回 'dial' | 'sendto' | 'view' 这类值），动作和可用性探测没有目标符号承接，验收条目只留「无可用 App 提示」
适用范围：规格提取时把源端拉起外部应用的 helper 翻成目标服务层契约
做法：
- 契约里给探测和动作各写目标符号：先用 bundleManager.canOpenLink 探测，再按动作 startAbility（mailto 对应 action 'ohos.want.action.sendToData'）；探测为 false 时返回「无可用应用」，由页面按源端提示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- startAbility({ action: 'ohos.want.action.sendToData', uri: 'mailto:…' })：从应用里拉起邮件应用的写法（出处：start-email-apps-by-mailto.md，从应用拉起）
- canOpenLink(mailto://) 探测 + startAbility{sendToData} 后，标签链接拉起与源端一致：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-29db923e9cadbe8ce53c（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；取值 2 ← 诊断
