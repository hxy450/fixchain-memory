# 宽窗的列表-详情分栏

agent 会看到什么：读到 Compose NavDisplay 用 ListDetailSceneStrategy 按目的地的 metadata（listPane、detailPane、detailPlaceholder）分栏；产物里驱动 Navigation .mode(NavigationMode.Split / Stack) 的宽窗条件和 navBarWidth

## 规矩

- rule-fd00af2a0b2f｜宽窗列表-详情分栏按当前目的地的 pane 角色判断，不按所在顶层｜读到：源端 ListDetailSceneStrategy 按各目的地的 metadata 分栏：只有某个目的地带 ListDetailSceneStrategy.detailPane()，列表根是 listPane(detailPlaceholder = …)，同顶层下 push 的其他目的地（如顶栏 Search）没有 pane 元数据；规格路由表只把详情目的地标为「详情 pane」；写错：分栏条件写成「宽窗 && 当前顶层 === 列表顶层」驱动 Navigation 的 .mode(NavigationMode.Split)，同一顶层下 push 的非详情目的地也被挤进右侧详情 pane
