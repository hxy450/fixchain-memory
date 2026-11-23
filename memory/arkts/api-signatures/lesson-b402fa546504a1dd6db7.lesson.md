# TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象

ID：`lesson-b402fa546504a1dd6db7` · 版本：2

[本主题](index.md)

## 何时使用

页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时

## 适用情境

目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。

## 例外与边界

- 只改以对象字面量写页签标题（如 { title }）的地方；已经以 @Builder（CustomBuilder）、TabBarOptions 或 SubTabBarStyle/BottomTabBarStyle 写的页签照原样保留，不为统一写法改成纯字符串——改成字符串会丢掉原有的图标、选中色等样式。
- API 18 起 tabBar 还接受 ComponentContent；工程最低 API 不低于 18 时，已有的 ComponentContent 页签不算错。

## 原因

tabBar 的重载里没有 title 字段；{ title: 'X' } 在全部重载下都不匹配，编译报 10505001 No overload matches this call。来源中修复者为修无关的导入错误重写主页，把此前未见报错的 @Builder 页签换成了 { title } 对象。

## 做法

1. 纯文字页签写 .tabBar('首页')；文字加图标用 TabBarOptions 的 { icon, text } 或 BottomTabBarStyle；只改选中与未选中的文字颜色或 svg 图标颜色时，可用 SubTabBarStyle/BottomTabBarStyle 的 labelStyle、iconStyle 设置；需要其他自定义样式时用 @Builder 方法作为 CustomBuilder 传入。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-11c15d99c36e52d8aa59](../../../store/cases/case-11c15d99c36e52d8aa59/13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af.json) · 结论：diagnosis, recommendation:2
  卡片版本：`13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af`
