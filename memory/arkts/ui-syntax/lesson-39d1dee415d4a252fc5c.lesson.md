# stateStyles 各状态只写 @Styles 方法引用、全局 @Styles 函数名或以点号开头的内联样式块，不写 { 属性名: 值 } 对象：后者编译放行、页面渲染即崩；块内属性按源端按压反馈定

ID：`lesson-39d1dee415d4a252fc5c` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段为容器写按压等状态样式时；编译修复阶段处理 .stateStyles 报 10905203（'.stateStyles' doesn't conform standard）并选择替代写法时

## 适用情境

ArkUI 容器用 .stateStyles({ pressed: … }) 复刻源端列表选择器等按压反馈；d.ts 中 StateStyles 各字段类型为 any，ets-loader 只检查单属性对象字面量的形状，并把该属性的值当作属性调用来绑定；同一 .ets 文件里可能还有其他 struct（如页内弹窗组件）。

## 原因

{ backgroundColor: x } 这类键值对象能通过编译，转换时键名被丢弃，渲染该页即报 undefined is not callable；只看构建结果、不打开页面的编译门发现不了。来源中修复者读了 ets-loader 源码，只看校验器是否放行就选了键值对象。同一应用里，多 struct 文件引用成员 @Styles 报过 10905203，单 struct 文件则正常。

## 做法

1. 各状态值只用三种写法：同组件 @Styles 方法 this.xxx、全局 @Styles function 名，或内联样式块 pressed: { .backgroundColor(...) }；花括号内应是以点号开头的属性方法调用，不是“名称: 值”。 本条只管写法，不决定块内用哪个属性和取值：按源端按压反馈定，例：View 体系列表选择器画在内容下面时用 backgroundColor 底色（见 lesson-fde79829831c2269e925），不以 opacity 作通用按压样式。
2. 同一文件还有其他 struct、成员 @Styles 引用报 10905203 时，只改报错的那一处，改用内联样式块或全局 @Styles。
3. 引用编译器或转换器源码论证 UI DSL 替代写法时，沿转换逻辑核对最终生成的代码，不只看校验是否放行；这类改动在编译门报告里列为需打开页面验证的项，并写明页面入口。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-17cc6385b404d180e82e](../../../store/cases/case-17cc6385b404d180e82e/18d819b1147f57d6677c47d87fb6a735925c349d0707de3e3558bc4caea9c6f1.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`18d819b1147f57d6677c47d87fb6a735925c349d0707de3e3558bc4caea9c6f1`
- [case-ecf6bf1e97fdf99c99a3](../../../store/cases/case-ecf6bf1e97fdf99c99a3/d5716cab92a9e3fd4fff5cac88d305c04d6f6ccbf742ced773b9dce8cf253802.json) · 结论：diagnosis, recommendation:6
  卡片版本：`d5716cab92a9e3fd4fff5cac88d305c04d6f6ccbf742ced773b9dce8cf253802`
