# 在回调中设置的状态连同时机移植，并补齐源控件自带的前置过滤

ID：`lesson-af89611fa71ea0eb6f45` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android 回调中的命令式状态（尾部按钮、进度、空态）和控件监听映射为 ArkUI 声明式条件与事件时

## 适用情境

源在搜索执行等回调里才设置尾部按钮与进度条；SearchView 只在去空白后非空时回调 onQueryTextSubmit，映射参考只给出监听名到事件名的对应。

## 原因

改写成仅由参数派生的静态条件会让元素提前出现；漏掉框架自带过滤、并在提前 return 时不复位加载标志，会无限转圈。

## 做法

1. 用只在该回调执行后才置位的状态门控条件渲染。
2. 映射控件监听前先核对 Android 控件的前置过滤（如空提交不回调）并在目标事件里补上；凡置了加载标志的路径，提前 return 时都复位。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-aa81c21ff3eaca257ba4](../../../store/cases/case-aa81c21ff3eaca257ba4/186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674.json) · 结论：diagnosis
  卡片版本：`186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674`
- [case-f226842558d82e3f3ad9](../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：recommendation:1, recommendation:2
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
