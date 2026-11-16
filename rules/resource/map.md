资源：27 个族，135 条规矩。用短号取族（如 recall.py show f001）。

应用级信息（AppScope）（25 条）：源端 Gradle 有 applicationId、resValue，AndroidManifest 的 <application> 写了 android:label、android:icon；目标端有 AppScope/app.json5 的 bundleName、vendor、icon，app_name、EntryAbility_label 字符串，或分层图标、启动窗图标时
  f496 AppScope/app.json5 的应用身份字段（6）；f499 应用图标、分层图标和启动窗图标（11）；f501 应用显示名的字符串键（app_name、EntryAbility_label）（8）
颜色（25 条）：源端有 colors.xml、values-night、布局和 Compose 里的色值，或颜色来自 ?attr 主题属性、控件默认样式、@android:color 和 Material 等库主题；目标端有 color.json 和 dark 目录时
  f494 主题、平台或库提供的颜色和外观值（17）；f495 源端写明的颜色值转 color.json（7）；f909 dark 目录 color.json 对页面色键的覆盖（1）
图片和矢量图（11 条）：源端 drawable 下有位图和 <vector>、<animated-vector>，布局或代码用 @drawable、R.drawable 引用图片，或 Compose 用 Icons.* 图标；目标端有 resources 下 media 目录里的图片和 SVG 时
  f497 矢量图标转 SVG 媒体资源（10）；f500 布局和代码引用的 @drawable 位图（1）
模块配置（module.json5）（23 条）：源 AndroidManifest 有 <activity>、<service>、<intent-filter>，res/xml 下有 shortcuts、appwidget-provider，或导航图里有页面；目标端有 module.json5 的 abilities、extensionAbilities、skills、metadata，app.json5 的 configuration，或 profile 下的 main_pages.json、form_config.json 时
  f498 桌面快捷方式配置和图标（4）；f503 intent-filter 对应的 module.json5 skills（8）；f504 extensionAbilities 条目的 type（1）
  f505 跟随系统设置的应用配置（屏幕方向、字号缩放）（3）；f506 appwidget-provider 转成的 form_config.json（2）；f510 main_pages.json 的 src 页面登记（2）
  f511 前台服务转成的 backgroundModes 声明（2）；f910 module.json5 的 querySchemes（1）
权限声明（12 条）：源 AndroidManifest 有 uses-permission，或目标 module.json5 的 requestPermissions 里要声明 ohos.permission.* 时
权限声明 / 系统接口要的权限（9 条）：源端有 uses-permission，或目标代码调了 http、Web、振动、剪贴板、定位这类要权限的系统接口时
  f489 module.json5 的权限声明（requestPermissions）（9）
权限声明 / 三方要求和受限的权限（3 条）：要按三方 SDK 文档或插件默认申请在 requestPermissions 里加 ohos.permission.*，或真机安装因权限被拒时
  f508 module.json5 的 requestPermissions 权限声明（3）
原始文件（rawfile）（3 条）：源工程 src/main/assets 下有音频、预置数据等文件，代码用 AssetManager、openFd 按文件名读；目标端有 resources/rawfile 和 getRawFd 时
  f502 源 assets 下的文件迁到 rawfile（3）
资源名和资源键（5 条）：目标端 resources 下有 media 文件和 element/*.json 的条目，页面用 $r('app.…')、module.json5 用 $string: 引用它们，或源 res 来自 apktool 反编译、资源由转换脚本批量生成写回时
  f493 资源文件名和 element name 里的非法字符（2）；f507 页面 $r 引用的 element 资源键（2）；f513 模板工程里已有的 element 文件（string.json）（1）
字符串（29 条）：源端有 res/values*/strings.xml、arrays.xml 和 values-* 语言目录，或控件、代码引用的 @string、@android:string、android.R.string 文案；目标端有 string.json、strarray.json 和语言限定词目录时
  f490 values-* 语言目录对应的限定词目录（8）；f491 strings.xml、arrays.xml 的值转写成 element JSON（10）；f492 string.json 条目的文案来源（11）
三方 SDK 和插件（2 条）：源端接了微信 OpenSDK 等三方 SDK 或 Flutter 插件；目标端有 oh-package.json5 的依赖、querySchemes，或根 pubspec.yaml 的 dependency_overrides 时
  f509 微信 OpenSDK 的工程配置（1）；f512 根 pubspec.yaml 的 dependency_overrides（1）
