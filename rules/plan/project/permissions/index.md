# 规格和插件要的权限与 module.json5 的 requestPermissions

agent 会看到什么：规格有 uses-permission 映射段、应用经 permission_handler 请求 Permission.xxx、插件 OHOS 实现里有 requestPermissions / ohosPermissions，计划没有任务落到 module.json5，或插件记录凭构建通过标 verified / build_verified

## 通用查法

### 涉及权限的计划或插件记录，逐项查清目标权限和级别并落到 module.json5

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

## 规矩

- rule-7c5e7a95b87b｜规格写了网络权限必配时，计划要有任务落到 module.json5 的权限声明｜读到：规格里有权限映射段：android.permission.INTERNET → ohos.permission.INTERNET（必配）、ACCESS_NETWORK_STATE → ohos.permission.GET_NETWORK_INFO，或写明 requestPermissions 要配哪几项；写错：任务拆分里没有任何任务的 input 指向规格的权限段，也没有任务的 output 含 module.json5 的 requestPermissions；网络任务的 input 只指向网络段
- rule-f1f36ffaa235｜标插件 verified 前，检索它 OHOS 实现的权限调用并与宿主 module.json5 对账｜读到：插件的 OHOS 实现或 Dart 常量里有 `requestPermissions`、`ohosPermissions`、`photoAccessHelper`、`ohos.permission.READ_IMAGEVIDEO`；写错：`final_verification` 把插件标 verified，依据只有 pub get、HAP 构建、注册器和 solutions 文件；没有列出插件所需权限，也没和宿主 module.json5 的 requestPermissions 对账
- rule-3df0a1c0faed｜权限插件换成 OHOS 同包分支时，逐组核对应用实际请求的权限映射，不以构建通过放行｜读到：应用 Dart 代码经 permission_handler 请求 Android 专用权限组（Permission.storage、Permission.photos 等），并用授予结果门控下载、保存等核心流程；写错：插件替代记录里 permission_handler 只写成同包同 API 分支（F2）的 dependency_overrides，solution JSON 的 methods 为空，以注册器加 HAP 构建标成 build_verified，没有逐组写权限映射
- rule-07f0dcb3010a｜派工接入 OAID 采集时，把 module.json5 和字符串资源一起划进写域｜读到：任务要接入 identifier.getOAID（需要 APP_TRACKING_CONSENT 权限）；写错：派工说明的写域只列服务代码文件，没有 module.json5 和 base / en_US 的 string.json，权限声明只能被记成缺口
- rule-44c8c3166205｜已批零权限决策与 API 的 @permission 冲突时，核实级别后上报改判，不挂 deferred｜读到：派工写「module.json5 零权限声明」并引一条已批决策，而 d.ts 里所用 API 标了 @permission；写错：交回或占位登记把冲突挂成 deferred，理由是授予级别「未核实」或凭记忆写成 system_basic + ACL；交回写 module.json5 零改动，相关设备验收被列为「裁定前必败」
- rule-f1601aab7646｜权限类占位收口时核对 module.json5 声明和权限能否获得，不凭别条说明标 resolved｜读到：占位登记里有权限缺口条目（如媒体库写权限 `ohos.permission.WRITE_IMAGEVIDEO` 声明缺失），交给后续切片收口；写错：该条目被标为 resolved，理由是别处写的「无存储权限门」之类说明；`module.json5` 里没有对应的 `requestPermissions`，也没核对权限是否受限
