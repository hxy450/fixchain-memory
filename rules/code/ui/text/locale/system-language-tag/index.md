# 系统语言标签的解析和映射

agent 会看到什么：读到源端按设备语言主标签（=== 'zh'）映射成 zh-TW 一类的语言码，其余交给检测插件；产物里系统语言解析函数（getSystemLanguage、getFirstPreferredLanguage）对 zh-Hans / zh-Hant 的 script、region 分支

## 规矩

- rule-9dca56e6f5a4｜解析系统语言时按 script/region 分支映射，不把主标签 zh 一律映射为繁体｜读到：源端只在设备语言严格 `=== 'zh'` 时强制映射为 `zh-TW`，其余交给检测插件；写错：目标的系统语言解析函数在主标签为 `'zh'` 时一律返回 `'zh-TW'`，zh-Hans 系统显示繁体
