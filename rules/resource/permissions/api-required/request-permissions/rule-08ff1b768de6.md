# 代码调 setWindowPrivacyMode 时，module.json5 声明 PRIVACY_WINDOW

审的是：资源
触发（任一种）：
- 写错的样子：代码里有 setWindowPrivacyMode(true/false)，module.json5 没有 requestPermissions 或其中没有 ohos.permission.PRIVACY_WINDOW；运行时 201 PERMISSION_DENIED 只被 hilog 记下
适用范围：目标代码调用带 @permission 的窗口隐私接口时的 module.json5；按文档 PRIVACY_WINDOW 从 API 11 起是 normal
做法：
- 在 module.json5 的 requestPermissions 加 { "name": "ohos.permission.PRIVACY_WINDOW" }；它是 system_grant + normal，只需声明、安装即授予，不加运行时申请
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.permission.PRIVACY_WINDOW：权限级别 normal，授权方式 system_grant：只需声明，不涉及 ACL 或签名授权（出处：permissions-for-all.md，ohos.permission.PRIVACY_WINDOW）
- setWindowPrivacyMode(isPrivacyMode: boolean): Promise<void>，@permission ohos.permission.PRIVACY_WINDOW：声明这项权限的依据（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowPrivacyMode）
- setWindowPrivacyMode(isPrivacyMode: boolean, callback: AsyncCallback<void>): void：同族接口：回调形式，同样带 @permission ohos.permission.PRIVACY_WINDOW（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowPrivacyMode）
- 声明后开启安全模式截屏变黑、关闭后恢复：修法（出处：卡里修好并验证过）
针对本应用要查的：
- 其他 @permission 的授予方式和级别：鸿蒙 SDK 的 openharmony/toolchains/lib/PermissionDefinitions.json 按权限名找（文件名检索不区分大小写），或文档 permissions-for-all.md 的同名小节；读 grantMode、availableLevel；system_grant 且 normal 的只需在 module.json5 声明
来源：1 张卡，1 个应用
- case-0524405ca4510433cf06（GameOfLife）：做法第 1 步 ← 建议 3、诊断；取值 4 ← 诊断
