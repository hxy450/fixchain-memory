# 源界面 Text 里的 emoji 字面文本

agent 会看到什么：源端 ListItem 的 leadingContent 等处写 Text("⭐") 这类 emoji 字面文本，上下文另有「图标用 SymbolGlyph」的规则；规格或转换决策表里对 emoji 的处理

## 规矩

- rule-fbf074743c37｜源界面 Text 里的 emoji 是字面文本，规格写原样保留为 Text，不按 SymbolGlyph 规则替换｜读到：源端 ListItem 的 leadingContent 等处写 Text("⭐") 这类 emoji 字面文本；上下文里另有「图标用 SymbolGlyph、不把 emoji 塞进 Text」的规则；写错：规格写「emoji 替换为已验证 symbol」，转换决策表写 emoji → SymbolGlyph
