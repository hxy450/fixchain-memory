# 相机拍摄的照片/录像写入图库而签名未获 WRITE_IMAGEVIDEO 受限授权时，走相机系统资产保存，不用 createAsset 系列

ID：`lesson-bc279ce222e98e0d5ede` · 版本：1 · 阶段：spec/execute · 主题：[app/media-library](index.md)

概要：相机产出走系统资产保存，不靠受限写权限

信号：`MediaStore`, `IS_PENDING`, `MediaRecorder`, `createAsset`, `createAssetRequest`, `WRITE_IMAGEVIDEO`, `photoAssetAvailable`, `saveCameraPhoto`, `discardCameraPhoto`, `AUTO_CREATE_CAMERA_SCENE`, `fileGenerationMode`

## 何时使用

规格提取与相机保存实现阶段，为相机拍摄的照片和视频选择媒体库写入接口、PhotoOutput 与 AVRecorder 的输出回调时

## 适用情境

源端经 MediaStore insert（IS_PENDING 两段写）或 MediaRecorder 输出文件保存相机拍摄结果；目标为普通应用，签名 profile 没有 WRITE_IMAGEVIDEO 的受限权限授权；可选接口有 photoAccessHelper.createAsset、MediaAssetChangeRequest.createAssetRequest、PhotoOutput 的 photoAvailable/photoAssetAvailable 与 AVRecorderConfig.fileGenerationMode。

## 例外与边界

- 签名 profile 已获 WRITE_IMAGEVIDEO 受限权限授权（ACL），并已在 module.json5 声明、运行时申请
- 保存的是应用自己生成或下载的图片而非相机拍摄结果：改用 SaveButton 安全控件或 showAssetsCreationDialog 保存确认

## 原因

WRITE_IMAGEVIDEO 在本机 SDK toolchains/lib/PermissionDefinitions.json（API 24，6.1.1.125）中为 user_grant、availableLevel=system_basic，普通应用须在签名 profile 申请受限权限才能获得，只在 module.json5 声明再运行时请求拿不到；createAsset、applyChanges、deleteAssets 都标 @permission ohos.permission.WRITE_IMAGEVIDEO（@ohos.file.photoAccessHelper.d.ts，API 24），无授权时返回 201。相机场景另有系统建资产的路线：PhotoOutput 的 photoAssetAvailable 交出系统已建的 PhotoAsset，由 MediaAssetChangeRequest.saveCameraPhoto 保存（@since 12）；AVRecorder 的 FileGenerationMode.AUTO_CREATE_CAMERA_SCENE 由系统创建媒体文件并忽略应用设置的 url，stop 后经 photoAssetAvailable 回调 PhotoAsset（@ohos.multimedia.media.d.ts，API 24）。官方相机开发准备文档把读写图片视频权限限于克隆、备份、同步公共目录并要求走受控权限申请，保存优先用安全控件（OpenHarmony docs camera-preparation.md，访问于 2026-10-23）；系统资产路线上 applyChanges 是否豁免该权限，d.ts 与相机文档均未明写。

## 做法

1. 照片：commitConfig 前为 PhotoOutput 注册 photoAssetAvailable，不同时注册 photoAvailable（两者同时注册会重启流且只有 photoAssetAvailable 生效，OpenHarmony docs camera-deferred-capture.md，访问于 2026-10-23）；该回调只带 PhotoAsset，不带拍摄请求 ID。需要做 EXIF、水印等后处理时，先从该资产读出字节，处理后用 new MediaAssetChangeRequest(asset) 的 addResource 写回，再 saveCameraPhoto() 并 applyChanges；不保存的资产调用 discardCameraPhoto()。
2. 录像：AVRecorderConfig.fileGenerationMode 默认设 AUTO_CREATE_CAMERA_SCENE，prepare 前订阅 AVRecorder 的 photoAssetAvailable；stop 后等到资产回调并 saveCameraPhoto 成功，再上报 URI 或释放录制器，超时、出错或释放时 discard。
3. 只有调用方显式给出输出 URI（如外部拍摄请求的 EXTRA_OUTPUT）时才用 APP_CREATE 打开该 fd 写入。系统建资产模式下拿不到可轮询的文件，源端按文件大小停止、分段续录一类行为按当前决策明确提示不支持，不静默忽略。
4. 规格把 MediaStore insert 或 MediaRecorder 映射到 photoAccessHelper 时，写明上述路线和 WRITE_IMAGEVIDEO 的受限属性；处理写权限移交项时核对签名 profile 是否含该授权，不只写“声明 + 运行时请求”。

## 可选检查

- 对系统资产路线的权限要求有疑问时，用不含 WRITE_IMAGEVIDEO 授权的签名构建在设备上各拍一张照片、录一段视频，确认 applyChanges 不返回 201 且图库可见

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [权限按目标 API 的 @permission 汇总](../capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md)（共享 1 张卡）
- [资产回调无请求 ID 时一拍一输出，超时退役不串帧](../camera/capture/lesson-8a1d50b9fdcdee8a5752.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-58c3f872e3c907fb4b68](../../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：diagnosis, rec-243081f648, rec-7d2e1437bc, rec-437623b648, rec-382965df0d
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
