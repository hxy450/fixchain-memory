# 源解析和搜索流程的每个条件分支逐项迁过来，null 落入的 else 和 isLeft 回退都不能丢

审的是：代码
触发（任一种）：
- 读到：源端 when (x?.type) { "text" -> …; else -> 报错 }，值为 null（如响应缺 Content-Type）时落入 else；写错的样子：目标端写成 `contentType.length > 0 && 不是期望类型` 才报错，空或缺失的值被放行
- 读到：源端 onRight 里 if (result.isLeft()) 换一个地址再抓一次，后续字段取第二次的结果；写错的样子：目标端只按第一次结果赋值一次，没有 isLeft 时的二次抓取和回填
适用范围：把源端解析器、搜索或发现流程（ViewModel、parser）里的条件分支写成 ArkTS 服务时
做法：
- 先把源码每个条件分支列成对照表（含 when 的 else、可空值为 null 时走到的分支、onRight 里的 isLeft 回退），逐项写到 ArkTS；不只保留主路径，也不自己加宽松条件
- 可空值的判断写成「等于期望值才走主路径，其余（含 undefined、空串）都走源端 else 的结果」；isLeft 回退照源端写成第二次请求并用它的结果回填
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 空或缺失 Content-Type 返回不支持类型的错误；首次取元数据失败时按另一地址二次抓取并回填，按源码修正后对应 AC 通过：改法的依据（出处：卡里修好并验证过）
针对本应用要查的：
- 每个分支的条件和结果：源工程 Kotlin 里的 when / if 分支、?. 可空链、Either 的 isLeft / onRight / fold；每个分支记成一行「条件 → 结果」，目标端代码逐行对上；null 走哪一支按 Kotlin 的 when 匹配顺序读出
来源：1 张卡，1 个应用
- case-7d2130916d6ea67581fc（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
