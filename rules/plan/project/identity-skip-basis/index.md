# 援引部署期决策跳过 bundleName / vendor

agent 会看到什么：skill、执行规范或派工写「scope=dev-identity，不碰 bundleName/vendor，属部署期决策（D-…）」，派工、跳过清单或报告沿用这个说法和编号作依据，而决策台账里没有这个编号、讲的是别的事，或台账技术项要求对齐源包名

## 规矩

- rule-1d7c9bcc927c｜以 D-编号作跳过依据前，核对本项目台账里该编号确实覆盖此项，不符就记决策缺口｜读到：skill 或派工以决策台账编号（D- 加数字）作为跳过某个字段的依据，如「属部署期决策（对应 D-…）」「部署期再以 scope=full 落地」；写错：跳过清单、派工、worker 信封或迁移报告的遗留披露沿用这个编号作理由，而本项目决策台账里该编号不存在或讲的是别的事，且没有登记决策缺口
- rule-bf5268c2a0b6｜派工把 bundleName/vendor 划出身份迁移时，先核对台账依据，暂缓须登记例外｜读到：执行规范写「`scope=dev-identity`，不碰 bundleName/vendor，保留脚手架占位，部署期再以 `scope=full` 落地」，理由引了一个决策号；写错：派工照抄「不碰 bundleName/vendor」，而本项目决策台账里那个编号并不是推迟包名的决策，台账里也没有登记暂缓和复检条件
- rule-a3db4c7a72d4｜派工前把台账技术必做项逐条映射到任务，skill 默认与之冲突时按台账或写决策缺口｜读到：决策台账的技术必做项（T-xxx）要求改某些字段（如 bundleName 改为安卓 applicationId），执行 skill 的默认步骤却跳过这些字段（如 dev-identity 不碰 bundleName / vendor）；写错：派工只派 T 项里的部分字段，写「不碰 bundleName / vendor（部署期字段，保留脚手架值）」，没有引用这条 T 项，也没有安排后续任务或决策缺口；回报把这条 T 项记成 PASS
- rule-a8f2ae1e4a7d｜调身份技能的参数不写「不碰 bundleName」，台账已要求替换时按源包名交代｜读到：决策台账的技术项要求 bundleName 对齐源包名；执行规范或身份技能的 `scope=dev-identity` 说开发期跳过 bundleName / vendor，并引用一个台账里没有的部署期决策编号；写错：调用身份技能的参数或派工里写着「不碰 bundleName/vendor」「skip bundleName/vendor」，没有提台账技术项和签名决策
- rule-bc5fc9c5e420｜派工把 vendor 和 bundleName 并列跳过时，拆开写：vendor 模板值在开发阶段替换｜读到：流程或 skill 里写开发身份范围（dev-identity）「不碰 bundleName/vendor——与签名/AGC 强绑定，属部署期决策」；写错：派工说明或跳过清单把 vendor 和 bundleName 一起列为不改、部署期再定，没有单列「vendor 仍是模板值 example 要替换」；或者跳过了却没登记为预期遗留和落地时点，只以「PASS bundleName/vendor preserved」一类自检收尾
- rule-58dba6c45d70｜延后某个身份字段时，核对决策台账确有条目，并在报告里列出保留的模板值和理由｜读到：技能或派工以「与签名 / AGC 绑定，属部署期决策」并带一个决策编号为由要求保留 vendor、bundleName 的脚手架值；写错：迁移报告或占位登记里没有列出保留的模板值及理由，引用的决策编号在本工程决策台账里不存在或内容不符
- rule-e0a5358e05cd｜身份技术项没落实时，阶段报告和终报把它标为未完成，不以「身份已落地」收口｜读到：决策台账里有身份相关的技术项（bundleName、vendor 对齐源端）；写错：阶段报告或终报只写「App 身份已落地」，而 app.json5 的 bundleName 仍是 com.example.* 或 vendor 未改，没有把该技术项登记为未完成
