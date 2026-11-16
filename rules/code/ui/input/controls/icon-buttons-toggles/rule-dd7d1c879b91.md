# 用复用开关组件替换原开关行时，整行点击热区和无障碍分组不能缩成只剩图标

审的是：代码
触发（任一种）：
- 读到：被替换的原实现在整行的 Row 上挂 .onClick(…)；写错的样子：换成复用开关组件后只有其中的 Image 上有 .onClick，行容器上的点击没了，整行也不再作为一个无障碍单元
适用范围：ArkUI 页面里用复用开关组件替换原有开关行实现时
做法：
- 替换后保留原来的点击热区：行容器上仍挂 .onClick，调用同一个显式 setter，传当前状态取反
- 核对无障碍分组没有缩小：原来整行是一个可聚焦单元的，替换后行容器仍是一个单元
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- accessibilityGroup(value: boolean): T：开启后组件和它的所有子组件视为一个可选单元，无障碍服务不再聚焦单个子组件；默认 false（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityGroup）
- accessibilityText(value: string): T：给行容器设无障碍文本，参数是 string（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityText）
- accessibilityText(text: Resource): T：另一个重载收 Resource；没有收 ResourceStr 的重载，传 ResourceStr 类型的成员要先收窄成 string 或 Resource（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityText）
来源：1 张卡，1 个应用
- case-ab54d746c8c33d3061ed（骑行记录）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2
