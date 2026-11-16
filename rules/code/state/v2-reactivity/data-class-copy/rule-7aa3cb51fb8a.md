# 源端用 copy / replaceAll 更新列表元素时，目标生成新实例放进新数组再赋回，不原地改字段

审的是：代码
触发（任一种）：
- 读到：源端 Kotlin 用 toMutableList() 后替换、replaceAll { it.copy(...) }、list[i].copy(...)、it.copy(x = it.x.copy(read = true)) 更新列表元素；写错的样子：目标在下标元素或 forEach / map 回调里直接改字段（arr[idx].x = …、forEach(p => p.x = …)、map(v => { v.x = …; return v })）后只 slice() 返回，DTO 是没有 @ObservedV2 / @Trace 的普通 class；注释还写成与 copy 等价
适用范围：目标列表经 V2 的 @Trace / @Param 状态渲染、元素 DTO 是未加 @ObservedV2 / @Trace 的普通 class 时的状态更新函数和 VM 局部替换
做法：
- 逐个对照源端 copy：先整体克隆出同类新实例（如 Object.assign(new X(), src)，保留全部运行期字段），再覆写目标字段；嵌套的 copy 对内层对象同样克隆
- 把新实例放进新数组（slice() 后替换该下标，或 map 返回新对象），再整体赋回 @Trace 状态；注释里不把原地修改写成与 copy 等价
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 未被 @Trace 装饰的属性用在 UI 中无法感知到变化，也无法触发 UI 刷新：普通 class 元素原地改字段，界面不刷新（出处：arkts-new-observedV2-and-trace.md，概述）
- 同类新实例 + 新数组赋回 @Trace 状态：修好后隐藏、投票、已读等更新都能刷新列表（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ef3f002672e7158de02c（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；取值 2 ← 诊断
