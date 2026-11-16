# 相册选一张图作持久配置时用 PhotoViewPicker 单选，不走依赖 getAlbums 的自建相册页

审的是：代码
触发（任一种）：
- 读到：安卓源单图选择走应用自建的相册 Activity，选出（裁剪后）的图片文件路径写进会保存的配置；写错的样子：目标这个入口 push 自建相册页，该页靠 PhotoAccessHelper.getAlbums 全量查询，页头还有未完成的权限/相册绑定 TODO（P-S…-UNC- 一类未决记号），module.json5 没声明 ohos.permission.READ_IMAGEVIDEO
适用范围：目标要从相册选一张图作背景等持久配置的入口
不适用的情形：必须复用自建相册页时：先确认 module.json5 已声明对应媒体权限、运行时确实能拿到授权，且页面上没有未完成的权限/相册绑定 TODO
做法：
- 写成 const opts = new photoAccessHelper.PhotoSelectOptions(); opts.MIMEType = photoAccessHelper.PhotoViewMIMETypes.IMAGE_TYPE; opts.maxSelectNumber = 1; const res = await new photoAccessHelper.PhotoViewPicker().select(opts)，取 res.photoUris[0]
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- select(option?: PhotoSelectOptions): Promise<PhotoSelectResult>：PhotoViewPicker 拉起系统图库选择，返回所选 URI（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoViewPicker.select）
- PhotoViewMIMETypes.IMAGE_TYPE = 'image/*'；maxSelectNumber?: number：只选图片；单次最多选几张，单选写 1（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoViewMIMETypes.IMAGE_TYPE、BaseSelectOptions.maxSelectNumber）
- Picker 接口本身无需申请权限：用 PhotoViewPicker 不必声明媒体读权限（出处：photoAccessHelper-photoviewpicker.md，使用Picker选择媒体库资源）
- getAlbums(type: AlbumType, subtype: AlbumSubtype, options?: FetchOptions): Promise<FetchResult<Album>>，@permission ohos.permission.READ_IMAGEVIDEO：自建相册页的全量相册查询要读媒体权限，没声明、没授权就拿不到（出处：鸿蒙 SDK 的 ets/api/@ohos.file.photoAccessHelper.d.ts，PhotoAccessHelper.getAlbums）
- 入口改成 PhotoViewPicker 单图选择后，真机上拉起系统选择器、回填正常：改法的效果（出处：卡里修好并验证过）
未核实：卡里的 target_sdk 是 26.0.0，本机声明是 API 23
来源：1 张卡，1 个应用
- case-d465b188d96e33a7ffad（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；例外 1 ← 建议 1；取值 5 ← 诊断
