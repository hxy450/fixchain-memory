# 需授权的仓库方法里，无上下文、未授权、枚举失败都走声明的抛错通道，不静默 return []

审的是：代码
触发（任一种）：
- 读到：源端 ViewModel 在 catch 里置加载失败错误（失败经异常从仓库传到 VM）；规格要求扫描失败或权限拒绝时显示错误提示，空列表另显示空态引导；写错的样子：仓库方法注释写「权限拒绝时 throw」，却在权限检查前写 if (this.context === null) { return []; }，随后还用空结果 replaceAll 覆盖缓存
适用范围：依赖 UIAbilityContext 和运行时权限（如 ohos.permission.READ_IMAGEVIDEO）的数据仓库方法，写前置失败分支时
做法：
- 「上下文未初始化」「权限未授予」「枚举失败」统一走与注释和规格一致的失败通道：throw new Error(...)（或显式的错误结果），不在权限检查前加 return [] 兜底
- 逐一检查每个早退分支：返回空集合只用于确实没有数据；失败态不写入、不覆盖缓存
- 对照同类私有方法的映射（如权限检查已把 context 为 null 视为未授权），同一状态在各分支映射成同一结果
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- checkAccessTokenSync(tokenID: number, permissionName: Permissions): GrantStatus：AtManager 同步校验权限；结果不是 PERMISSION_GRANTED 时走失败通道（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.checkAccessTokenSync）
- GrantStatus.PERMISSION_DENIED = -1、PERMISSION_GRANTED = 0：权限校验结果（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，GrantStatus）
- 无上下文分支改为 throw new Error(...) 并核对调用点有 try-catch 后，权限拒绝能被调用方提示：修法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK API 22（6.0.2），本机核实用 API 23
来源：1 张卡，1 个应用
- case-57f20aa343aa460f1661（CleanSweep）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 3 ← 诊断
