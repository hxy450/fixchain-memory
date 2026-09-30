# TabContent.tabBar 只接受字符串、资源、CustomBuilder、TabBarOptions 与 SubTabBarStyle/BottomTabBarStyle，不传 { title } 对象

ID：`lesson-b402fa546504a1dd6db7` · 版本：1

[本主题](index.md)

## 何时使用

页面实现或编译修复阶段，为 Tabs 的 TabContent 编写或改写页签时

## 适用情境

目标主页用 Tabs + TabContent 做底部导航，页签为纯文字、文字加图标或带选中色的自定义样式；写者准备以对象字面量表达页签标题。

## 原因

tabBar 的重载里没有 title 字段；{ title: 'X' } 在全部重载下都不匹配，编译报 10505001 No overload matches this call。来源中修复者为修无关的导入错误重写主页，把此前未见报错的 @Builder 页签换成了 { title } 对象。

## 做法

1. 纯文字页签写 .tabBar('首页')；文字加图标用 TabBarOptions 的 { icon, text } 或 BottomTabBarStyle；需要按选中态改颜色等自定义样式时用 @Builder 方法作为 CustomBuilder 传入。

