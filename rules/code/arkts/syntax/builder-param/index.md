# @BuilderParam 插槽的传参和默认值

agent 会看到什么：读到子组件声明的 @BuilderParam 插槽、父组件要传的成员 @Builder 或 10905102 一类编译报错；产物里写成 content: this.someBuilder 方法引用、箭头函数默认值、箭头函数体里直接实例化自定义组件，或测试把直传写法定成契约

## 规矩

- rule-4e954fc0bb3b｜读父组件 this 的 @Builder 传给子组件 @BuilderParam 时，用箭头函数或尾随闭包包住｜读到：子组件用 @BuilderParam 接收内容（或尾随闭包报 10905102、子组件有多个 `@BuilderParam`），父组件要传的 @Builder 读 this 上的状态或调父组件的其他成员；写错：构造参数里写成裸方法引用 `contentBuilder: this.someBuilder`；编译通过，运行时 this 指向子组件，报 Cannot read property … of undefined 或栈溢出
- rule-bc3adcb8718f｜@BuilderParam 换写的测试不把 content: this. 直传定成契约，改断言尾随闭包或箭头包装｜写错：测试里用 grep 一类的断言要求源码必须匹配 `content: this\.` 加成员 `@Builder` 名，把直传写法定成契约
- rule-1be8783080b9｜@BuilderParam 槽的箭头函数体只转调 @Builder，槽里要放自定义组件先抽成 @Builder｜读到：共享容器组件声明 `@BuilderParam content: () => void = this.默认Builder`，已有调用范例写成 `content: () => { this.某个Builder() }`；写错：传给 `@BuilderParam` 的普通箭头函数体里直接实例化了自定义组件（如 `content: () => { 另一个容器组件({ ... }) }`），多层嵌套时只给最内层抽了 `@Builder`
- rule-40a688e6147b｜@BuilderParam 的默认值引用 @Builder 函数或方法，不用箭头函数｜读到：组件要提供可选的内容插槽（挂载点），设计或派工里写了插槽默认为空、用 @BuilderParam 接收；写错：写成 @BuilderParam 插槽名: () => void = (): void => {} 这类箭头函数默认值；编译报 @BuilderParam property can only initialized by @Builder function；或全局 @Builder 插在 @ComponentV2 和 struct 之间
