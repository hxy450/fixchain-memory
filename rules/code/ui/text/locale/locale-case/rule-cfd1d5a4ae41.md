# 源端判定函数内部先 lowercase 再比对时，目标的名称谓词也在内部先 toLowerCase

审的是：代码
触发（任一种）：
- 读到：源端判定函数内部先对名称做 lowercase(Locale.ROOT)（或 toLowerCase(Locale.ROOT)），再和小写字面量或集合比较；写错的样子：目标改写出的名称谓词内部直接用 === 或 Set.has 比较小写字面量，大小写归一只放在调用方的 name.toLowerCase() 里
适用范围：把源端的判定函数改写成按名称或字符串匹配的谓词函数，而源端在判定函数内部做了大小写、空白等归一时
做法：
- 谓词内部先归一再比较：const n = name.toLowerCase()，之后拿 n 和字面量或集合比；调用方已有的归一可以保留，重复归一结果不变
- 单测里用混合大小写的样例名直接调用每个谓词，结果要与源端 lowercase(Locale.ROOT) 后再判定一致，不只测经调用方归一后的路径
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- toLowerCase(): string：不看区域的小写转换，对应源端 Locale.ROOT 的语义（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，String.toLowerCase）
- toLocaleLowerCase(locales?: string | string[]): string：按宿主当前区域转换，不对应 Locale.ROOT，不用它代替（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，String.toLocaleLowerCase）
- Locale.ROOT：语言、国家都为空的基础区域，用作区域敏感操作的中性区域：源端 lowercase(Locale.ROOT) 是与区域无关的小写（出处：java.util.Locale#ROOT；java.lang.String#toLowerCase(Locale)）
- 谓词内部先 toLowerCase 后，直接传混合大小写名的单测由失败变为通过：返修后的写法（出处：卡里修好并验证过）
未核实：卡里的单测结果出自 HarmonyOS 6.0.2（API 22）环境
来源：1 张卡，1 个应用
- case-91a128fa3eca526ab6bb（CleanSweep）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
