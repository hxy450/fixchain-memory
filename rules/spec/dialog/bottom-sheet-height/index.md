# 底部弹层的展开高度（ModalBottomSheet、BottomSheetDialogFragment）

agent 会看到什么：读到 ModalBottomSheet(sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true))，或 BottomSheetDialogFragment 的 onShow 里调了名为 setupFullHeight 的方法、或没改 peekHeight 和高度；规格按名字写「全高」「半开/全开」，给 detents LARGE / MEDIUM

## 规矩

- rule-0f1d47e215ba｜提取 skipPartiallyExpanded = true 的底部弹层时，规格写明跳过半展开、高度跟随内容｜读到：源端 ModalBottomSheet(sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true))；写错：规格映射写「bindSheet 半模态（全展开 detent）」或 detents LARGE，没写高度跟随内容
- rule-f6e063e6ce1a｜BottomSheetDialogFragment 的弹层高度看方法体判定，没改高度的写 FIT_CONTENT｜读到：BottomSheetDialogFragment 的 onShow 里调了名为 setupFullHeight 之类的方法，方法体只把 getLayoutParams() 原样 setLayoutParams 回去，再 setState(STATE_EXPANDED)；写错：规格按方法名写“全高展开”，转换决策给 detents:[SheetSize.LARGE] 或“detents 全高”
