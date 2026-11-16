# 源端在组合期读主题色时，目标在 build() 或 getter 里取色，不写进字段初始化器和 @Param 默认值

审的是：代码
触发（任一种）：
- 读到：Compose 组件在 @Composable 函数体里读主题对象的 colors（经 CompositionLocal 下发），或把主题色写成参数默认值（每次组合求值）；写错的样子：ArkTS 组件写 `private colors = 取色函数()` 这类字段初始化器，或 `@Param colors: ... = 取色函数().某色` 默认值，构造期只取一次
适用范围：组件和页面读取会随深浅切换的主题色时
做法：
- 在 build() 里或 get 访问器（get chipColors() { return 取色函数()... }）里读主题色，不写进字段初始化器
- 颜色类 @Param 的默认值写 undefined，在 getter 里回落到主题色（this.colors ?? 取色函数().某色）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 构造期颜色改为渲染期 getter 后，组件随深浅切换重绘：修复后的形态；构造期快照即使主题状态可观察也不会重绘（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-2c6857febfce92e5d5bc（Jetsnack）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断
