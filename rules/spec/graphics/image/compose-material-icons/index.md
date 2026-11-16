# Compose 用的 Material Icons 具名图标

agent 会看到什么：读到 Compose 源里 Icon(imageVector = Icons.Outlined.* / Icons.Filled.* / Icons.AutoMirrored.*) 引用 material-icons 库的具名图标，res/drawable 里没有对应文件；规格的转换决策写「Icons.* → SymbolGlyph，按语义映射」「取最近的 symbol」，或给具名图标配了语义近似的 sys.symbol 名

## 规矩

- rule-b9d5cee3656d｜Compose 的 Icons.* 图标，规格逐个记原名和风格，转换决策写下载 Material Icons 原矢量｜读到：Compose 源里 Icon(imageVector = Icons.Outlined.* / Icons.Filled.* / Icons.AutoMirrored.*) 引用 material-icons 库的具名图标，res/drawable 里没有对应文件；写错：规格的转换决策写「Icons.Outlined.* → SymbolGlyph，按语义映射」「取清单里最近的 symbol」，或给具名图标配了语义近似的 sys.symbol 名（如书签写成星标）
