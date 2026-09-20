# ui/render/shadow

elevation→ShadowOptions 配方与单位

[上一级](../index.md)

## 本级经验

- [ArkUI ShadowOptions 的 radius/offset 单位是 px：dp 高程配方必须显式 vp2px，且全工程只走一条共享映射](lesson-2b6f4b263066bc60b199.lesson.md)
  - 时机：规格提取阶段为阴影/模糊/偏移这类数值型渲染属性写配方时；界面实现阶段把源侧 dp 高程落到 ArkUI .shadow() 时
  - 情境：源侧用 Compose Modifier.shadow(elevation: Dp) 或 Material 容器高程；目标用 .shadow(ShadowOptions | ShadowStyle)，工程已定义共享 elevation→shadow 映射函数。
