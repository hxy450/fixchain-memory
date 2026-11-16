# 模板工程里已有的 element 文件（string.json）

agent 会看到什么：读到模板工程的 base/element/string.json 已有 module_desc、EntryAbility_desc、EntryAbility_label，module.json5 用 $string:module_desc 等引用它们；转换脚本只用 Android strings 重建 string.json 并整文件写回，被引用的 $string 键没了

## 规矩

- rule-33dd21bcfeec｜资源转换写入模板工程已有的 string.json 等 element 文件时合并条目，不整文件覆盖｜读到：模板工程的 entry/src/main/resources/base/element/string.json 已有 module_desc、EntryAbility_desc、EntryAbility_label，module.json5 用 $string:module_desc 等引用它们；资源规则写明 element JSON 已存在时合并新条目、不要覆盖；写错：转换脚本只用 Android strings 重建 string.json 并整文件写回，module.json5、app.json5 引用的 $string 键被删，后面编译报 $string:module_desc 未定义
