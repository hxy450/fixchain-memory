# Service 只收不透明请求体时，Repository 照源端构造处逐项写 body，不写 {} 占位

审的是：代码
触发（任一种）：
- 读到：源端 Service 方法参数是 `@Body ... RequestBody`，请求体在调用它的 Repository 方法里组装；目标 Service 方法只收 `data: Object` 原样 POST；写错的样子：Repository 里写成 `const body: Record<string, Object> = {}` 直接传给只收 `data: Object` 的 Service 方法，源端组装的字段一个都没有
适用范围：目标 Service 方法只收不透明请求体（对应源端 @Body RequestBody），而规格没有列出该端点请求字段时，Repository 组装 POST body 的代码
做法：
- 从源端 ViewModel 的调用处追到实际调用的 Repository 方法，找到构造请求体的那一句，把每个键名和取值来源照搬成 `const body: Record<string, Object> = { '<键名>': <取值> }` 再传给 Service 方法
- 每个 POST 端点的 body 字段都要对得上源端构造处的一项；有任一字段来源为空就回源码补齐，不用 `{}` 占位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- body 为空对象时服务端返回 400；照源端构造处补齐字段后请求成功：空 body 不是可以接受的默认值（出处：卡里修好并验证过）
针对本应用要查的：
- 源端请求体的键名和每个值的来源：源工程里带 @Body 参数的 Service 接口方法，顺着 ViewModel 调用的 Repository 方法找到构造 RequestBody 的那一句；逐项读出键名和取值（取自哪个工具方法、偏好项或入参），在目标 Repository 里用同名键、同来源的值写出
来源：1 张卡，1 个应用
- case-2c1f292dab668274366a（polypal-app-ohos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
