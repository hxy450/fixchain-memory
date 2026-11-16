# Uri、Base64、MIME 类型这类安卓工具方法的移植

agent 会看到什么：读到源码用 Uri.parse(…).path 取路径、Base64.decode(…, Base64.DEFAULT)、ContentResolver.getType 加 MimeTypeMap 回退；产物里目标端对原始串手写的前缀判断、宽松的 Base64 解码和静态扩展名 MIME 表

## 规矩

- rule-cb1f5fc0b5de｜Uri.parse().path、Base64.decode(DEFAULT)、getType 照 AOSP 逐分支移植｜读到：源码 Uri.parse(path).path 取路径后再判前缀；写错：目标对原始串直接 replace(/\/+/g, '/') 后判 startsWith('/data')，file:///data/… 被放行
