# 源端读写外部存储公共目录和 MediaStore 媒体库

agent 会看到什么：读到源码申请 WRITE_EXTERNAL_STORAGE / READ_MEDIA_AUDIO，下载到公共目录后发 ACTION_MEDIA_SCANNER_SCAN_FILE，或查询 MediaStore.Audio 列本地音频；规格的下载链没有导出步骤、把媒体扫描标「不迁移」，或写成 MediaLibraryKit 查询加权限申请

## 规矩

- rule-5c883f39a0fe｜源端写公共目录并做媒体扫描、目标改落沙箱时，规格那条链要写出导出步骤｜读到：源码先查 WRITE_EXTERNAL_STORAGE、下载到外部存储公共目录（如 /sdcard/Download/…），成功后发 ACTION_MEDIA_SCANNER_SCAN_FILE；映射参考写「下载目录 → 沙箱 filesDir + picker 导出」；写错：规格的下载链写成 request.agent 完成 → 提示成功 → 入库，数据流、服务接口和验收条目里都没有导出步骤
- rule-c0f167a4607c｜源端扫 MediaStore.Audio 时，规格写 AudioViewPicker 导入沙箱而非媒体库查询｜读到：安卓源码先申请 READ_EXTERNAL_STORAGE / READ_MEDIA_AUDIO，再查询 MediaStore.Audio 列出本地音频；写错：规格或验收条目写成「MediaStore 音频扫描 → MediaLibraryKit 查询音频资产」「READ_EXTERNAL_STORAGE → 音频库读取权限 + requestPermissionsFromUser，拒绝→引导空态」，或把 READ_MEDIA_AUDIO 映射成 READ_AUDIO「按需 user_grant」
- rule-62b359265807｜规格映射 MediaStore 时写明 WRITE_IMAGEVIDEO 受限和相机资产路线｜读到：源端用 `MediaStore` insert（`IS_PENDING` 两段写）或 `MediaRecorder` 输出文件保存照片、视频；写错：映射行只写「photoAccessHelper PhotoAsset 创建/提交（IS_PENDING 两段写）」，没写 WRITE_IMAGEVIDEO 是受限开放权限、能否获得，也没写相机拍摄走系统资产路线
- rule-33e1421f28e1｜MediaStore 查询映射到 getAssets 时写明需 READ_IMAGEVIDEO，画廊以自存 URI 为准｜读到：源端用 MediaStore 查询最近媒体（scoped storage 下应用天然可见自己保存的媒体），再 loadThumbnail 取缩略图；写错：规格把「MediaStore 查询 / loadThumbnail」映射成 photoAccessHelper.getAssets + getThumbnail，没写读权限，也没写画廊入口以应用自己保存成功的 URI 为准
- rule-834db86b03dd｜规格把源端公共目录改成沙箱时，同一 AC 写明用户可见性降级并与映射表一致｜读到：源端把文件写到 Environment.getExternalStoragePublicDirectory(...) 或封装它的工具方法下的目录（如 Documents 下的日志目录），用户在文件管理里看得到；写错：规格的 AC 写“映射到应用沙箱目录”，同一文件的映射表却写“用户文件目录”，两处矛盾，也没写用户可见性降低了
