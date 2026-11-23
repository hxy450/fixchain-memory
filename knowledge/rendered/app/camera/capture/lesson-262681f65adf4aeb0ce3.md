# 相机拍摄的照片与录像走相机系统资产保存，不默认用需受限写权限 WRITE_IMAGEVIDEO 的 createAsset 系列

## 何时使用

相机拍照与录像的保存实现阶段，为相机产出的照片、视频选择媒体库写入接口与 PhotoOutput、AVRecorder 输出回调时（源端存进系统相册、目标没有 WRITE_IMAGEVIDEO 受限权限签名授权）；规格提取写 MediaStore → photoAccessHelper 映射行时

## 适用情境

源端经 MediaStore insert（IS_PENDING 两段写）或 MediaRecorder 输出文件保存拍摄结果；目标是没有受限权限签名授权的普通应用，候选有 photoAccessHelper createAsset/createAssetRequest、PhotoOutput 的 photoAvailable/photoAssetAvailable、AVRecorderConfig.fileGenerationMode 的 APP_CREATE 与 AUTO_CREATE_CAMERA_SCENE。

## 例外与边界

- 工程已具备 ohos.permission.WRITE_IMAGEVIDEO 的受限权限签名授权，且当前决策要求应用自建资产
- 调用方（如外部拍照/录像请求）显式给出输出 URI 时，写入该 URI
- 源端把照片或录像只写在应用私有目录、不进系统相册的，目标照源端写应用沙箱（照片走 photoAvailable 取字节、录像用 APP_CREATE + 沙箱文件 fd），不改成相机系统资产：saveCameraPhoto 与 AUTO_CREATE_CAMERA_SCENE 会把文件存进相册。

## 原因

createAsset 系列需要 WRITE_IMAGEVIDEO，它是受限开放权限，只声明并运行时申请拿不到，写入返回 201；相机场景另有不需要该权限的系统资产路线。photoAssetAvailable 只携带 PhotoAsset、不带 capture ID，超时后仍保持订阅的输出会把迟到的资产交给下一次拍摄。

## 做法

1. 照片：commitConfig 前为 PhotoOutput 注册 photoAssetAvailable（不同时订阅 photoAvailable），用 requestImageData 读字节完成 EXIF、水印等处理，再以 MediaAssetChangeRequest(asset) 的 addResource、saveCameraPhoto、applyChanges 写回同一资产；未使用的资产 discard。
2. 录像：默认 fileGenerationMode 设为 AUTO_CREATE_CAMERA_SCENE，prepare 前订阅 photoAssetAvailable，stop 后等资产保存成功再上报 URI 或释放录制器；该模式下拿不到可轮询的 fd，文件大小上限与续录要显式决策（如提示不支持），不静默失效；只有调用方给出输出 URI 时才用 APP_CREATE + fd。
3. 资产回调没有请求 ID：按一次拍摄独占当前输出设计，超时或失败时退役该 PhotoOutput 并重建会话，恢复完成后再接受下一次拍摄，不把迟到的资产交给当时的结果接收者。
4. 选媒体库写入 API 前查 d.ts 的 @permission 及该权限是否受限；读 SDK 时出现的模式枚举（如 FileGenerationMode）逐项评估，不凭记忆中的示例跳过。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 4 步〕PhotoAccessHelper.createAsset 的各个重载和 PhotoAccessHelper.applyChanges 都声明需要 ohos.permission.WRITE_IMAGEVIDEO，无权限时抛 201；文档另写可用安全控件或授权弹窗创建媒体资源
- 〔原因〕ohos.permission.WRITE_IMAGEVIDEO 列在受限开放权限里，权限级别 system_basic，授权方式为用户授权（user_grant）
- 〔原因 / 例外与边界〕APL 为 normal 的应用要用受限开放权限，需要把 HarmonyAppProvision 配置的 bundle-info > apl 声明为 system_basic 及以上并重新签名（ACL 跨级申请）
- 〔原因〕模拟器上没有受限权限签名授权的构建，用 createAsset 系列写入相册时系统返回 201
- 〔做法第 1 步〕没有 WRITE_IMAGEVIDEO 签名授权的构建上，对 PhotoOutput 经 photoAssetAvailable 交付的资产，用 requestImageData 读字节、MediaAssetChangeRequest 的 addResource 与 saveCameraPhoto 写回并提交后，照片存入了相册（applyChanges 的声明和文档标的是需要 WRITE_IMAGEVIDEO）
- 〔做法第 2 步〕fileGenerationMode 为 AUTO_CREATE_CAMERA_SCENE 时，stop 后由 photoAssetAvailable 交付的录像资产经 saveCameraPhoto 存入了相册
- 〔原因 / 做法第 1、3 步〕PhotoOutput.on('photoAssetAvailable') 的回调参数只有 PhotoAsset，不带 capture ID；声明写明目前不允许在 on() 的回调里用 off() 注销该回调
- 〔做法第 1 步〕Session 开始后在已注册 photoAssetAvailable 的 PhotoOutput 上再注册 photoAvailable，两者同时注册会导致流被重启，仅 photoAssetAvailable 生效
- 〔做法第 2 步〕FileGenerationMode.APP_CREATE 由应用自行在沙箱创建媒体文件；AUTO_CREATE_CAMERA_SCENE 由系统创建媒体文件，会忽略应用设置的 url
- 〔做法第 2 步〕AVRecorder.on('photoAssetAvailable') 只在 prepare 配置的 FileGenerationMode 为系统创建媒体文件时、stop 结束后回调系统创建的 PhotoAsset；重复订阅时以最后一次订阅的回调为准
