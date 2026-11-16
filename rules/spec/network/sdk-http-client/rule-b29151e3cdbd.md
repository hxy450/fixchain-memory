# SDK 有自定义异常映射时，规格写明哪类响应转哪种异常、message 取什么值

审的是：规格
触发（任一种）：
- 读到：SDK 的 exception 包和响应校验里按状态码和响应体把响应转成 SDK 自定义异常；应用按异常类型或 message 处理错误；写错的样子：规格的异常契约只写「4xx/5xx + body {error}」「某异常（4xx，带 body 文本）」，没写转换的条件、其余响应转什么、message 取什么值
适用范围：要手写客户端替代三方 HTTP SDK 时，规格里写异常契约的那一节
做法：
- 读 SDK 的异常类和响应校验代码，逐条写：状态码范围 + 响应体条件 → 异常类型；不满足条件的响应抛什么；每种异常的 message 取值（如服务端错误码原文）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 修好后新增响应异常和超时异常两类，message 恢复为错误码原文：异常分类和 message 照 SDK 写，下游按 message 的匹配才能命中（出处：卡里修好并验证过）
针对本应用要查的：
- SDK 的异常转换条件和 message 取值：三方 SDK 源码的 exception 包，以及创建 HttpClient 时的响应校验（HttpResponseValidator / expectSuccess）；读出每种异常在什么状态码、什么响应体下抛出，构造时 message 传的是什么。例：卡里那个 SDK 只在 4xx 且响应体是 JSON 错误信封时转 BadRequest 类异常、message 即错误码原文，其余是 HTTP 库自己的响应异常
未核实：例子里的异常分类条件来自修复期 javap，生成材料里没有原文可复核
来源：1 张卡，1 个应用
- case-65e0c79d46f36cb5abe7（jerboa）：做法第 1 步 ← 建议 2；取值 1 ← 诊断
