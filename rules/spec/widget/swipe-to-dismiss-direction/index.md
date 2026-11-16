# SwipeToDismissBox 的滑删方向

agent 会看到什么：读到源 `SwipeToDismissBox` 写 `enableDismissFromStartToEnd = false`、`SwipeToDismissBoxValue.EndToStart` 才算 dismiss；规格写「EndToStart，即右滑」，或只写枚举名、没写手势方向和 offset 符号

## 规矩

- rule-5de7cb7054fd｜规格转写 SwipeToDismissBox 方向时，同时写枚举、手势方向和 offset 符号｜读到：源 `SwipeToDismissBox` 写 `enableDismissFromStartToEnd = false`，`currentValue == SwipeToDismissBoxValue.EndToStart` 才算 dismiss，背景 `horizontalAlignment = Alignment.End`；写错：规格里写「EndToStart，即右滑」「右滑滑删过阈值」，或只写枚举名、没写手势方向和 offset 符号
