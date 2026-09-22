# ui/components/material

从 Material 组件调用推导真实尺寸、槽位和留白时进入。

[上一级](../index.md)

## 本级经验

- [Material 交互组件的声明尺寸、布局占位和触控区域应分开映射](lesson-b7e0ff573247b0324bef.lesson.md)
  - 时机：规格提取或界面实现阶段，将 Material 交互组件的 size 映射为目标端固定尺寸时
  - 情境：源端 IconButton 等交互组件带 size 修饰符，同时受组件库最小交互尺寸与约束影响；源码合成快照缺少实际 bounds。
  - 例外：当前版本与配置已明确关闭相关最小尺寸约束，或已有覆盖目标状态的可靠布局与视觉边界
- [Material 容器留白按侧和槽位映射，不把起始侧 inset 复制到末端](lesson-de5e7c73d852009e81b6.lesson.md)
  - 时机：规格提取或界面实现阶段，将 Material TopAppBar 等容器的内部留白映射为目标布局时
  - 情境：源组件通过标题、导航或动作槽提供单侧 inset，调用点未完整展示库内部布局。
  - 例外：当前工程明确覆写了库内留白规则，并已有相应组件契约
