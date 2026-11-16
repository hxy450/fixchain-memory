# 源码自定义的触底加载 helper

agent 会看到什么：读到源端列表调用自定义的触底 helper，函数体是 derivedStateOf { 末项可见判定 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；规格的转换决策只写「helper → List.onReachEnd」或「onReachEnd / onScrollIndex」，没写触发条件、触发时机和调用点的重试参数

## 规矩

- rule-f64a3cc6a009｜源码自定义触底触发 helper 时，规格先读函数体，写清触发条件、时机和调用点实参｜读到：源端列表调用自定义的触底 helper，函数体是 derivedStateOf { 末项可见判定 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；写错：规格转换决策只写「helper → List.onReachEnd」或「onReachEnd / onScrollIndex」「onReachEnd / onDidScroll 阈值」，没写触发条件、触发时机和调用点的重试参数
