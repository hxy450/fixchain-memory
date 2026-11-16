# 普通签名应用的 module.json5 不为选图声明 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO

审的是：资源
触发（任一种）：
- 读到：插件 Dart 常量或 OHOS 实现里默认申请 `ohos.permission.READ_IMAGEVIDEO` / `ohos.permission.WRITE_IMAGEVIDEO`；写错的样子：module.json5 的 requestPermissions 里加了 `ohos.permission.READ_IMAGEVIDEO` 或 `ohos.permission.WRITE_IMAGEVIDEO`，安装报 9568289
适用范围：APL 为 normal 的应用，为图片选择补宿主权限声明时
做法：
- 撤回这两项权限声明，连同为它加的 string.json 授权说明串；选图改走系统选择器（见同卡代码类规矩）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.permission.READ_IMAGEVIDEO：权限级别 system_basic，授权方式 user_grant：受限开放权限，normal 应用要走 ACL 才能申请（出处：restricted-permissions.md，ohos.permission.READ_IMAGEVIDEO）
- READ_IMAGEVIDEO 和 WRITE_IMAGEVIDEO 为受控权限，使用前需要额外申请 ACL 白名单：相册管理模块的开发准备里写明的前提（出处：photoAccessHelper-preparation.md，申请相册管理模块功能相关权限）
- 9568289 install failed due to grant request permissions failed：normal 应用声明了 system_basic 级权限时的安装报错（出处：bm-tool.md，9568289 权限请求失败导致安装失败）
针对本应用要查的：
- 应用签名的 APL 等级：目标工程签名用的 Profile（HarmonyAppProvision 配置）里 bundle-info 的 apl 字段；是 normal 就不声明这两项；已按 ACL 申请到的才可以保留
来源：1 张卡，1 个应用
- case-96b417fb2e059d43f8bf（app-photo-shop-flutter）：做法第 1 步 ← 诊断、建议 2
