# 派工把 vendor 和 bundleName 并列跳过时，拆开写：vendor 模板值在开发阶段替换

审的是：计划与派工
触发（任一种）：
- 读到：流程或 skill 里写开发身份范围（dev-identity）「不碰 bundleName/vendor——与签名/AGC 强绑定，属部署期决策」；写错的样子：派工说明或跳过清单把 vendor 和 bundleName 一起列为不改、部署期再定，没有单列「vendor 仍是模板值 example 要替换」；或者跳过了却没登记为预期遗留和落地时点，只以「PASS bundleName/vendor preserved」一类自检收尾
适用范围：迁移执行阶段派发应用身份同步任务（app.json5 身份字段）的派工说明、跳过清单和移交登记
做法：
- 派工里把 vendor 单列：仍是模板值 example 时，本次身份同步就替换为非模板值；只有 bundleName 以与签名/AGC 绑定为由保留现值
- 若仍决定跳过 vendor，在迁移报告的遗留登记里写明它是预期遗留、计划在哪个阶段落地，并注明验收门的应用身份检查会因 vendor==example 判阻断；不以「preserved」自检算通过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 验收门的应用身份检查（CHECK-4）有一条「vendor 等于 example 则 FAIL」，列为阻断门控：生成期跳过 vendor 与验证期规则不一致，跳过就会在验收时阻断（出处：卡里修好并验证过）
未核实：派工正文在材料里是加密的，开发身份范围的跳过说法据派发前说明和子代理复述认定
来源：1 张卡，1 个应用
- case-c164fb6e384f47fb7ecf（话费流量查询助手）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；取值 1 ← 诊断
