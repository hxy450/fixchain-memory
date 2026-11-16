# Cipher 的 update/doFinal 结果先判空再取 .data，改成同步 API 时保留兜底

审的是：代码
触发（任一种）：
- 读到：Java 端用 Cipher.getInstance("AES/GCM/NoPadding") 加密可能为空的请求体、解密响应；写错的样子：目标端对 cipher.updateSync(...)、cipher.doFinalSync(...) 或 await cipher.doFinal(...) 的结果直接取 .data，没有 ?.data ?? new Uint8Array(0) 这类判空
- 读到：为修 Promise / DataBlob 类型的编译错误，把异步 update / doFinal 改写成 updateSync / doFinalSync；写错的样子：改写后把原来的 ?.data ?? 兜底删掉，直接写 result.data
适用范围：ArkTS cryptoFramework 的 Cipher 做对称加解密（GCM 等模式）时，取 update/updateSync、doFinal/doFinalSync 的返回值
做法：
- 每次取结果都判空：const out = cipher.updateSync(input); const part = out ? out.data : new Uint8Array(0)；doFinalSync(...)、await doFinal(...) 同样写，再按顺序把各段拼起来
- 从异步改写成同步 API 时原有的空值兜底原样保留；声明里返回类型写的是非空 DataBlob，不能据此删掉判空
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- updateSync(data: DataBlob): DataBlob：Cipher 的同步分段加解密，声明上返回非空 DataBlob（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，Cipher.updateSync）
- doFinalSync(data: DataBlob | null): DataBlob：Cipher 的同步收尾加解密，声明上返回非空 DataBlob（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，Cipher.doFinalSync）
- doFinal(data: DataBlob | null): Promise<DataBlob>：同族接口：Cipher 的异步收尾，结果同样要判空（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，Cipher.doFinal）
- doFinal 的结果可能为 null，用 .data 前先判空；解密时 GCM、CCM、CFB、OFB、CTR 模式 doFinal 传 null 返回 null：文档写明的可空情形，doFinalSync 的注意事项同 doFinal（出处：js-apis-cryptoFramework.md，Cipher / doFinal 的说明）
- update 没凑满一个新分组时此次输出为 null：update/updateSync 的结果也可能为 null（出处：js-apis-cryptoFramework.md，Cipher / update 的说明）
- 删掉兜底后真机在空请求体加密和响应解密两处读到 null 的 data；补回判空后加解密正常：GCM 空明文加密、GCM 解密收尾都会出现 null 结果（出处：卡里修好并验证过）
未核实：文档写 doFinalSync 的 data 在对称加解密中允许为 null、但不允许传 {data: 空 Uint8Array}；空请求体时该传什么，卡里没写
来源：1 张卡，1 个应用
- case-c5fdc6640404c3d6440e（android-train-ticket-vest7）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 6 ← 诊断
