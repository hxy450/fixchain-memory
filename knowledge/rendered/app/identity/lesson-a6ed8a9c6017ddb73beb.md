# 源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量

## 何时使用

接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时

## 适用情境

源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。

## 原因

复制成页面常量后版本号有两份来源，发版只改 app.json5 时关于页和更新提示就会失准。来源中接手者推理写明“从 AppScope 取版本码、加常量”，随后在两个页面写死版本字面量并删掉占位标记。

## 做法

1. 读取 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT) 的 versionName / versionCode。
2. 删除占位标记后 grep 页面代码，确认没有与 app.json5 相同的版本字面量。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕以 BundleFlag.GET_BUNDLE_INFO_DEFAULT 调 getBundleInfoForSelfSync / getBundleInfoForSelf 时，返回的 BundleInfo 带 versionName、versionCode 等顶层字段，但不填 applicationInfo（appInfo）、hapModuleInfo、ability、extensionAbility、signatureInfo 和权限信息；这些子信息要在 bundleFlags 里组合对应标志才会带回（如 GET_BUNDLE_INFO_WITH_APPLICATION；ability、extensionAbility 的标志单独用不生效，要和 GET_BUNDLE_INFO_WITH_HAP_MODULE 一起传）。〔成立范围：对象：@ohos.bundle.bundleManager 的 getBundleInfoForSelf / getBundleInfoForSelfSync 的 bundleFlags 参数。条件：依据是文档说明（SDK 声明注释与接口文档对 BundleFlag 各值的说明），实现未看。不成立：bundleFlags 组合了 GET_BUNDLE_INFO_WITH_APPLICATION 等标志时，对应子信息会填上。〕
