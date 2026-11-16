# 资源名和资源键

目标端 resources 下有 media 文件和 element/*.json 的条目，页面用 $r('app.…')、module.json5 用 $string: 引用它们，或源 res 来自 apktool 反编译、资源由转换脚本批量生成写回时

## 触发族

- [资源文件名和 element name 里的非法字符](resource-names/index.md)（2 条）：源 res 来自 apktool 反编译，drawable 里有 $<父名>__N 内联片段；产物 resources 下 media 文件名或 element 的 name 含 $、-、. 等 [a-zA-Z0-9_] 以外的字符，构建报 Invalid resource name
- [页面 $r 引用的 element 资源键](r-ref-keys/index.md)（2 条）：页面 .ets 里的 $r('app.float.…') / $r('app.color.…') / $r('app.string.…') 引用，和 resources/base/element/*.json 里追加的键；源布局同一容器写了几个方向的 padding / layout_margin 时常漏键
- [模板工程里已有的 element 文件（string.json）](template-element-merge/index.md)（1 条）：读到模板工程的 base/element/string.json 已有 module_desc、EntryAbility_desc、EntryAbility_label，module.json5 用 $string:module_desc 等引用它们；转换脚本只用 Android strings 重建 string.json 并整文件写回，被引用的 $string 键没了
