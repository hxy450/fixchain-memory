# 收尾一致性结论里的富文本链接

agent 会看到什么：源端有多处 HtmlCompat.fromHtml / setMovementMethod(LinkMovementMethod) 调用点，前面环节转述「已页内自渲染解决」，收尾结论凭转述写「通过」

## 规矩

- rule-07e03d9d5261｜收尾判富文本链接一致时逐个对照源端 fromHtml / LinkMovementMethod 调用点查目标代码｜读到：源端有多处 HtmlCompat.fromHtml / setMovementMethod(LinkMovementMethod) 调用点；前面环节转述「已页内自渲染解决」；写错：收尾的一致性结论写「通过」，依据是转述，没有逐个调用点对照目标代码
