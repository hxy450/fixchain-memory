# 源端声明 INTERNET（及 ACCESS_NETWORK_STATE）且目标有网络请求时，在 module.json5 声明 ohos.permission.INTERNET（及 GET_NETWORK_INFO），并让这项声明有确定的写者

ID：`lesson-faec7be031b7f64752c4` · 版本：2

[本主题](index.md)

## 何时使用

迁移计划拆分、网络层实现与接线收尾阶段，确定由哪个任务、何时在 module.json5 声明网络权限时

## 适用情境

源 AndroidManifest 声明 android.permission.INTERNET，可能还有 ACCESS_NETWORK_STATE；目标新建请求封装与页面调用，module.json5 尚无 requestPermissions，或只有其他功能的权限；计划模板按能力段给任务分配输入，网络层任务的写域可能不含 module.json5。

## 原因

HarmonyOS 应用发起网络请求需要在 module.json5 声明 ohos.permission.INTERNET；生成期只读不写 module.json5 时，问题要到联调才暴露。来源中生成者读到源 Manifest 的 INTERNET 声明，也两次读取 module.json5，网络层落地时仍未声明，后续对接接口时才补上。规格已写明必配时，若计划拆分没有任务引用权限段、网络层 worker 又不能写 module.json5，这项要求就没有承接者；之后首次创建 requestPermissions 的接线任务只按单个切片草稿落地了其他权限。

## 做法

1. 与网络层同一轮在 module.json5 的 requestPermissions 加入 { "name": "ohos.permission.INTERNET" }；代码会判断连接状态时同时加入 ohos.permission.GET_NETWORK_INFO（均为 system_grant，无需 reason）。
2. 计划拆分时核对规格的权限映射段有任务引用：写进网络任务的 input/output（output 含 module.json5 的 requestPermissions），或单列一个工程配置任务。
3. 网络层写域不含 module.json5 时，在返回信封里把权限声明列为跨文件改动草稿；接线任务首次创建 requestPermissions 时，对照规格的权限映射表与工程中的 http、Web 调用补齐网络权限。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-63a0f0066a7a0376735f](../../../store/cases/case-63a0f0066a7a0376735f/d718ff4dd50ba6ac13049e17f074d2fa7d8124a2edcae8d67f27b8ce3f13b014.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d718ff4dd50ba6ac13049e17f074d2fa7d8124a2edcae8d67f27b8ce3f13b014`
- [case-6be1461999c00a7fe781](../../../store/cases/case-6be1461999c00a7fe781/6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7.json) · 结论：diagnosis, recommendation:3
  卡片版本：`6d6fafe3319ae7f96ea8861f32e80ef334e2e1fb9a7eaa64e3951c3b097c33d7`
