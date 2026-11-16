# 系统选择器和相册保存控件

agent 会看到什么：读到源端用 Intent（ACTION_OPEN_DOCUMENT、EXTRA_ALLOW_MULTIPLE）、自建相册页或 MediaStore 选取和保存图片、音频、文件，产物里是 PhotoViewPicker、AudioViewPicker、DocumentViewPicker、photoAccessHelper 和 SaveButton 的写法

## 规矩

- rule-469bafc42ee0｜相册选一张图作持久配置时用 PhotoViewPicker 单选，不走依赖 getAlbums 的自建相册页｜读到：安卓源单图选择走应用自建的相册 Activity，选出（裁剪后）的图片文件路径写进会保存的配置；写错：目标这个入口 push 自建相册页，该页靠 PhotoAccessHelper.getAlbums 全量查询，页头还有未完成的权限/相册绑定 TODO（P-S…-UNC- 一类未决记号），module.json5 没声明 ohos.permission.READ_IMAGEVIDEO
- rule-efe5785e8c8c｜photoAccessHelper 找音频时不写 PhotoType.AUDIO，改用 AudioViewPicker｜读到：规格写「MediaLibraryKit 查询音频资产」，而 photoAccessHelper 参考或声明里按类型筛选只有 PhotoType.IMAGE / PhotoType.VIDEO；写错：代码里出现 PhotoType.AUDIO，例如 predicates.equalTo(PHOTO_TYPE, PhotoType.AUDIO)
- rule-145b6b8ed299｜EXTRA_ALLOW_MULTIPLE 不限数量时，maxSelectNumber 取上限 500｜读到：Intent.EXTRA_ALLOW_MULTIPLE 设为 true，源端没有数量限制；写错：maxSelectNumber 写成比 500 小的「安全值」（如 100），或没写（DocumentSelectOptions 默认 1）
- rule-9e7603149fc5｜SaveButton 保存链里，下载和缓存放在点击之前，SUCCESS 回调内只写相册｜读到：现有实现先下载或缓存、准备完成后才渲染 SaveButton；服务或头注写明临时授权在点击 SUCCESS 后只在有限窗口内有效；写错：SaveButton 的 .onClick 里判断 SaveButtonOnClickResult.SUCCESS 之后才开始下载或缓存（await 下载），再调 photoAccessHelper 写相册
- rule-437faebc060d｜选出的图要写进持久配置时，先复制到 filesDir 校验非空，再存 file:// 路径｜写错：目标把 PhotoViewPicker 返回的 photoUris[0]，或者落在 cacheDir 下的中间副本路径，直接写进会保存、之后重新读取的配置
- rule-8393d2bb910b｜源端下载到公共目录并媒体扫描，迁成沙箱下载后要补 DocumentViewPicker.save 导出｜读到：源码查 WRITE_EXTERNAL_STORAGE、写外部存储目录，下载成功后 sendBroadcast(ACTION_MEDIA_SCANNER_SCAN_FILE)；写错：request.agent 下载到 filesDir 后直接提示成功并入库，没有 DocumentViewPicker.save；注释写沙箱目录与 /sdcard 目录「等价」或媒体扫描「已裁剪」
- rule-83208087db7d｜选图回填配置时，取消保留旧值、失败给可见错误，不留空 catch｜写错：选图结果回调或复制、写配置的步骤用 `catch (e) {}` 吞掉异常，页面只回到空态；或者用户取消（photoUris 为空）时把配置覆盖成空值
- rule-e861abbc457d｜源端取 DISPLAY_NAME 作文件名时，目标对 picker URI 去 query/fragment 后解码末段｜读到：源端取导入文件名走 ContentResolver 查 OpenableColumns.DISPLAY_NAME 的 helper；写错：文件名写成 uri.split('?')[0] 的末段（baseName），没有 decodeURIComponent
- rule-d83c34ad7ff8｜相机照片走 photoAssetAvailable + saveCameraPhoto，不用 createAsset｜读到：源端拍照后经 `MediaStore` insert（`IS_PENDING` 两段写）保存照片；规格只写「photoAccessHelper PhotoAsset 创建/提交」；写错：目标用 `photoAvailable` 取字节，再经 `createAssetRequest` / `createAsset` 两段写进媒体库，无受限权限授权时报 201
- rule-f40e07278e08｜存相册未声明 WRITE_IMAGEVIDEO 时改用 showAssetsCreationDialog 授权写入｜读到：源端用 MediaStore 入库；规格写鸿蒙侧走免权限的媒体库/picker 通道；写错：代码用 MediaAssetChangeRequest.createAssetRequest + addResource + applyChanges 入库，而 module.json5 的 requestPermissions 里没有 ohos.permission.WRITE_IMAGEVIDEO，也没有运行时申请
- rule-8b5f0640d24e｜选媒体库写入接口前查 @permission，受限权限没有签名授权就不作默认保存路线｜读到：参考资料或规格把 `ohos.permission.WRITE_IMAGEVIDEO` 写成普通 user_grant（`module.json5` 声明 + 运行时请求即可）；写错：默认保存路线调用 `createAsset` / `createAssetRequest` + `applyChanges` / `createAssetWithShortTermPermission`，工程没有对应受限权限的签名授权
