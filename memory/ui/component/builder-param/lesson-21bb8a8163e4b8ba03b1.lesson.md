# 给 @BuilderParam 槽传内容时箭头函数体只写 this.<@Builder>()；多层嵌套共享组件逐层抽 @Builder

ID：`lesson-21bb8a8163e4b8ba03b1` · 版本：1

[本主题](index.md)

## 何时使用

界面收敛/实现阶段，把带 @BuilderParam 内容槽的共享容器组件层层嵌套、为每一层槽位写内容时

## 适用情境

目标工程有自带 @BuilderParam content 槽的自定义容器组件（Surface / Card / GradientBorder 等），页面组件要把另一个自定义组件作为槽内容嵌套两层以上；输入里已有这些组件的 @BuilderParam 声明和既有调用范例（content: () => { this.<@Builder>() }）。

## 原因

普通箭头函数体内直接实例化自定义组件不会被编译成 UI-DSL，运行期 this.content() 把 struct 当类调用 → 冷启 jscrash `class constructor cannot called without 'new'`；hvigor 编译、structural-closure 骨架审计、FV 全量编译都不报。W2a 同轮七处写对，唯独两层嵌套处把最内层抽成 @Builder、中间层 GradientBorderComponent({...}) 直接写进 Surface content 的箭头函数体。

## 做法

1. 槽内容里只要出现自定义组件实例化（含第二、第三层嵌套），先抽成本组件的 @Builder 方法再传；每一层 content 都要有自己的 @Builder 承载。
2. 写完后用正则扫描 `<param>: () => {` 闭包体内是否出现 `大写组件名({`，命中即改；把该扫描加进 group-closer / FV 静态门，或至少冷启一次目标页。
3. 维护材料：v2-codegen-patterns.md §@BuilderParam 只写了「默认值必须是 @Builder 方法」和尾随闭包坑，应补「箭头函数体内不得直接实例化自定义组件」反例。

## 检查

- 闭包扫描 0 命中；冷启含该组件的页面无 jscrash（编译通过不能作为证据）。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-09b88fde1629ba4bf4b7](../../../../store/cases/case-09b88fde1629ba4bf4b7/8842ef8c7f0f030f84f7449391df6be3be79ff7bf2750bceba128a30c73bbf03.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`8842ef8c7f0f030f84f7449391df6be3be79ff7bf2750bceba128a30c73bbf03`
