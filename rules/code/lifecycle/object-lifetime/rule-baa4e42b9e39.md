# 源端按 getLast…NonConfigurationInstance 判空分支时，目标按配置重建标志分支

审的是：代码
触发（任一种）：
- 读到：Activity.onCreate 里 getLastCustomNonConfigurationInstance() / getLastNonConfigurationInstance() 为 null 才按 Intent 启动参数分支；写错的样子：目标代码写成 if (!…hasInstance()) {按启动参数分支} else {复用单例}，或用全局状态是否存在决定是否忽略启动参数，注释写「续存优先：参数忽略」
适用范围：源 Activity 没有用 android:configChanges 接管配置变化，迁成 ArkTS 页面时进入页面、组装状态的那段代码
做法：
- 给组装状态的入口加一个「是否由配置变化重建」的布尔参数，只有 onConfigurationUpdate 触发、按源端重建时序重新组装的路径传 true，正常进入传 false；判定写成 if (!<是否配置变化重建> || !hasInstance()) 才按启动参数分支，否则复用当前对象
- 规格把源条件换成了别的目标条件（如 getLast… 非空 → hasInstance）时，把入口×前置状态表分别代入源条件和目标条件，任一组合结果不同就按源语义实现，并在 source-notes 里标注与规格的差异
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onConfigurationUpdate(newConfig: Configuration): void：Ability 的配置变化回调，UIAbility 继承它；这里是唯一应传「配置变化重建」为 true 的路径（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Ability.d.ts，Ability.onConfigurationUpdate）
- onConfigurationUpdate(newConfig: Configuration): void：同族接口：AbilityStage 的全局配置变化回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityStage.d.ts，AbilityStage.onConfigurationUpdate）
- Activity#getLastNonConfigurationInstance 返回 onRetainNonConfigurationInstance() 的对象，只在配置变化重建后的新实例里非空：源条件「取回为空」等价于「本次不是配置变化重建」，不等价于「单例不存在」（出处：android.app.Activity#getLastNonConfigurationInstance）
- 正常进入一律按启动参数分支，只在 onConfigurationUpdate 重建路径且已有对象时复用：返修后的判定（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6e71bead39034fb1d84f（Blockinger）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 3；取值 4 ← 诊断
