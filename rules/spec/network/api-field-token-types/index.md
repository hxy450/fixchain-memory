# 接口字段表里 id 的线上类型和数值量级

agent 会看到什么：读到 Android 模型把 id、*_id 声明为 String，golden 响应或探针里同一字段是 JSON 数值；接口字段表只记声明类型，响应契约没写大整数按字符串保真

## 规矩

- rule-a0f52d604cb5｜接口字段表记线上 token 类型和量级，雪花类长整数 id 在响应契约写按字符串保真｜读到：Android 模型把 id、*_id 声明为 String，golden 响应或探针里同一字段是 JSON 数值；写错：接口字段表只记 Android 声明类型 String，没有线上 JSON token 类型和取值量级；响应契约里没写超过 2^53 的数值按字符串保真
