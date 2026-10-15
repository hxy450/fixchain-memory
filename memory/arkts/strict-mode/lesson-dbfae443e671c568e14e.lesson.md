# catch 中继续抛出时先把异常收窄为 Error，非 Error 值包装时保留 message 与 code，不直接 throw catch 变量

ID：`lesson-dbfae443e671c568e14e` · 版本：3

[本主题](index.md)

## 何时使用

功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时

## 适用情境

ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。

## 例外与边界

- 抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error

## 原因

ArkTS 只允许 throw Error 及其子类，catch 变量类型未定，原样 throw error 会在编译时报 arkts-limited-throw（10605087）。Kit API 拒绝的 BusinessError 可能是只含 code、message 的普通对象，new Error(String(error)) 会把它变成“[object Object]”并丢掉 code，上层按 code 分类随之失效。不自行编译的修改里，这类错误会留到下一次全量编译。

## 做法

1. 需要 rethrow 时写成 throw error instanceof Error ? error : toError(error)：toError 用公共取消息函数读 message 与 code（lesson-b19162077a2ab886d809），构造保留 code 的 Error 子类或带 code 字段的 Error 再抛；不写 new Error(String(error))。

## 可选检查

- 编译门之后落地、又不能自行编译的修改，写完用 rg 查 throw [A-Za-z_]+; 这类直接抛变量的语句，并对照工程构建错误表里的 ArkTS 严格模式条目自查。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-7da8b355891030ab0ada](../../../store/cases/case-7da8b355891030ab0ada/e6be8a04ed9e23e71666c989b05f838c659d80abab9ce4eedab885e809c5a86d.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`e6be8a04ed9e23e71666c989b05f838c659d80abab9ce4eedab885e809c5a86d`
- [case-bae545fb004bef3f5772](../../../store/cases/case-bae545fb004bef3f5772/202dfa20bff6ca2b3221ab25b77223092fe02d509456a14e35dc422c81db15fc.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`202dfa20bff6ca2b3221ab25b77223092fe02d509456a14e35dc422c81db15fc`
