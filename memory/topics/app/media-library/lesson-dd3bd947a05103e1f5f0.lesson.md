# 删除媒体改用 deleteAssets 时，先取得 WRITE_IMAGEVIDEO 授权，把确认框取消（可能同为 201）与失败分开处理

ID：`lesson-dd3bd947a05103e1f5f0` · 版本：1 · 阶段：execute/repair · 主题：[app/media-library](index.md)

概要：deleteAssets 先授权再删，取消与失败分开

信号：`deleteAssets`, `MediaAssetChangeRequest.deleteAssets`, `WRITE_IMAGEVIDEO`, `ContentResolver.delete`, `requestPermissionsFromUser`, `BusinessError`, `201`, `user deny`

## 何时使用

删除链实现与返修阶段，为 deleteAssets 编写授权、等待结果、提示映射和对应测试时

## 适用情境

源端删除本应用写入的 MediaStore 条目（ContentResolver.delete），失败通常只记日志；目标改用 photoAccessHelper.MediaAssetChangeRequest.deleteAssets，它先校验 WRITE_IMAGEVIDEO、再弹系统删除确认框，Promise 拒绝可能来自权限不足，也可能来自用户取消。

## 原因

deleteAssets 标 @permission ohos.permission.WRITE_IMAGEVIDEO，d.ts 只列 201 Permission denied、401、14000002、14000011，没有取消码（@ohos.file.photoAccessHelper.d.ts，API 24）；该权限为 system_basic 受限权限（本机 SDK PermissionDefinitions.json），没有授权时调用必然 201。一次设备实测中，用户在确认框点取消，Promise 以 code 201、message 'user deny' 拒绝，与权限不足同码；把 201 一律映射为“无权删除”会在取消时误报，假定的取消码（如 14000011）也与设备不符。'user deny' 是否为稳定契约尚未核实。

## 做法

1. 确认签名 profile 含 WRITE_IMAGEVIDEO 受限授权，在 module.json5 声明（带 reason）；用户发起删除时 requestPermissionsFromUser 并复核授予，再调用 deleteAssets。
2. await deleteAssets 的结果：只在成功后清除最近媒体记录、提示已删除；失败保留记录和当前缩略图。
3. 把“确认框取消”列为独立结果：先在设备上点一次取消，记下拒绝路径（同步抛出还是 Promise 拒绝）与 code/message，再写映射；按实测特征识别取消（已观察到异步拒绝 201 + 'user deny'），只记日志、不提示、不清记录；同步异常与授权失败才按当前契约提示失败或缺权限。

## 可选检查

- 测试替身的取消值用设备实测值，分别覆盖成功、确认框取消、同步异常与授权失败；已有“拒绝或取消”合并用例先拆开再改期望

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [权限按目标 API 的 @permission 汇总](../capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-68b4a8d96f961e70b0c9](../../../../store/cases/case-68b4a8d96f961e70b0c9/386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2.json) · 结论：diagnosis, rec-1a6519cdca
  卡片版本：`386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2`
- [case-cd4f1c37e7e321bb50d6](../../../../store/cases/case-cd4f1c37e7e321bb50d6/4fb0ffcdece4d841ec76fdecf759848b61eb9cfea967109883a5f5f07c53f8f2.json) · 结论：diagnosis, rec-e2ac5a1f41, rec-4fc0257edb, rec-be778a07e3
  卡片版本：`4fb0ffcdece4d841ec76fdecf759848b61eb9cfea967109883a5f5f07c53f8f2`
