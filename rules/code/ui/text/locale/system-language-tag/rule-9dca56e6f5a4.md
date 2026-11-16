# 解析系统语言时按 script/region 分支映射，不把主标签 zh 一律映射为繁体

审的是：代码
触发（任一种）：
- 读到：源端只在设备语言严格 `=== 'zh'` 时强制映射为 `zh-TW`，其余交给检测插件；写错的样子：目标的系统语言解析函数在主标签为 `'zh'` 时一律返回 `'zh-TW'`，zh-Hans 系统显示繁体
适用范围：目标端把系统语言 BCP 47 标签映射到源端语言包代码的函数
做法：
- 分支写成：裸 'zh'→'zh-TW'（源端规则）；含 'Hans' 或以 '-CN' 结尾→'zh-CN'；其余 zh 变体→'zh-TW'
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 裸 zh→zh-TW，含 Hans 或以 -CN 结尾→zh-CN，其余 zh 变体→zh-TW：修复后的映射，zh-Hans 系统显示简体，与安卓基线一致（出处：卡里修好并验证过）
- 系统语言为简体中文时 i18n.System.getSystemLanguage() 返回 'zh-Hans'：目标端拿到的是带 script 的标签（出处：js-apis-i18n.md，getSystemLanguage）
- static getSystemLanguage(): string：取当前系统语言（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，System.getSystemLanguage）
未核实：卡里环境是 API 26，本机按 API 23 的声明和文档核对接口
来源：1 张卡，1 个应用
- case-b3a0f2338f5f2dd14ef8（Countdate）：做法第 1 步 ← 诊断、建议 2；取值 1 ← 诊断
