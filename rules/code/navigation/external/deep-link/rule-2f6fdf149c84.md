# 深链 scheme 常量来自外部库时先核实值，核不到按 manifest 的 scheme 加冒号做前缀匹配

审的是：代码
触发（任一种）：
- 读到：源端 getDataString().startsWith(<外部库常量>) 判深链，manifest 的 <data android:scheme=…> 只有 scheme、没有 host；写错的样子：目标端 startsWith(...) 用的深链常量写成 `'<scheme>://'` 形式（预设了 //），注释称「值 per manifest / spec」，库里的实际值没核过
适用范围：源端深链前缀常量定义在外部库、目标端要判断 Want 的 uri 时
做法：
- 先取外部库源码或字节码核实常量值；核不到就按 manifest 的 scheme 做前缀匹配，写成 'scheme:'（返修写的是 'hashtag:'），不预设 '//'
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- opaque URI（如 mailto:nobody@google.com）的 scheme-specific part 不以 / 开头：只有 scheme 的深链形如 scheme:xxx，没有 //（出处：android.net.Uri#isOpaque）
针对本应用要查的：
- 外部库里的深链前缀常量值：该库同版本的 AAR 反编译结果或源码里的常量定义；读出字面量照写；例：卡里核实的 pixlui UrlCompleter.HASHTAG_SCHEME 是 "hashtag:"
来源：1 张卡，1 个应用
- case-7b71b27d8bbbbbd73267（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断
