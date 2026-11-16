# 取自身包名用 BundleInfo.name，不按安卓命名写 bundleName / packageName

审的是：代码
触发（任一种）：
- 读到：派工或源端要按自身包名拉起应用市场详情（packageName）；写错的样子：代码里写 info.bundleName（info 来自 getBundleInfoForSelf / getBundleInfoForSelfSync），编译报 Property 'bundleName' does not exist on type 'BundleInfo'
适用范围：用 bundleManager 取到的 BundleInfo 读包名时
做法：
- 包名取 info.name，info 由 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT) 或 getBundleInfoForSelf 返回；用平台对象的字段前在声明里核对字段名，只核函数签名不够
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- readonly name: string：BundleInfo 的包名字段；BundleInfo 里没有 bundleName 字段（出处：鸿蒙 SDK 的 ets/api/bundleManager/BundleInfo.d.ts，BundleInfo.name）
- function getBundleInfoForSelfSync(bundleFlags: number): BundleInfo；function getBundleInfoForSelf(bundleFlags: number): Promise<BundleInfo>：取自身的 BundleInfo，同步和异步两种（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，bundleManager.getBundleInfoForSelfSync、bundleManager.getBundleInfoForSelf）
- GET_BUNDLE_INFO_DEFAULT = 0x00000000：BundleFlag 的默认值，取回的 BundleInfo 不含 signatureInfo、applicationInfo、hapModuleInfo 等，name 仍在（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT）
- readonly name: string（ApplicationInfo）：同族接口：ApplicationInfo 的 name 和 bundleName 相同（出处：鸿蒙 SDK 的 ets/api/bundleManager/ApplicationInfo.d.ts，ApplicationInfo.name）
- readonly bundleName: string（AbilityInfo）：同族接口：AbilityInfo 里包名字段才叫 bundleName（出处：鸿蒙 SDK 的 ets/api/bundleManager/AbilityInfo.d.ts，AbilityInfo.bundleName）
- info.bundleName 改成 info.name 后编译通过：修复时按声明改过的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-5235937ddd5c78dbe0ed（DeepAI全能PPT）：做法第 1 步 ← 建议 6、诊断；取值 6 ← 诊断
