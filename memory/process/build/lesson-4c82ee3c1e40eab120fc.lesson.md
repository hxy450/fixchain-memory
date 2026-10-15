# 编译报 API、字段或枚举成员不存在、类型不符时，按原调用语义在本地 d.ts 选替代，不就近换名、不连内容删掉、不换数据源

ID：`lesson-4c82ee3c1e40eab120fc` · 版本：2

[本主题](index.md)

## 何时使用

编译修复阶段，报错指向 SDK 不存在的 API、参数字段或枚举成员，或指出类型不符（如 Resource 不能赋给 string）时；规格或实现阶段为源端系统 API 选目标 API 时

## 适用情境

报错来自调用了 SDK 不存在的参数字段（如在 AlertDialog 参数里写自定义内容 builder），修复者准备删掉该字段连同其中承载的控件；或报错指向不存在的 API（如映射给单调时钟的 Web API），修复者准备换成语义不同的替代（如会随校时跳变的墙钟）；或枚举没有某成员（如 FontWeight.SemiBold），修复者准备按名称换成相邻成员；或 Resource 赋给只收 string 的字段（如 PopupOptions.message），修复者准备换成枚举名、rawName 等字面串。

## 原因

按名称就近替换或连内容一起删掉能通过编译，却改变了原调用承担的语义（字重、单调性、本地化文案、复选框与偏好写入），退化之后不会再报错；只剩语义不同的替代时在编译门内落地，差异就只停留在遗留披露里。

## 做法

1. 先写明原调用承担的语义（原调用注释、规格映射或源端 API，如 System.nanoTime 是单调时钟），再在当前 SDK 的 ets/api 与 kits d.ts 中按语义检索候选并读完声明，包括属性方法是否另接受数值等能精确表达原值的形式（如 fontWeight 接受 600）；不按名称就近换成相邻成员。
2. 报错指向不存在的参数字段时，改用能承载同一内容的 API（带复选框的确认框改用 openCustomDialog 或 @CustomDialog 自定义弹窗），不连内容一起删掉；改写组件属性参数前，按 d.ts 签名或编译器重载提示确认可用类型，不自造对象字段。
3. 类型不符时只转换类型、不换数据来源：Resource 赋给只收 string 的字段时，用 resourceManager.getStringSync 把原 Resource 解析成当前语言字符串，或改用接受 Resource 或 builder 的重载；要以“源端本来如此”解释改动时，先回读对应源码。
4. 只剩语义不同的替代（如墙钟代替单调时钟）时不在编译门内落地，作为决策缺口回报主线程，在生成期补查并修正；只能临时降级时按占位规则登记丢失的行为，并在报告中列为行为差异。

来源支持：7 张卡 · 4 次迁移 · 4 个应用

## 来源（按需复核）

- [case-036361d8949e7daf5247](../../../store/cases/case-036361d8949e7daf5247/c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79.json) · 结论：recommendation:4
  卡片版本：`c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79`
- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：recommendation:7
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-11c15d99c36e52d8aa59](../../../store/cases/case-11c15d99c36e52d8aa59/13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af.json) · 结论：recommendation:2
  卡片版本：`13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af`
- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, recommendation:4
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-7ced02d9c41ab6f4919a](../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：recommendation:4
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
- [case-abb1f63235ed950c4841](../../../store/cases/case-abb1f63235ed950c4841/f5b824a9ef757f00ab0eb7c877fdd33947c2fdd54420510962728ba20a259f79.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f5b824a9ef757f00ab0eb7c877fdd33947c2fdd54420510962728ba20a259f79`
- [case-d8867d30fe76e4d44ceb](../../../store/cases/case-d8867d30fe76e4d44ceb/3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932`
