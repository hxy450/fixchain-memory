# 工具栏菜单项按 showAsAction 分流到图标位或溢出菜单，可勾选项开启勾选指示

ID：`lesson-a6121cc7eaf207b702f7` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，转换工具栏菜单 XML 时

## 适用情境

源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。

## 原因

全部放进溢出菜单或只设选中态，会丢掉工具栏图标位与勾选指示。

## 做法

1. 含 ifRoom/always 且有图标的项放工具栏图标位，仅 never/collapseActionView 的进溢出；checkable 项显式开启 selectIcon 等勾选指示。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:5
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
