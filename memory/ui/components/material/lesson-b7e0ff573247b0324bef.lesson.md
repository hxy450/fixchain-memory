# 迁移 Material 组件时应区分调用方修饰符与库内测量及槽位

ID：`lesson-b7e0ff573247b0324bef` · 版本：1

[本主题](index.md)

## 何时使用

规格提取或界面实现阶段，从 Material 组件调用点推导目标端尺寸、留白与元素位置时

## 适用情境

源代码只显式给出部分 size、padding 或内容槽，真实界面还受组件库的最小交互尺寸、标题 inset、导航槽和动作槽布局影响；可用快照可能由源码合成且没有 bounds。

## 例外与边界

- 源组件关闭或覆盖了库默认约束，或已有当前版本真机 bounds 可直接作为权威输入

## 原因

调用方字面值不等于组件最终测量值，库内规则也常具有方向性；把较小 size 当成实绘尺寸或把起始侧 inset 复制到两侧，会在下游固化错误的尺寸和位置。

## 做法

1. 按当前组件库版本列出调用方修饰符、最小交互尺寸、内容实绘边界和各槽位占位，分侧记录留白，不将单侧 token 扩成对称 padding。
2. 无真机 bounds 时，将由库默认值推导的具体尺寸标为低置信并安排设备复核；调整外框尺寸时以视觉中心和各侧边距为约束。
3. 规格一旦引用某个库默认值，就同时覆盖决定该组件几何的相关 inset 与槽位规则。

## 检查

- 用当前库版本的真机 dump 或截图测量组件外框、内容框、视觉中心以及两端到屏缘距离，并逐项替换合成快照中的推断值。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-2280cf8a2bf7682ff26b](../../../../store/cases/case-2280cf8a2bf7682ff26b/cc8fc7c67dc300609c7e0e3f4aade4d9a14da59a39a9ca7d03283e9b02a90e48.json) · 结论：recommendation:1, recommendation:2, recommendation:3
  卡片版本：`cc8fc7c67dc300609c7e0e3f4aade4d9a14da59a39a9ca7d03283e9b02a90e48`
- [case-6eec56e15cefd5c659cb](../../../../store/cases/case-6eec56e15cefd5c659cb/c485b924cd70665967de43755b2e70352a1b4ceb7eb6723c9079f3d09eba0b93.json) · 结论：recommendation:1, recommendation:2
  卡片版本：`c485b924cd70665967de43755b2e70352a1b4ceb7eb6723c9079f3d09eba0b93`
