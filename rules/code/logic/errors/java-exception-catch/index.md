# Java 异常的捕获和分流

agent 会看到什么：读过的 Java 源码里有 try/catch、按异常类或 getMessage() 分流；交回的代码里 catch 的范围、取消息和按错误分类的写法

## 通用查法

### 源端按异常类或消息分流时，去目标接口 d.ts 的 @throws 读错误码，按 code 写分支

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

## 规矩

- rule-bfd51c760d6c｜Kit API 的 catch 值不按 Error 实例取消息，统一走公共取消息函数｜读到：源端 catch 里用 e.getMessage() / exception.getMessage() 写日志、提示、通知或下载结果详情；写错：目标端 catch 里写 error instanceof Error ? error.message : String(error)，被捕获的是 @ohos.net.http、文件、数据库等 Kit 抛出或 reject 的 BusinessError
- rule-d035bedf8b4f｜网络错误分类先比 BusinessError.code，不复用 Java 异常的英文消息做关键词｜读到：源端按 SocketTimeoutException / UnknownHostException / IllegalArgumentException / IOException 分类，证书失败靠消息 'Trust anchor for certification path not found' 判断；写错：目标端按消息匹配 'timeout'、'Unknown host'、'Failed to parse url'、'malformed'、'Trust anchor…' 等 Java/英文关键词分类，没有先比 code
- rule-03c3dd077335｜移植 try/catch 时保持源端异常作用域和遍历顺序，整个循环一个 try 就首错即停｜读到：源端 for 循环整个包在一个 try { … } catch (IOException e) 里，遍历 AssetManager.list(...) 返回的文件名；写错：目标改成循环体内逐项 try/catch、失败后继续，或不按文件名而按自己排的固定顺序遍历 getRawFileListSync 等取到的列表，注释称单项失败只记日志
- rule-f10de3f52030｜迁移 EXIF 写入的失败和早退语义时只兜源端实际 catch 的异常，没有早退就不加 return｜读到：源 updateExif 声明 throws IOException，只 catch NoClassDefFoundError；setExifFromData 没有早退，源图没有 EXIF 也照常 setExif → modifyExif → removeExifTags；写错：目标 updateExif 用 catch (error) 吞掉全部异常并原样返回，注释称与源兜底同义；setExifFromData 在源图无 EXIF 时 return
- rule-d50744e28486｜SDK 异常 message 是错误码原文时，目标异常类保留原值，状态码放独立字段｜读到：SDK 异常的 message 是服务端错误码原文；下游（如登录错误文案映射）按 exception.message 字符串匹配；写错：目标异常类把 message 拼成 `HTTP ${code}: ${errorText}` 这类字符串，下游的 message 匹配永远不命中
- rule-d093ed6be4cd｜实现兜底/继续类 AC 时，只兜源码 catch 的异常，null 解引用处抛出终止任务｜读到：Java 源码只 `catch (IOException e)` 返回空对象，解析异常（Gson JsonSyntaxException）不在其内；对 `findFile(...)` 等可能为 null 的返回值直接解引用；写错：ArkTS 把 `JSON.parse` 包进 try/catch，失败后 hilog.error 并返回空对象继续；目录不存在时 `return false`，随后照样走后续步骤并发完成通知
