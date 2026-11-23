# 显示本应用最近拍摄的媒体以自身保存成功的 URI 为准：整库 getAssets 需受限的 READ_IMAGEVIDEO，失败不清空缩略图

## 何时使用

规格提取与实现阶段，把 Android MediaStore 最近媒体查询（画廊按钮缩略图、打开最新照片或视频）映射到 photoAccessHelper 时

## 适用情境

源端在 scoped storage 下查询 MediaStore 最近媒体，应用天然可见自己写入的媒体；目标为没有 READ_IMAGEVIDEO 授权的普通应用（该权限受限开放），实现者计划用 photoAccessHelper.getAssets 整库查最新项，失败分支清空缩略图。

## 例外与边界

- 应用已具备 READ_IMAGEVIDEO 的申请资格并获授权，且功能确需展示其他应用写入的媒体

## 原因

目标没有“未授权时仍可见本应用媒体”的语义，未授权时整库 getAssets 失败；失败分支若清空缩略图，恢复与冷启动都会丢掉画廊入口。把 scoped storage 的可见性套到目标上，规格与实现都会漏掉读权限这一前提。

## 做法

1. 以本应用保存成功返回的 URI 作为“最近媒体”来源：保存后记录并持久化（如写入偏好），恢复时直接解码该 URI；确认删除当前 URI 时才移除记录。
2. 确需整库查询时，先用 abilityAccessCtrl 的 checkAccessTokenSync 核对 READ_IMAGEVIDEO，未授权不查询；查询失败或无结果都保留已有缩略图。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕PhotoAccessHelper.getAssets 声明的 @permission 是 ohos.permission.READ_IMAGEVIDEO，缺权限时报 201 Permission denied
- 〔适用情境 / 例外与边界〕ohos.permission.READ_IMAGEVIDEO 权限级别 system_basic、授权方式 user_grant，属受限开放权限；API 9 到 24 申请后可访问云上和本地图片视频，API 26.0.0 起只能读用户本地公共目录的图片视频（超出本机 SDK 的 API 23）
- 〔做法第 1 步〕读写媒体库图片视频不申请权限的推荐方案是用 Picker 读取、用保存控件或授权弹窗保存；受限使用方案才申请 READ_IMAGEVIDEO 或 WRITE_IMAGEVIDEO
- 〔原因〕工程没有声明 READ_IMAGEVIDEO 时，设备上 photoAccessHelper.getAssets 查询失败
