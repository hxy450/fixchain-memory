# 源端 BuildConfig.VERSION_NAME/VERSION_CODE 迁为运行时读取应用包信息，不把 app.json5 的版本值复制成页面常量

ID：`lesson-a6ed8a9c6017ddb73beb` · 版本：4 · 阶段：execute · 主题：[app/resources](index.md)

概要：版本号经 bundleManager 运行时读取，不写成常量

信号：`BuildConfig.VERSION_NAME`, `BuildConfig.VERSION_CODE`, `bundleManager.getBundleInfoForSelfSync`, `GET_BUNDLE_INFO_DEFAULT`, `versionName`, `versionCode`, `app.json5`

## 何时使用

接线阶段闭合“显示版本号”“按版本码判断更新提示”这类占位时

## 适用情境

源页面用 BuildConfig.VERSION_NAME/VERSION_CODE 显示版本或比较更新提示；目标 app.json5 已写有 versionName/versionCode，页面留有“由服务提供版本”的前向占位。

## 原因

复制成页面常量后版本号有两份来源，发版只改 app.json5 时关于页和更新提示就会失准。来源中接手者推理写明“从 AppScope 取版本码、加常量”，随后在两个页面写死版本字面量并删掉占位标记。

## 做法

1. 读取 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT) 的 versionName / versionCode。
2. 删除占位标记后 grep 页面代码，确认没有与 app.json5 相同的版本字面量。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [解前向占位按触发文本逐项兑现，写常量不算闭合](../../process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md)（共享 1 张卡）
- [沿用脚手架包名前核对决策与签名；vendor 按源端落地](lesson-fb996956b33a1ba65861.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f935850c669c48f05a00](../../../../store/cases/case-f935850c669c48f05a00/69dfa72ef88368edd0415d1e9f4e42348abeb6abd342525bb8b208074d2011a3.json) · 结论：diagnosis, rec-3470eae6b4, rec-be475ac843
  卡片版本：`69dfa72ef88368edd0415d1e9f4e42348abeb6abd342525bb8b208074d2011a3`
