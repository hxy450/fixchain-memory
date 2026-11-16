# 媒体库的查询和删除（photoAccessHelper.getAssets、MediaAssetChangeRequest.deleteAssets）

agent 会看到什么：读到源端用 MediaStore 经 ContentResolver.query 查最近媒体、经 contentResolver.delete 删自有条目；产物里 photoAccessHelper.getAssets、MediaAssetChangeRequest.deleteAssets 调用前的 READ_IMAGEVIDEO / WRITE_IMAGEVIDEO 核对、有没有 await、catch 里按 err.code（201、'user deny'）分的提示，以及删除取消的测试替身

## 规矩

- rule-1346e18fd8f1｜整库 getAssets 前先核 READ_IMAGEVIDEO，查询失败不清空缩略图，画廊入口用自存 URI｜读到：源端用 MediaStore 查询最近媒体给画廊按钮取缩略图；写错：photoAccessHelper.getAssets 整库查询前没有权限检查；查询失败就 resolve(null) 并把画廊缩略图置空；没有记录应用自己保存的 URI
- rule-45a4f89d8a8b｜deleteAssets 前先确认图库写权限，await 结果，201 与其他失败分别提示｜读到：源端删除自有 MediaStore 条目（contentResolver.delete），失败静默、count > 0 才提示；写错：目标直接调用 MediaAssetChangeRequest.deleteAssets，没有 WRITE_IMAGEVIDEO 的授权检查或请求，没有 await 结果，失败只记日志，删除前就清理了最近媒体
- rule-a0f6f2bca1f5｜deleteAssets 被拒绝时把用户取消单列为静默结果，不把 201 一律当权限不足｜读到：目标删除走 photoAccessHelper.MediaAssetChangeRequest.deleteAssets（先校验 WRITE_IMAGEVIDEO、再弹系统删除确认框）；源端删除失败只记日志不提示；已有测试把 `rejected or cancelled` 删除定为不提示；写错：catch 里把 err.code === 201 一律映射成「无权删除」提示、其余拒绝映射成删除失败提示，用户在确认框点取消也弹提示或清掉媒体记录
- rule-ef9fca324bfe｜删除取消的测试替身用设备实测的 201 + 'user deny'，取消和失败分开断言｜读到：已有回归测试里 `rejected or cancelled` 删除用例断言不提示、保留当前缩略图和持久目标；写错：测试把取消假定成 `14000011` 之类没核实的码并期望失败提示，或者把 `rejected or cancelled` 用例的期望从无提示改成失败提示
