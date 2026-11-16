# 相机照片走 photoAssetAvailable + saveCameraPhoto，不用 createAsset

审的是：代码
触发（任一种）：
- 读到：源端拍照后经 `MediaStore` insert（`IS_PENDING` 两段写）保存照片；规格只写「photoAccessHelper PhotoAsset 创建/提交」；写错的样子：目标用 `photoAvailable` 取字节，再经 `createAssetRequest` / `createAsset` 两段写进媒体库，无受限权限授权时报 201
适用范围：目标是没有受限权限签名授权的普通应用，保存相机拍摄的照片时
做法：
- 在 commitConfig 前给 PhotoOutput 注册 photoOutput.on('photoAssetAvailable', (err, asset) => …)，不同时订阅 photoAvailable
- 拿到资产后 MediaAssetManager.requestImageData 读字节、做完 EXIF 水印等处理，再 req = new MediaAssetChangeRequest(asset)；req.addResource(ResourceType.IMAGE_RESOURCE, data)；req.saveCameraPhoto()；await helper.applyChanges(req)
- 没用上的资产调 req.discardCameraPhoto() 丢弃
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- on(type: 'photoAssetAvailable', callback: AsyncCallback<photoAccessHelper.PhotoAsset>): void：PhotoOutput 交付相机系统创建的照片资产（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.camera.d.ts，PhotoOutput.on('photoAssetAvailable')）
- photoAssetAvailable 和 photoAvailable 同时注册会导致流重启，仅 photoAssetAvailable 生效；不建议同时注册：只订阅 photoAssetAvailable（出处：camera-deferred-capture.md，设置拍照photoAssetAvailable的回调）
- static requestImageData(context: Context, asset: PhotoAsset, requestOptions: RequestOptions, dataHandler: MediaAssetDataHandler<ArrayBuffer>): Promise<string>：按资产读取图片字节（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetManager.requestImageData）
- addResource(type: ResourceType, data: ArrayBuffer): void；saveCameraPhoto(): void；saveCameraPhoto(imageFileType: ImageFileType): void；discardCameraPhoto(): void：MediaAssetChangeRequest 上写回字节、保存或丢弃相机照片（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，MediaAssetChangeRequest.addResource、saveCameraPhoto、discardCameraPhoto）
- createAsset(photoType: PhotoType, extension: string, options?: CreateOptions): Promise<string>，@permission ohos.permission.WRITE_IMAGEVIDEO，无权限时抛 201：应用自建资产要受限写权限（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoAccessHelper.createAsset）
- photoAssetAvailable 取资产 + requestImageData 处理 + saveCameraPhoto 写回同一资产后，没有签名授权的构建也能存入相册：验证过的照片保存路线（出处：卡里修好并验证过）
未核实：卡里的效果在目标 API 24 上验证，本机核对用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-58c3f872e3c907fb4b68（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 6 ← 诊断
