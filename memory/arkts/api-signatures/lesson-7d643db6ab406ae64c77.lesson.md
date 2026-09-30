# 向子组件 @BuilderParam 传页面自己的 @Builder 时用箭头闭包或尾随闭包，不传 this.xxx 方法引用

ID：`lesson-7d643db6ab406ae64c77` · 版本：2

[本主题](index.md)

## 何时使用

界面实现或编译修复阶段，把页面 @Builder 内容交给自定义容器组件（Scaffold、Card、下拉刷新一类）的 @BuilderParam，或把原本内联在系统容器尾随闭包里的内容改交给新封装的公共组件，或为消除尾随闭包编译错误改写传参方式时

## 适用情境

目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 读取页面状态（如列表数据）或调用其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。仓内可能已有 content: this.XxxBuilder 直传的先例。

## 原因

以 content: this.xxx 传入的方法引用在子组件内执行时，this 指向子组件（编译产物为 this.content.bind(this)()）：builder 里的 this.content() 解析成子组件自己的 @BuilderParam，形成无限递归，运行时 RangeError: Stack overflow；builder 读取的 this.items 等页面状态则变成子组件上不存在的成员，抛 TypeError。编译照常通过，只在进入该页时崩溃。来源中构建修复者以 Scaffold({ content: this.scaffoldContent }) 传入后进入个人页即栈溢出；另一应用把 Refresh 尾随闭包里读 this.items 的内容抽成成员 @Builder，以 content: this.RefreshContent 交给新的下拉刷新组件，写前读到了“方法当值传递会丢失 this”的通用规则与仓内同形先例，自写的 grep 测试还把这种写法定为契约，编译和边界测试都通过，真机进入页面即崩溃。

## 做法

1. 向 @BuilderParam 传页面 builder 时写箭头闭包：Comp({ content: () => { this.pageBody() } })，由闭包保留页面的词法 this；不写 content: this.pageBody。只声明了一个 @BuilderParam 的组件优先用尾随闭包 Comp({...}) { 原内容 }，内联内容迁过来时保持原样放进尾随闭包。
2. 多 @BuilderParam 组件报 10905102（尾随闭包要求组件只有一个 @BuilderParam）时，改为命名参数加箭头闭包，不改回尾随闭包，也不换成方法引用。
3. 仓内已有 content: this.Xxx 写法只说明能编译，不作为运行时正确的依据；边界测试不要把直传方法引用固化为契约，应断言尾随闭包或箭头包装。
4. 改动了 builder 或 @BuilderParam 接线的页面，编译通过后至少启动并进入一次该页再收口；编译 PASS 排除不了这类 this 错绑。

## 可选检查

- 不确定时查编译中间产物：出现 this.xxx.bind(this)()，且该 builder 内部调用了与子组件成员同名的 this.yyy() 或读取页面独有的状态，即有错绑风险。

