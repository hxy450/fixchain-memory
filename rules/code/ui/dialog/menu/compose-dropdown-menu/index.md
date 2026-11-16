# Compose 的 DropdownMenu、Popup 和 cascade 菜单

agent 会看到什么：读到 Compose 的 DropdownMenu / me.saket.cascade 的 CascadeDropdownMenu 锚在触发 IconButton 的 Box 里、Popup(Alignment.Center) 加 Surface(tonalElevation) 的居中菜单、带 children 的子菜单；产物里页面级 Stack 浮层的灰遮罩和固定 .position、bindMenu 的自定义内容、子菜单并排或平铺、onBackPress 先不先关菜单

## 规矩

- rule-9a9a1aedbfc3｜源端锚定或居中的无遮罩菜单，目标用 bindMenu 锚定或透明点外层，不加灰遮罩和固定位置｜读到：Compose 菜单（DropdownMenu / CascadeDropdownMenu）放在触发 IconButton 所在的 Box 里锚定弹出，没有变暗遮罩；写错：页面级 Stack 浮层：遮罩写成 .backgroundColor('#33000000') 或 '#66000000'，面板用 .position({ top: …, right: … }) 固定在屏幕某处
- rule-de6075010bba｜Compose Popup 菜单迁成无遮罩、点外和返回键先关的弹层，保留 tonalElevation｜读到：Popup(alignment = Alignment.Center, properties 或参数 focusable = true) + Surface(tonalElevation, shadowElevation)，无遮罩；调用方传 tonalElevation（如 6.dp）；写错：目标菜单加了 Column().backgroundColor('#66000000') 灰色遮罩、去掉 tonalElevation 参数；或写成 if (…) 的普通 Stack 子节点，onBackPress 不先关菜单
- rule-7542a9b5b75d｜cascade 子菜单在同一容器内原地切层，不并排多列、不平铺；bindMenu 承载时截断触摸冒泡｜读到：me.saket.cascade 的 CascadeDropdownMenu，或带 children 的菜单项在同一菜单内切到子层；写错：子菜单写成 Row 里并排的多列面板，或把 children 平铺成同级 MenuItem / Select 选项
