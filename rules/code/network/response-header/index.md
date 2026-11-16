# Retrofit Response<> 带的响应头

agent 会看到什么：读到源端 Retrofit 接口返回 Response<BaseResponse<T>>、Repository 从 headers()["Authorization"] 取 token，交回的 HTTP 封装或解析函数只返回、只读 body

## 规矩

- rule-d654fb69edf8｜源接口有 Response<> 包裹的端点时，HTTP 封装把响应头随结果返回，不只返回 body｜读到：Retrofit 接口返回 Response<BaseResponse<T>>，调用方读 headers()；写错：HTTP 封装只 JSON.parse(response.result) 返回 body，response.header 被丢弃；统一响应类里没有承载响应头的字段
- rule-2074a19dd56c｜源 Repository 从响应头取 token 和 refreshToken 时，目标照源取值，不传空串｜读到：源 Repository 成功回调里用 headers()["Authorization"] 等响应头写 accessToken 和 refreshToken，body 的 data 只存用户信息；写错：目标的解析函数只从 resp.data 取 token，不读 response.header；保存凭证时 refreshToken 一参传空串 `''`；新补的登录方法直接复用已有解析函数
