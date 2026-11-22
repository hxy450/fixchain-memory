# 源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量

## 何时使用

接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时

## 适用情境

源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。只处理源端取自 BuildConfig 的版本值；源端本来就写死在代码里的版本数字（更新日志条目、数据迁移的版本阈值、和服务端比较的固定版本）照源端保留，不因和 app.json5 的值相同而改成运行时读取。

## 原因

复制成页面常量后版本号有两份来源，发版只改 app.json5 时关于页和更新提示就会失准。来源中接手者推理写明“从 AppScope 取版本码、加常量”，随后在两个页面写死版本字面量并删掉占位标记。

## 做法

1. 读取 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT) 的 versionName / versionCode。
2. 删除占位标记后 grep 页面代码，确认没有与 app.json5 相同的版本字面量。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕用 BundleFlag.GET_BUNDLE_INFO_DEFAULT 取到的 BundleInfo 不含 signatureInfo、applicationInfo、hapModuleInfo、ability、extensionAbility 和 permission 信息，但版本字段 versionCode、versionName 在内
- 〔原因 / 做法第 1 步〕BundleInfo.versionCode 是应用包的版本号、versionName 是版本文本描述，分别对应 app.json5 里配置的 versionCode、versionName 字段
