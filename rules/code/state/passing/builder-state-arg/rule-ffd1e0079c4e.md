# 会被整体重赋的数组作多参数 @Builder 值参时，改成在 builder 内直接读 this 上的状态

审的是：代码
触发（任一种）：
- 写错的样子：多参数的 `@Builder` 收数组值参并在里面 `ForEach(items)`，调用处传 `this.<状态数组>`，而这个数组之后会被整体重新赋值（如异步查询结果）
- 写错的样子：接线代码先改分支状态切到某个 `if` 分支，再 `await` 查询后整体重赋 `@Local` 数组，而该数组在 build 里是经 `@Builder` 值参消费的
适用范围：ArkTS 页面（含 @ComponentV2 + @Local）用 @Builder 渲染同构列表，且列表数据在分支创建后才被整体重赋时
做法：
- builder 只收一个枚举或 key（如列表种类），在 builder 内按它直接读 this 上对应的状态数组，调用处不再传数组
- 或把这块改成 @ComponentV2 子组件，用 @Param 接入数组（建议里的另一种写法，卡里没验证）
- 把异步结果写回 @Local 前，grep 它在 build 里的全部消费点，确认界面直接读该状态，没有经 @Builder 值参
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 调用 @Builder 默认按值传递，参数是状态变量时，状态变量的改变不会引起 @Builder 内的 UI 刷新：传进去的是调用时刻的快照（出处：arkts-builder.md，按值传递参数）
- 按引用传递只在传入一个参数且该参数直接传入对象字面量时生效，有多个参数时不支持 @Builder 内 UI 刷新：多参数 builder 无论怎么传都不会随状态刷新（出处：arkts-builder.md，参数传递规则）
- @Param 的数据源是状态变量时，数据源的修改会同步给 @Param（由父到子单向同步）：改用子组件 @Param 接入时数组重赋能传下去（出处：arkts-new-param.md，概述）
- builder 改为只接收列表种类、在内部直接读 this 上的各个数组后，搜索结果正常显示：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9ad29d4616c38b46a04d（app_hnaccurateweather_live_android）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 4 ← 诊断
