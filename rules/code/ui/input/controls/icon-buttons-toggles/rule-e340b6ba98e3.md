# 会变的开关状态不作成员 @Builder 的值参，每个开关行直接绑定自己的状态

审的是：代码
触发（任一种）：
- 读到：源端多个开关各自持有状态字段，各自的 setOnClickListener 只翻转自身字段、写对应偏好并 setImageResource 刷新自身图标；写错的样子：几个开关行共用一个成员 `@Builder`，把随 @Local / @Trace 变化的开关状态（boolean）作为值参传入，在 Builder 里据此画图标或再传给子组件的 @Param
适用范围：ArkUI 页面（@ComponentV2 / @Local 持有开关状态）把多个独立开关行抽成共享 @Builder 或接入复用开关组件时
做法：
- 每个开关各写一个开关行，在 build() 里把它的状态参数直接写成这个开关自己的 @Local 成员，不经成员 @Builder 的值参转一手
- 要复用行模板时，把开关行抽成 @ComponentV2 子组件，用 @Param 接收状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 调用 @Builder 装饰的函数默认按值传递；参数是状态变量时，它的改变不会引起 @Builder 函数内的 UI 刷新：值参只是调用时刻的快照（出处：arkts-builder.md，按值传递参数）
- 两个或两个以上参数时，即使用对象字面量传，值的改变也不会触发 UI 刷新：多参数的共享 Builder（标题、说明、状态、回调）无论怎么传状态都不刷新（出处：arkts-builder.md，@Builder存在两个或两个以上参数）
- @ComponentV2 组件里用简单数据类型按值传给 @Builder 不可以触发 UI 刷新：boolean 开关状态属于简单类型（出处：arkts-builder.md，使用@ComponentV2装饰器触发动态刷新）
- @Param 装饰的变量类型为 boolean、string、number 时，可观察数据源同步变化：子组件用 @Param 接 @Local 的 boolean，父侧改值会同步进来（出处：arkts-new-param.md，观察变化）
- 拆成两个独立开关行、状态参数直接绑定各自的 @Local 后，两开关互不干扰并能跨重启保持：修好的做法（出处：卡里修好并验证过）
未核实：第二轮复测里串线的确切运行时路径（值参快照、组件更新还是回调绑定）卡里没有复现
来源：1 张卡，1 个应用
- case-ab54d746c8c33d3061ed（骑行记录）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
