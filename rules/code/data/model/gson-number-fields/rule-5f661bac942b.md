# 响应里有 64 位整数字段时不用裸 JSON.parse，换保精度解析，请求体配 bigint 的 replacer

审的是：代码
触发（任一种）：
- 读到：响应模型里有 Long 字段（val id: Long、userId: Long）；写错的样子：HTTP 层统一写 JSON.parse(body) as BaseResponse<T>，请求体 JSON.stringify(data)，没有 bigint 处理
适用范围：网络层解析响应、序列化请求体，且其中有服务器生成的 64 位整数字段时
做法：
- 解析前把这些 64 位整数加引号，再 JSON.parse(text, reviver)，reviver 里把它们转成 BigInt(值)
- 请求体用 JSON.stringify(data, replacer)，replacer 里 typeof v === 'bigint' 时返回 v.toString()
- 最小检查：解析一个含 19 位整数 id 的 JSON 后，id.toString() 原样返回这 19 位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- JSON.parse 前给 64 位整数加引号、reviver 转 BigInt，请求用 bigint 的 replacer：修复后响应里的 19 位 id 原样保留（出处：卡里修好并验证过）
- type Transformer = (this: Object, key: string, value: Object) => Object | undefined | null：reviver / replacer 函数的形状：按键名和值返回替换后的值（出处：鸿蒙 SDK 的 ets/api/@ohos.util.json.d.ts，json.Transformer）
未核实：卡里上机的目标 SDK 是 6.0.2(22)，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-c179cd94000a4fea75a5（polypal-app-ohos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 1 ← 诊断
