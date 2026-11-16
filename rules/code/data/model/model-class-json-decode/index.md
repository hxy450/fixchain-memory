# 从 Kotlin data class 迁来的模型类和 JSON 解码

agent 会看到什么：读到 Kotlin data class 模型（Int / Long / Boolean / String 字段）、kapt stub、assets 下的 JSON 样本；产物里模型 class 的字段、fromJson 的取值写法和它的注释

## 通用查法

### 写模型类和 fromJson 时，字段取自源 .kt 的 data class 定义，解码按样本里的实际 JSON 类型

审的是：代码
触发（任一种）：
- 读到：源端模型是 Kotlin `data class`（字段 Int / Long / Boolean / String），数据来自 assets 下的 JSON 或接口响应；写错的样子：目标模型 `class` 的字段或 fromJson 取值是推测的：照搬同文件另一个类的字段、`(json['k'] as number) ?? 0`、只收 JSON number 的严格读法
适用范围：把源端数据模型和它的 JSON 解码迁成 ArkTS 模型类时
做法：
- 按类名在所属 .kt 源文件里找 `class <类名>(…)` 的定义，读出构造参数的名字和类型；一个 Kotlin 文件可有多个类，不只读 kapt 生成的同名 stub
- 到源工程 assets 下的 JSON 或接口响应样本读至少一条完整记录，记下每个字段的实际 JSON 类型（值带引号的是字符串）
- fromJson 按实际类型先 typeof / instanceof 判断再赋值，数字串用 Number(s) 转、Number.isFinite 判断，`??` 只兜缺失和 null；没读到定义就在汇报里列为未核实
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (value?: any): number：Number(x) 把任意值转成 number，用来解析数字字符串（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，NumberConstructor）
- isFinite(number: unknown): boolean：Number.isFinite 不做强制转换，只有类型为 number 的有限值返回 true；用来判断转换结果（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，NumberConstructor.isFinite）
- typeof 只能用在表达式里，不能用作类型（规则 arkts-no-type-query）：`typeof x === 'number'` 这种判断在 ArkTS 里合法（出处：typescript-to-arkts-migration-guide.md，仅允许在表达式中使用typeof运算符）
针对本应用要查的：
- Model 类的真实字段：源工程里按类名全文搜 `class <类名>`，常和同模块的其他 Model、类型常量写在同一个 .kt 里；读出构造参数的名字、类型和默认值，以及同文件里配套的常量对象，原样写到目标 Model
- 每个字段在源数据里的实际 JSON 类型：源工程 assets 下的 JSON 文件（或接口的响应样本），读完至少一条完整记录；值带引号的是字符串，要在解码边界转换；不带引号的才是 JSON number
- 共享解码工具的某个方法接不接受字符串：目标工程里解码工具的实现文件，按方法名找；看它对非 number 值是转换还是抛错；抛错的就是严格方法，不能用于样本里是字符串的字段
未核实：安卓端怎样把字符串 id 转成 Int 的加载实现，族里规矩没有核实；as 转换类型不符时，卡里观察到值原样进入字段，文档写会抛 ClassCastException，未上机复核
来源：3 张卡，3 个应用
- case-b98aad1336d85a238cd7（polypal-app-ohos）：做法第 1 步 ← 建议 4；做法第 3 步 ← 建议 4
- case-c9f068102d7b9057938e（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 1
- case-d039f1148c72f9d6e2ad（CleanSweep）：做法第 3 步 ← 建议 1

## 规矩

- rule-08b1200864fa｜派工要求读源码确认 Model 字段时，到所属 .kt 源里找类定义，没读到就报未核实｜读到：所属的 .kt 源文件里同时定义了多个 `data class`，而只读了 kapt 生成的同名 stub；写错：目标 Model 的 `class` 字段照搬了同文件另一个类的字段，注释写「占位，字段由 Feature Spec 补充」，汇报却说字段已从源码核实
- rule-96e3749f2588｜fromJson 取值写成 (x as T) ?? 默认时，改成先 typeof / instanceof 判断再赋值｜读到：源模型是 Kotlin data class，字段为 Int / Long / Boolean / String 等强类型，运行期类型由语言保证；写错：目标模型的 fromJson(json: Record<string, Object>) 里字段写成 `(json['k'] as number) ?? 0`、`(json['k'] as boolean) ?? false` 这类，只靠 as 加 ?? 取值
- rule-3a62e1a7ed04｜源 JSON 把数值存成字符串时，解码边界把数字串转成 number，不用严格 number 解码｜读到：源端 assets 下的 JSON 或接口样本里数值字段带引号存成字符串（`"id": "123"` 这种），源模型却声明为 `Int` / `Long`；写错：解码函数按目标字段类型 `number` 选了只接受 JSON number 的严格读法（`typeof v === 'number'` 不成立就抛错），没有把数字字符串转成 number
- rule-d6ac11c504e0｜源端没有序列化代码而自行补 fromJson 时，注释写明缺字段、null、类型不符三种输入的结果｜读到：源模型 Kotlin data class 文件里没有任何序列化代码（没有 fromJson / toJson）；写错：目标模型里新补的 fromJson 没有注释（或交回说明里没有）写明缺字段、值为 null、类型不符三种输入各自得到什么
