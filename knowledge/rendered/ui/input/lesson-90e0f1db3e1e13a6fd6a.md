# Android 平台公开正则常量按定义逐段移植并保持全串匹配语义

## 何时使用

界面实现阶段，移植 Patterns.WEB_URL、Patterns.EMAIL_ADDRESS 等平台正则对用户输入的全串校验（String.matches 或 matcher().matches()）时

## 适用情境

源以 String.matches(Patterns.X.pattern()) 做全串校验，目标没有同名 API，需要自行提供正则。

## 例外与边界

- 源端用 matcher(text).find() 或 Linkify 一类在文本里查找链接的，是子串查找语义，移植同一正则时不要加首尾锚定
- 不加源端没有的输入规范化：源端校验和后续传递的都是原始文本（未 trim、未改大小写）时，目标也校验并传递原始文本

## 原因

自拟的“实用等价式”会丢分支（如 IP 主机）或多收非法输入，而一般视觉验收不会输入这些边界值。

## 做法

1. 按公开定义逐段移植，目标正则引擎不支持的写法（内联 (?i)、UTF-16 代理对区间）改成等价写法，并保留全串匹配；仍有已知差异时登记具体会判错的输入。

## 可选检查

- 无法逐段移植、或确认与转交校验类不确定项前，用覆盖各分支的代表输入（带顶级域名的域名、IPv4 加端口、无 scheme、裸 localhost、IDN、前导空格）与源端预期离线对照

来源支持：3 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕安卓 Patterns.WEB_URL 依次拼接：可选的协议加 userinfo、主机（DOMAIN_NAME_STR）、可选端口、可选路径和查询，最后是词边界 (?:\b|$|^)
- 〔原因 / 做法第 1 步〕安卓 Patterns 的主机 DOMAIN_NAME_STR 是「带顶级域名的主机名（(IRI_LABEL\.)+TLD）」或「IP 地址」二选一，不带点的裸主机名（如 localhost）匹配不上
- 〔做法第 1 步〕安卓 Patterns 的 PROTOCOL 为 (?i:http|https|rtsp|ftp)://，用内联 (?i:…) 让协议不分大小写
- 〔做法第 1 步〕安卓 Patterns 的 UCS_CHAR 含 \uD800\uDC00-\uD83F\uDFFD 这类 UTF-16 代理对区间和 &&[^…] 字符类交集写法
- 〔适用情境 / 做法第 1 步〕Java 的 String.matches(regex) 等同 Pattern.matches(regex, str)，Matcher.matches 要求整个输入与模式匹配，是全串匹配
