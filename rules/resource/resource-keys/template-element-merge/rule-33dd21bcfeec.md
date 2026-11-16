# 资源转换写入模板工程已有的 string.json 等 element 文件时合并条目，不整文件覆盖

审的是：资源
触发（任一种）：
- 读到：模板工程的 entry/src/main/resources/base/element/string.json 已有 module_desc、EntryAbility_desc、EntryAbility_label，module.json5 用 $string:module_desc 等引用它们；资源规则写明 element JSON 已存在时合并新条目、不要覆盖；写错的样子：转换脚本只用 Android strings 重建 string.json 并整文件写回，module.json5、app.json5 引用的 $string 键被删，后面编译报 $string:module_desc 未定义
适用范围：在已有 DevEco 模板工程上做资源迁移，往 string.json、color.json 等 element 文件写入时
做法：
- 先读入模板里已有的 element JSON，把 Android 转来的条目按 name 合并进去，模板已有的条目保留
- 写完 grep module.json5 和 app.json5 里的 $string:… / $color:… 引用，确认每个键在对应 resources 的 element 文件里仍然存在
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- module.json5 的 abilities 里 "label": "$string:EntryAbility_label"，需要在 entry/src/main/resources/base/element/string.json 配置 name 为 EntryAbility_label 的资源：module.json5 引用的身份键必须在模块的 string.json 里（出处：layered-image.md，配置单层图标和应用名称）
- app.json5 的 "label": "$string:app_name"，需要在 AppScope/resources/base/element/string.json 配置 name 为 app_name 的资源：app.json5 引用的键在 AppScope 的 string.json 里（出处：layered-image.md，配置单层图标和应用名称）
- 编译时 AppScope 下的资源合入模块资源，同目录同组重名时只保留 AppScope 的：合并时注意 AppScope 与模块的同名键（出处：resource-categories-and-access.md，资源匹配）
来源：1 张卡，1 个应用
- case-224eb9de83aa652829f4（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
