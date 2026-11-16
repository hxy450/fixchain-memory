# 功能规格的哨兵值与 Base 常量不一致时，对外的偏好缺省和列表行 id 在本层投影成规格值

审的是：代码
触发（任一种）：
- 读到：功能规格写明某哨兵的值（如「初值 … = 0」），而读到的 Base 模型层里 `export const` 的同名常量是另一个数；写错的样子：只在本层另定义一个 `const` 哨兵，读偏好时仍经 Base 的 getter 取缺省、列表行对外 id 仍沿用 Base 常量，注释说「只靠类型字段分类」「不影响分支」
适用范围：功能实现阶段，功能规格的哨兵值和已冻结的 Base 常量冲突时
做法：
- 不因分支选择等价就放行：读偏好处直接用规格值作缺省（preferences.get(key, 规格值)），对外的列表行 id 在本层投影成规格值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- get(key: string, defValue: ValueType): Promise<ValueType>：Preferences 读值，键不存在时返回 defValue，对外缺省就由这里决定（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.get）
- getSync(key: string, defValue: ValueType): ValueType：同族接口：Preferences 同步读值（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.getSync）
- 在读取处直接以规格值作偏好缺省，并把对外行 id 投影为规格值：修好后的写法（出处：卡里修好并验证过）
未核实：卡里说修复后效果「仅据代码推断，未重跑」
来源：1 张卡，1 个应用
- case-d566b74cf503495617bb（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
