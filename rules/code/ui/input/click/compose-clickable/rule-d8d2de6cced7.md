# 源端整卡 clickable(role = Button) 合并子文本时，目标容器合并朗读，独立关闭键单给 BUTTON

审的是：代码
触发（任一种）：
- 读到：源端标题和正文放在同一个 Column.clickable(onClick, role = Role.Button) 里，关闭键是独立的 IconButton(onClick = …)；写错的样子：目标只给外层容器挂 .onClick(...)，标题、正文各自被单独朗读，关闭键没有 accessibilityRole
适用范围：整卡可点击、卡内另有独立动作按钮的组件转写时
做法：
- 容器写 .accessibilityGroup(true) 或合并好的 .accessibilityText(...) 加 .accessibilityRole(AccessibilityRoleType.BUTTON)，子 Text 写 .accessibilityLevel('no') 不再单独朗读
- 独立的关闭或动作按钮单独写 .accessibilityRole(AccessibilityRoleType.BUTTON)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- accessibilityGroup(value: boolean): T，默认 false：开启后组件和子组件被当成一个可选单元，读屏不再聚焦单个子组件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityGroup）
- accessibilityLevel(value: string): T，取值 "auto"、"yes"、"no"、"no-hide-descendants"，默认 auto："no" 让该组件不被无障碍服务识别（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityLevel）
- accessibilityText(text: Resource): T；组件同时有文本和无障碍文本时只读无障碍文本：合并朗读的文本用资源写（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityText）
- 合并 accessibilityText、子文本 accessibilityLevel('no')、关闭键独立 BUTTON：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8dd5c1f1f269d142cc22（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
