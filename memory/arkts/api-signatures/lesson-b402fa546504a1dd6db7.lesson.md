# 为 TabContent 写页签时按 tab_content.d.ts 的 tabBar 重载传值，不传 { title } 对象

ID：`lesson-b402fa546504a1dd6db7` · 版本：2

[本主题](index.md)

## 何时使用

页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时

## 适用情境

目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。

## 原因

tabBar 的重载（tab_content.d.ts：string | Resource | CustomBuilder | TabBarOptions；SubTabBarStyle | BottomTabBarStyle；API 18 起另有含 ComponentContent 的合并重载）里没有 title 字段；{ title: 'X' } 在全部重载下都不匹配，编译报 10505001 No overload matches this call。

## 做法

1. 纯文字页签写 .tabBar('首页')；文字加图标用 TabBarOptions 的 { icon, text } 或 BottomTabBarStyle；需要按选中态改颜色等自定义样式时用 @Builder 方法作为 CustomBuilder 传入；compatibleSdkVersion 不低于 API 18 时也可传 ComponentContent。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-11c15d99c36e52d8aa59](../../../store/cases/case-11c15d99c36e52d8aa59/13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af.json) · 结论：diagnosis, recommendation:2
  卡片版本：`13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af`
