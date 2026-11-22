# Java/ICU 正则、String/List 方法与 Android 工具类不按形似 JS 内建改写：先列语义差异，不等价就按源实现移植

## 何时使用

服务层、模型层与页面逻辑实现阶段，把源码直接调用的 Java 正则、String/List 方法或 Android 平台工具类翻译成 ArkTS 表达式时；规格提取阶段为这些调用写契约时

## 适用情境

源方法体调用的是平台库而不是应用自身代码：Pattern/matches/replaceAll（\s、\p{L}、Pattern.quote 交替）、String.split("")、compareToIgnoreCase、List.remove(Object)、android.util.Base64.decode、Uri.parse(path).getPath()、ContentResolver.getType；目标只有 JS RegExp/String/Array 与内建解码可用，写者准备在注释里写“等价/直迁”。 也包括 Kotlin 的 contains/endsWith/startsWith（未传 ignoreCase）、lineSequence().firstOrNull(String::isNotBlank) 一类判定与截取；也包括 String.replaceFirst(…, ignoreCase)、java.net.URL.host、Patterns.WEB_URL.matcher().matches()、io.ktor.http.Url 等依赖库语义的 URL 工具函数，目标准备改用手写正则或 @ohos.url URL（WHATWG 语义）。

## 例外与边界

- 规格或差异决策已明确接受对应差异，并写明受影响的输入

## 原因

这些调用与 JS 内建形似而语义不同：Android 的 java.util.regex 由 ICU 实现，\s 匹配 Unicode 空白而不只 ASCII 空白，\p{L} 不含组合标记 \p{M}；Pattern.quote 交替的 replaceAll 单遍扫描，拆成多遍 split/join 会重复替换；split("") 按码点切分而 JS 字符串按 UTF-16 单元；compareToIgnoreCase 逐字符先比大写再比小写，不等于整串小写比较；List.remove(Object) 原地移除首个相等元素，filter 新建数组并删掉全部；Base64.decode(DEFAULT) 跳过字母表外字符并按状态机处理“=”；Uri.parse(path).getPath() 剥离 scheme/authority 并做百分号解码；ContentResolver.getType 对未知扩展名常返回 application/octet-stream（例：FileProvider）。近似实现加“等价”注释收口后，编译与常规样例都通过，只在边界输入上偏离。

## 做法

1. 写“等价/直迁”前逐项列出所用调用的源端语义与 JS 内建的差异：正则字符类所属引擎、替换是否单遍、切分单位、比较规则、原地修改还是新建、解码容错、URI 解析与解码、未知值的平台默认；对不上的按源实现逐分支移植成共享函数，各调用点复用。
2. 常用对照：\s、\p{L} 按 ICU 字符集写成显式 Unicode 类并用 u 标志；Pattern.quote 交替的 replaceAll 写成一个交替正则单遍替换；split("") 用 Array.from 按码点切（应用 targetSdkVersion ≤ 28，或系统是 Android 9 及以下时，源端结果开头还多一个空串）；compareToIgnoreCase 逐字符先比 toUpperCase 再比 toLowerCase；List.remove(Object) 用 indexOf + splice 原地移除首个（元素类覆写了 equals 时，按源端 equals 比较的字段找下标）；Base64.decode(DEFAULT) 移植 android.util.Base64 的解码状态机；Uri.parse(path).getPath() 先解析 scheme/authority 再百分号解码；getType 未知扩展名回退 application/octet-stream 后再走源端归类；Kotlin contains/endsWith/startsWith 不传 ignoreCase 即大小写敏感，不自行加 toLowerCase，isNotBlank/isBlank 只用于判断、返回原串不 trim，lineSequence()/lines() 按 \r\n、\n、\r 分行。
3. 规格提取写这类契约时写语义点（切分与截断规则、正则引擎、舍入、解码容错、未知值默认）并标“需逐语义移植”，不用“非空白字符数”“拒绝某前缀”一类口语描述。
4. 源仓库有覆盖这些函数的单测（如 app/src/test 下的 *Test.kt）时先读，把用例当作移植样例逐条对拍；常见差异：java.net.URL.host 不含 userinfo 与端口、replaceFirst 只替换首个、Kotlin String.replace 替换全部、matcher().matches() 为整串匹配、ktor Url 接受相对路径；选用 @ohos.url URL 替代 java.net.URL 或 ktor Url 前同样用这些用例核对，不以“边缘情况可接受”跳过。源端以 URL(link) 是否抛 MalformedURLException 判定绝对、有无 scheme 或合法时，不用 new url.URL 构造器的抛错复刻：本地 @ohos.url.d.ts 中构造器标 @useinstead parseURL，已观察到它对无 scheme、相对路径与非法串不抛错，host 也省略默认端口；先用 scheme 正则（如 /^[a-zA-Z][a-zA-Z0-9+.-]*:/）判定，带 scheme 再解析校验，无 scheme 才补 http://，非绝对才按 base 解析，OrThrow 语义的调用点过滤失败项；URL(base, "/path") 取基址时按字符串截取 scheme://authority 并保留显式端口。

## 可选检查

- 对“等价”有疑问时，用边界输入与源端对照：emoji 与组合字符、全角空格、大小写变体、尾随分隔符、含空白或非法字符的 Base64、带 scheme 与百分号编码的路径、未知扩展名

来源支持：4 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1（Patterns 另比对 AOSP android-8.0.0_r1、11.0.0_r1、12.0.0_r1、13.0.0_r1；ICU 正则取 AOSP external/icu main）；androidx.core:core 1.1.0–1.19.0（字节码）；kotlin-stdlib 1.8.0、2.3.0 源码包；ktor-http-jvm 2.3.12、3.4.0 源码包。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 4 步〕Kotlin 的 CharSequence.contains(other, ignoreCase = false)、String.startsWith(prefix, ignoreCase = false)、String.endsWith(suffix, ignoreCase = false) 不传 ignoreCase 时大小写敏感；String.replace(oldValue, newValue, ignoreCase = false) 替换全部出现处，String.replaceFirst(oldValue, newValue, ignoreCase = false) 只替换第一处
- 〔适用情境 / 做法第 2 步〕Kotlin 的 CharSequence.isBlank() 在空串或全部字符满足 Char.isWhitespace() 时为 true；JVM 上 Char.isWhitespace() = Character.isWhitespace(c) || Character.isSpaceChar(c)，所以 U+00A0、U+3000 这类 Unicode 空格分隔符也算空白；isBlank/isNotBlank 只做判断，不改动原串
- 〔做法第 2 步〕Kotlin 的 CharSequence.lineSequence() 与 lines() 以 CRLF、LF、CR 三种分隔符分行，结果不含行尾分隔符
- 〔原因 / 做法第 2 步〕Android 2.3 起 java.util.regex 的匹配由 ICU4C 实现，行为照 ICU；预定义字符类 \s 定义为 \p{IsWhite_Space}（Unicode White_Space 属性，不只 ASCII 空白）；\p{L} 是 Unicode 字母类，组合标记属于 \p{M}，不在 \p{L} 内；ICU 下字面的右花括号 } 要转义
- 〔原因 / 做法第 2 步〕Matcher.replaceAll(replacement) 先 reset，再从头单遍扫描输入：不属于任何匹配的字符原样追加，每个匹配换成替换串，替换进去的文本不再参与匹配；替换串里 $ 引用捕获组、\ 转义下一个字符。Pattern.quote(s) 返回让 s 按字面匹配的模式串（元字符和转义都不生效）
- 〔原因 / 做法第 2 步〕String.split(regex) 等于 split(regex, 0)：结尾的空串全部去掉；regex 是单个非元字符或「\ + 元字符」时走 Pattern.fastSplit 按该字符切，其余（含空串 ""）交给 Pattern.split；Pattern.split 遇到输入开头的零宽匹配时：设备 Android 10 起按应用 targetSdkVersion 分，> 28 不产生开头空串、≤ 28 产生；Android 9 及以下的设备一律产生
- 〔原因 / 做法第 2 步〕Android 的正则查找由 ICU 执行：上一处匹配长度为 0 时，下一次 find 从当前位置前进一个码点（UTEXT_NEXT32 / U16_FWD_1），不会落在代理对中间；因此 split("") 按码点切，单个码点的 emoji 等补充平面字符整体成段，组合标记是独立码点、单独成段；由多个码点组成的字符（ZWJ 连接的 emoji、带肤色修饰的 emoji、国旗）按码点拆成几段
- 〔原因 / 做法第 2 步〕String.compareToIgnoreCase 与 String.CASE_INSENSITIVE_ORDER 逐个 char（UTF-16 单元）比较：不等时先各自 Character.toUpperCase 再比，仍不等再各自 Character.toLowerCase 比，仍不等返回两者之差；较短串是前缀时返回长度差；不看 locale
- 〔做法第 2 步〕Java 的 String.trim() 只去掉两端码点 ≤ U+0020 的字符，U+00A0、U+3000 等不去；JS 的 String.prototype.trim() 去掉两端的空白和行终止符，范围比 Java 大
- 〔原因 / 做法第 2 步〕List.remove(Object o) 移除满足 Objects.equals(o, get(i)) 的最小下标那一个元素，原地修改，返回是否找到；ArkTS 的 Array.splice(start, deleteCount?) 原地删除并返回被删元素数组，Array.filter 返回新数组、保留全部满足条件的元素
- 〔原因 / 做法第 2 步〕android.util.Base64.decode(str, DEFAULT)：先用 String.getBytes() 按平台字符集把串转成字节；解码表里字母表以外的字节（空白、换行、'-'、'_'、非 ASCII 字节等）一律跳过；'=' 只能出现在一组的第 3 或第 4 位，在第 3 位出现时必须紧跟（可隔着被跳过的字符）第二个 '='，补位之后只允许出现被跳过的字符；结尾补位可省；结尾只剩 1 个数据字符、'=' 位置或个数不对时抛 IllegalArgumentException("bad base-64")；flags 带 URL_SAFE 时字母表用 '-'、'_' 代替 '+'、'/'
- 〔做法第 2 步〕鸿蒙 util.Base64Helper 的 decodeSync(src: Uint8Array | string, options?: Type): Uint8Array（Base64Helper @since 9，options 从 API 10 起）；Type.BASIC（默认）、Type.MIME（输入含回车换行）、Type.BASIC_URL_SAFE、Type.MIME_URL_SAFE（后两个 @since 12）；声明和文档都没写遇到字母表外字符、'=' 位置或个数不对时怎样处理
- 〔原因 / 做法第 2 步〕Uri.parse(s) 不做校验，取整串第一个 ':' 作 scheme 分隔：有 ':' 而其后不是 '/'（或 ':' 在末尾）时是不透明 URI，getPath() 返回 null；':' 后是 '//' 时跳过 authority 到下一个 '/' 或 '\'（认 '\' 是 Android 9 起，8.1 及以前只认 '/'），authority 里先遇到 '?' 或 '#' 时路径为空串；没有 ':' 时整串按相对 URI 处理；路径到第一个 '?' 或 '#' 为止；getPath() 返回经 Uri.decode 解码的路径：按 UTF-8 解 %XX，非法序列换成 U+FFFD，'+' 不转空格
- 〔原因 / 做法第 2 步〕ContentResolver.getType(uri) 返回 provider 给出的 MIME，URL 无效或类型未知时返回 null，非 content:// 的 URI（如 file://）拿不到 provider 时也返回 null；androidx.core 的 FileProvider.getType 取文件名最后一个 '.' 之后的扩展名查 MimeTypeMap，查不到或没有扩展名时返回 "application/octet-stream"（core 1.1.0 到 1.19.0 都是这样）
- 〔做法第 4 步〕String.matches(regex) 等同 Pattern.matches(regex, str)；Matcher.matches() 要整个区域都匹配才为 true（只要求前缀匹配的是 lookingAt()，find() 找子串）
- 〔做法第 4 步〕android.util.Patterns.WEB_URL 的组成依次是：可选的「PROTOCOL + 可选 USER_INFO」、DOMAIN_NAME_STR（HOST_NAME 或 IPv4 地址）、可选 PORT_NUMBER（\:\d{1,5}）、可选 PATH_AND_QUERY（Android 8.0 起以 / 或 ? 开头，7.x 只认 / 开头）、WORD_BOUNDARY (?:\b|$|^)；HOST_NAME = (IRI_LABEL\.)+TLD，TLD 是 xn-- 开头的 punycode 或 2–63 个字母或 UCS 字符，所以主机至少带一个点，裸 localhost 不匹配（Android 7.0 起是这样组成；6.0 及以前的 WEB_URL 是另一套写法）
- 〔做法第 4 步〕Patterns 是框架类，运行时用设备系统自带的那一份：PROTOCOL 在 Android 7.0 到 11 为 (?i:http|https|rtsp)://（7.x 源码把 / 写成 \/，含义相同），Android 12 起为 (?i:http|https|rtsp|ftp)://（协议名不分大小写，用内联 (?i:…)）；Android 6.0 及以前的 WEB_URL 只认 http、https、rtsp 和首字母大写的 Http、Https、Rtsp
- 〔做法第 4 步〕Patterns 的 UCS_CHAR 在 Java 源里用 UTF-16 代理对写补充平面区间（如 \uD800\uDC00-\uD83F\uDFFD 即 U+10000–U+1FFFD，依次到 U+E1000–U+EFFFD），末尾用字符类交集 &&[^…] 排除 U+00A0、U+2000–U+200A、U+2028、U+2029、U+202F、U+3000；整体是 U+00A0–U+D7FF、U+F900–U+FDCF、U+FDF0–U+FFEF 加这些补充平面区间
- 〔做法第 4 步〕java.net.URL(String spec)：先去掉首尾码点 ≤ U+0020 的字符，可带 "url:" 前缀；在第一个 '/' 之前找第一个 ':'，冒号前的串是合法协议名（字母开头，其后只有字母、数字、+、-、.）才取作协议（转小写）；没有协议抛 MalformedURLException("no protocol: …")，协议没有处理器抛 "unknown protocol"——没装 URLStreamHandlerFactory、也没设 java.protocol.handler.pkgs 时，Android 内置的处理器只有 file、ftp、jar、http、https；URL(context, spec) 在 spec 没写协议时沿用 context 的协议、authority 和路径；spec 写的协议与 context 相同时，只有 context 的路径以 '/' 开头才同样沿用
- 〔做法第 4 步〕java.net.URL.getHost() 只返回主机名（IPv6 字面量带方括号），不含 userinfo 和端口；getPort() 没写端口时为 -1，写了 :443 就返回 443；getAuthority() 才包含 userinfo 和端口
- 〔做法第 4 步〕ktor 的 Url(urlString)（ktor-http-jvm 2.3.12、3.4.0）：去掉首尾空白，空白串什么都不解析；没有 scheme 时，开头有两个以上 '/'（如 //host/x）照样解析 userinfo 和 host，否则不解析 host，开头没有 '/' 的整串按相对路径拆成路径段、一个 '/' 开头的按根路径；build 时 host 为空（且不是 file 协议）的补上 JVM 上的 origin（协议 http、主机 localhost）：host 变成 localhost，协议在 2.3.12 是默认的 HTTP，3.x（3.0.0 起有 protocolOrNull）把为 null 的 protocolOrNull 也补成 HTTP，所以空白串和相对路径都不抛错、得到主机为 localhost 的 http URL；路径段里的 % 转义不完整或不是十六进制时在 build 解码路径段时抛 URLDecodeException；takeFrom 解析过程中的异常包成 URLParserException
- 〔做法第 4 步〕@ohos.url 的 URL 带参构造器 constructor(url: string, base?: string | URL) @since 7、自 API 9 废弃（@useinstead ohos.url.URL.parseURL），声明里没有 @throws；static parseURL(url: string, base?: string | URL): URL（@since 9）声明了 @throws 401 和 10200002 Invalid url string；url 是相对 URL 时要给 base，文档示例 parseURL('/path/path1') 不给 base 会抛错；相对路径格式相对 base 当前目录解析，以 / 开头的相对 base 的 origin 解析
- 〔做法第 4 步〕new url.URL(…) 对 'google.com'、'/y'、'/feed' 这类无 scheme 或相对的串，以及 'not-a-url' 这类非法串不抛错，单测拿到的是原样返回的值；文档里废弃构造器的示例写的是 new url.URL('/path/path1') 抛 TypeError，运行时以卡里单测实测为准
- 〔做法第 4 步〕@ohos.url 解析时端口等于当前协议的默认端口（http 80、https 443、ftp 21、gopher 70、ws 80、wss 443）就解析成空串，toString() 也省掉这个端口；hostname 不带端口，host 是 hostname 加非默认端口（如 'host:8080'）
- 〔做法第 2、4 步〕ArkTS 字符串的 replace(searchValue: string | RegExp, replaceValue: string)：searchValue 是字符串或不带 g 的 RegExp 时只替换第一个匹配，带 g 才替换全部；replaceAll(searchValue, replaceValue) 替换全部匹配
