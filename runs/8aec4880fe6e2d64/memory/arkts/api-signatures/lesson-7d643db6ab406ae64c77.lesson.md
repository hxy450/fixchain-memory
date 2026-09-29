# 向子组件 @BuilderParam 传页面自己的 @Builder 时用箭头闭包包装，不传 this.xxx 方法引用

ID：`lesson-7d643db6ab406ae64c77` · 版本：1

[本主题](index.md)

## 何时使用

界面实现或编译修复阶段，把页面 @Builder 内容交给自定义容器组件（Scaffold、Card 一类）的 @BuilderParam，或为消除尾随闭包编译错误改写传参方式时

## 适用情境

目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 调用页面状态或其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。

## 原因

以 content: this.xxx 传入的方法引用在子组件内执行时，this 指向子组件（编译产物为 this.content.bind(this)()）：builder 里的 this.content() 解析成子组件自己的 @BuilderParam，也就是它本身，形成无限递归，运行时 RangeError: Stack overflow。编译照常通过，只在进入该页时崩溃。来源中构建修复者为消除 10905102 新增 scaffoldContent() 调用 this.content()，再以 Scaffold({ content: this.scaffoldContent }) 传入，编译 PASS 后收口，进入个人页即栈溢出。

## 做法

1. 向 @BuilderParam 传页面 builder 时写箭头闭包：Comp({ content: () => { this.pageBody() } })，由闭包保留页面的词法 this；不写 content: this.pageBody。只声明了一个 @BuilderParam 的组件也可用尾随闭包 Comp() { this.pageBody() }。
2. 多 @BuilderParam 组件报 10905102（尾随闭包要求组件只有一个 @BuilderParam）时，改为命名参数加箭头闭包，不改回尾随闭包，也不换成方法引用。
3. 改动了 builder 或 @BuilderParam 接线的页面，编译通过后至少启动并进入一次该页再收口；编译 PASS 排除不了这类递归。

## 可选检查

- 不确定时查编译中间产物：出现 this.xxx.bind(this)()，且该 builder 内部调用了与子组件成员同名的 this.yyy()，即有自调用风险。

## 来源（按需复核）

- case-24118d7af444a7062829 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`669ee707220668081e583be3d334bc16fc6de973f6bf937f0ce051c1d0643264`
