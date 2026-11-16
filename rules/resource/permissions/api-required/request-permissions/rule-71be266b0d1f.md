# 新增的 Web 页加载在线 URL 时，requestPermissions 补 INTERNET 权限

审的是：资源
触发（任一种）：
- 读到：源端入口打开 WebView 加载 https:// 在线 URL；写错的样子：目标端新增了 Web(...) 加载在线地址的页面，module.json5 的 requestPermissions 里没有 ohos.permission.INTERNET
适用范围：目标端用 Web 组件访问在线网页时的模块配置
做法：
- 在 module.json5 的 module.requestPermissions 里加 { "name": "ohos.permission.INTERNET" }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- "requestPermissions":[ { "name" : "ohos.permission.INTERNET" } ]：使用 Web 组件访问在线网页时需要的网络权限声明（出处：web-component-overview.md，需要权限）
来源：1 张卡，1 个应用
- case-4042c8947009b8610581（android-train-ticket-vest7）：做法第 1 步 ← 诊断
