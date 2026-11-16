# 资源阶段宣布通过前，按值形态分组列出未解析项并扫一遍 color.json，非法数为零才算过

审的是：计划与派工
触发（任一种）：
- 读到：转换脚本运行后只打印总数（unresolved: N、值非法若干条）；写错的样子：资源阶段 brief 或 resource-mapping 宣布 PASS，只有未解析总数，没有按 @android: / @color/ / ?attr 分组的清单，也没有 color.json 值合法性扫描和 $color: 目标存在性核对的结果
适用范围：资源转换阶段的完成报告、资源映射文档和阶段门禁
做法：
- 写完 element JSON 后，把未解析项按值形态分组列出：@android:、@color/、?attr，各自的条数和名字
- 用正则扫一遍 color.json 的所有 value（只许 ^#([0-9A-Fa-f]{3,4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$ 或 ^\$color:\w+$），并核对每个 $color: 的目标条目存在；非法数为零后再写 PASS
来源：1 张卡，1 个应用
- case-6f9262e95abc71d3d226（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
