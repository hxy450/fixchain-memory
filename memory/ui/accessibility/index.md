# ui/accessibility

无障碍语义：可点击行与卡片的角色、可用态与合并朗读，图标无障碍文本按源 contentDescription 取值与多语言资源；页内遮罩弹窗的读屏模态见 dialog

[上一级](../index.md)

## 本级经验

- [图标无障碍文本按源 contentDescription 转写：null 或空串不臆造；源端有文本时用 $r 资源并沿用各语言值，不写死单一语言字面量](lesson-d80ced7be82765244889.lesson.md)
  - 时机：界面实现阶段，为图标、图标按钮、FAB 等设置 ArkUI accessibilityText、转写源端 contentDescription 时
  - 情境：源端 Icon/Image/IconButton 的 contentDescription 为 null、空串或 stringResource(R.string.x)；目标工程带多语言字符串资源；同工程里既有用 $r 的页面，也有写死某一语言无障碍文本的页面可参照。
- [转写 Compose 可点击行与卡片时一并落实无障碍语义：role 写 accessibilityRole、enabled 写 .enabled()，整卡合并朗读、卡内独立按钮单独成节点](lesson-5caf7eadb69e940926f9.lesson.md)
  - 时机：界面实现阶段，把 Compose 可点击行、卡片与图标按钮的 clickable/combinedClickable 修饰转写为 ArkUI 点击、长按与无障碍属性时；规格提取阶段为这类组件写验收条目时
  - 情境：源端用 clickable 或 combinedClickable(enabled = 条件, role = Role.Button, onLongClick = …) 让整行或整卡可点（常经共享的行背景组件），卡内另有 IconButton 等独立关闭或动作按钮；目标准备用 onClick、LongPressGesture 实现，规格或验收条目只写了结构、样式与回调。
