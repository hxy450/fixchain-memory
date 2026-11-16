# 源端用 BuildConfig.VERSION_NAME/CODE 时，目标从应用包信息读，不抄成页面常量

审的是：代码
触发（任一种）：
- 读到：源端页面用 BuildConfig.VERSION_NAME 显示版本，或用 BuildConfig.VERSION_CODE 比较更新提示；写错的样子：页面里出现与 app.json5 的 versionName / versionCode 相同的字面量（模块常量，或 aboutToAppear 里的赋值）
- 读到：占位登记里 FWD-REF 行的 trigger 写由 Service 或 ViewModel 提供版本；写错的样子：删掉了 FWD-REF 标记，换成写死的版本常量
适用范围：接线阶段闭合页面上的版本号占位（关于页显示版本、更新提示比较版本码）
做法：
- import { bundleManager } from '@kit.AbilityKit'；const info = bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT)；VERSION_NAME 对应 info.versionName，VERSION_CODE 对应 info.versionCode
- 闭合前对照登记表的 trigger：要求服务或 ViewModel 提供值的，写常量不算闭合；删掉标记后在页面代码里搜 app.json5 的版本值，确认没有同值字面量
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getBundleInfoForSelfSync(bundleFlags: number): BundleInfo：同步取当前应用自己的包信息（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，bundleManager.getBundleInfoForSelfSync）
- BundleFlag.GET_BUNDLE_INFO_DEFAULT = 0x00000000：取默认包信息（不含签名、applicationInfo、hapModuleInfo 等），版本字段在内（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，BundleFlag.GET_BUNDLE_INFO_DEFAULT）
- readonly versionCode: number；readonly versionName: string：BundleInfo 里的版本码和版本名，对应 app.json5 的 versionCode / versionName（出处：鸿蒙 SDK 的 ets/api/bundleManager/BundleInfo.d.ts，BundleInfo.versionCode、BundleInfo.versionName）
- function getBundleInfoForSelf(bundleFlags: number): Promise<BundleInfo>：同族接口：异步版本（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，bundleManager.getBundleInfoForSelf）
- 删除两处字面量、改读 getBundleInfoForSelfSync(GET_BUNDLE_INFO_DEFAULT) 的 versionName / versionCode：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-f935850c669c48f05a00（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
