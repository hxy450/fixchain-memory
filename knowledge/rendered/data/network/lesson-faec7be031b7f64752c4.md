# 源端声明 INTERNET（及 ACCESS_NETWORK_STATE）且目标有网络请求时，在 module.json5 声明 ohos.permission.INTERNET（及 GET_NETWORK_INFO），并让这项声明有确定的写者

## 何时使用

迁移计划拆分、网络层实现与接线收尾阶段，确定由哪个任务、何时在 module.json5 声明网络权限时

## 适用情境

源 AndroidManifest 声明 android.permission.INTERNET，可能还有 ACCESS_NETWORK_STATE；目标新建请求封装与页面调用，module.json5 尚无 requestPermissions，或只有其他功能的权限；计划模板按能力段给任务分配输入，网络层任务的写域可能不含 module.json5。

## 原因

HarmonyOS 应用发起网络请求需要在 module.json5 声明 ohos.permission.INTERNET；生成期只读不写 module.json5 时，问题要到联调才暴露。来源中生成者读到源 Manifest 的 INTERNET 声明，也两次读取 module.json5，网络层落地时仍未声明，后续对接接口时才补上。规格已写明必配时，若计划拆分没有任务引用权限段、网络层 worker 又不能写 module.json5，这项要求就没有承接者；之后首次创建 requestPermissions 的接线任务只按单个切片草稿落地了其他权限。

## 做法

1. 与网络层同一轮在 module.json5 的 requestPermissions 加入 { "name": "ohos.permission.INTERNET" }；代码会判断连接状态时同时加入 ohos.permission.GET_NETWORK_INFO（均为 system_grant，无需 reason）。requestPermissions 里已有其他功能的权限项（如振动、相机）时只追加网络项，原有条目和它们的 reason、usedScene 原样保留，不整段重写。
2. 计划拆分时核对规格的权限映射段有任务引用：写进网络任务的 input/output（output 含 module.json5 的 requestPermissions），或单列一个工程配置任务。
3. 网络层写域不含 module.json5 时，在返回信封里把权限声明列为跨文件改动草稿；接线任务首次创建 requestPermissions 时，对照规格的权限映射表与工程中的 http、Web 调用补齐网络权限。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕HttpRequest.request 需要 ohos.permission.INTERNET，缺这项权限时以 BusinessError 201（Permission denied）失败
- 〔做法第 1 步〕ohos.permission.INTERNET 和 ohos.permission.GET_NETWORK_INFO 都是 normal 级、系统授权（system_grant）的权限
- 〔做法第 1 步〕module.json5 的 requestPermissions 里，reason 只在申请 user_grant 或 manual_settings 权限时必填，usedScene 也只在这两类权限时必填，其他情况下选填
- 〔做法第 1 步〕connection.hasDefaultNet、connection.getDefaultNet 需要 ohos.permission.GET_NETWORK_INFO，缺这项权限时以 BusinessError 201 失败
- 〔做法第 3 步〕Web 组件访问在线网页同样需要 ohos.permission.INTERNET
