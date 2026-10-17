# 在回调中设置的状态连同时机移植，并补齐源控件自带的前置过滤

ID：`lesson-af89611fa71ea0eb6f45` · 版本：2 · 阶段：execute · 主题：[ui/state/binding](index.md)

概要：回调中置位的状态按回调门控并补控件过滤

信号：`onQueryTextSubmit`, `SearchView`, `onSubmit`, `isLoading`

## 何时使用

界面实现阶段，把 Android 回调中的命令式状态（尾部按钮、进度、空态）和控件监听映射为 ArkUI 声明式条件与事件时

## 适用情境

源在搜索执行等回调里才设置尾部按钮与进度条；SearchView 只在去空白后非空时回调 onQueryTextSubmit，映射参考只给出监听名到事件名的对应。

## 原因

改写成仅由参数派生的静态条件会让元素提前出现；漏掉框架自带过滤、并在提前 return 时不复位加载标志，会无限转圈。

## 做法

1. 用只在该回调执行后才置位的状态门控条件渲染。
2. 映射控件监听前先核对 Android 控件的前置过滤（如空提交不回调）并在目标事件里补上；凡置了加载标志的路径，提前 return 时都复位。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [不补源端没有的元素；框架默认元素须保留](../../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）
- [源端层层委托时追到最终实现再写规格与代码](../../../process/inferred-not-traced/lesson-4606ccc434e247d4a240.lesson.md)（共享 1 张卡）
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../../theme/sources/lesson-47785524c7f132ea7efe.lesson.md)（共享 1 张卡）
- [圆角加描边时 radius 写进 .border()](../../theme/effects/lesson-8b7c4ece5e5bf7704a44.lesson.md)（共享 1 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f226842558d82e3f3ad9](../../../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：rec-b4dc51e8e3, rec-d98a2d341a
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
