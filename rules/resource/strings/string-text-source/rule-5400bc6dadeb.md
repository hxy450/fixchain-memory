# 追加 string.json 键时，把源端代码格式化的标题、数量、单位格式串一并登记

审的是：资源
触发（任一种）：
- 读到：源端代码用 `SimpleDateFormat`、`String.format` 或拼接生成带单位的标题、数量（如 `"yyyy年M月"`、`"%02d月"`）；写错的样子：模块 `string.json` 追加了一批静态文案键，却没有这段文案的格式串（如 `%s年%s月`）
适用范围：界面转换时往模块 string.json 追加文案键
做法：
- 写组件前先看本模块 string.json 已有的 %s / %d 条目和命名前缀，沿用同一写法
- 追加静态文案键时，把本页动态标题、数量、单位等格式串一并登记成 `{ "name": "<同前缀>_<用途>", "value": "%s年%s月" }` 这样的条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- { "string": [ { "name": "message_notification", "value": "Hello, %1$s!,You have %2$d new messages." } ] }：string.json 里带占位符的条目写法（出处：resource-categories-and-access.md，资源文件示例）
- `%s年%s月` 这样的重复 %s 条目可用，配合 $r 传两个字符串参数显示正确：卡里修好后用的格式串（出处：卡里修好并验证过）
针对本应用要查的：
- 本模块已有的参数化条目和命名前缀：目标工程该模块 resources/base/element/ 下的 string.json；找 value 里带 % 的条目，照它的 name 前缀和占位符写法登记新键
来源：1 张卡，1 个应用
- case-c8f1e6989f066bb2f51a（掌上燃气管家）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 2 ← 诊断
