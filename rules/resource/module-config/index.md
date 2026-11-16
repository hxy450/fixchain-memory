# 模块配置（module.json5）

源 AndroidManifest 有 <activity>、<service>、<intent-filter>，res/xml 下有 shortcuts、appwidget-provider，或导航图里有页面；目标端有 module.json5 的 abilities、extensionAbilities、skills、metadata，app.json5 的 configuration，或 profile 下的 main_pages.json、form_config.json 时

## 触发族

- [桌面快捷方式配置和图标](shortcuts/index.md)（4 条）：源端有 App Shortcuts（shortcuts.xml、ShortcutManager / ShortcutInfo）或规格定了快捷方式入口；module.json5 的 ohos.ability.shortcuts metadata 缺失或放在 module 级，profile 下没有快捷方式配置，或图标是整张拉伸到 1024×1024
- [intent-filter 对应的 module.json5 skills](intent-filter-skills/index.md)（8 条）：源 AndroidManifest 的 <intent-filter> 带 VIEW / BROWSABLE 和 <data android:scheme / host / pathPrefix>、android:autoVerify，或 NFC 的 TECH_DISCOVERED；module.json5 的 skills 只有 entity.system.home 一项，uris 漏了源端的 scheme、host 或加了源端没有的，缺 domainVerify，或没有 TAG_FOUND skill
- [extensionAbilities 条目的 type](extension-type/index.md)（1 条）：目标源文件 extends 某个 ExtensionAbility 子类（AppServiceExtensionAbility、WorkSchedulerExtensionAbility 等），module.json5 的 extensionAbilities 里对应条目写的 type
- [跟随系统设置的应用配置（屏幕方向、字号缩放）](follow-system/index.md)（3 条）：源端 <activity> 没写 android:screenOrientation、文本用 sp 或有系统对话框（安卓缺省随系统旋转、随系统字号缩放），目标 module.json5 的 orientation、app.json5 的 configuration 有没有显式写
- [appwidget-provider 转成的 form_config.json](form-config/index.md)（2 条）：源端 appwidget-provider 的 targetCellWidth / targetCellHeight、min/maxResizeWidth、resizeMode、updatePeriodMillis，目标 form_config.json 里写的 supportDimensions、defaultDimension、resizable 和刷新配置
- [main_pages.json 的 src 页面登记](main-pages/index.md)（2 条）：源端导航图里的目标 Fragment、底部导航或 DialogFragment，目标 main_pages.json 的 src 登记了哪些文件：router.pushUrl 的目标页、被 import 的 Tab 子组件和 @CustomDialog，以及编译报 10905402
- [前台服务转成的 backgroundModes 声明](background-modes/index.md)（2 条）：源端前台服务 startForeground(...)、foregroundServiceType（如 dataSync），目标 module.json5 里 backgroundModes 写在 abilities 还是 extensionAbilities 条目上
- [module.json5 的 querySchemes](query-schemes/index.md)（1 条）：源端用 Intent 拉起外部应用（geo:、mailto:、tel: 等 URI）并在拉起前查可用性，目标代码调了 bundleManager.canOpenLink；entry 模块 module.json5 的 module.querySchemes 里有没有登记这些 scheme
