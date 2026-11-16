# 迁移 release 响应解密时照源端算法、key/IV 和编码写解码器，release 不透传密文

审的是：代码
触发（任一种）：
- 读到：源端在 Gson 解析前（如拦截器 beforeResponse 里）对响应做 Base64 解码再 Cipher.getInstance("AES/CBC/PKCS5Padding") 解密，key 与 IV 来自 BuildConfig，debug/release 分支不同；写错的样子：目标没有解码器，或解码器为 null 时把响应原样交给 JSON.parse，release 下密文直接进解析
适用范围：迁移源端对网络响应的解密（AES/CBC 加 Base64）时
做法：
- util.Base64Helper 的 decodeSync 解 Base64 → createSymKeyGenerator('AES128') 用 key 字节 convertKey → createCipher('AES128|CBC|PKCS5') → init(cryptoFramework.CryptoMode.DECRYPT_MODE, key, { algName: 'IvParamsSpec', iv: { data: <IV 字节> } }) → doFinal；密钥位数照源端 key 长度，debug/release 分支照源端
- 用合成向量测试解码器（已知明文按源端算法加密后再解回）；release 下解码器缺失不能默认透传
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- createCipher(transformation: string): Cipher；CBC 支持 [128|192|256] 位密钥和 NoPadding、PKCS5、PKCS7 填充：按「算法+位数|模式|填充」拼字符串，如 'AES128|CBC|PKCS5'（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，cryptoFramework.createCipher；crypto-sym-encrypt-decrypt-spec.md，AES）
- 算法库里 PKCS5 和 PKCS7 都按分组大小填充，AES 填充至 16 字节：源端 PKCS5Padding 用 PKCS5 或 PKCS7 结果相同（出处：crypto-sym-encrypt-decrypt-spec.md，AES）
- IvParamsSpec 的 iv：AES 的 CBC、CTR、OFB、CFB 模式是 16 字节：源端 key 兼作 IV 时，IV 取同样的 16 字节（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，IvParamsSpec.iv）
- init(opMode: CryptoMode, key: Key, params: ParamsSpec | null): Promise<void>；DECRYPT_MODE = 1；doFinal(data: DataBlob | null): Promise<DataBlob>：解密的初始化和收尾（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，Cipher.init、CryptoMode.DECRYPT_MODE、Cipher.doFinal）
- convertKey(key: DataBlob): Promise<SymKey>：把 key 字节转成对称密钥（出处：鸿蒙 SDK 的 ets/api/@ohos.security.cryptoFramework.d.ts，SymKeyGenerator.convertKey）
- decodeSync(src: Uint8Array | string, options?: Type): Uint8Array：Base64 解码（出处：鸿蒙 SDK 的 ets/api/@ohos.util.d.ts，Base64Helper.decodeSync）
针对本应用要查的：
- 解密的 key、IV、编码和分支：源端解密工具类里 SecretKeySpec、IvParameterSpec 的构造参数和 Cipher.getInstance 的字符串，以及模块级 Gradle 构建脚本 buildTypes 里 AES_KEY 等 buildConfigField；照抄算法串和 key/IV 的来源（是否 key 兼作 IV、字符编码），只在源端解密的那个分支里解密
未核实：卡里修复后对合法 JSON 的响应透传（服务端也会回明文），release 下哪些响应加密要看源端分支
来源：1 张卡，1 个应用
- case-613cce143fdc193142d7（骑行记录）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
