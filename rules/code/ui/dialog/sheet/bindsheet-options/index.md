# bindSheet 的挂载点和 SheetOptions

agent 会看到什么：读到没有关闭按钮和拖拽把手的 BottomSheetDialogFragment，或同一页弹出多个底部弹层；产物里 bindSheet 的 SheetOptions（height、showClose、dragBar、detents）和几个 bindSheet 挂在哪个组件上

## 规矩

- rule-8a3a9fff45f7｜宿主挂 Material 底部弹层时 bindSheet 显式写 FIT_CONTENT、showClose:false｜读到：源端是 BottomSheetDialogFragment，界面里没有关闭按钮和拖拽把手；内容组件头注释写外壳参数归宿主，或给了带 showClose:false 的宿主样例；写错：宿主 bindSheet 的 options 只写了 height、dragBar 或 detents，没写 showClose: false 和 backgroundColor；或者写成 detents: [SheetSize.MEDIUM, SheetSize.LARGE] + dragBar: true；或从邻页锚点块照抄了缺项的 options
- rule-7534208555b6｜一个页面要挂多个 bindSheet 时，每个挂在独立的零尺寸锚点上，不在同一组件上连写｜读到：源端同一页面由菜单或按钮分别弹出多个 BottomSheetDialogFragment / 对话框；写错：同一组件上连写多个 .bindSheet(...)（两个 .bindSheet 之间没有新组件），只有最后一个能打开；或照抄先例页面的整段 bindSheet 属性链
- rule-760d27021744｜源弹层跳过半展开时，bindSheet 写 height: SheetSize.FIT_CONTENT｜读到：源端 rememberModalBottomSheetState(skipPartiallyExpanded = true)；或规格写「bindSheet 半模态（全展开 detent）」；写错：目标 bindSheet 的 options 写 detents: [SheetSize.LARGE]，或没写 height（默认 LARGE）
- rule-bd9f15a3ae62｜页面有多个独立底部弹窗时，每个 bindSheet 绑在不同节点上，不在同一组件上链式绑两次｜读到：页面并列两个以上 @Composable 底部弹窗组件，各自用独立的 visible 参数和状态控制显隐；写错：同一个组件上连续写 .bindSheet($$this.showA, this.sheetA()).bindSheet($$this.showB, this.sheetB())
