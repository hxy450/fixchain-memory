# 源加密工具对空串直接返回时，目标加密封装开头保留同样的分支，空值不进 Cipher

审的是：代码
触发（任一种）：
- 读到：安卓 AES 工具首行有前置返回：if (TextUtils.isEmpty(content)) return ""，或 Kotlin 的 if (content.isEmpty() || password.isEmpty()) return ""；写错的样子：目标端加密封装无条件 cryptoFramework.createCipher(...) → init → doFinal({ data: 编码后的 value })，没有空值分支
适用范围：网络层把安卓请求参数加密工具（逐值 AES 等）移植成 ArkTS 加密封装时
做法：
- 逐分支列出源工具的前置返回（空串、密钥长度、异常回退），在目标封装里逐一保留，输出与源端一致
- 空串分支写在封装开头：if (value.length === 0) return ''，不调用 createCipher / doFinal
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 封装开头加 if (value.length === 0) return '' 后，缺值参数的请求能正常发出：修法；修前空值进 Cipher 时在组装阶段抛 byteLength of undefined，请求没发出（出处：卡里修好并验证过）
- TextUtils.isEmpty(@Nullable CharSequence str)：str 为 null 或长度为 0 时返回 true：源端这个分支对 null 和空串都直接返回（出处：android.text.TextUtils#isEmpty）
- doFinal(data: DataBlob | null): Promise<DataBlob>；doFinalSync(data: DataBlob | null): DataBlob：Cipher 结束加密的接口（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，Cipher.doFinal）
- doFinal 的结果可能为 null，用 .data 取数据前要先判断：不加前置分支时，取结果的 .data 可能直接报错（出处：js-apis-cryptoFramework.md，doFinal）
针对本应用要查的：
- 源加密工具有哪些前置返回分支：源工程里加密工具类（如 AES 工具的 .java / .kt）的 encrypt / decrypt 方法开头；把每个 if (…) return … 的条件和返回值逐条列出，目标封装逐条对应
来源：1 张卡，1 个应用
- case-951ecf2aad87b8f0fe96（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断、建议 1；取值 1 ← 诊断
