# 不扩大源端的语言匹配条件；BCP 47 标签按 script/region 分别列映射并各给 AC 样例

审的是：规格
触发（任一种）：
- 读到：源端只在设备语言严格 `=== 'zh'` 时做强制映射；目标系统语言接口返回带 script/region 的 BCP 47 标签（如 zh-Hans-CN、zh-Hant-TW）；写错的样子：规格写成「主标签 zh 的任意 script/region 变体都映射为 zh-TW」，判据含 zh-Hans-CN→zh-TW
适用范围：规格里写系统语言到源端语言包代码的映射时
做法：
- 保持源端匹配条件：严格等于 'zh' 不改成主标签前缀匹配
- 按 script/region 分别列映射：Hans 或 CN→zh-CN，Hant、TW、HK→zh-TW，裸 zh→源端规则；每类各给一条 AC 判据样例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 系统语言为简体中文时 i18n.System.getSystemLanguage() 返回 'zh-Hans'：目标端系统语言带 script，不是裸 zh（出处：js-apis-i18n.md，getSystemLanguage）
- 系统语言简体中文、地区中国时 getSystemLocale() 返回 'zh-Hans-CN'：区域 ID 带 script 和 region（该接口文档标 deprecated）（出处：js-apis-i18n.md，getSystemLocale）
- static getFirstPreferredLanguage(): string：取系统偏好语言列表中的第一个语言（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，System.getFirstPreferredLanguage）
来源：1 张卡，1 个应用
- case-b3a0f2338f5f2dd14ef8（Countdate）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
