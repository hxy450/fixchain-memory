# deleteAssets 前先确认图库写权限，await 结果，201 与其他失败分别提示

审的是：代码
触发（任一种）：
- 读到：源端删除自有 MediaStore 条目（contentResolver.delete），失败静默、count > 0 才提示；写错的样子：目标直接调用 MediaAssetChangeRequest.deleteAssets，没有 WRITE_IMAGEVIDEO 的授权检查或请求，没有 await 结果，失败只记日志，删除前就清理了最近媒体
适用范围：迁移媒体删除链（photoAccessHelper 删除受权限和系统确认约束）时
做法：
- 用户删除时先用 checkAccessToken 查 ohos.permission.WRITE_IMAGEVIDEO，未授予就 requestPermissionsFromUser 请求并再次复核授予结果
- await deleteAssets(context, uriList)；catch 里按 err.code === 201 和其他失败分别给可见提示；只在成功后清理最近媒体并提示已删除
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static deleteAssets(context: Context, uriList: Array<string>): Promise<void>，@throws { BusinessError } 201 - Permission denied：异步，缺权限抛 201（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.deleteAssets）
- checkAccessToken(tokenID: number, permissionName: Permissions): Promise<GrantStatus>：查权限是否已授予（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.checkAccessToken）
- requestPermissionsFromUser(context: Context, permissionList: Array<Permissions>): Promise<PermissionRequestResult>：运行时弹窗请求 user_grant 权限（出处：鸿蒙 SDK 的 ets/api/@ohos.abilityAccessCtrl.d.ts，AtManager.requestPermissionsFromUser）
未核实：卡里环境是鸿蒙 6.1.1(24)，本机按 API 23 核对
来源：1 张卡，1 个应用
- case-68b4a8d96f961e70b0c9（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 4、诊断
