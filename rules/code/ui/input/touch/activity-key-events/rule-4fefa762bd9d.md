# 要由按键驱动的选择和展开态放进 @ObservedV2/@Trace 模型，不放组件 @Local

审的是：代码
触发（任一种）：
- 读到：源端 onKeyDown 的遥控导航在模型侧逐行逐项改弹层或面板的选择、展开和高亮（行/项下标字段）；写错的样子：面板组件用 `@Local` 保存选中下标和展开态，弹层分组的模型是普通类（没有 @ObservedV2 / @Trace），控件没有高亮入参
适用范围：状态管理 V2 的页面里，弹层、面板的选择和展开要由按键或遥控驱动时
做法：
- 模型类加 @ObservedV2，选择下标、展开态、遥控高亮行/项等字段加 @Trace；去掉组件里的 @Local 副本，组件从模型读这些字段并接收高亮入参
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @ObservedV2 与 @Trace 装饰类和类中属性，使其可深度观测；未加 @Trace 的属性变化不触发 UI 刷新：模型侧改值要让界面刷新的写法（出处：arkts-new-observedV2-and-trace.md，概述；鸿蒙 SDK 的 ets/component/common.d.ts，ObservedV2、Trace）
- @Local 装饰的变量无法从外部初始化，只能在组件内部初始化：@Local 是组件内部的状态，外部不能给它初始化（出处：arkts-new-local.md，概述）
- 分组模型加 @ObservedV2 / @Trace、去掉组件 @Local 下标、展开态移入模型后，遥控能驱动选择：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-cbf23fa7a4ed42d37671（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
