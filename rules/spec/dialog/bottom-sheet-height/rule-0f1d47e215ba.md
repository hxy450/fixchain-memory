# 提取 skipPartiallyExpanded = true 的底部弹层时，规格写明跳过半展开、高度跟随内容

审的是：规格
触发（任一种）：
- 读到：源端 ModalBottomSheet(sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true))；写错的样子：规格映射写「bindSheet 半模态（全展开 detent）」或 detents LARGE，没写高度跟随内容
适用范围：规格提取 Compose ModalBottomSheet 的展开方式时
做法：
- 规格写「跳过半展开，展开高度跟随内容」，映射写 bindSheet(…, { height: SheetSize.FIT_CONTENT })，不写全展开 detent 或 LARGE
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SheetSize.FIT_CONTENT = 2（@since 12）：弹层高度随内容自适应（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetSize.FIT_CONTENT）
- SheetOptions.height?: SheetSize | Length，@default SheetSize.LARGE：不写 height 时就是 LARGE，规格必须写明（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.height）
来源：1 张卡，1 个应用
- case-e332c2cc4929f36c08c7（Cofi）：做法第 1 步 ← 建议 2
