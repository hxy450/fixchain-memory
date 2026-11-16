# 读父组件 this 的 @Builder 传给子组件 @BuilderParam 时，用箭头函数或尾随闭包包住

审的是：代码
触发（任一种）：
- 读到：子组件用 @BuilderParam 接收内容（或尾随闭包报 10905102、子组件有多个 `@BuilderParam`），父组件要传的 @Builder 读 this 上的状态或调父组件的其他成员；写错的样子：构造参数里写成裸方法引用 `contentBuilder: this.someBuilder`；编译通过，运行时 this 指向子组件，报 Cannot read property … of undefined 或栈溢出
- 读到：原在系统容器（如 `Refresh`）尾随闭包里读 `this.` 状态的内容改由自定义组件 `@BuilderParam` 注入，或工程里已有 `content: this.` 直传的先例；写错的样子：把内容抽成成员 `@Builder`，以 `content: this.成员名`（不带括号、不包箭头函数）传入
适用范围：父组件（@Component 或 @ComponentV2）把读本组件 this 的内容交给子组件的 @BuilderParam 时
做法：
- 改成箭头包装 contentBuilder: (): void => { this.someBuilder() }（子组件有多个 @BuilderParam 时显式命名传参）；子组件只有一个无参 @BuilderParam 时也可用尾随闭包 Child({ …其他参数 }) { 原内容 }
- 不把编译通过或 `content: this.` 先例当证据：搜构造参数里「参数名: this.方法名」，逐个确认被传的 @Builder 是否读父组件 this 或与子组件成员同名，是就按上一步改；必要时看编译产物有没有 this.xxx.bind(this)()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- customBuilderParam: this.componentBuilder 时 this 指向子组件；(): void => { this.componentBuilder() } 时 this 指向宿主（父组件）：裸引用会换掉接收者，箭头函数保留父组件接收者（出处：arkts-builderparam.md，初始化@BuilderParam装饰的方法）
- @ComponentV2 组件里同样：裸引用 this 指向子组件，箭头函数 this 指向宿主：V1、V2 组件行为一致（出处：arkts-builderparam.md，在@ComponentV2装饰的自定义组件中使用@BuilderParam）
- 尾随闭包里的内容看作 @Builder 函数传给 @BuilderParam：尾随闭包写在父组件 build 里，内容在父组件上下文构建（出处：arkts-builderparam.md，尾随闭包初始化组件）
- 尾随闭包时子组件有且仅有一个 @BuilderParam 接收它，且该 @BuilderParam 方法不能有参数；这时子组件不支持通用属性：尾随闭包写法的使用条件；有多个 @BuilderParam 时只能用箭头包装的显式命名参数（出处：arkts-builderparam.md，限制条件、尾随闭包初始化组件）
- 改成 contentBuilder: (): void => { this.xxx() } 后渲染正常，不再崩溃：修复只换传参方式，没改子容器的默认 Builder（出处：卡里修好并验证过）
- 直传后运行时 this 指向子组件，读父组件状态的 .length 抛 TypeError；编译和只匹配写法的测试都能通过：这个错只在进入页面时暴露（出处：卡里修好并验证过）
- 方法引用写法编译通过，运行时 RangeError: Stack overflow；改成箭头闭包后进入页面不再崩溃：builder 里的 this.xxx 与子组件成员同名时自调用，修好前后的表现（出处：卡里修好并验证过）
未核实：工程里其他同形的 `content: this.` 直传在运行时是否同样出错
来源：3 张卡，3 个应用
- case-24118d7af444a7062829（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 7 ← 诊断
- case-6781d80f0d751dabef2e（话费流量查询助手）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断
- case-8081ee8b9265d77fd5a8（记得日历）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 6 ← 诊断
