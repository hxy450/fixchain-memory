# 页面有可点击入口时，规格逐个写出源码目标页、URL 常量和参数，不写「打开对应业务页」

审的是：规格
触发（任一种）：
- 读到：源码的点击回调里调起目标：某个 Fragment 的 start(url) 打开 WebView 加载固定 URL，或 start(列表[i]) 打开详情 Fragment、startActivity(Intent)；写错的样子：规格的行为契约只写「打开对应 H5 业务页」「进入对应业务」，没写每个入口的目标页、URL 常量和默认值、所带参数
适用范围：规格提取时，页面上横幅、宫格图片等可点击入口的导航契约
做法：
- 行为契约里每个入口一行：入口 → 源码目标（目标 Fragment/Activity 或 WebView 页）、URL 常量及默认值、参数（如列表索引第几项）
针对本应用要查的：
- 每个入口的点击目标、URL 默认值和参数：源工程里该页面 Fragment/Activity 的 Kotlin 或 Java 文件，从 setOnClickListener 或 onClick 方法往下跟；跟到 start(...)、startActivity(...)、WebView 加载的调用为止，记下目标类名、URL 常量的默认值、传入的参数表达式
来源：1 张卡，1 个应用
- case-4042c8947009b8610581（android-train-ticket-vest7）：做法第 1 步 ← 建议 1
