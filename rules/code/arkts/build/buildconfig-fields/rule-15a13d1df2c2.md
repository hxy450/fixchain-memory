# 源码有 debug/release 构建分支时，目标按 appProvisionType 判两支，不写「不迁移」

审的是：代码
触发（任一种）：
- 读到：源方法里有按 BuildConfig.DEBUG 判构建形态的分支（如 debug 构建直接切换、release 构建走渐显动画）；写错的样子：目标只留一支（如恒 animateTo），注释写「debug 分支无构建形态对等，不迁移」
适用范围：源方法按构建形态（debug/release）分支，迁成 ArkTS 页面或服务时
做法：
- 用 bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION).appInfo.appProvisionType === 'debug' 作 debug 判据，两支都照源写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getBundleInfoForSelfSync(bundleFlags: number): BundleInfo：同步取自身包的 BundleInfo（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，bundleManager.getBundleInfoForSelfSync）
- BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION = 0x00000001：要拿到 appInfo 必须带这个标志（出处：鸿蒙 SDK 的 ets/api/@ohos.bundle.bundleManager.d.ts，BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION）
- readonly appProvisionType: string，取值 debug 或 release：应用签名证书文件的类型，对应源端的构建形态（出处：鸿蒙 SDK 的 ets/api/bundleManager/ApplicationInfo.d.ts，ApplicationInfo.appProvisionType；js-apis-bundleManager-applicationInfo.md，ApplicationInfo）
- 返修按 appProvisionType 判 debug 后，debug 直切、release 渐显两支都恢复：返修后的写法（出处：卡里修好并验证过）
未核实：卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-f3d590ba381f544833aa（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
