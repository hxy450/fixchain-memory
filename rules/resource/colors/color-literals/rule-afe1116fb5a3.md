# 给主题色追加 base 颜色键时，同时按深色套写 dark 的同名键，已有文件只追加不覆盖

审的是：资源
触发（任一种）：
- 读到：源端 Compose 主题按 isSystemInDarkTheme() 在 Light / Dark 两套颜色里选，深色套里同名颜色取不同值；写错的样子：base/element/color.json 追加了主题色键，dark/element/color.json 里没有同名键
- 写错的样子：用整体写入覆盖了已存在的 dark/element/color.json，模板里原有的 start_window_background 等条目被删
适用范围：页面转换中为主题色追加颜色资源（base 与 dark 限定目录）时
做法：
- 为主题色追加 base 键时，同一次按源端深色套在 dark/element/color.json 写同名键和深色值
- 写前列出 resources/dark 目录；文件已存在就先读取再只追加缺的键，不整体覆盖，保留 start_window_background 等既有条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 系统优先从匹配设备状态的限定词目录找资源，限定词目录里找不到时才去 base 目录：dark 里缺的键在深色下回落成 base 的浅色值（出处：resource-categories-and-access.md，资源匹配）
- 限定词 dark 表示深色模式，目录名形如 dark/element：深色值写在 resources/dark/element/color.json（出处：resource-categories-and-access.md，限定词目录）
- dark 目录补齐主题色同名键、恢复 start_window_background 后，深色下颜色和启动窗正确：修复后的形态（出处：卡里修好并验证过）
针对本应用要查的：
- 每个主题色键的深色值：源工程 Compose 主题文件里的深色调色板（按 isSystemInDarkTheme() 选中的那一套）；按同名颜色取深色套的值写进 dark/element/color.json；深色套没覆盖的键沿用浅色值
来源：1 张卡，1 个应用
- case-2c6857febfce92e5d5bc（Jetsnack）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断；取值 3 ← 诊断
