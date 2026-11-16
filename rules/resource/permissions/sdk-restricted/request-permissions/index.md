# module.json5 的 requestPermissions 权限声明

agent 会看到什么：要在 module.json5 的 requestPermissions 里声明 ohos.permission.*（第三方 SDK 文档要求的、插件默认申请的），或真机安装因权限被拒；产物里声明了受限、系统级或所调接口没要求的权限

## 通用查法

### module.json5 声明权限前，按权限级别、授权方式和接口 @permission 定去留

审的是：资源
触发（任一种）：
- 读到：要在 module.json5 声明 ohos.permission.*：第三方 SDK 文档要求、插件默认申请，或真机安装报 9568289；写错的样子：requestPermissions 里有应用签名等级申请不到的权限（system_basic 级），或有所调接口 @permission 没要求的；留下的 user_grant 权限缺 reason、usedScene
适用范围：目标工程 module.json5 的 requestPermissions，新增、照搬或因安装失败删减权限声明时
做法：
- 按权限名在权限文档里读权限级别和授权方式：级别高于应用签名 APL（普通应用为 normal）的不声明，为它加的 string.json 说明串一并撤回
- 只留所调接口在鸿蒙 SDK 声明里 @permission 写到的权限，第三方文档或插件默认多列的不照抄；安装失败要删时只删没被实际调用的接口要的那条
- 留下的 user_grant 权限带 "reason": "$string:…" 和 "usedScene": { "abilities": ["…"], "when": "inuse" }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 每个权限的小节写明「权限级别」（normal、system_basic 等）和「授权方式」（user_grant、system_grant）：判断一项权限普通应用能不能声明、要不要带 reason 和 usedScene 的依据（出处：permissions-for-all-user.md、restricted-permissions.md、permissions-for-system-apps.md，按权限名的小节）
- 申请 user_grant 权限时 reason 必填、usedScene 必填，when 只能填 inuse 或 always：留下的 user_grant 权限这一条声明要带的字段（出处：declare-permissions.md，在配置文件中声明权限）
- 9568289 install failed due to grant request permissions failed：normal 应用声明了 system_basic 级权限时的安装报错（出处：bm-tool.md，9568289 权限请求失败导致安装失败）
针对本应用要查的：
- 应用签名的 APL 等级：目标工程签名用的 Profile（HarmonyAppProvision 配置）里 bundle-info 的 apl 字段；是 normal 就只声明级别为 normal 的权限；更高级别的要已按 ACL 申请到才保留
- 每项权限的级别和授权方式：OpenHarmony 文档 security/AccessToken 下的 permissions-for-all-user.md、restricted-permissions.md、permissions-for-system-apps.md，按权限名找小节；读小节里的「权限级别」「授权方式」两行。例：ohos.permission.ACCESS_BLUETOOTH 是 normal、user_grant，ohos.permission.MANAGE_BLUETOOTH 是 system_basic、system_grant
- 所调接口要求的权限：鸿蒙 SDK 里所调接口的声明（.d.ts）注释中的 @permission；只声明实际调用到的接口 @permission 写到的权限
未核实：接口要求的权限以鸿蒙 SDK 声明里的 @permission 为准，出自卡的建议，族里规矩没有引声明原文核对
来源：2 张卡，2 个应用
- case-96b417fb2e059d43f8bf（app-photo-shop-flutter）：做法第 1 步 ← 诊断、建议 2
- case-fa0174cd489361d7586d（骑行记录）：做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3

## 规矩

- rule-e206835fd44d｜权限按所调接口的 @permission 声明，不照第三方文档加 MANAGE_BLUETOOTH｜读到：第三方（如打印机）SDK 文档要求声明 ohos.permission.MANAGE_BLUETOOTH；或真机安装因系统级权限被拒；写错：module.json5 的 requestPermissions 里有 ohos.permission.MANAGE_BLUETOOTH；或删权限时连带把应用内开关改成跳系统设置
- rule-2bd0ce4315cf｜普通签名应用的 module.json5 不为选图声明 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO｜读到：插件 Dart 常量或 OHOS 实现里默认申请 `ohos.permission.READ_IMAGEVIDEO` / `ohos.permission.WRITE_IMAGEVIDEO`；写错：module.json5 的 requestPermissions 里加了 `ohos.permission.READ_IMAGEVIDEO` 或 `ohos.permission.WRITE_IMAGEVIDEO`，安装报 9568289
