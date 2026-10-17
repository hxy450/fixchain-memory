# 负责上抛自身可见性的组件必须常建，不被条件构建或 Visibility.None 包住

ID：`lesson-3a00fd66c5188f5cfdf4` · 版本：2 · 阶段：execute · 主题：[ui/state/binding](index.md)

概要：上抛自身可见性的组件常建，不包 if/None

信号：`Visibility.None`, `visibility="gone"`, `aboutToAppear`, `Fragment`, `setVisibility`

## 何时使用

界面实现阶段，翻译“容器初始隐藏、内部组件常驻并自行通知宿主显示”的结构，或向他人预留的条件槽位嵌入组件时

## 适用情境

源容器 visibility=gone，但内部 Fragment 在 onCreate 即挂载，并由它调用宿主的可见性方法；目标用 if 或 Visibility 控制容器。

## 原因

ArkUI 中 if 为假或 Visibility.None 下的自定义组件不会实例化（aboutToAppear 不执行，修复期实测），唯一能把可见性置真的组件不存在，形成死锁。

## 做法

1. 让该组件常建（高度 0 加 clip，或用 opacity、命中控制显示），不用 if 或 Visibility.None 包住。
2. 向宿主槽位嵌入组件前读取包住槽位的构建条件；若条件依赖本组件上抛的状态，先改宿主为常建或登记接线问题。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [?attr 主题色逐主题取值导出 base/dark 对键](../../theme/tokens/lesson-1856958fc6d369f0e2bb.lesson.md)（共享 1 张卡）
- [底栏之上的 BottomSheet 面板用布局内 Stack](../../layout/layers/lesson-9f45b5d79206b5654aff.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-590e7a719e7ced6a558d](../../../../../store/cases/case-590e7a719e7ced6a558d/a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a.json) · 结论：diagnosis, rec-b1dac6c973, rec-77d85e4373
  卡片版本：`a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a`
