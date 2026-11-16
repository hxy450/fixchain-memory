# data class 用 copy 更新的列表项和模型字段

agent 会看到什么：读到 Kotlin data class 用 copy(...) 替换同 id 的列表项、ViewModel 改模型字段，交回的代码里模型写成 readonly、ForEach 的键只取 id，或用新对象替换元素而行组件 @Param 收整个元素

## 规矩

- rule-91f360ee4711｜源端 ViewModel 会改的字段，ArkTS 模型不写 readonly，写成 @Trace 并去掉「从不修改」注释｜读到：源端 ViewModel 有改这个字段的方法（增减、更新），界面也显示它；模型本身是不可变的 data class；写错：ArkTS 模型类把它写成 readonly、类上没有 @ObservedV2，头注释写「静态 mock」「从不修改」「无有态需求」这类没核实的说法
- rule-a1357f817bd7｜ForEach 只以 id 作 key 且行用 @Param 收整个元素时，行内字段用 @Trace 原位改｜读到：Kotlin data class 列表项用 it.copy(...) 替换同 id 的那一项，Compose 列表按稳定 id 作 key；写错：ArkTS 的更新方法用 .map(...) 生成 new 对象替换同 id 的元素，ForEach 的 keyGenerator 只返回 id，行组件以 @Param 接收整个元素；或改写时删掉了原有的 @ObservedV2 类和 @Trace 字段
- rule-efd07f7e8443｜条目以同 id 新对象替换时，ForEach 键要含会变且要显示的字段，不能只取 id｜读到：源端 Compose 里 forEach { ... } 不设 key 逐项渲染，修改条目用 data class 的 copy(...) 生成新对象、map 出新列表；写错：目标的修改动作用 new X(同 id, 新值) 替换数组元素，而 ForEach(arr, item => Child({ field: item.field }), item => item.id) 的键只取 id
- rule-3fc07c9278bf｜列表行按多个可变字段渲染时，ForEach key 拼入全部会被改写的展示字段｜读到：源端列表行组件按多个可变字段分支渲染（隐藏、锁定、置顶、删除、移除、封禁、已读、计数），列表回调用 copy(...) 改这些字段；写错：ForEach / LazyForEach 的 keyGenerator 只拼 id 和部分字段（投票、收藏、已读等），漏掉行内会被后续操作改写的展示字段
- rule-7aa3cb51fb8a｜源端用 copy / replaceAll 更新列表元素时，目标生成新实例放进新数组再赋回，不原地改字段｜读到：源端 Kotlin 用 toMutableList() 后替换、replaceAll { it.copy(...) }、list[i].copy(...)、it.copy(x = it.x.copy(read = true)) 更新列表元素；写错：目标在下标元素或 forEach / map 回调里直接改字段（arr[idx].x = …、forEach(p => p.x = …)、map(v => { v.x = …; return v })）后只 slice() 返回，DTO 是没有 @ObservedV2 / @Trace 的普通 class；注释还写成与 copy 等价
