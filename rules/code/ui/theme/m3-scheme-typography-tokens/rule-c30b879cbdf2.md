# 迁 M3 色板和排版令牌时，库默认的 surfaceContainer*、字重、字距一并迁

审的是：代码
触发（任一种）：
- 读到：Typography() 基准上各档只 copy(fontSize = …, lineHeight = …)；色板用 lightColorScheme(...) / darkColorScheme(...) 构造，没显式传 surfaceContainer*；写错的样子：文字令牌只有 fontSize、lineHeight，没有 fontWeight、letterSpacing；颜色令牌不设 surfaceContainer* 字段，或注明「源未显式提供，不设」
适用范围：把 Compose Material3 的 ColorScheme 和 Typography 迁成目标端令牌层时
做法：
- 源码没显式传、但库默认会提供的字段也迁入：每档文字令牌带 fontWeight 和 letterSpacing（取 M3 各档默认值），色板按明暗补 surfaceBright、surfaceDim、surfaceContainerLowest 到 surfaceContainerHighest 的基线值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontWeight(value: number | FontWeight | ResourceStr): TextAttribute：落文字令牌的字重（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- letterSpacing(value: number | ResourceStr): TextAttribute，number 单位 fp：落文字令牌的字距；M3 的 letterSpacing 是 sp，数值对应 fp（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.letterSpacing）
针对本应用要查的：
- M3 各档文字的默认字重、字距，和明暗两套 surfaceContainer* 基线色：应用依赖的 androidx.compose.material3:material3 版本的库源码：Typography 默认构造用的各档令牌，lightColorScheme / darkColorScheme 的默认参数；按档读出 fontWeight 和 letterSpacing（sp），按明暗读出 surfaceBright、surfaceDim、surfaceContainer* 的色值，写进目标令牌
未核实：M3 默认字重、字距和 surfaceContainer* 基线值出自库代码，本机没有源码，没能逐字核实
来源：1 张卡，1 个应用
- case-4f288900adbe48a3c049（jerboa）：做法第 1 步 ← 建议 4、诊断
