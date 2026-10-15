# 替换源端取文件显示名的 helper 前读完实现：picker URI 去掉 query 后对末段 decodeURIComponent

ID：`lesson-f22b8d9ae2c8a0d9db25` · 版本：2

[本主题](index.md)

## 何时使用

页面与数据层实现阶段，把源端按 OpenableColumns.DISPLAY_NAME 取文件名的 helper（getFileName 一类）迁到目标，处理 DocumentViewPicker 返回的 URI 时

## 适用情境

源端以 getFileName 一类 helper 查询 ContentResolver 的 OpenableColumns.DISPLAY_NAME，并按 URI scheme 分支处理；目标从 DocumentViewPicker 得到 file://docs/... 形式的 URI。

## 原因

picker 返回的 URI 末段是百分号编码的，直接当显示名会出现 %20 一类字符；不读 helper 实现就凭印象近似，还会漏掉它按 scheme 区分的分支。

## 做法

1. 先读完源端 helper 的实现；从 URI 去掉 query 与 fragment 后取末段，decodeURIComponent 后作显示名，用含空格或中文的文件名自测。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-ce5d3e2da2846b40767d](../../../store/cases/case-ce5d3e2da2846b40767d/1df2aefde0f2b6579fe50390d58011413bdb64fc3891b30caf4a48b7b8953d1c.json) · 结论：recommendation:5, diagnosis
  卡片版本：`1df2aefde0f2b6579fe50390d58011413bdb64fc3891b30caf4a48b7b8953d1c`
