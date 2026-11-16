# 配置地址拼接运行期参数的链接

agent 会看到什么：读到配置读取类的 getter 返回 url + 渠道 getter() 一类拼接、assets JSON 配置里的地址 query 以 = 结尾；产物里 Service 把配置地址写成 const / static readonly URL 常量，取链接的方法直接返回它

## 规矩

- rule-172dd060a29c｜源端链接 getter 在配置地址后拼渠道等参数时，目标按完整表达式构造 URL，不只抄配置地址｜读到：配置读取类的 getter 返回 `return url + 渠道getter()` 这类拼接表达式；assets JSON 等配置里的地址 query 最后一个参数是空值、以 `=` 结尾；写错：目标 Service 里把配置 address 原样写成 `const` / `static readonly` URL 常量，链接仍以 `=` 结尾，取链接的方法直接返回常量，没拼任何运行期参数
