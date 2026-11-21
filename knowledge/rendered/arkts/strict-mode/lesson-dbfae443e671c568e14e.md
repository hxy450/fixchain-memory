# catch 中继续抛出时先把异常收窄为 Error，不直接 throw catch 变量

## 何时使用

功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时

## 适用情境

ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。

## 例外与边界

- 抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error

## 原因

ArkTS 只允许 throw Error 及其子类，catch 变量类型未定，原样 `throw error` 会在编译时报 arkts-limited-throw（10605087）。来源中这条规则写在派工要求预加载的 skill 里，但 worker 批量读取 skill 时输出被截断，规则没有进入上下文；这次修改又落在组编译之后、worker 不能自行编译，错误一直留到终态全量编译才暴露。

## 做法

1. 需要 rethrow 时写成 `throw error instanceof Error ? error : new Error(String(error))`，或抛出带原因说明的新 Error。catch 到的是 Kit 以普通对象拒绝的 BusinessError（如 @ohos.net.http 的失败）时，String(error) 只得到“[object Object]”，新 Error 的消息里写入它的 code 与 message。
2. 编译门之后落地、又不能自行编译的修改，写完用 rg 查 `throw [A-Za-z_]+;` 这类直接抛变量的语句，并对照 hmos-fix-build-errors 错误表里的 ArkTS 严格模式条目自查。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕catch 到 @ohos.net.http 这类以普通对象拒绝的 BusinessError 时，error instanceof Error 为 false，走 new Error(String(error)) 分支，而 String(error) 是“[object Object]”，新 Error 的 message 丢掉了原来的 code 与 message。〔成立范围：对象：catch 变量是 Kit 用 napi_create_object 建的错误对象（已核 @ohos.net.http 的 request、requestInStream 失败值）。条件：依据是 OpenHarmony communication_netstack 仓 master 的实现（http_exec.cpp 失败时用 NapiUtils::CreateErrorMessage 建普通对象）与 ECMAScript 的 Object.prototype.toString；HarmonyOS 商用版本的实现未核。不成立：经 napi_throw_error / napi_create_error 抛出的错误是 Error 实例，原样再抛，code 保留（见条目 2）。〕
- 〔做法第 1 步〕经 napi_throw_error 抛出的 Kit 错误（如 geoLocationManager 的同步出错路径）是 Error 实例，code 是字符串属性；instanceof Error 分支把它原样再抛，上层按数值常量严格比较 code 仍会落空。〔成立范围：对象：经 napi_throw_error 抛错的 Kit 接口。条件：依据是 arkui_napi 仓 napi_throw_error 与 base_location 仓 HandleSyncErrCode 的实现（master）。不成立：经 napi_create_error 传数值 code 或 napi_throw_business_error 抛出的，code 是数。〕
