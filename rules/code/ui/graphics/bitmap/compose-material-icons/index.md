# Compose 内置的 Icons 矢量图标

agent 会看到什么：读到 Compose 里用 Icons.AutoMirrored.* 这类内置矢量图标（如 Icons.AutoMirrored.Rounded.ArrowBack）；产物里转成的 Image($r('app.media.…')) 有没有 .matchTextDirection(true)

## 规矩

- rule-851161871449｜Icons.AutoMirrored 图标转 Image 时写 matchTextDirection(true)｜读到：Compose 里用 Icons.AutoMirrored.*（如 Icons.AutoMirrored.Rounded.ArrowBack）；写错：转成普通 Image($r('app.media.…'))，没有 .matchTextDirection(true)
- rule-6a68feccc49e｜Material Icons 的 media 未就绪时，按原名引用并登记占位，不用近似 sys.symbol｜读到：Compose 源里 Icons.Filled.Bookmark、Icons.Outlined.MoreVert、Icons.Outlined.Menu 这类具名 Material 图标，目标 media 里还没有对应 SVG；写错：写成 SymbolGlyph($r('sys.symbol.star_fill'))、sys.symbol.ellipsis、sys.symbol.list_bullet 等近似字形，报告自认「视觉近似降级」
