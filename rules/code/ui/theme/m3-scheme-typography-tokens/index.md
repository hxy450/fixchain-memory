# M3 色板和排版令牌的构造

agent 会看到什么：读到 lightColorScheme(...) / darkColorScheme(...) 构造的色板、Typography() 基准上 copy(fontSize = …, lineHeight = …) 的排版；产物里的颜色令牌和文字令牌只迁了源端显式写的字段，缺 surfaceContainer*、fontWeight、letterSpacing

## 规矩

- rule-c30b879cbdf2｜迁 M3 色板和排版令牌时，库默认的 surfaceContainer*、字重、字距一并迁｜读到：Typography() 基准上各档只 copy(fontSize = …, lineHeight = …)；色板用 lightColorScheme(...) / darkColorScheme(...) 构造，没显式传 surfaceContainer*；写错：文字令牌只有 fontSize、lineHeight，没有 fontWeight、letterSpacing；颜色令牌不设 surfaceContainer* 字段，或注明「源未显式提供，不设」
