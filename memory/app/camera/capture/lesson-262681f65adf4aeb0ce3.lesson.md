# 相机拍摄的照片与录像走相机系统资产保存，不默认用需受限写权限 WRITE_IMAGEVIDEO 的 createAsset 系列

ID：`lesson-262681f65adf4aeb0ce3` · 版本：1

[本主题](index.md)

## 何时使用

相机拍照与录像的保存实现阶段，为相机产出的照片、视频选择媒体库写入接口与 PhotoOutput、AVRecorder 输出回调时；规格提取写 MediaStore → photoAccessHelper 映射行时

## 适用情境

源端经 MediaStore insert（IS_PENDING 两段写）或 MediaRecorder 输出文件保存拍摄结果；目标是没有受限权限签名授权的普通应用，候选有 photoAccessHelper createAsset/createAssetRequest、PhotoOutput 的 photoAvailable/photoAssetAvailable、AVRecorderConfig.fileGenerationMode 的 APP_CREATE 与 AUTO_CREATE_CAMERA_SCENE。

## 例外与边界

- 工程已具备 ohos.permission.WRITE_IMAGEVIDEO 的受限权限签名授权，且当前决策要求应用自建资产
- 调用方（如外部拍照/录像请求）显式给出输出 URI 时，写入该 URI

## 原因

createAsset 系列需要 WRITE_IMAGEVIDEO，它是受限开放权限，只声明并运行时申请拿不到，写入返回 201；相机场景另有不需要该权限的系统资产路线。photoAssetAvailable 只携带 PhotoAsset、不带 capture ID，超时后仍保持订阅的输出会把迟到的资产交给下一次拍摄。

## 做法

1. 照片：commitConfig 前为 PhotoOutput 注册 photoAssetAvailable（不同时订阅 photoAvailable），用 requestImageData 读字节完成 EXIF、水印等处理，再以 MediaAssetChangeRequest(asset) 的 addResource、saveCameraPhoto、applyChanges 写回同一资产；未使用的资产 discard。
2. 录像：默认 fileGenerationMode 设为 AUTO_CREATE_CAMERA_SCENE，prepare 前订阅 photoAssetAvailable，stop 后等资产保存成功再上报 URI 或释放录制器；该模式下拿不到可轮询的 fd，文件大小上限与续录要显式决策（如提示不支持），不静默失效；只有调用方给出输出 URI 时才用 APP_CREATE + fd。
3. 资产回调没有请求 ID：按一次拍摄独占当前输出设计，超时或失败时退役该 PhotoOutput 并重建会话，恢复完成后再接受下一次拍摄，不把迟到的资产交给当时的结果接收者。
4. 选媒体库写入 API 前查 d.ts 的 @permission 及该权限是否受限；读 SDK 时出现的模式枚举（如 FileGenerationMode）逐项评估，不凭记忆中的示例跳过。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-58c3f872e3c907fb4b68](../../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:6
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
