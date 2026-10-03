# 从图库选图用系统 PhotoViewPicker 并复制进应用目录：一次性处理放缓存，要写进持久配置的复制到 filesDir 并校验非空；不以申请 READ_IMAGEVIDEO 读媒体库或经权限未接通的自建相册页实现

ID：`lesson-ad1db0aa0434c2e766fd` · 版本：2

[本主题](index.md)

## 何时使用

平台能力映射与实现阶段，为“从相册选择图片导入”选择 HarmonyOS 读取方式与权限声明时，包括在 Flutter 本地兼容插件中实现选图时；为背景等持久配置接入“从相册选一张图”并保存结果时

## 适用情境

源端经媒体库查询（MediaStore，或 photo_manager 一类插件）列出并读取相册图片，依赖媒体库读写权限；目标应用为普通应用，功能只需用户主动选择的图片。 也包括选出的图片要作为背景等持久配置反复读取，而工程里另有依赖 getAlbums 全量查询、带未完成权限或相册绑定 TODO 的自建选择页。

## 例外与边界

- 应用已确认具备申请 READ_IMAGEVIDEO 所需的签名等级与权限审批，且功能确需浏览整个媒体库

## 原因

经 photoAccessHelper 读取媒体库需要 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO；未声明时请求被拒、图库界面不出现，表现为点击无反应；来源环境中普通应用签名声明该权限后安装直接失败（9568289 grant request permissions failed）。系统选择器只授予用户所选文件的访问，不需要该权限。

## 做法

1. 选图入口用 PhotoViewPicker（Flutter 中可复用已适配 OHOS、按图片类型选择的 file_picker）；一次性导入、预览或编辑的图片把返回的 URI 复制到应用缓存，后续都用缓存路径；用户取消时按原接口的“无结果”返回。
2. 上层期待原选图 API 的对象（如 AssetEntity）时，在兼容层用缓存路径构造该对象，并为依赖它的原生读取方法（原图、缩略图、文件）补本地路径分支。
3. 结果要写进会被保存、之后重新读取的配置时，复制到 context.filesDir 下的应用目录并校验非空后再写 file:// 路径，不保存 picker 的临时授权 URI 或 cacheDir 中间副本；取消保留旧值，失败给出可见错误，不留空 catch。
4. 复用自建相册页前确认 module.json5 已声明对应媒体权限、运行时确能授权且页面没有未完成的权限 TODO，否则改用 PhotoViewPicker；收口前在设备上走一遍“选图 → 回填”。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-96b417fb2e059d43f8bf](../../../store/cases/case-96b417fb2e059d43f8bf/b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e.json) · 结论：diagnosis, recommendation:2
  卡片版本：`b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e`
- [case-d465b188d96e33a7ffad](../../../store/cases/case-d465b188d96e33a7ffad/d87e9d7a3a5b06822a636cbc0dacb4092ee9f0cf5055f2c05f8cd32373e25253.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d87e9d7a3a5b06822a636cbc0dacb4092ee9f0cf5055f2c05f8cd32373e25253`
