# backgroundModes 只写在 UIAbility 条目上，不写进 extensionAbilities

审的是：资源
触发（任一种）：
- 读到：安卓源前台服务 startForeground(...)，foregroundServiceType 如 dataSync；或注册指引里写着扩展条目带 backgroundModes；写错的样子：module.json5 的 extensionAbilities 条目里写了 "backgroundModes": ["dataTransfer"]
适用范围：在 module.json5 里登记前台服务对应的扩展能力和长时任务类型时
做法：
- extensionAbilities 条目里不写 backgroundModes；需要长时任务时 backgroundModes 写在 abilities[] 的 UIAbility 条目上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- abilities 标签的 backgroundModes：标识当前 UIAbility 组件的长时任务集合，字符串数组，可缺省：backgroundModes 属于 abilities[] 的 UIAbility（出处：module-configuration-file.md，abilities标签）
- extensionAbilities 条目写 backgroundModes 时构建 schema 拒绝，删去后通过：extensionAbilities 的 schema 不接受该字段（出处：卡里修好并验证过）
未核实：卡里环境是 API 22（HarmonyOS 6.0.2）
来源：1 张卡，1 个应用
- case-b92afb07b8ec2465afcf（CleanSweep）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
