# 从图库选图用系统 PhotoViewPicker 并复制进应用目录：一次性处理放缓存，要写进持久配置的复制到 filesDir 并校验非空；不以申请 READ_IMAGEVIDEO 读媒体库或经权限未接通的自建相册页实现

## 何时使用

平台能力映射与实现阶段，为“从相册选择图片导入”选择 HarmonyOS 读取方式与权限声明时，包括在 Flutter 本地兼容插件中实现选图时；为背景等持久配置接入“从相册选一张图”并保存结果时

## 适用情境

源端经媒体库查询（MediaStore，或 photo_manager 一类插件）列出并读取相册图片，依赖媒体库读写权限；目标应用为普通应用，功能只需用户主动选择的图片。 也包括选出的图片要作为背景等持久配置反复读取，而工程里另有依赖 getAlbums 全量查询、带未完成权限或相册绑定 TODO 的自建选择页。

## 例外与边界

- 应用已确认具备申请 READ_IMAGEVIDEO 所需的签名等级与权限审批，且功能确需浏览整个媒体库
- 改用 PhotoViewPicker 时照源端设选择范围：源端只选图片就设 MIMEType 为图片类型，单选就设 maxSelectNumber 为 1（不设时图片和视频都可选、最多 50 张）

## 原因

经 photoAccessHelper 读取媒体库需要 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO；未声明时请求被拒、图库界面不出现，表现为点击无反应；来源环境中普通应用签名声明该权限后安装直接失败（9568289 grant request permissions failed）。系统选择器只授予用户所选文件的访问，不需要该权限。

## 做法

1. 选图入口用 PhotoViewPicker（Flutter 中可复用已适配 OHOS、按图片类型选择的 file_picker）；一次性导入、预览或编辑的图片把返回的 URI 用 fileIo.openSync 以只读打开取得 fd，再复制到应用缓存（copyFile 的 src 只收沙箱路径或 fd，不收 URI），后续都用缓存路径；用户取消时按原接口的“无结果”返回。
2. 上层期待原选图 API 的对象（如 AssetEntity）时，在兼容层用缓存路径构造该对象，并为依赖它的原生读取方法（原图、缩略图、文件）补本地路径分支。
3. 结果要写进会被保存、之后重新读取的配置时，复制到 context.filesDir 下的应用目录并校验非空后，再写由 fileUri.getUriFromPath 生成的 file:// URI，不保存 picker 的临时授权 URI 或 cacheDir 中间副本；取消保留旧值，失败给出可见错误，不留空 catch。
4. 复用自建相册页前确认 module.json5 已声明对应媒体权限、运行时确能授权且页面没有未完成的权限 TODO，否则改用 PhotoViewPicker；收口前在设备上走一遍“选图 → 回填”。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 例外与边界〕ohos.permission.READ_IMAGEVIDEO 是 system_basic 级、用户授权（user_grant）的受限开放权限，普通应用要经 ACL 跨级申请；API 26.0.0 起它只能读用户本地公共目录的图片视频（超出本机 SDK 的 API 23）
- 〔原因〕APL 为 normal 的应用声明 system_basic 或 system_core 级权限时，安装报 9568289 install failed due to grant request permissions failed；API 18 起报错后附具体权限名
- 〔原因〕HAP 没有声明 READ_IMAGEVIDEO、WRITE_IMAGEVIDEO 时，经媒体库接口请求这两项权限被拒，图库界面不出现
- 〔适用情境 / 做法第 4 步〕PhotoAccessHelper.getAlbums 要求 ohos.permission.READ_IMAGEVIDEO，未获授权时以错误码 201 失败
- 〔原因 / 做法第 1 步〕PhotoViewPicker 拉起系统图库，接口本身不需要申请权限，适用于界面 UIAbility、由窗口组件触发；select 返回的 URI 只有只读权限
- 〔做法第 1 步〕PhotoSelectOptions 不设 MIMEType 时可选图片和视频两类；maxSelectNumber 取值 [1, 500]，不设时为 50
- 〔做法第 1、3 步〕文档要求不在 picker 的回调里直接用返回的 URI 打开文件，而是先保存 URI，等界面从图库返回、由另一次操作调用 fileIo.openSync 打开
- 〔做法第 3 步〕PhotoSelectResult.photoUris 只能凭临时授权使用；经 Picker 获得的临时授权在应用退出或设备重启后清除
- 〔做法第 1、3 步〕fileIo.copyFile 的 src、dest 只收沙箱路径或文件描述符，mode 只支持 0（默认，完全覆盖目标文件）；fileIo.openSync 的 path 既可是沙箱路径也可是 URI；收 URI 的是 fileIo.copy（API 11 起）
- 〔做法第 1、3 步〕filesDir 存默认长期保存的文件，随应用卸载清理；cacheDir 的文件在超过配额或系统空间达到一定条件时被自动清理
- 〔做法第 3 步〕fileUri.getUriFromPath 把沙箱路径转成 file://<包名>/data/storage/... 形式的 URI，中文和非数字字母的特殊字符会被百分号编码；Image 显示沙箱文件要传这样转换后的 URI，ArkTS 卡片不支持 file:// 前缀
