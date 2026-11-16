# Service 接口的参数类型和请求体

agent 会看到什么：读到 Retrofit Service 方法参数是 Long 的 userId / id，或是在调用方组装的 @Body RequestBody，端点在别的模块；规格的 ArkTS 目标签名写 number，API 表漏了跨模块端点或没写请求体字段

## 规矩

- rule-409c57a33d72｜源端参数是 Long 的 id / userId，规格的 ArkTS 目标签名写 bigint，不照模板写 number｜读到：源码方法参数 userId: Long、@Query("userId") userId: Long；写错：规格「服务层（ArkTS 目标接口）」写成 (userId: number)，或照模板示例写 (feedItemId: number)
- rule-81fc539f9350｜功能调用跨模块端点时，规格的 API 表列上它，并写出不透明请求体的字段和取值来源｜读到：源端功能代码经 ViewModel、Repository 调到别的模块的 Service 方法，该方法参数是 `@Body ... RequestBody`，请求体在调用方组装；写错：规格的 API 表只列了本模块 Service 的端点，漏了本功能调用的跨模块端点；或者列了端点，但对 @Body RequestBody 这类不透明参数没写字段名和取值来源
- rule-c26478d33ac5｜API 清单和端点目录为每个 POST 端点写明 Content-Type，不只列参数名｜读到：Android Retrofit 接口里同时有 @FormUrlEncoded + @FieldMap 的重载和 @Body 的重载；写错：API 清单或规格的接口一节只列方法、路径和参数名（如 POST /path 加参数 keyword），没有写请求编码或 Content-Type
