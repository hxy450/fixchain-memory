# 源端声明 INTERNET 且目标有网络请求时，在 module.json5 的 requestPermissions 声明 ohos.permission.INTERNET

ID：`lesson-faec7be031b7f64752c4` · 版本：1

[本主题](index.md)

## 何时使用

网络基础设施实现阶段，新建 HTTP 请求封装并接入页面请求时

## 适用情境

源 AndroidManifest 声明 android.permission.INTERNET；目标新建请求封装与页面调用，module.json5 尚无 requestPermissions。

## 原因

HarmonyOS 应用发起网络请求需要在 module.json5 声明 ohos.permission.INTERNET；生成期只读不写 module.json5 时，问题要到联调才暴露。来源中生成者读到源 Manifest 的 INTERNET 声明，也两次读取 module.json5，网络层落地时仍未声明，后续对接接口时才补上。

## 做法

1. 与网络层同一轮在 module.json5 的 requestPermissions 加入 { "name": "ohos.permission.INTERNET" }。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6be1461999c00a7fe781](../../../store/cases/case-6be1461999c00a7fe781/6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7.json) · 结论：diagnosis, recommendation:3
  卡片版本：`6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7`
