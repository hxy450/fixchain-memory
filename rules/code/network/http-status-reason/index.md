# HTTP 非 2xx 响应的状态码和原因短语

agent 会看到什么：读到源端按 isSuccessful、response.code / getResponseCode 判 2xx，非 2xx 分支用 OkHttp 的 response.message（原因短语）构造 HttpError(code, message)；产物里 requestInStream 返回的响应码有没有判 2xx、错误文案用没用 rcp Response.reasonPhrase、错误类的 message 和 description 怎么取

## 规矩

- rule-c660b7cf4603｜requestInStream 的 Promise<number> 是 HTTP 响应码，按 2xx 判成功，不删校验｜读到：原稿按 resp.responseCode 在 200–299 才返回字节，编译报 responseCode 不存在于 number；写错：改成 await httpRequest.requestInStream(...) 后无条件返回拼合的字节，删掉了 2xx 判定
- rule-41296089350b｜源端读 OkHttp response.message 时，目标用 rcp Response.reasonPhrase｜读到：源端非 2xx 分支用 OkHttp 的 response.message（HTTP 原因短语）构造错误；写错：目标非 2xx 分支传 'HTTP ' + response.statusCode 一类自造文案，没用 Response.reasonPhrase，也没在差异清单登记
- rule-9358a5d63160｜移植错误数据类时逐字段照搬：message 取原因短语，code: message 只给 description｜读到：Kotlin 错误类构造 HttpError(code, message = response.message)，description 默认值 "$code: $message"；写错：目标错误类的 message 和 description 都写成 `code + ': ' + message`
