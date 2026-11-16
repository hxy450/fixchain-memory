# 资源（resource）

27 个族，135 条规矩。整个产物的族一页看完见 [map.md](map.md)（每个主题一行，下面是「短号 族名（条数）」）。

## 一级主题

- [应用级信息（AppScope）](app-info/index.md)（25 条）：源端 Gradle 有 applicationId、resValue，AndroidManifest 的 <application> 写了 android:label、android:icon；目标端有 AppScope/app.json5 的 bundleName、vendor、icon，app_name、EntryAbility_label 字符串，或分层图标、启动窗图标时
- [颜色](colors/index.md)（25 条）：源端有 colors.xml、values-night、布局和 Compose 里的色值，或颜色来自 ?attr 主题属性、控件默认样式、@android:color 和 Material 等库主题；目标端有 color.json 和 dark 目录时
- [图片和矢量图](media/index.md)（11 条）：源端 drawable 下有位图和 <vector>、<animated-vector>，布局或代码用 @drawable、R.drawable 引用图片，或 Compose 用 Icons.* 图标；目标端有 resources 下 media 目录里的图片和 SVG 时
- [模块配置（module.json5）](module-config/index.md)（23 条）：源 AndroidManifest 有 <activity>、<service>、<intent-filter>，res/xml 下有 shortcuts、appwidget-provider，或导航图里有页面；目标端有 module.json5 的 abilities、extensionAbilities、skills、metadata，app.json5 的 configuration，或 profile 下的 main_pages.json、form_config.json 时
- [权限声明](permissions/index.md)（12 条）：源 AndroidManifest 有 uses-permission，或目标 module.json5 的 requestPermissions 里要声明 ohos.permission.* 时
- [原始文件（rawfile）](rawfile/index.md)（3 条）：源工程 src/main/assets 下有音频、预置数据等文件，代码用 AssetManager、openFd 按文件名读；目标端有 resources/rawfile 和 getRawFd 时
- [资源名和资源键](resource-keys/index.md)（5 条）：目标端 resources 下有 media 文件和 element/*.json 的条目，页面用 $r('app.…')、module.json5 用 $string: 引用它们，或源 res 来自 apktool 反编译、资源由转换脚本批量生成写回时
- [字符串](strings/index.md)（29 条）：源端有 res/values*/strings.xml、arrays.xml 和 values-* 语言目录，或控件、代码引用的 @string、@android:string、android.R.string 文案；目标端有 string.json、strarray.json 和语言限定词目录时
- [三方 SDK 和插件](third-party-sdk/index.md)（2 条）：源端接了微信 OpenSDK 等三方 SDK 或 Flutter 插件；目标端有 oh-package.json5 的依赖、querySchemes，或根 pubspec.yaml 的 dependency_overrides 时
