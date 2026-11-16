# @ohos.xml 的 XmlPullParser 解析回调

agent 会看到什么：读到源端 SAX 的 ContentHandler.startElement(uri, localName, qName, Attributes) 或 XmlPullParser 在 START_TAG 读属性、按命名空间分发，产物里是 @ohos.xml 的 tokenValueCallbackFunction、attributeWithTagCallbackFunction 循环和 ParseInfo.getNamespace() 的用法

## 规矩

- rule-9941e5431c9b｜@ohos.xml 开始标签与属性分两路回调时，START_TAG 先挂起，到下一 token 连同属性分发｜读到：源端 SAX 的 ContentHandler.startElement(uri, localName, qName, Attributes) 或 XmlPullParser 在 START_TAG 时读本元素属性；规格要求开始事件带齐 attrs；写错：tokenValueCallbackFunction 收到 START_TAG 就把 attributeWithTagCallbackFunction 已累积的属性快照、清空并分发，注释写「属性先/后于 token 两种顺序行为一致」
- rule-a2d33fed5ef3｜按命名空间分发的 SAX 迁移时，元素 URI 不只靠 getNamespace，用 xmlns 作用域栈回退｜读到：源端 SAX(namespaceAware) 的 startElement(uri, localName, qName, atts) 或 XmlPullParser.getNamespace() 按 uri + prefix 分发 itunes:、media:、Atom 默认命名空间等元素；写错：元素 uri 只取 ParseInfo.getNamespace()，没有读 xmlns / xmlns:p 属性做回退，uri 为空时分发不到命名空间 handler
