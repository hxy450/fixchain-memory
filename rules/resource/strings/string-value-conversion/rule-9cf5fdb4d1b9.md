# 数组资源项里的 @string/ 等引用同样改写成 $string: 形式，并检查全文件无残留

审的是：资源
触发（任一种）：
- 读到：源端 <string-array> 的 <item> 写成 @string/name 等资源引用；写错的样子：strarray.json 的数组项原样保留 `@string/`；转换脚本只对 string、integer、bool 标量做了引用改写
适用范围：把安卓数组资源里的资源引用项转成鸿蒙 element JSON 时
做法：
- 数组项里的安卓资源引用和标量值一样走引用映射：@string/x → $string:x，@color/x → $color:x
- 脚本跑完后检查每个 element JSON 全文件没有残留的 '@string/' 等安卓引用前缀，通过后再镜像到限定目录
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 数组项包成对象并把 '@string/' 改为 '$string:' 后编译通过：修复后的引用写法（出处：卡里修好并验证过）
- "label": "$string:app_name"：鸿蒙侧资源引用的写法是 $类型:名（出处：resource-categories-and-access.md，静态overlay配置方式（module.json5 的 label 写法））
来源：1 张卡，1 个应用
- case-66bbb9dcd4568f498efa（AntennaPod）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 3；取值 1 ← 诊断
