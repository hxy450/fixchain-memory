# implementation/arkui/builders

实现 @Builder 与 @BuilderParam 内容槽时进入。

[上一级](../index.md)

## 本级经验

- [每层 @BuilderParam 槽都应由 @Builder 方法承载自定义组件树](lesson-5afc18d10358b3e0e807.lesson.md)
  - 时机：ArkUI 实现或收敛阶段，为带 @BuilderParam 内容槽的自定义容器传入一层或多层嵌套组件时
  - 情境：内容槽以箭头函数传入，闭包体内直接实例化自定义组件；多层共享容器嵌套时，某些层已抽为 @Builder，另一些中间层仍留在普通闭包中。
  - 例外：当前 ArkUI 工具链与运行时明确支持该闭包写法，并已通过目标页面冷启动验证
