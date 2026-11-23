# APPROXIMATELY_LOCATION 与 LOCATION 成组声明、申请与判定：要精确定位也两项同申，任一授予就继续定位

## 何时使用

定位能力实现阶段，编写定位权限的 module.json5 声明、运行期申请与申请结果判定时

## 适用情境

目标同时申请 ohos.permission.APPROXIMATELY_LOCATION 与 ohos.permission.LOCATION；工程 skill 提供通用的权限辅助模板（遍历 authResults，任一不为 0 即返回失败）；功能规格只要求两项权限都声明、都处理。源端以 ACCESS_FINE_LOCATION 与 ACCESS_COARSE_LOCATION 一起请求；工程的通用权限表可能只列了 ohos.permission.LOCATION。

## 原因

用户可以只授予模糊位置，此时精确权限为拒绝；按“全部授予”判定会把这种情况当成无权限，定位按钮直接失败。来源中实现者照搬通用模板写出全部授予的循环，skill 与规格都没有说明定位权限组可以只授予模糊位置。另一应用中，实现者把源端的精确+模糊两项压成只申请 LOCATION，module.json5 也只声明这一项，系统判定不需要弹窗，定位入口没有授权弹窗；规格指向的核验 skill 写明 LOCATION 不能单独申请，实现者没有读它，只参考了通用权限表。

## 做法

1. authResults 中任一定位权限授予（至少模糊位置为 0）就继续定位；只有精确权限缺失时按降级精度处理，两项都拒绝才走失败提示。
2. Android 的 ACCESS_FINE_LOCATION + ACCESS_COARSE_LOCATION 映射为 LOCATION + APPROXIMATELY_LOCATION：需要精确定位时，module.json5 的 requestPermissions 与 requestPermissionsFromUser 的列表都同时包含两项，LOCATION 不单独申请；调用定位 API 前查 d.ts 的 @permission 注解，不以通用常用权限表代替。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕geoLocationManager.getCurrentLocation 声明的 @permission 是 ohos.permission.APPROXIMATELY_LOCATION
- 〔原因 / 做法第 1 步〕前台定位只允许两种申请方式：只申请 APPROXIMATELY_LOCATION 得模糊位置（精确度 5 公里）；同时申请 APPROXIMATELY_LOCATION 和 LOCATION 得精准位置（米级）
- 〔做法第 2 步〕API 9 及之后无法单独申请 ohos.permission.LOCATION（单独申请得不到位置），它要与 APPROXIMATELY_LOCATION 一起才可申请
- 〔做法第 2 步〕APPROXIMATELY_LOCATION 与 LOCATION 是 user_grant 权限，module.json5 里 reason、usedScene 必填，usedScene.when 只能填 inuse 或 always
- 〔做法第 1 步〕requestPermissionsFromUser 返回的 authResults 与申请列表逐项对应：0 已授予，-1 未授予，2 请求无效
- 〔做法第 2 步〕缺少接口 @permission 要求的权限时编译照常通过，调用时以 BusinessError 201 - Permission denied 失败
