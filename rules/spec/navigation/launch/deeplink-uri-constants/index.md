# 由常量拼出的深链和分享链接 URI

agent 会看到什么：读到 navDeepLink { uriPattern = "$常量/路径/{id}" } 或复制链接的字符串由域名常量拼出；页面数据、规格或 AC 里出现源码中没有的自定义 scheme，没写常量展开后的地址

## 规矩

- rule-000c6e355ea2｜源端深链 URI 由常量拼接时，规格先展开常量写出完整 URI，展不开就标待查，不自拟 scheme｜读到：navDeepLink { uriPattern = "$常量/路径/{id}" } 或复制链接的字符串由一个域名常量拼出；写错：页面数据、规格或 AC 里出现源码中不存在的自定义 scheme（如 xxx://路径/{id}），没有写出常量展开后的 https 地址
