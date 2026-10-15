# 向 @BuilderParam 槽传内容用箭头闭包只调用 @Builder，不传 this.xxx 方法引用、不在闭包里直接实例化组件

ID：`lesson-7d643db6ab406ae64c77` · 版本：6

[本主题](index.md)

## 何时使用

界面实现、收敛改写或编译修复阶段，把页面 @Builder 内容或自定义组件交给自定义容器组件（Scaffold、Card、Surface、下拉刷新一类）的 @BuilderParam，或把原本内联在系统容器尾随闭包里的内容改交给新封装的公共组件，或为消除尾随闭包编译错误改写传参方式时；在组件内为可选 @BuilderParam 声明默认值时

## 适用情境

目标自定义组件声明了一个或多个 @BuilderParam（如 content、topBar），页面要把自己的 @Builder 方法作为内容传入；该 builder 内部用 this 读取页面状态（如列表数据、弹窗变体）或调用其他 builder，名字可能与子组件的 @BuilderParam 相同（如 content）。组件有多个 @BuilderParam 时尾随闭包会报 10905102，需要改成命名参数。仓内可能已有 content: this.XxxBuilder 直传的先例。也包括槽内容本身含自定义组件（共享容器层层嵌套时把中间层组件直接写在 content: () => { Inner({...}) } 里），以及为可选插槽写空默认值时准备用箭头函数。

## 原因

以 content: this.xxx 传入的方法引用在子组件内执行时，this 指向子组件（编译产物为 this.content.bind(this)()）：builder 里的 this.content() 解析成子组件自己的 @BuilderParam，形成无限递归，运行时 RangeError: Stack overflow；builder 读取的页面状态变成子组件上不存在的成员，抛 TypeError；按状态分派的 builder 读不到变体后报 Cannot read property bind of undefined。编译照常通过，只在进入该页时崩溃。在已观察的 ArkUI 工具链中，普通箭头闭包体内直接实例化自定义组件得不到所需的构建转换，运行期报 class constructor cannot called without 'new'；已观察到的情形是多层嵌套时只给最内层抽出 @Builder、漏掉中间层。@BuilderParam 的声明默认值只能由 @Builder 函数或方法初始化，箭头函数默认值编译报 '@BuilderParam' property can only initialized by '@Builder' function。

## 做法

1. 向 @BuilderParam 传页面 builder 时写箭头闭包：Comp({ content: () => { this.pageBody() } })，由闭包保留页面的词法 this；不写 content: this.pageBody。只声明了一个 @BuilderParam 的组件优先用尾随闭包 Comp({...}) { 原内容 }，内联内容迁过来时保持原样放进尾随闭包。
2. 多 @BuilderParam 组件报 10905102（尾随闭包要求组件只有一个 @BuilderParam）时，改为命名参数加箭头闭包，不改回尾随闭包，也不换成方法引用。
3. 仓内已有 content: this.Xxx 写法只说明能编译，不作为运行时正确的依据；边界测试不要把直传方法引用固化为契约，应断言尾随闭包或箭头包装。
4. 槽内容含自定义组件时，把组件树放进本组件的 @Builder 方法，闭包体只写 this.<builder>()；多层共享组件嵌套时逐层各有一个 @Builder 承载，不只给最内层抽取。示意：content: () => { Inner({...}) } 改为 @Builder innerBody() { Inner({...}) } 加 content: () => { this.innerBody() }，方法名仅为示意。
5. 声明侧：可选插槽的默认值写成全局 @Builder function emptySlot() {} 或组件内的 @Builder 方法，再以 @BuilderParam slot: () => void = emptySlot 引用；新增的全局 @Builder 放在组件装饰器之前，不插在装饰器与 struct 之间。声明处默认值不用箭头函数；调用方传内容时仍用箭头闭包包装。

## 可选检查

- 不确定时查编译中间产物：出现 this.xxx.bind(this)()，且该 builder 内部调用了与子组件成员同名的 this.yyy() 或读取页面独有的状态，即有错绑风险。
- 改动了 builder 或 @BuilderParam 接线的页面，编译通过后至少启动并进入一次该页再收口；编译 PASS 排除不了这类 this 错绑。

来源支持：5 张卡 · 5 次迁移 · 4 个应用

## 来源（按需复核）

- [case-09b88fde1629ba4bf4b7](../../../store/cases/case-09b88fde1629ba4bf4b7/c2e159df7726b38ecf7030a66b6f2667420ba0971f55de2d95d7542e07c7168f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c2e159df7726b38ecf7030a66b6f2667420ba0971f55de2d95d7542e07c7168f`
- [case-24118d7af444a7062829](../../../store/cases/case-24118d7af444a7062829/fbf192a9e65930a755e50cbf7ca6668227d6f46275793d4bfa2859c279832928.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fbf192a9e65930a755e50cbf7ca6668227d6f46275793d4bfa2859c279832928`
- [case-6781d80f0d751dabef2e](../../../store/cases/case-6781d80f0d751dabef2e/028227e450d45569fe3c8b9efacbef2e92aee69aa7688829b8eedea1f6d07af6.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`028227e450d45569fe3c8b9efacbef2e92aee69aa7688829b8eedea1f6d07af6`
- [case-8081ee8b9265d77fd5a8](../../../store/cases/case-8081ee8b9265d77fd5a8/b45088a666c525a38b412ae81d73c335245dc4f9969f972d5b772297f6fe3503.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b45088a666c525a38b412ae81d73c335245dc4f9969f972d5b772297f6fe3503`
- [case-d33b282e5bf383e03328](../../../store/cases/case-d33b282e5bf383e03328/1dda694184b7fe969b4168eab455475da924bf8c39cf9e3dcdcb55cc6c09b7d4.json) · 结论：diagnosis, recommendation:2
  卡片版本：`1dda694184b7fe969b4168eab455475da924bf8c39cf9e3dcdcb55cc6c09b7d4`
