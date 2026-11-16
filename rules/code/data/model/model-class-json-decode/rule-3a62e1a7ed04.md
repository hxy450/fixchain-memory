# 源 JSON 把数值存成字符串时，解码边界把数字串转成 number，不用严格 number 解码

审的是：代码
触发（任一种）：
- 读到：源端 assets 下的 JSON 或接口样本里数值字段带引号存成字符串（`"id": "123"` 这种），源模型却声明为 `Int` / `Long`；写错的样子：解码函数按目标字段类型 `number` 选了只接受 JSON number 的严格读法（`typeof v === 'number'` 不成立就抛错），没有把数字字符串转成 number
适用范围：为预置资源（rawfile 里的 JSON）或接口 JSON 写字段解码函数，源样本里的字段类型和目标模型字段类型不一致时
做法：
- 按源样本里字段的实际 JSON 类型选解码方式：是有限 number 直接用；是字符串则 const n = Number(s)，Number.isFinite(n) 时用 n；其余值仍明确报错
- 调用工程里共享的解码工具前先读它的实现：只接受 JSON number 的严格方法，不能用于源样本里是字符串的字段
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 接受有限 number 或能解析为有限数的数字字符串，其余值仍报错：修好的解码边界的取舍：放宽到数字串，但不吞掉坏数据（出处：卡里修好并验证过）
- (value?: any): number：Number(x) 把任意值转成 number，用来解析数字字符串（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，NumberConstructor）
- isFinite(number: unknown): boolean：Number.isFinite 不做强制转换，只有类型为 number 的有限值返回 true；用来判断转换结果（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，NumberConstructor.isFinite）
针对本应用要查的：
- 每个数值字段在源数据里的实际 JSON 类型：源工程 assets 下的 JSON 文件（或接口的响应样本），读完至少一条完整记录；值带引号的是字符串，要在解码边界转换；不带引号的才是 JSON number
- 共享解码工具的某个方法接不接受字符串：目标工程里解码工具的实现文件，按方法名找；看它对非 number 值是转换还是抛错；抛错的就是严格方法
未核实：安卓端怎样把字符串 id 转成 Int 的加载实现卡里没核实
来源：1 张卡，1 个应用
- case-c9f068102d7b9057938e（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
