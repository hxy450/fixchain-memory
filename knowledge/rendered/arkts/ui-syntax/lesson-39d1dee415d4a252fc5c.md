# stateStyles 各状态只写 @Styles 方法引用、全局 @Styles 函数名或以点号开头的内联样式块，不写 { 属性名: 值 } 对象：后者编译放行、页面渲染即崩；块内属性按源端按压反馈定

## 何时使用

界面实现阶段为容器写按压等状态样式时；编译修复阶段处理 .stateStyles 报 10905203（'.stateStyles' doesn't conform standard）并选择替代写法时

## 适用情境

ArkUI 容器用 .stateStyles({ pressed: … }) 复刻源端列表选择器等按压反馈；d.ts 中 StateStyles 各字段类型为 any，ets-loader 只检查单属性对象字面量的形状，并把该属性的值当作属性调用来绑定；同一 .ets 文件里可能还有其他 struct（如页内弹窗组件）。

## 原因

{ backgroundColor: x } 这类键值对象能通过编译，转换时键名被丢弃，渲染该页即报 undefined is not callable；只看构建结果、不打开页面的编译门发现不了。来源中修复者读了 ets-loader 源码，只看校验器是否放行就选了键值对象。同一应用里，多 struct 文件引用成员 @Styles 报过 10905203，单 struct 文件则正常。

## 做法

1. 各状态值只用三种写法：同组件 @Styles 方法 this.xxx、全局 @Styles function 名，或内联样式块 normal: { .backgroundColor(Color.Transparent) }, pressed: { .backgroundColor(...) }；花括号内应是以点号开头的属性方法调用，不是“名称: 值”。写了 pressed 的 stateStyles 同时写 normal，写回 pressed 所改属性的静止值，@Styles 方法引用同样成对；静止值取这个组件原有的值——原本没有底色才写 Color.Transparent，原本有底色就写原色，不照示例一律写透明。 本条只管写法，不决定块内用哪个属性和取值：按源端按压反馈定，例：View 体系列表选择器画在内容下面时用 backgroundColor 底色（见 lesson-fde79829831c2269e925），不以 opacity 作通用按压样式。
2. 同一文件还有其他 struct、成员 @Styles 引用报 10905203 时，只改报错的那一处，改用内联样式块或全局 @Styles。
3. 引用编译器或转换器源码论证 UI DSL 替代写法时，沿转换逻辑核对最终生成的代码，不只看校验是否放行；这类改动在编译门报告里列为需打开页面验证的项，并写明页面入口。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕.stateStyles 的状态值写成 { backgroundColor: x } 这类“属性名: 值”对象时能通过编译（StateStyles 的各状态字段在声明里是 any 类型），打开该页面渲染时报 TypeError undefined is not callable 崩溃
- 〔做法第 1 步〕文档给出的 stateStyles 状态值写法：内联样式块（pressed: { .backgroundColor(…) }，花括号里是以点号开头的属性方法），或引用组件内的 @Styles 方法（normal: this.normalStyle，不加括号）
