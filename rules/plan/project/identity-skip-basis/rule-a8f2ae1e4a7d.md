# 调身份技能的参数不写「不碰 bundleName」，台账已要求替换时按源包名交代

审的是：计划与派工
触发（任一种）：
- 读到：决策台账的技术项要求 bundleName 对齐源包名；执行规范或身份技能的 `scope=dev-identity` 说开发期跳过 bundleName / vendor，并引用一个台账里没有的部署期决策编号；写错的样子：调用身份技能的参数或派工里写着「不碰 bundleName/vendor」「skip bundleName/vendor」，没有提台账技术项和签名决策
适用范围：执行编排的应用身份落地步骤，为身份技能选调用范围、写调用参数时
不适用的情形：工程台账里确有已批准的部署期身份决策、且已有签名配置时，才可以写延后
做法：
- 调用前在台账里查规则所引的部署期决策编号和身份技术项，再看签名决策和 build-profile 的 signingConfigs：编号不存在、签名为 unsigned 或为空、技术项要求替换时，参数里写明「bundleName 写源 Manifest 的 package 值」，不写「不碰 bundleName」
针对本应用要查的：
- 规则所引的部署期身份决策是否存在、是否已有签名配置：决策台账按 D- 编号找；目标工程 build-profile.json5 的 signingConfigs；台账里的签名决策；查不到编号或签名为空，就以台账技术项为准
来源：1 张卡，1 个应用
- case-e6f851fe0dda3d49dc04（Blockinger）：做法第 1 步 ← 建议 1；例外 1 ← 建议 3
