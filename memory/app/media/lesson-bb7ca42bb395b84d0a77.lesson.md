# 显示本应用最近拍摄的媒体以自身保存成功的 URI 为准：整库 getAssets 需受限的 READ_IMAGEVIDEO，失败不清空缩略图

ID：`lesson-bb7ca42bb395b84d0a77` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-d5c3514ada560cb5134d](../../../store/cases/case-d5c3514ada560cb5134d/f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f`
