# 吐司和 Snackbar 的显示位置

agent 会看到什么：读到 Toast.makeText(...).show() 没调 setGravity / setMargin，或 Compose Scaffold 同时带 bottomBar、floatingActionButton 和 SnackbarHost；产物里 showToast 有没有传 bottom、自绘 Snackbar 有没有按底栏和 FAB 留出底部偏移

## 规矩

- rule-e0f68ff44815｜Toast 未设 setGravity 时，showToast 显式传 bottom，取 toast_y_offset｜读到：`Toast.makeText(...).show()`，没调 `setGravity` / `setMargin`；写错：`showToast({ message, duration })` 或公共 Toast 封装的 show() 只传文案和时长，没有 `bottom`，位置落在默认 80vp
- rule-ff6f98d01732｜叠加层自绘 Snackbar 时提供底部偏移，按源 Scaffold 的 bottomBar 和 FAB 传入｜读到：源页面 Scaffold(bottomBar = …, floatingActionButton = …, snackbarHost = { SnackbarHost(…) })；写错：叠加层实现的 Snackbar 固定贴底、没有底部偏移参数，显示时盖住底栏或 FAB
