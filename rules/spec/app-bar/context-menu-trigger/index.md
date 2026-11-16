# 上下文菜单（registerForContextMenu、openContextMenu）

agent 会看到什么：读到源码 registerForContextMenu(view)、点击时 openContextMenu(view)（不带坐标）、onCreateContextMenu 里 setHeaderTitle / setHeaderIcon；规格写「openContextMenu 锚定在按钮上弹出」或「长按/点击 → Menu 弹出列表」，不分点击和长按两种形态，也没写标题和图标

## 规矩

- rule-28f456283ea7｜规格区分上下文菜单的两种触发：点击 openContextMenu 是居中模态列表，长按是触点浮动菜单｜读到：源码对视图 registerForContextMenu(view)，点击时 openContextMenu(view)（不带坐标），onCreateContextMenu 里 setHeaderTitle / setHeaderIcon；写错：规格写“openContextMenu 锚定在按钮上弹出”或“长按/点击 → Menu 弹出列表”，不区分两种形态，也没写标题和图标
