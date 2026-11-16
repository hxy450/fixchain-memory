# 源端 Cipher 加解密工具的空值和失败分支

agent 会看到什么：读到源端用 Cipher.getInstance 的加解密工具（空串前置返回、catch 里返回原文、按构建类型解密响应），产物里是目标 cryptoFramework 加解密封装和请求、响应中间件里对应的分支

## 规矩

- rule-d199c0a5ac28｜迁移 release 响应解密时照源端算法、key/IV 和编码写解码器，release 不透传密文｜读到：源端在 Gson 解析前（如拦截器 beforeResponse 里）对响应做 Base64 解码再 Cipher.getInstance("AES/CBC/PKCS5Padding") 解密，key 与 IV 来自 BuildConfig，debug/release 分支不同；写错：目标没有解码器，或解码器为 null 时把响应原样交给 JSON.parse，release 下密文直接进解析
- rule-08988fca8129｜源端解密失败返回原文时，目标解密失败回退按原文解析，解析也失败才报错｜读到：源端解密工具在 catch (Exception e) 里 printStackTrace 后 return 原文，响应转换器解密后直接交给 Gson TypeAdapter；写错：目标响应中间件在解密的 `catch` 里直接 `throw` 解密错误，不再按原文 JSON.parse
- rule-9b13f207ffe8｜源加密工具对空串直接返回时，目标加密封装开头保留同样的分支，空值不进 Cipher｜读到：安卓 AES 工具首行有前置返回：if (TextUtils.isEmpty(content)) return ""，或 Kotlin 的 if (content.isEmpty() || password.isEmpty()) return ""；写错：目标端加密封装无条件 cryptoFramework.createCipher(...) → init → doFinal({ data: 编码后的 value })，没有空值分支
- rule-e325b124589d｜目标端用 String(value ?? '') 归一化空值时，核对源端 toString() 后进哪个分支｜读到：安卓请求拦截对每个业务值调用加密工具，参数写成 value.toString()；写错：目标端请求中间件写 String(value ?? '') 把 null / undefined 统一成空串再送进加密封装，没核对源端同一个值进的是哪个分支
- rule-f2dbea9845ac｜移植带空值分支的加密工具时，请求组装单测补空值用例，用真实加密封装断言｜读到：安卓加密工具有 TextUtils.isEmpty(content) / content.isEmpty() 的前置返回，业务参数可能为空或缺省；写错：请求组装的单测（describe(...) / it(...) / expect(...).assertEqual(...)）只用假加密器验证字段顺序，没有业务参数为 '' 或缺省时调用真实加密封装的用例
