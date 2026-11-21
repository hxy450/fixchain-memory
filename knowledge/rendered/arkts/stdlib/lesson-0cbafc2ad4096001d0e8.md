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
2. 常用对照：\s、\p{L} 按 ICU 字符集写成显式 Unicode 类并用 u 标志；Pattern.quote 交替的 replaceAll 写成一个交替正则单遍替换；split("") 用 Array.from 按码点切；compareToIgnoreCase 逐字符先比 toUpperCase 再比 toLowerCase；List.remove(Object) 用 indexOf + splice 原地移除首个；Base64.decode(DEFAULT) 移植 android.util.Base64 的解码状态机；Uri.parse(path).getPath() 先解析 scheme/authority 再百分号解码；getType 未知扩展名回退 application/octet-stream 后再走源端归类；Kotlin contains/endsWith/startsWith 不传 ignoreCase 即大小写敏感，不自行加 toLowerCase，isNotBlank/isBlank 只用于判断、返回原串不 trim，lineSequence()/lines() 按 \r\n、\n、\r 分行。
3. 规格提取写这类契约时写语义点（切分与截断规则、正则引擎、舍入、解码容错、未知值默认）并标“需逐语义移植”，不用“非空白字符数”“拒绝某前缀”一类口语描述。
4. 源仓库有覆盖这些函数的单测（如 app/src/test 下的 *Test.kt）时先读，把用例当作移植样例逐条对拍；常见差异：java.net.URL.host 不含 userinfo 与端口、replaceFirst 只替换首个、Kotlin String.replace 替换全部、matcher().matches() 为整串匹配、ktor Url 接受相对路径；选用 @ohos.url URL 替代 java.net.URL 或 ktor Url 前同样用这些用例核对，不以“边缘情况可接受”跳过。源端以 URL(link) 是否抛 MalformedURLException 判定绝对、有无 scheme 或合法时，不用 new url.URL 构造器的抛错复刻：本地 @ohos.url.d.ts 中构造器标 @useinstead parseURL，已观察到它对无 scheme、相对路径与非法串不抛错，host 也省略默认端口；先用 scheme 正则（如 /^[a-zA-Z][a-zA-Z0-9+.-]*:/）判定，带 scheme 再解析校验，无 scheme 才补 http://，非绝对才按 base 解析，OrThrow 语义的调用点过滤失败项；URL(base, "/path") 取基址时按字符串截取 scheme://authority 并保留显式端口。

## 可选检查

- 对“等价”有疑问时，用边界输入与源端对照：emoji 与组合字符、全角空格、大小写变体、尾随分隔符、含空白或非法字符的 Base64、带 scheme 与百分号编码的路径、未知扩展名

来源支持：4 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕android.util.Base64.decode(…, DEFAULT) 按状态机解码：字母表外的字节（空白、换行和其他任何非 Base64 字符）在任何位置都直接跳过；结尾的 '=' 可以省略，但写了就必须个数正确，'=' 出现在不该出现的位置、'=' 之后再有数据字符、或最后只剩 1 个数据字符时抛 IllegalArgumentException（"bad base-64"）；String 入参先按默认字符集转成字节。鸿蒙 util.Base64Helper.decodeSync 的 options 缺省为 Type.BASIC，文档写明输入含回车换行时用 Type.MIME。〔成立范围：对象：android.util.Base64.decode 的 DEFAULT 标志。条件：输入可能带换行、空格或混入非法字符。不成立的情形：带 URL_SAFE 标志时改用 '-'、'_' 字母表，'+'、'/' 反而成了被跳过的字母表外字符。〕
- 〔做法第 2 步〕android.net.Uri#getPath 返回解码后的路径，解码由 Uri.decode 完成：只解 %XX、不把 '+' 转成空格，非法的百分号序列替换成 U+FFFD、不抛异常；非层级 URI（如 mailto:）返回 null。鸿蒙侧 decodeURIComponent 遇到格式不正确的输入抛 URIError（未捕获即 jscrash）。〔成立范围：对象：Uri.parse(s).getPath()。条件：路径里可能有孤立的 '%'、截断的 %X 或非 UTF-8 序列。不成立的情形：getEncodedPath 返回未解码的原串。〕
- 〔做法第 4 步〕Java 的 String.matches(regex) 与 Matcher.matches() 要求整串匹配（相当于隐式首尾锚定），Patterns.WEB_URL.matcher(s).matches() 同理；Matcher.find() 和 JS 的 RegExp.test 是在串中找子串，部分匹配就返回 true。〔成立范围：对象：源端 matches() 判定迁成 JS 正则时。条件：正则本身没有 ^ 和 $。不成立的情形：源端用 Matcher.find() 时本来就是子串查找。〕
- 〔做法第 2 步〕String.compareToIgnoreCase 与 String.CASE_INSENSITIVE_ORDER 逐个 UTF-16 字符比较：两字符不等时先各自 Character.toUpperCase，仍不等再各自 toLowerCase，返回两者之差；共同前缀比完则返回长度差。不看区域设置，也不做语言排序。〔成立范围：对象：Android 的 java.lang.String#compareToIgnoreCase 与 String.CASE_INSENSITIVE_ORDER。条件：准备改写成 localeCompare、Intl.Collator 或先 toLowerCase() 再比较时。不成立的情形：源端用 java.text.Collator 时本就是区域相关排序。〕
- 〔做法第 4 步〕java.net.URL#getHost 只返回主机名，端口由 getPort 单独给出，URL 里没写端口时 getPort 返回 -1 而不是协议默认端口；@ohos.url 的 URL.host 是“主机名:端口”（如 host:8080），hostname 才不带端口；端口等于协议默认端口（http 80、https 443、ftp 21、gopher 70、ws 80、wss 443）时 port 解析为空串，host 也不带端口。〔成立范围：对象：java.net.URL 的 getHost/getPort 迁到 url.URL.parseURL 结果的 host、hostname、port。条件：URL 带非默认端口，或源端拼 scheme://host:port 时依赖 getPort。不成立的情形：URL 不带端口时 host 与 hostname 相同。〕
- 〔做法第 4 步〕java.net.URL(String) 在没有协议、协议未知或入参为 null 时抛 MalformedURLException；Android 内置的协议处理器只有 file、ftp、jar、http、https，所以 mailto:、content:、data: 这类带 scheme 的串同样抛异常。〔成立范围：对象：源端用 new URL(s) 是否抛 MalformedURLException 判定合法或绝对的分支。条件：应用没有调用 URL.setURLStreamHandlerFactory，也没设 java.protocol.handler.pkgs。不成立的情形：注册了自定义处理器的协议可以正常构造；只用 scheme 正则判定时这类串会被当成带 scheme 的合法串。〕
