# 新增字符串资源前确认源端 strings.xml 有对应文案，没有就不建

审的是：资源
触发（任一种）：
- 读到：源端 res/values/strings.xml 里没有对应的 `<string>` 条目；写错的样子：目标 string.json 里新建了源端没有的文案条目（随补出的按钮一起加）
适用范围：修复或补 UI 时往 resources/base/element/string.json 加条目
做法：
- 新增 string.json 条目前，在源端 strings.xml（含各语言 values-*）里找到对应文案；找不到就不建，并回查这处 UI 该不该加
来源：1 张卡，1 个应用
- case-5e406619f9f3d3f028c6（话费流量查询助手）：做法第 1 步 ← 建议 3
