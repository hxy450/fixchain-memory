# 系统栏外观按源主题实际表现设置，横屏时显式显示状态栏

ID：`lesson-9f63aee8d01fcad54884` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，在入口Ability中为全屏页设置窗口布局、系统栏颜色与显隐时

## 适用情境

源Activity使用未定制系统栏的标准主题（无translucent、statusBarColor、全屏或SYSTEM_UI标志），目标规格只要求按沉浸式架构实施；源端支持横屏。

## 例外与边界

- 源端确实设置了透明或沉浸系统栏、全屏标志时，按源端设置迁移

## 原因

沉浸式模板的透明系统栏是模板默认值，不是源端外观；“背景延伸到系统栏下”与“系统栏透明”是两件事。鸿蒙手机横屏默认隐藏状态栏，而安卓横屏仍显示。

## 做法

1. 按源主题与targetSdk的默认外观设置statusBarColor/navigationBarColor（未定制系统栏的旧主题通常为不透明黑底白图标），同时保留全屏布局与安全区避让。
2. 源端横屏显示状态栏时，调用setSpecificSystemBarEnabled('status', true)，并在avoidAreaChange与windowSizeChange中都重算避让区。
3. 规格注入沉浸式契约时，同时记录源端系统栏外观和横竖屏显隐。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5d9359065333b58b22e1](../../../store/cases/case-5d9359065333b58b22e1/b1b9d96485ff863b1016ab0b477ed90f4da12accb0ecd4746f5538a431bc6962.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b1b9d96485ff863b1016ab0b477ed90f4da12accb0ecd4746f5538a431bc6962`
