# Service 只收不透明请求体时，从源端调用链追到 body 的构造处照抄字段与取值来源，不用空对象占位

ID：`lesson-0bc494e864b2d8ab1a34` · 版本：1

[本主题](index.md)

## 何时使用

数据层实现与规格提取阶段，编写 Repository 调用网络 Service、确定 POST 请求体字段时

## 适用情境

目标 Service 方法只接收 data: Object（对应源端 @Body RequestBody），规格 API 表没列这个端点或它的请求字段；源端由 ViewModel 调用某个 Repository 方法，在那里组装 body（如 device_id 取自设备 ID 工具）。

## 原因

不透明参数把字段决定权留给调用方，签名本身提示不了缺什么；空对象能通过编译和所有静态检查，直到服务端返回 400。来源中切片实现者的派工要求读源码，它却判断规格已足够，把游客登录的 body 写成 {}；规格 API 表也没列这个跨模块端点。

## 做法

1. 规格提取时，API 表也列出本功能调用的跨模块端点；遇到 @Body RequestBody 这类不透明参数就追到构造处，记下字段名和取值来源。
2. 实现 Repository 时，从规格锚点里的 ViewModel 追到源端实际调用的 Repository 方法，逐项照搬 body 字段；先给每个 POST 端点列出字段出处，出处为空就读源码，不写 {} 占位。

