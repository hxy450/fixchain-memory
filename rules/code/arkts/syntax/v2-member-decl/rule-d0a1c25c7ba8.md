# V2 组件里 @Event、@Local、@Param 等裸写，不带括号；只有工厂装饰器带括号

审的是：代码
触发（任一种）：
- 读到：派工或规格写「装饰器锁 V2（@ComponentV2 / @Local / @Param / @Event / …）」，组件要向宿主暴露交互回调；写错的样子：@ComponentV2 组件里写出 @Event()、@Local()、@Param() 这类带空括号的成员装饰器；编译报 Expected 2 arguments, but got 0
适用范围：在 @ComponentV2 自定义组件里声明 @Event 回调和 @Local / @Param / @Once / @Trace 成员时
做法：
- @Local / @Param / @Once / @Event / @Trace 裸写（如 @Event onToggle: () => void = () => {}）；只有 @Provider() / @Consumer()、@Monitor('…') 这类工厂装饰器带括号
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare const Event: PropertyDecorator;：@Event 本身就是属性装饰器，加括号等于把它当函数调用（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Event）
- declare const Local: PropertyDecorator; declare const Param: PropertyDecorator;：@Local、@Param 同样裸写（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Local、Param）
- declare const Provider: (aliasName?: string) => PropertyDecorator;：@Provider 是工厂，要写 @Provider()；@Consumer 同形（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Provider、Consumer）
- declare type MonitorDecorator = (value: string, ...args: string[]) => MethodDecorator;：@Monitor 要带被监听的路径，写 @Monitor('…')（出处：鸿蒙 SDK 的 ets/component/common.d.ts，MonitorDecorator）
未核实：卡里记的鸿蒙 SDK 是 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-d33b282e5bf383e03328（AntennaPod）：做法第 1 步 ← 建议 1、诊断
