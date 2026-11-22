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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕Android 2.3 起 java.util.regex 的后端是 ICU4C；\s 定义为 \p{IsWhite_Space}（Unicode 空白，含全角空格等），不只是 ASCII 空白
- 〔原因 / 做法第 2 步〕String.compareToIgnoreCase 对每个字符做 Character.toLowerCase(Character.toUpperCase(c)) 后逐字符比较，不是整串小写后比较
- 〔原因 / 做法第 2 步〕List.remove(Object) 原地删除第一次出现的相等元素；JS Array.filter 返回满足条件的元素组成的新数组
- 〔原因 / 做法第 2 步〕android.util.Base64.decode：结尾的 '=' 可省略，但一旦出现个数必须正确；解码表里字母表以外的字符记为 SKIP，解码时跳过而不报错
- 〔原因 / 做法第 2 步〕android.net.Uri.getPath 返回解码后的路径，不是分层 URI 时返回 null
- 〔原因 / 做法第 2 步〕String.split(regex) 等于 limit 为 0 的 split，结果里不含末尾的空串；JS split 会保留末尾空串
- 〔原因 / 做法第 2 步〕Java String.trim 只去掉两端码点 ≤ U+0020 的字符；JS String.trim 去掉两端的空白符和行终止符，范围更宽
- 〔做法第 4 步〕String.matches(regex) 等同 Pattern.matches(regex, str)，Matcher.matches 要求整个区域匹配，不是前缀或包含
- 〔适用情境 / 做法第 4 步〕android.util.Patterns.WEB_URL 依次是可选的协议加 userinfo、主机、可选端口、可选路径和查询、词边界；协议是不分大小写的 http|https|rtsp|ftp；主机须为带 TLD 的主机名（一个以上「标签.」后接 TLD）或 IP 地址，不带点的裸 localhost 不匹配
- 〔做法第 4 步〕JS String.replace 的 searchValue 是字符串或不带 g 标志的正则时只替换第一个匹配
- 〔做法第 4 步〕java.net.URL.getHost 只返回主机名，userInfo、端口分别由 getUserInfo、getPort 返回
- 〔做法第 4 步〕java.net.URL 构造时没有协议抛 MalformedURLException（no protocol），协议未知同样抛 MalformedURLException（unknown protocol）
- 〔做法第 4 步〕@ohos.url 的 URL.parseURL：相对 URL 必须给 base，给的是绝对 URL 时忽略 base；非法串抛 10200002（Invalid url string）
- 〔做法第 4 步〕@ohos.url 的带参构造 URL(url, base) 自 API 9 起废弃、@useinstead parseURL，声明里没有列出抛错条件
- 〔做法第 4 步〕@ohos.url 解析时端口等于当前协议的默认端口（http 80、https 443）就解析为空字符串，host 里也不带这个端口
- 〔做法第 3 步〕Java Math.round(float) 取最接近的整数，正好在中间时向正无穷取；参数为 NaN 时结果是 0（JS Math.round(NaN) 是 NaN）
