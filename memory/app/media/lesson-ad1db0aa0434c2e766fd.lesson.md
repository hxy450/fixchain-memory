# 从图库选图导入用系统 PhotoViewPicker 并复制进应用缓存，不以申请 READ_IMAGEVIDEO 读媒体库实现

ID：`lesson-ad1db0aa0434c2e766fd` · 版本：1

[本主题](index.md)

## 何时使用

平台能力映射与实现阶段，为“从相册选择图片导入”选择 HarmonyOS 读取方式与权限声明时，包括在 Flutter 本地兼容插件中实现选图时

## 适用情境

源端经媒体库查询（MediaStore，或 photo_manager 一类插件）列出并读取相册图片，依赖媒体库读写权限；目标应用为普通应用，功能只需用户主动选择的图片。

## 例外与边界

- 应用已确认具备申请 READ_IMAGEVIDEO 所需的签名等级与权限审批，且功能确需浏览整个媒体库

## 原因

经 photoAccessHelper 读取媒体库需要 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO；未声明时请求被拒、图库界面不出现，表现为点击无反应；来源环境中普通应用签名声明该权限后安装直接失败（9568289 grant request permissions failed）。系统选择器只授予用户所选文件的访问，不需要该权限。

## 做法

1. 选图入口用 PhotoViewPicker（Flutter 中可复用已适配 OHOS、按图片类型选择的 file_picker），把返回的 URI 复制到应用缓存，后续预览、读取、编辑都用缓存路径；用户取消时按原接口的“无结果”返回。
2. 上层期待原选图 API 的对象（如 AssetEntity）时，在兼容层用缓存路径构造该对象，并为依赖它的原生读取方法（原图、缩略图、文件）补本地路径分支。

