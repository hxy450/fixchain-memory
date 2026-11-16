# cryptoFramework 的密钥规格串和加解密结果

agent 会看到什么：读到 Java 端 KeyFactory、Cipher.getInstance 的算法串，产物里是 cryptoFramework.createAsyKeyGenerator / createCipher 的规格串，以及 update、doFinal 结果的 .data 取值

## 规矩

- rule-b1406e042ef9｜解析 X.509 RSA 公钥时，createAsyKeyGenerator 只写 'RSA'+位数，不加 |PKCS1｜读到：Java 端 KeyFactory.getInstance("RSA") + X509EncodedKeySpec 解析 BEGIN PUBLIC KEY 公钥，Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding") 加密；写错：写成 createAsyKeyGenerator('RSA1024|PKCS1') 这类：规格串带 |PKCS1 等后缀，或位数和实际公钥不符；真机报 create c generator fail
- rule-ba3bb3bf9a9d｜Cipher 的 update/doFinal 结果先判空再取 .data，改成同步 API 时保留兜底｜读到：Java 端用 Cipher.getInstance("AES/GCM/NoPadding") 加密可能为空的请求体、解密响应；写错：目标端对 cipher.updateSync(...)、cipher.doFinalSync(...) 或 await cipher.doFinal(...) 的结果直接取 .data，没有 ?.data ?? new Uint8Array(0) 这类判空
- rule-c85ca38142d7｜MessageDigest 输入可能为空时，Md 遇空串不调 update，直接返回空串摘要常量｜读到：源码对可能为空的字符串调用 `MessageDigest.digest(value.toByteArray())` 求摘要，或规格允许空字段参与哈希；写错：ArkTS 里无条件 `md.update({ data: bytes })` 后 `md.digest()`，没有处理 bytes 长度为 0 的情况
