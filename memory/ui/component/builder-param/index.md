# ui/component/builder-param

@BuilderParam 槽内容承载

[上一级](../index.md)

## 本级经验

- [给 @BuilderParam 槽传内容时箭头函数体只写 this.&lt;@Builder&gt;()；多层嵌套共享组件逐层抽 @Builder](lesson-21bb8a8163e4b8ba03b1.lesson.md)
  - 时机：界面收敛/实现阶段，把带 @BuilderParam 内容槽的共享容器组件层层嵌套、为每一层槽位写内容时
  - 情境：目标工程有自带 @BuilderParam content 槽的自定义容器组件（Surface / Card / GradientBorder 等），页面组件要把另一个自定义组件作为槽内容嵌套两层以上；输入里已有这些组件的 @BuilderParam 声明和既有调用范例（content: () =&gt; { this.&lt;@Builder&gt;() }）。
