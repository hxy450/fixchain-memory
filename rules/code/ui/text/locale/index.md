# 应用语言与区域

源端有 AppCompatDelegate.setApplicationLocales / getApplicationLocales、supported_locales、Locale.getDisplayName、按设备语言主标签映射语言码、lowercase(Locale.ROOT) 或按 locale 的 toUpperCase / textAllCaps，目标端有 i18n.System.setAppPreferredLanguage、getSystemLanguage / getFirstPreferredLanguage、getConfigurationSync().locale、toLocaleUpperCase 时

## 触发族

- [大小写转换和区域标签](locale-case/index.md)（2 条）：读到源端判定函数里 lowercase(Locale.ROOT) 后再比对，或按资源的 locale 做 textAllCaps / toUpperCase；产物里谓词内部直接 === / Set.has 比较，或把 getConfigurationSync().locale 原样传给 toLocaleUpperCase
- [应用内切换语言与语言名](in-app-language/index.md)（4 条）：源端用 AppCompatDelegate.setApplicationLocales / getApplicationLocales、supported_locales 做应用内语言切换并 recreate，或用 Locale.getDisplayName 生成语言名；目标端有 i18n.System.setAppPreferredLanguage / getAppPreferredLanguage、语言表和切换后取串的刷新
- [系统语言标签的解析和映射](system-language-tag/index.md)（1 条）：读到源端按设备语言主标签（=== 'zh'）映射成 zh-TW 一类的语言码，其余交给检测插件；产物里系统语言解析函数（getSystemLanguage、getFirstPreferredLanguage）对 zh-Hans / zh-Hant 的 script、region 分支
