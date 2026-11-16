# 规格给吸顶列映射时写明吸顶内容仍属滚动容器，只给 ListItemGroup header 加 sticky

审的是：规格
触发（任一种）：
- 读到：源端 Compose LazyColumn 里有 stickyHeader，或按开关在 stickyHeader 与 item 间切换；写错的样子：规格的吸顶映射并列「Stack + offset」这类可能把头部移出滚动容器的方案，或没写必须保持的行为（从吸顶区起拖照常滚动）；验收条目里没有从吸顶区起拖的检查
适用范围：规格提取阶段写 stickyHeader 的组件映射和验收条目时
做法：
- 映射写「LazyColumn + stickyHeader → List + ListItemGroup({ header }) + .sticky(StickyStyle.Header)」，并写明必须保持的行为：吸顶内容仍属滚动容器，从它起拖照常滚动、点击照常命中；不并列 Stack + offset
- 验收条目写：吸顶后从吸顶区起拖，列表滚动
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- sticky(value: StickyStyle): ListAttribute，默认 StickyStyle.None：List 上设 ListItemGroup 头部吸顶（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.sticky）
- List 的 sticky 属性配合 ListItemGroup 使用，设为 StickyStyle.Header 即得粘性标题：规格里该写的那种映射（出处：arkts-layout-development-create-list.md，添加粘性标题）
来源：1 张卡，1 个应用
- case-172936bfc4a46ffc1d0f（GameOfLife）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 4
