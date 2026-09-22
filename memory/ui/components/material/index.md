# ui/components/material

从 Material 组件调用推导真实尺寸、槽位和留白时进入。

[上一级](../index.md)

## 本级经验

- [迁移 Material 组件时应区分调用方修饰符与库内测量及槽位](lesson-b7e0ff573247b0324bef.lesson.md)
  - 时机：规格提取或界面实现阶段，从 Material 组件调用点推导目标端尺寸、留白与元素位置时
  - 情境：源代码只显式给出部分 size、padding 或内容槽，真实界面还受组件库的最小交互尺寸、标题 inset、导航槽和动作槽布局影响；可用快照可能由源码合成且没有 bounds。
  - 例外：源组件关闭或覆盖了库默认约束，或已有当前版本真机 bounds 可直接作为权威输入
