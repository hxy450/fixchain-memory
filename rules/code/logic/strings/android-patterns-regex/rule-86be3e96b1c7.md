# 源端用 Patterns.WEB_URL 整串匹配时，目标逐段移植公开定义并 ^…$ 锚定

审的是：代码
触发（任一种）：
- 读到：输入用 String.matches(Patterns.WEB_URL.pattern()) 或 Patterns.EMAIL_ADDRESS 这类平台正则常量校验；写错的样子：目标写自拟的「等价」正则（如主机只收字母 TLD 或 localhost），丢了 IP_ADDRESS_STRING 分支，或没有 ^…$ 锚定
- 读到：源码 Patterns.WEB_URL.matcher(text).matches() 判定文本是否为 URL；写错的样子：目标换成通用的 Web URL 正则，或复用的正则只锚 ^ 不锚 $，「example.com is great」这样的句子也判为 URL
适用范围：源端用 android.util.Patterns 的正则常量以 matches() 整串匹配，迁到 ArkTS 时
做法：
- 按 android.util.Patterns 的定义逐段移植 IP_ADDRESS_STRING、UCS_CHAR、LABEL_CHAR、IRI_LABEL、TLD、HOST_NAME、DOMAIN_NAME_STR、PROTOCOL、USER_INFO、PORT_NUMBER、PATH_AND_QUERY、WORD_BOUNDARY，照 WEB_URL 的顺序拼起来，不换成通用 URL 正则
- 整体包成 new RegExp('^(?:' + WEB_URL + ')$', 'u').test(s) 保留 matches() 的全串语义；目标引擎不支持的写法（内联 (?i:…)、UTF-16 代理对区间、字符类交集 &&）改成等价写法
- 复用已有正则前先确认两端锚定，用「example.com is great」这类样本验证它不算 URL
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- WEB_URL = "(" + "(" + "(?:" + PROTOCOL + "(?:" + USER_INFO + ")?" + ")?" + "(?:" + DOMAIN_NAME_STR + ")" + "(?:" + PORT_NUMBER + ")?" + ")" + "(" + PATH_AND_QUERY + ")?" + WORD_BOUNDARY + ")"：WEB_URL 的拼接顺序：可选协议和 userinfo、主机、可选端口、可选路径和查询、词边界（出处：android.util.Patterns#WEB_URL）
- DOMAIN_NAME_STR = "(" + HOST_NAME + "|" + IP_ADDRESS_STRING + ")"；HOST_NAME = "(" + IRI_LABEL + "\\.)+" + TLD：主机是带 TLD 的主机名或 IPv4 地址；不带点的裸 localhost 不匹配（出处：android.util.Patterns#DOMAIN_NAME_STR、HOST_NAME）
- PROTOCOL = "(?i:http|https|rtsp|ftp)://"：协议不分大小写，用的是内联 (?i:…) 写法（出处：android.util.Patterns#PROTOCOL）
- UCS_CHAR 里有 \uD800\uDC00-\uD83F\uDFFD 这类 UTF-16 代理对区间和 &&[^…] 字符类交集：这些是要改写成目标引擎能用的等价写法的部分（出处：android.util.Patterns#UCS_CHAR）
- str.matches(regex) 等同 Pattern.matches(regex, str)，Matcher.matches 匹配整个输入：源端是全串匹配，不是前缀或包含，目标要加 ^…$（出处：java.lang.String#matches；java.util.regex.Matcher#matches）
- 按各段常量逐段重建 WEB_URL（u 模式、全串匹配）后，IP 主机加端口的地址通过校验：修复后先跑对照测试再替换正则（出处：卡里修好并验证过）
- 修好后移植了完整的 Patterns.WEB_URL 并改为整串匹配：普通句子判为假（出处：卡里修好并验证过）
针对本应用要查的：
- WEB_URL 的完整正则：Android SDK sources/android-<compileSdk>/android/util/Patterns.java 里的 WEB_URL 及它引用的常量（PROTOCOL、USER_INFO、DOMAIN_NAME_STR 等）；逐个展开字符串常量，按 WEB_URL 的拼接顺序拼成一个正则串
未核实：Patterns 的定义可能随平台版本不同，本机按 android-36.1 的源码核实
来源：3 张卡，2 个应用
- case-4b8ebe5007982e666e18（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 7 ← 诊断
- case-53fd6cc643582558ba6d（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 6 ← 诊断
- case-6582e6c5e66cee6e4cc9（jerboa）：做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 4、诊断
