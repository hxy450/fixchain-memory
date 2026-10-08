# 播放器面等运行时 addView 挂到根部的层，按运行时层级实现，不按 XML 里的占位区域定几何

ID：`lesson-c3dcc5a25a0ad59c53c1` · 版本：5 · 阶段：execute · 主题：[ui/layout/layers](index.md)

概要：addView 挂根部的视图放 Stack 最底层铺满

信号：`addView`, `removeView`, `LayoutParams`, `Stack`, `Adapter`, `Fragment`

## 何时使用

界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时

## 适用情境

源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0) 无约束铺满），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。

## 原因

只看 XML 会把封面/控制区当成视频区，把视频夹在标题行与按钮行之间；运行时视频其实铺满、标题与按钮浮在其上。来源中写者读到了 addView 调用，仍按 XML 区域写，视频区结构性偏小、标题错位。

## 做法

1. 先在 Fragment/Adapter 中查 addView/removeView/LayoutParams，确认运行时视图挂在哪一层、有无约束，再定层级：无约束挂到根部的，放在根 Stack 最底层铺满；XML 占位区只保留封面与播放态显隐。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [ConstraintLayout 转顺序流前先列出各子项锚点](../constraints/lesson-3fe0026df9abc72ff788.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c85d8667f78c2cc8f53a](../../../../../store/cases/case-c85d8667f78c2cc8f53a/0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf.json) · 结论：diagnosis, rec-27b8d425c2
  卡片版本：`0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf`
