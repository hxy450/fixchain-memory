# 标插件 verified 前，检索它 OHOS 实现的权限调用并与宿主 module.json5 对账

审的是：计划与派工
触发（任一种）：
- 读到：插件的 OHOS 实现或 Dart 常量里有 `requestPermissions`、`ohosPermissions`、`photoAccessHelper`、`ohos.permission.READ_IMAGEVIDEO`；写错的样子：`final_verification` 把插件标 verified，依据只有 pub get、HAP 构建、注册器和 solutions 文件；没有列出插件所需权限，也没和宿主 module.json5 的 requestPermissions 对账
适用范围：Flutter 插件适配 OHOS，标记插件 verified 之前
做法：
- 在插件的 ohos 目录和 Dart 源里搜 requestPermissions、ohosPermissions、photoAccessHelper，列出所需权限，逐项对宿主 module.json5 的 requestPermissions
- 所需权限是 READ_IMAGEVIDEO / WRITE_IMAGEVIDEO 这类媒体库权限时，写明当前签名等级能否申请；普通应用申请不了的不标 verified，登记为改走系统选择器
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.permission.READ_IMAGEVIDEO、ohos.permission.WRITE_IMAGEVIDEO：权限级别 system_basic，用户授权，列在受限开放权限里：normal 等级的应用要走 ACL 跨级申请才能用（出处：restricted-permissions.md，ohos.permission.READ_IMAGEVIDEO、ohos.permission.WRITE_IMAGEVIDEO 两节）
- APL 为 normal 的应用声明了 system_basic 权限，安装报 9568289 install failed due to grant request permissions failed：补声明后装不上，就是签名等级不够（出处：bm-tool.md，9568289 权限请求失败导致安装失败）
针对本应用要查的：
- 应用签名的 APL 等级：目标工程签名用的 Profile（HarmonyAppProvision 配置）里 bundle-info 的 apl 字段；normal 时不能申请 system_basic 级的权限；要用就得走 ACL 申请，否则改走系统选择器
来源：1 张卡，1 个应用
- case-96b417fb2e059d43f8bf（app-photo-shop-flutter）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
