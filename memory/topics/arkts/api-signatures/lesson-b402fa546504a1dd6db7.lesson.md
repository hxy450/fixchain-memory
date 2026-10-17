# TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象

ID：`lesson-b402fa546504a1dd6db7` · 版本：2 · 阶段：execute/repair · 主题：[arkts/api-signatures](index.md)

概要：tabBar 不接受 { title } 对象字面量

信号：`TabContent`, `.tabBar(`, `TabBarOptions`, `BottomTabBarStyle`, `SubTabBarStyle`, `Tabs`, `CustomBuilder`

## 何时使用

页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时

## 适用情境

目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。

## 原因

tabBar 的重载里没有 title 字段；{ title: 'X' } 在全部重载下都不匹配，编译报 10505001 No overload matches this call。来源中修复者为修无关的导入错误重写主页，把此前未见报错的 @Builder 页签换成了 { title } 对象。

## 做法

1. 纯文字页签写 .tabBar('首页')；文字加图标用 TabBarOptions 的 { icon, text } 或 BottomTabBarStyle；需要按选中态改颜色等自定义样式时用 @Builder 方法作为 CustomBuilder 传入。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [编译修复只改报错行，不删功能或换异义替代](../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [编译按完整 ERROR 列表判定，失败只记 FAIL](../../process/claimed-without-receipt/lesson-7426a20525e52e34c2e7.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-11c15d99c36e52d8aa59](../../../../store/cases/case-11c15d99c36e52d8aa59/13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af.json) · 结论：diagnosis, rec-722d65c029
  卡片版本：`13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af`
