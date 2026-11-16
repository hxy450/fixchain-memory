# Linkify 自动链接的识别和切分

agent 会看到什么：读到源端 Linkify.addLinks、LinkifyPlugin.create(Linkify.WEB_URLS) 在文本上跑一个或多个 Pattern、按 getSpanStart / getSpanEnd 原位挂 URLSpan；产物里自动链接的正则只认 https?:// 或 www. 前缀，或切 run 时命中段和间隔文本的输出顺序被打乱

## 规矩

- rule-2320c73dd00c｜规格写明 WEB_URLS 语义时，移植 AUTOLINK_WEB_URL 和 @ 前不链接过滤，不缩成协议前缀｜读到：源端 LinkifyPlugin.create(Linkify.WEB_URLS)；规格 AC 写「裸 URL（WEB_URLS 语义，不含 email）」；写错：自动链接（autoLink）的正则只认 `https?://` 或 `www.` 前缀，注释写「语义近似、不识别无协议域名」
- rule-df9371685bbe｜按多个正则把文本切成 run 时，命中和间隔文本按原位置顺序输出，单测断言拼接等于原文｜读到：源端在同一文本节点上用 Linkify.addLinks 跑多个 Pattern，再按 start + getSpanStart / getSpanEnd 原位挂 span，文本顺序不变；写错：切分循环里把每个命中直接 push 成 LINK run，间隔文本先收进另一个数组、循环结束后再输出；单测只测正则命中与捕获组
