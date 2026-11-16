# .stateStyles 的状态值写成「名称: 值」键值对象时，改成点号开头的内联样式块或 @Styles 引用

审的是：代码
触发（任一种）：
- 读到：构建日志报 10905203 '.stateStyles' doesn't conform standard，要给 .stateStyles 换一种写法；写错的样子：写成 `.stateStyles({ pressed: { backgroundColor: $r(…) } })`：状态值的花括号里是「属性名: 值」，不是以点号开头的属性方法调用
适用范围：ArkUI 组件上用 .stateStyles 写按压等状态样式时，编译修复换写法和界面实现都适用
做法：
- 每个状态的值只用三种写法之一：同组件 @Styles 方法 this.<方法名>（不加括号）、全局 @Styles function 的名字、以点号开头的内联样式块 pressed: { .backgroundColor($r(…)) }
- 改完自查：状态值花括号里应是以「.」开头的属性方法调用；看到「名称: 值」的一律改写，不能因为编译通过就放行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stateStyles(value: StateStyles): T：所有组件都有的多态样式接口（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.stateStyles）
- StateStyles 的 normal、pressed、disabled、focused、clicked 字段类型都是 any（selected 是 object）：类型检查不约束状态值怎么写，编译通过不代表运行时可用（出处：鸿蒙 SDK 的 ets/component/common.d.ts，StateStyles.pressed）
- pressed: { .backgroundColor('#ff707070') }：内联样式块：花括号里直接写以点号开头的属性方法（出处：arkts-statestyles.md，基础场景）
- normal: this.normalStyle, pressed: this.pressedStyle：引用组件内 @Styles 方法：this.方法名，不加括号（出处：arkts-statestyles.md，@Styles和stateStyles联合使用）
- 全局 @Styles 要在方法名前加 function，组件内的不加：全局 @Styles 的定义写法（出处：arkts-style.md，装饰器使用说明）
- 单属性对象字面量能过编译校验，但只把属性的值当成属性调用绑定、键名丢掉；{ backgroundColor: $r(…) } 一打开页面就报 TypeError undefined is not callable：键值对象写法的实际后果（出处：卡里修好并验证过）
- 改回 this.<@Styles 方法名> 或改成内联样式块 { .backgroundColor($r(…)) } 后页面能打开、长按不崩：卡里验证过的两种修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-17cc6385b404d180e82e（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2；取值 6 ← 诊断；取值 7 ← 诊断
