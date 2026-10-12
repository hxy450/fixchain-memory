# 转写 Compose 可点击行与卡片时一并落实无障碍语义：role 写 accessibilityRole、enabled 写 .enabled()，整卡合并朗读、卡内独立按钮单独成节点

ID：`lesson-5caf7eadb69e940926f9` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose 可点击行、卡片与图标按钮的 clickable/combinedClickable 修饰转写为 ArkUI 点击、长按与无障碍属性时；规格提取阶段为这类组件写验收条目时

## 适用情境

源端用 clickable 或 combinedClickable(enabled = 条件, role = Role.Button, onLongClick = …) 让整行或整卡可点（常经共享的行背景组件），卡内另有 IconButton 等独立关闭或动作按钮；目标准备用 onClick、LongPressGesture 实现，规格或验收条目只写了结构、样式与回调。

## 原因

ArkUI 的 onClick 与手势只承载事件，不会像 Compose clickable 那样带出按钮角色、禁用态与子内容合并；只转写回调时，读屏听不到“按钮”，不可操作时仍报可激活，整卡被拆成多段文字，卡内关闭键也没有角色。规格未写这些语义时，源 Modifier 仍足以推出。

## 做法

1. 逐项转写源修饰的语义参数：role = Role.Button 写 .accessibilityRole(AccessibilityRoleType.BUTTON)；enabled 条件原样写 .enabled(条件)，点击与长按共用这一可用态（源端常写成“onClick 或 onLongClick 存在即可用”）。
2. 整卡可点、子文本在源端合并为一个朗读节点时，让容器成为单一节点：容器内没有独立动作时可用 .accessibilityGroup(true)；容器内还有关闭等独立按钮时，accessibilityGroup(true) 会把子组件一并并入，改为给容器设由同一资源文本组成的合并 accessibilityText，子 Text 设 .accessibilityLevel('no')，独立按钮保留自身节点、BUTTON 角色与源端的无障碍文本。
3. 规格提取写组件验收条目时，把源端的角色、可用条件、合并与独立朗读关系写进条目，不只写结构、样式与回调。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-8dd5c1f1f269d142cc22](../../../store/cases/case-8dd5c1f1f269d142cc22/20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9.json) · 结论：diagnosis, recommendation:1, recommendation:5
  卡片版本：`20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9`
