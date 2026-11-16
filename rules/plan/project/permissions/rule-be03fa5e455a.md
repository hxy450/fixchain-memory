# 涉及权限的计划或插件记录，逐项查清目标权限和级别并落到 module.json5

审的是：计划与派工
触发（任一种）：
- 读到：规格里有 uses-permission 到 module.json5 的权限映射段，或应用 Dart 经 permission_handler 请求 Permission.xxx，或插件 OHOS 实现里有 requestPermissions / ohosPermissions；写错的样子：计划里没有任务的 output 含 module.json5 的 requestPermissions；或插件记录凭 pub get、HAP 构建、注册器标 verified / build_verified，没有逐项列出所需权限、映射和级别
适用范围：拆计划任务、做插件替代和插件最终核验时，处理源端或插件所需权限的那一处
做法：
- 列出所需的每个权限：规格的权限映射段、应用实际请求的每个 Permission.xxx、插件 OHOS 实现里申请的 ohos.permission；逐项查目标权限名、授权方式和权限级别
- 计划里让一个任务的 output 写明 module.json5 requestPermissions 的各项；插件记录逐项写映射和能否申请，映射为空或签名等级申请不到的不标 verified
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.permission.INTERNET：权限级别 normal，授权方式 system_grant：开放给所有应用的权限按权限名在这份清单里查级别和授权方式；system_grant 的只需在 requestPermissions 里声明（出处：permissions-for-all.md，ohos.permission.INTERNET）
- ohos.permission.READ_IMAGEVIDEO：权限级别 system_basic，列在受限开放权限里，普通应用要经 ACL 跨级申请：受限开放的权限按权限名在这份清单里查；normal 等级的应用直接声明申请不到（出处：restricted-permissions.md，ohos.permission.READ_IMAGEVIDEO 和「申请方式」）
针对本应用要查的：
- 应用和插件实际要的权限：规格的权限映射段；应用 Dart 代码里 permission_handler 的 Permission.xxx 调用及其门控流程；依赖的插件 ohos 目录和 Dart 源里的 requestPermissions、ohosPermissions、photoAccessHelper；逐个列出；按组请求的，到 dependency_overrides 指向的 OHOS 分支源码里读出每组映射到的 ohos.permission 列表，列表为空时看返回的状态。例：规格写 android.permission.INTERNET 时，目标是 ohos.permission.INTERNET
- 应用签名的 APL 等级：目标工程签名用的 Profile（HarmonyAppProvision 配置）里 bundle-info 的 apl 字段；normal 时不能直接申请 system_basic 级的权限，要用就走 ACL 申请，否则改走系统选择器
未核实：permission_handler 以外的权限插件，OHOS 分支里分组到 ohos.permission 的映射写在哪，族里规矩只查过 permission_handler
来源：3 张卡，2 个应用
- case-3cc99a6c512ab85ed874（app-photo-shop-flutter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-63a0f0066a7a0376735f（DeepAI全能PPT）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-96b417fb2e059d43f8bf（app-photo-shop-flutter）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
