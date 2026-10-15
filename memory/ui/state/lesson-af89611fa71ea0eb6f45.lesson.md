# SearchView.onQueryTextSubmit 等回调里才置位的尾部按钮与进度，连同触发时机和控件自带的空提交过滤一起移植

ID：`lesson-af89611fa71ea0eb6f45` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android 回调中的命令式状态（尾部按钮、进度、空态）和控件监听映射为 ArkUI 声明式条件与事件时

## 适用情境

源在 onQueryTextSubmit 等回调触发的搜索流程里才设置尾部按钮与进度条；SearchView 只在去空白后非空时回调 onQueryTextSubmit，映射参考只给出监听名到事件名的对应，不含这层过滤。

## 原因

改写成仅由参数派生的静态条件会让元素提前出现；目标事件没有源控件的前置过滤时，空提交也会进入处理；先置加载标志、随后在空查询等分支提前返回而不复位，会一直转圈。

## 做法

1. 用只在该回调执行后才置位的状态门控条件渲染。
2. 映射控件监听前先核对 Android 控件的前置过滤（如 SearchView 去空白后为空不回调）并在目标事件开头补上：先过滤，通过后再置加载标志；置了加载标志之后仍会提前返回的路径（如处理函数内的空查询分支）都要复位。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f226842558d82e3f3ad9](../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
