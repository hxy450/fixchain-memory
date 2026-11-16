# 构造 Record<string, Object> 时先建空字典再下标赋值，不写标识符键的对象字面量

审的是：代码
触发（任一种）：
- 读到：工程里已编译的写法和模型模板用 const x: Record<string, Object> = {} 再 x['key'] = v，或 { 'id': this.id as Object } 这种字符串键；写错的样子：写成 const x: Record<string, Object> = { key: value, … }、toJson() 里 return { key: this.key, … }，或把内联的 { x: …, y: … } 当 Object 值嵌进去
适用范围：ArkTS 严格模式下新写模型、toJson 或参数字典，要构造 Record<string, Object> 时
做法：
- 写成 const x: Record<string, Object> = {}; x['key'] = value；嵌套值也先建成有类型的变量（同样空字典加下标赋值）再赋进去
- 确要用字面量时键写成字符串字面量并 as Object：{ 'key': value as Object }
- 同一文件已被改成空字典加下标赋值后，后来新增的代码沿用它，不再写回标识符键字面量
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 标识符键的 Record 字面量编译报 arkts-no-untyped-obj-literals；改成空字典加下标赋值后通过：卡里的报错和修好后的写法（出处：卡里修好并验证过）
- 对象的属性名不能为数字或字符串；例外：支持属性名为字符串字面量和枚举中的字符串值：规则 arkts-identifiers-as-prop-names，用字面量时的键写法依据（出处：typescript-to-arkts-migration-guide.md，对象的属性名必须是合法的标识符）
- 需要显式标注对象字面量的类型，否则编译时错误（错误码 10605038）：规则 arkts-no-untyped-obj-literals（出处：typescript-to-arkts-migration-guide.md，需要显式标注对象字面量的类型）
未核实：卡里的编译报错出自 API 26（target_sdk 26.0.0）工具链；字符串键加 as Object 的字面量写法卡里没有上机验证
来源：1 张卡，1 个应用
- case-5f5a856b7e04d91c8df6（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 5、诊断；取值 1 ← 诊断
