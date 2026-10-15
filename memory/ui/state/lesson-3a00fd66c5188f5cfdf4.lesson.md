# 负责上抛自身可见性的组件必须常建，不被条件构建或 Visibility.None 包住

ID：`lesson-3a00fd66c5188f5cfdf4` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，翻译“容器初始隐藏、内部组件常驻并自行通知宿主显示”的结构，或向他人预留的条件槽位嵌入组件时

## 适用情境

源容器 visibility=gone，但内部 Fragment 在 onCreate 即挂载，并由它调用宿主的可见性方法；目标用 if 或 Visibility 控制容器。

## 原因

ArkUI 中 if 为假或 Visibility.None 下的自定义组件不会实例化（aboutToAppear 不执行，修复期实测），唯一能把可见性置真的组件不存在，形成死锁。

## 做法

1. 让该组件常建（高度 0 加 clip，或用 opacity、命中控制显示），不用 if 或 Visibility.None 包住。
2. 向宿主槽位嵌入组件前读取包住槽位的构建条件；若条件依赖本组件上抛的状态，先改宿主为常建或登记接线问题。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-590e7a719e7ced6a558d](../../../store/cases/case-590e7a719e7ced6a558d/a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`a06d50e4608fc813ee38b5709db5b02832a251760aec789ba9ab960201db143a`
