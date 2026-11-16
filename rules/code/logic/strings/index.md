# 字符串、字节与编解码

源端有 BufferedReader.readLine、String.split / trim、android.util.Patterns、byte[] 字面量、substring 下标、proto 字段的 varint / fixed32，目标端有 split、TextDecoder、RegExp、Uint8Array 和手写的 codec 时

## 触发族

- [Java 读行和字符串处理的语义](java-string-semantics/index.md)（7 条）：源端用 BufferedReader.readLine、FileReader / InputStreamReader、String.split、String.trim 处理文本，对应目标的 split('\n')、JS trim()、util.TextDecoder 解码和各处的兼容函数
- [手写 proto 编解码的标量读写方法](proto-scalar-codec/index.md)（2 条）：读到字段表（字段号 | wire type | 标量类型）里同时有 wire type 0 的 INT32 和 FIXED32 / SFIXED32 字段；产物里手写 codec 的 int32() / fixed32() / sfixed32() / varint() / le32() 读写方法和各字段的调用
- [手写字节编解码里的有符号整数](signed-int-bytes/index.md)（3 条）：读到 proto 字段类型 int32（wire type 0、可能为负）或 Java 源码里 byte 与 0x80 以上 int 字面量比较；产物里手写的 varint 编码、Uint8Array / number[] 字节比较和编解码单测
- [源码里的字节数组字面量和切片下标](byte-literal-index/index.md)（2 条）：读过的源码里有 byte[] 字面量、substring(起, 止) 这类按下标取的区间，规格另写了公式或区间；交回的代码里 Uint8Array 的逐下标内容和切片端点
- [android.util.Patterns 的平台正则](android-patterns-regex/index.md)（2 条）：读过的源码 import android.util.Patterns，用 matches(Patterns.WEB_URL.pattern()) 或 Patterns.EMAIL_ADDRESS 校验输入；交回的代码里自拟的「等价」RegExp 丢了分支或没有 ^…$ 全串锚定
- [替代 ExifInterface 的手写 EXIF/TIFF 编解码](exif-tiff-codec/index.md)（5 条）：读到源端用 ExifInterface（androidx.exifinterface）按 TAG_* 名 setAttribute / saveAttributes、setGpsInfo 写 EXIF，对 JPEG / PNG / WebP 输出都写；产物里手写的 TIFF/IFD 编解码：tag 号表、DataView 的有无符号读写、serialize 的值区偏移、APP1 / eXIf / VP8X 容器写法
- [Uri、Base64、MIME 类型这类安卓工具方法的移植](android-util-port/index.md)（1 条）：读到源码用 Uri.parse(…).path 取路径、Base64.decode(…, Base64.DEFAULT)、ContentResolver.getType 加 MimeTypeMap 回退；产物里目标端对原始串手写的前缀判断、宽松的 Base64 解码和静态扩展名 MIME 表
- [Kotlin / Java 字符串和正则函数的语义](jvm-string-regex-semantics/index.md)（4 条）：读到 Kotlin / Java 源码的 contains / startsWith / endsWith（传没传 ignoreCase）、lineSequence() / lines()、replaceFirst / replace，或 Pattern 正则里的 \s、\p{L} 和交替替换；产物里 TS 自加的 toLowerCase 归一、split('\n')、只换首个的 String.replace、手写的 ASCII 字符类或拆成两遍的替换
- [Kotlin 字符串的转数和判空函数](kotlin-string-ext/index.md)（2 条）：读过的 Kotlin 源里对字符串调用 toIntOrNull / toLongOrNull 转数、isBlank / isNotBlank 做筛选；交回的 TS 用 parseInt、正则或 trim 手写了等价
- [源端的 URL 解析和链接截取](url-parsing/index.md)（6 条）：读到源码用 java.net.URL(url).host、URL(base, path)、try { URL(link) } catch (MalformedURLException)、io.ktor.http.Url，或 substringBefore('#') / substringAfterLast('/') 这类 helper 解析链接；产物里是 url.URL.parseURL、靠 new url.URL 抛错判合法，或正则、lastIndexOf 手写截取
- [正则字面量里的 U+2028 / U+2029](regex-line-separator/index.md)（1 条）：交回的 ArkTS 正则字面量 /…/（如 .replace(/…/g, …)，常是复刻 JsonWriter 的 htmlSafe 转义）里直接放了 U+2028 或 U+2029 原字符
- [字符串常量里的控制字符转义](string-escape-control-chars/index.md)（1 条）：产物里字符串常量本该含 NUL 等控制字符（如 Exif、ASCII 头后补的 \u0000），却写成了字面反斜杠加 u0000，或用脚本批量把原始控制字符改写成转义
