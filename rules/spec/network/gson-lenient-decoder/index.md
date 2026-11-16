# Gson 反序列化改写成显式 decoder 的契约

agent 会看到什么：读到源端用 Gson 反序列化 BaseResponse<T> 和各 Bean，真实响应样例还没采集（golden 标 needs_capture）；规格只写「Gson BaseResponse<T> → 显式 JSON decoder」「decoder 必须显式校验字段」，没写数字↔字符串、布尔转字符串这类要保留的宽松转换

## 规矩

- rule-d076b471723a｜规格写「Gson → 显式 decoder」契约时，写明要保留的宽松转换｜读到：源端用 Gson 反序列化 BaseResponse<T> 和各 Bean；真实响应样例还没采集（golden 标 needs_capture）；写错：规格只写「Gson BaseResponse<T> → 显式 JSON decoder，保留名称、可空性和泛型边界」「decoder 必须显式校验字段」，没写数字↔字符串、布尔转字符串的宽松转换
