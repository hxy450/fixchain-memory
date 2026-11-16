# 按命名空间分发的 SAX 迁移时，元素 URI 不只靠 getNamespace，用 xmlns 作用域栈回退

审的是：代码
触发（任一种）：
- 读到：源端 SAX(namespaceAware) 的 startElement(uri, localName, qName, atts) 或 XmlPullParser.getNamespace() 按 uri + prefix 分发 itunes:、media:、Atom 默认命名空间等元素；写错的样子：元素 uri 只取 ParseInfo.getNamespace()，没有读 xmlns / xmlns:p 属性做回退，uri 为空时分发不到命名空间 handler
适用范围：用 @ohos.xml 的 XmlPullParser 重建按命名空间分发的解析时
做法：
- 把 xmlns 与 xmlns:p 属性按元素深度（ParseInfo.getDepth()）压入作用域栈，END_TAG 时弹出
- getNamespace() 为空时按前缀解析 uri：前缀取 getPrefix()，或从名字里的「p:」拆出，查作用域栈；无前缀元素用当前默认命名空间
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getNamespace(): string；getPrefix(): string；getDepth(): number：ParseInfo 给出元素的命名空间、前缀和深度（出处：鸿蒙 SDK 的 ets/api/@ohos.xml.d.ts，ParseInfo.getNamespace / getPrefix / getDepth）
- ignoreNameSpace?: boolean，默认 false；true 时不解析命名空间：要取命名空间就不能设成 true（出处：js-apis-xml.md，ParseOptions）
- uri 是元素的命名空间 URI，没有命名空间或没开命名空间处理时为空串：源端 startElement 的 uri 参数（出处：org.xml.sax.ContentHandler#startElement）
- 加入按 xmlns / xmlns:p 建的前缀作用域、uri 为空时拆前缀补 uri 后，设备复查作者与时长等带前缀字段恢复显示：改后的效果（出处：卡里修好并验证过）
未核实：修复期没打印 getNamespace() 的返回值；文档 getNamespace 示例（ignoreNameSpace:false）里带前缀元素能取到 URI，xmlns 回退是否在所有情形都必需没核实
来源：1 张卡，1 个应用
- case-b5cceb2aa00d9c09058a（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 4 ← 诊断
