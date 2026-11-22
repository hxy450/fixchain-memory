# 转写 Compose 可点击行与卡片时一并落实无障碍语义：role 写 accessibilityRole、enabled 写 .enabled()，整卡合并朗读、卡内独立按钮单独成节点

## 何时使用

界面实现阶段，把 Compose 可点击行、卡片与图标按钮的 clickable/combinedClickable 修饰转写为 ArkUI 点击、长按与无障碍属性时；规格提取阶段为这类组件写验收条目时

## 适用情境

源端用 clickable 或 combinedClickable(enabled = 条件, role = Role.Button, onLongClick = …) 让整行或整卡可点（常经共享的行背景组件），卡内另有 IconButton 等独立关闭或动作按钮；目标准备用 onClick、LongPressGesture 实现，规格或验收条目只写了结构、样式与回调。 只转写源修饰实际给出的语义参数：源端 clickable 没写 role（role 默认为空）时不补 BUTTON 角色，没写 enabled 条件时不臆造可用条件。

## 原因

ArkUI 的 onClick 与手势只承载事件，不会像 Compose clickable 那样带出按钮角色、禁用态与子内容合并；只转写回调时，读屏听不到“按钮”，不可操作时仍报可激活，整卡被拆成多段文字，卡内关闭键也没有角色。规格未写这些语义时，源 Modifier 仍足以推出。

## 做法

1. 逐项转写源修饰的语义参数：role = Role.Button 写 .accessibilityRole(AccessibilityRoleType.BUTTON)；enabled 条件原样写 .enabled(条件)，点击与长按共用这一可用态（源端常写成“onClick 或 onLongClick 存在即可用”）。
2. 整卡可点、子文本在源端合并为一个朗读节点时，让容器成为单一节点：容器内没有独立动作时可用 .accessibilityGroup(true)；容器内还有关闭等独立按钮时，accessibilityGroup(true) 会把子组件一并并入，改为给容器设由同一资源文本组成的合并 accessibilityText，子 Text 设 .accessibilityLevel('no')，独立按钮保留自身节点、BUTTON 角色与源端的无障碍文本。
3. 规格提取写组件验收条目时，把源端的角色、可用条件、合并与独立朗读关系写进条目，不只写结构、样式与回调。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 未用。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕enabled(false) 时组件不响应点击操作
- 〔做法第 2 步〕accessibilityGroup 默认 false；设为 true 时组件和它的全部子组件被当成一个可选单元，读屏不再分别聚焦其中的子组件（含子组件里的按钮）
- 〔做法第 2 步〕accessibilityLevel 默认 "auto"（由无障碍分组服务和 ArkUI 决定能否被识别）；"no" 让该组件不被无障碍服务识别，"no-hide-descendants" 让组件和子组件都不被识别
- 〔做法第 2 步〕组件同时有文本内容和 accessibilityText 时，读屏只读 accessibilityText
