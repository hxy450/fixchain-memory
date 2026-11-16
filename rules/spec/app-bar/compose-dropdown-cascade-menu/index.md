# Compose 的下拉菜单和级联菜单

agent 会看到什么：读到 Compose 源端用 M3 DropdownMenu、CascadeDropdownMenu 或基于 Popup 的菜单，放在触发 IconButton 所在的 Box 里，带 children 的项在同一菜单里切到子层；规格写「两级 Menu / 半模态面板」「ArkUI Menu 不支持嵌套子菜单」「弹出形态差异由 visual 断言容忍」

## 规矩

- rule-82a010b26065｜规格把下拉和级联菜单的弹出形态写成验收契约：锚点、无遮罩、点外与返回关闭、子层原地切换｜读到：Compose 源里菜单是 M3 DropdownMenu、me.saket.cascade 的 CascadeDropdownMenu 或基于 Popup 的居中菜单，放在触发 IconButton 所在的 Box 里；带 children 的项在同一菜单内切到子层；写错：规格把级联菜单映射成「两级 Menu / 半模态面板」，写了「弹出形态差异由 visual 断言容忍」这类放行条款，没写锚点、有无遮罩、关闭方式和子层切换方式
- rule-8ca57a9508e9｜规格写「ArkUI 不支持级联/子菜单」这类平台能力判断前先查文档，不确定就列待验证｜读到：源端菜单项带 children 子层（CascadeDropdownMenu）；写错：规格里写「ArkUI Menu 不支持嵌套子菜单」「无 ArkUI 等价」，并据此把形态降级为两级下拉、底部弹层或平铺
