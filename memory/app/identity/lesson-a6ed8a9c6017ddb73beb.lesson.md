# 源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量

ID：`lesson-a6ed8a9c6017ddb73beb` · 版本：1

[本主题](index.md)

## 何时使用

接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时

## 适用情境

源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。

## 原因

复制成页面常量后版本号有两份来源，发版只改 app.json5 时关于页和更新提示就会失准。来源中接手者推理写明“从 AppScope 取版本码、加常量”，随后在两个页面写死版本字面量并删掉占位标记。

## 做法

1. 读取 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT) 的 versionName / versionCode。
2. 删除占位标记后 grep 页面代码，确认没有与 app.json5 相同的版本字面量。

