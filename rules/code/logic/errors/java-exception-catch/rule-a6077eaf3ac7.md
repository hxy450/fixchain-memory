# 源端按异常类或消息分流时，去目标接口 d.ts 的 @throws 读错误码，按 code 写分支

审的是：代码
触发（任一种）：
- 读到：源端 catch 按异常类（SocketTimeoutException、UnknownHostException、IOException 等）或 e.getMessage() 的内容分流；写错的样子：目标端 catch 按 error.message 里的英文关键词或 instanceof Error 分流，没有先比 (e as BusinessError).code
适用范围：目标端 catch 到 Kit 接口（网络、文件、数据库等）抛出或 reject 的 BusinessError、要按失败种类分流时
做法：
- 在鸿蒙 SDK 的 ets/api 下按 import 的模块名找到被调接口的 d.ts（如 @ohos.net.http.d.ts），读被调方法注释里的 @throws { BusinessError } 码表，每行是一个错误码和英文说明
- 把源端每一类异常对到说明相符的码，写成先比 (e as BusinessError).code 的分支；按消息匹配只作兜底，关键词用码表说明的原文，不用 Java 异常消息
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- export interface BusinessError<T = void> extends Error { code: number; … }：Kit 抛出或 reject 的错误带数字 code，分流按它比（出处：鸿蒙 SDK 的 ets/api/@ohos.base.d.ts，BusinessError）
- HttpRequest.request 的 @throws 有 2300003（URL 格式）、2300006（主机解析失败）、2300028（超时）、2300060 / 2300077（证书）等：例：网络请求的码表；码表随接口而变，别的 Kit 照同样的位置查（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
针对本应用要查的：
- 被调接口会抛哪些错误码、各码的含义：鸿蒙 SDK 的 ets/api 下该 Kit 的 d.ts，在被调方法的注释里找 @throws { BusinessError }；逐行读出码和说明，按说明把源端的异常类别对过去；说明对不上源端哪一类的码，不凭猜测归类
来源：1 张卡，1 个应用
- case-bae545fb004bef3f5772（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
