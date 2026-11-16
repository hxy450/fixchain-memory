# stickyHeader 写成 ListItemGroup header 加 sticky，不移出 List

审的是：代码
触发（任一种）：
- 读到：Compose LazyColumn 里有 stickyHeader { … }，或按开关在 stickyHeader 与 item 之间切换同一块内容；写错的样子：吸顶内容被放到 List 外做固定兄弟（先放吸顶内容、再放只含其余项的 List），注释或报告称「Stack+offset」「行为等价」；或 List 上没有 .sticky(StickyStyle.Header)
适用范围：Compose LazyColumn 的 stickyHeader 迁成 ArkUI List 时，含按开关切换吸顶与普通项的情形
做法：
- 写成 List() { ListItemGroup({ header: this.吸顶内容的 @Builder }) { ListItem() { 其余内容 } } }.sticky(StickyStyle.Header)，吸顶内容留在 List 里
- 开关切换吸顶与普通项时，两种状态都在同一个 List 内：吸顶态放进 ListItemGroup 的 header，普通态是一个 ListItem
- 对吸顶写法仍没把握时，照规格指定的结构写出并登记 TODO 交编译门，不改用换了结构的替代写法
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- sticky(value: StickyStyle): ListAttribute，默认 StickyStyle.None：List 上设 ListItemGroup 头部吸顶或尾部吸底（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.sticky）
- StickyStyle.None = 0、Header = 1、Footer = 2、BOTH = 3（@since 20）：stickyHeader 对应 Header（出处：鸿蒙 SDK 的 ets/component/list.d.ts，StickyStyle）
- (options?: ListItemGroupOptions): ListItemGroupAttribute；ListItemGroupOptions.header?: CustomBuilder：吸顶内容用 @Builder 传给 ListItemGroup 的 header（出处：鸿蒙 SDK 的 ets/component/list_item_group.d.ts，ListItemGroupOptions.header）
- List 的 sticky 属性配合 ListItemGroup 使用，设为 StickyStyle.Header 即得粘性标题：官方的吸顶写法（出处：arkts-layout-development-create-list.md，添加粘性标题）
- 改成 ListItemGroup header + .sticky(StickyStyle.Header) 后，从吸顶区起拖列表照常滚动，点格子照常命中：移到 List 外时外观一样，但从吸顶区起拖不滚动（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-172936bfc4a46ffc1d0f（GameOfLife）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 3；取值 5 ← 诊断
