# 源端从响应头取登录凭证时，规格的鉴权模型写明凭证来源、头名和写入点

审的是：规格
触发（任一种）：
- 读到：Retrofit 接口返回 Response<BaseResponse<T>>，调用方在成功回调里用 headers()["Authorization"] 等读响应头写 token、refreshToken；写错的样子：网络层或登录功能规格的鉴权一节只写「统一 token 注入 + 401 刷新」，API 表写「返回 用户 DTO + token」，没写凭证来自响应头、头名和写入点
适用范围：规格提取阶段整理鉴权模型和登录接口时
做法：
- 列出返回 Response<…> 的端点，逐个查调用方是否读 headers()；读了的把头名（如 Authorization）和写入哪个凭证（token / refreshToken）写进网络层与登录功能规格的凭证获取来源一项
- 鉴权清单（auth_model 的 token_acquisition）没交付时，在规格里标为阻塞，不用端点计数代替
针对本应用要查的：
- 哪些端点的凭证从响应头取、头名是什么：源工程 Retrofit 接口声明里返回类型为 Response<…> 的方法，再到调用它们的 Repository 成功回调里搜 headers()；记下每个端点读的头名和写进的凭证字段；body 的 data 里只有用户信息的，凭证就只在头里
来源：1 张卡，1 个应用
- case-31852e28af4327a408a3（polypal-app-ohos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
