# 路由参数和 @State 集合元素类型用显式类，不写 { id } 和 Array<{…}>

审的是：代码
触发（任一种）：
- 写错的样子：`@State xs: Array<{ id: number; … }>` 这类用对象字面量声明的类型
- 写错的样子：路由跳转直接传 `{ id: item.id }`，或 `id > 0 ? { id: id } : undefined` 当参数
适用范围：目标工程启用 ArkTS 严格检查，界面实现写路由参数、状态字段类型时
做法：
- 声明显式类作元素类型：`class Item { id: number = 0; name: string = ''; }`，状态写 `@State items: Item[] = []`
- 路由参数写成类型化类实例：`const p = new <参数类>(); p.id = item.id;` 再传给跳转方法
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- arkts-no-obj-literals-as-types，级别错误，错误码 10605040：不支持用对象字面量声明类型，要用类或接口（出处：typescript-to-arkts-migration-guide.md，对象字面量不能用于类型声明）
- arkts-no-untyped-obj-literals，错误码 10605038：路由参数 { id } 没有声明类型，同样报错（出处：typescript-to-arkts-migration-guide.md，需要显式标注对象字面量的类型）
- 路由参数改为参数类实例后通过编译并保留：修好后的写法（出处：卡里修好并验证过）
未核实：导航 skill 当时是否已含「路由参数必须是类型化类实例」的规矩，卡里没核到
来源：1 张卡，1 个应用
- case-3f4f88ebb6c941692239（青商城）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
