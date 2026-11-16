# 规格写了网络权限必配时，计划要有任务落到 module.json5 的权限声明

审的是：计划与派工
触发（任一种）：
- 读到：规格里有权限映射段：android.permission.INTERNET → ohos.permission.INTERNET（必配）、ACCESS_NETWORK_STATE → ohos.permission.GET_NETWORK_INFO，或写明 requestPermissions 要配哪几项；写错的样子：任务拆分里没有任何任务的 input 指向规格的权限段，也没有任务的 output 含 module.json5 的 requestPermissions；网络任务的 input 只指向网络段
适用范围：从规格拆计划任务、而计划模板没有工程配置槽位时，规格里写了安卓 uses-permission 到 module.json5 requestPermissions 的映射
做法：
- 逐段核对规格各章节都有任务引用；权限段没有固定槽位时，写进网络任务的 input，并在它的 output 里写明「module.json5 requestPermissions：ohos.permission.INTERNET（代码判断连接状态时加 ohos.permission.GET_NETWORK_INFO）」
- 或者单列一个工程配置任务：input 指向规格的权限段，output 是 module.json5 的 requestPermissions
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android.permission.INTERNET → ohos.permission.INTERNET；android.permission.ACCESS_NETWORK_STATE → ohos.permission.GET_NETWORK_INFO：安卓网络权限在 module.json5 里对应的权限名（出处：卡里修好并验证过）
- ohos.permission.INTERNET：normal 级，system_grant：系统授权，只需在 requestPermissions 里声明（出处：permissions-for-all.md，ohos.permission.INTERNET）
- ohos.permission.GET_NETWORK_INFO：normal 级，system_grant：系统授权，只需在 requestPermissions 里声明（出处：permissions-for-all.md，ohos.permission.GET_NETWORK_INFO）
来源：1 张卡，1 个应用
- case-63a0f0066a7a0376735f（DeepAI全能PPT）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
