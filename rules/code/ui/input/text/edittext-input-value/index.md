# EditText 输入值的取用

agent 会看到什么：读到源端各执行方法从本组 EditText 的 getText().toString() 原文取值去校验和传参，产物里是 TextInput 的 @State 表单字段、请求 interface 的字段和校验前的 trim / toLowerCase

## 规矩

- rule-7c75a2515a67｜源端校验和传参都用原始输入时，目标不加 trim 等规范化，校验和传参都用原文｜读到：EditText 的 getText().toString() 原文直接用于 matches(...) 校验和后续传参，没有 trim()；写错：目标校验或传参前做了 .trim()、.toLowerCase() 这类源端没有的规范化
- rule-ec33e236ea90｜源页面多组表单字段同名时，执行请求按写模式各设独立字段，不复用别的表单槽位｜读到：同一 Activity 里有几组语义相近的输入控件（都叫扇区/块/数值一类），各执行方法分别从本组的 EditText#getText 取值；写错：目标的请求 interface 只有一组扇区/块/数值字段，页面从一个 @State 表单取值填进去，另一个表单的值没进请求或被别的表单值顶替
