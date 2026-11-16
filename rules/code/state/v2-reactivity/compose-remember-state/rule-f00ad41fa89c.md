# 源端靠引用比较判脏时，V2 里不拿 @Local 数组和另存数组做 ===，改用已替换标志

审的是：代码
触发（任一种）：
- 读到：Compose 里 `remember(x) { mutableStateOf(x) }` 取初值，退出前的未保存判断用 state !== x 引用比较（未改动时两侧是同一对象）；写错的样子：目标新建两个独立数组 `@Local steps = []` 与另存的初始数组，判脏写成 this.steps === this.initial…，新增模式两个 [] 恒不等，编辑模式 @Local 代理与原数组也不等
适用范围：把源端依赖对象身份的未保存判断迁成 ArkUI 状态管理 V2 时
做法：
- 先确认源端未改动时比较两侧是否同一对象；目标改用显式的「已替换」布尔标志：保存、删除、移动、追加等每条修改路径置 true，载入时复位为 false
- 确要比对象时比较 UIUtils.getTarget(this.steps) 与载入时保存的原对象；在新增、编辑两个入口各验证一次「未改动直接返回」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 状态管理 V2 给 @Trace、@Local 装饰的 Date、Map、Set、Array 添加一层代理：@Local 数组与赋给它的原数组 === 不成立（出处：arkts-new-getTarget.md，概述）
- static getTarget<T extends object>(source: T): T（@since 12）：取代理前的原始对象（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，UIUtils.getTarget）
- 改为 stepsReplaced 一类标志（修改路径置位、载入复位）后，未改动离开不再弹「未保存」：卡里的修法（出处：卡里修好并验证过）
未核实：编辑模式「代理 ≠ 原数组」没有在生成态构建上直接运行验证，依据 V2 代理语义和复审结论
来源：1 张卡，1 个应用
- case-36f0b5f441f81e98f6c6（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
