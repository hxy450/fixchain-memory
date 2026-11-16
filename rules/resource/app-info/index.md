# 应用级信息（AppScope）

源端 Gradle 有 applicationId、resValue，AndroidManifest 的 <application> 写了 android:label、android:icon；目标端有 AppScope/app.json5 的 bundleName、vendor、icon，app_name、EntryAbility_label 字符串，或分层图标、启动窗图标时

## 触发族

- [AppScope/app.json5 的应用身份字段](app-identity/index.md)（6 条）：源模块 Gradle 构建脚本里有 applicationId / namespace（反域名，第二段是组织）；AppScope/app.json5 的 bundleName、vendor、versionName 仍是模板值（com.example.myapplication、example、1.0.0），理由写成部署期、与签名绑定，或交回里没指出
- [应用图标、分层图标和启动窗图标](app-icon/index.md)（11 条）：源 AndroidManifest 的 android:icon 指向 launcher 图标（mipmap、<adaptive-icon> 的 foreground / background），启动画面取图标前景；产物 AppScope / entry media 下的 layered_image、前景背景、startIcon.png 仍是模板图，尺寸不对或没裁可见区，app.json5 的 icon 没指向分层图标
- [应用显示名的字符串键（app_name、EntryAbility_label）](app-name/index.md)（8 条）：源 AndroidManifest 的 android:label="@string/app_name" 或 Gradle 的 resValue 给了应用名；AppScope 的 app_name、entry 的 EntryAbility_label 只改了一处、写成规格给的别的字面值或按目录名自造，en_US 等语言目录里仍是 label 一类模板值
