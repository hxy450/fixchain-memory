# 规格写鉴权头「统一注入」时，代码有 token 就给所有请求带 Bearer，不按端点表注入

审的是：代码
触发（任一种）：
- 读到：规格或端点契约写「SDK 层统一注入」「defaultRequest 拦截，auth != null 时 headers[Authorization]=Bearer」；写错的样子：代码按端点表的 auth 列决定带不带 Authorization: Bearer，查不到端点（未登记路径）或 auth=none 时不带
适用范围：手写网络客户端替代三方 SDK、规格写明鉴权头由客户端统一注入时，代码里加请求头的地方
做法：
- 在客户端级统一加：有 token 就给所有请求带 Authorization: Bearer <token>；端点表的鉴权列只当记录，不用来决定注入
- 端点表里查不到的路径不静默降为匿名请求
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 修好后 Bearer 改为统一注入：按端点注入时漏带的请求恢复正常（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-65e0c79d46f36cb5abe7（jerboa）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断
