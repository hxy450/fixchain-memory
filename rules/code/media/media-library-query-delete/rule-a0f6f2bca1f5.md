# deleteAssets 被拒绝时把用户取消单列为静默结果，不把 201 一律当权限不足

审的是：代码
触发（任一种）：
- 读到：目标删除走 photoAccessHelper.MediaAssetChangeRequest.deleteAssets（先校验 WRITE_IMAGEVIDEO、再弹系统删除确认框）；源端删除失败只记日志不提示；已有测试把 `rejected or cancelled` 删除定为不提示；写错的样子：catch 里把 err.code === 201 一律映射成「无权删除」提示、其余拒绝映射成删除失败提示，用户在确认框点取消也弹提示或清掉媒体记录
适用范围：调用带系统确认框的媒体删除接口、处理 Promise 拒绝和用户提示的代码
做法：
- 先同步取得 deleteAssets 返回的 Promise；同步抛出的异常和权限申请失败照常走失败提示
- Promise 异步拒绝且 err.code === 201 && err.message === 'user deny' 时按用户取消处理：只记 info 日志，不提示，不清除媒体记录
- 其余拒绝才显示失败或权限提示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- static deleteAssets(context: Context, assets: Array<PhotoAsset>): Promise<void>；static deleteAssets(context: Context, uriList: Array<string>): Promise<void>：MediaAssetChangeRequest 的删除，删除的文件进回收站，需 ohos.permission.WRITE_IMAGEVIDEO（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.deleteAssets）
- @throws 201 - Permission denied；14000011 - System inner fail（声明里没有单列用户取消的码）：声明里的错误码；取消不在其中（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.deleteAssets）
- 确认框点取消时 deleteAssets 的 Promise 异步拒绝，code 201、message 'user deny'：设备上取消的实际返回；按 201 一律报权限不足时会误报成没有删除权限（出处：卡里修好并验证过）
- createDeleteRequest(uriList: Array<string>): Promise<void>（@deprecated since 11，改用 MediaAssetChangeRequest#deleteAssets）：同族接口：旧的弹删除确认框接口，权限错误码是 13900012（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoAccessHelper.createDeleteRequest）
未核实：'user deny' 是否稳定契约，卡里也没核到；卡里设备是 API 24（6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-cd4f1c37e7e321bb50d6（opencamera-hmos）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 1；做法第 3 步 ← 建议 1、建议 2；取值 3 ← 诊断
