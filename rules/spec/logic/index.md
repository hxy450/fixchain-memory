# 源码逻辑与数值

读到源码里决定结果的分支、异常、集合遍历、float 运算、常量、格式化、日期时间和线程调用，规格的 AC、映射行或源码笔记要按它写出确切行为时

## 子主题

- [分支、异常与集合](branch/index.md)（12 条）：读到 catch 后返回、提前 return、零分母和钳制保护、HashSet / HashMap 遍历、由不同调用点传入的一组常量、克隆的命名和内容、没捕获的异常退出，规格的 AC 或映射表写这些分支和顺序时
- [线程与调用顺序](concurrency/index.md)（9 条）：读到新开 Thread 后 Handler.post / runOnUiThread、单线程执行器、sleep 重连循环或前后依赖的同步调用，规格里写竞态、异步形态和串行要求时
- [数值、常量与日期时间](numeric/index.md)（16 条）：读到 (float) 强转后 (int) 截断、byte[] 协议常量、DecimalFormat / NumberFormat / String.format、SimpleDateFormat / Calendar、System.nanoTime，规格里写公式、常量表、格式化精度、时区和计时 API 时

## 触发族

- [源端的字符串切分、正则和解码调用](string-parse-semantics/index.md)（3 条）：读到源方法体直接调 String.split / trim、正则、Base64.decode、Uri.parse，或用 split、下标、拼接解析深链和 URL（如 `"?" + x.split("?")[1]`）；规格只写口语描述，或服务层公式、验收条目和示例互相矛盾，把没有分隔符时的结果写成空串
- [源端取设备语言和语言映射的逻辑](device-language-mapping/index.md)（2 条）：读到源端取设备语言后做映射（严格 `=== 'zh'` 才强制映射、取语言的 async 函数没被 await、同步跑 i18n.use(LanguageDetector).init({ lng })），目标系统语言接口返回 zh-Hans-CN 这类 BCP 47 标签；规格把匹配条件放宽到任意 script/region 变体，或照异步分支写初始语言的 AC
- [源码交给依赖库算出的结果（RRULE 序列化、相对时间、URL 解析）](library-defined-output/index.md)（4 条）：读到源码把常量或输入交给依赖库求值：ical4j 的 RRule.toString()、PrettyTime.format()，或靠 java.net.URL、Patterns.WEB_URL 语义的工具函数；规格的 algo-io、映射行或 AC 只登记原始常量、写「自研」「intl 相对时间」或只给标准样例，没写库输出的字面格式和边界样例
