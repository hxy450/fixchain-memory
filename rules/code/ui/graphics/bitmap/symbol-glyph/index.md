# 当图标用的字符和 SymbolGlyph 系统符号

agent 会看到什么：读到源端 Text / TextView 里当图标用的字符（emoji、粗体的“-”“+”、'✓'），或派工要求把这类字符换成 SymbolGlyph；产物里写了 SymbolGlyph($r('sys.symbol.…'))，外形和原字符不同，或 .fontColor 沿用了单值

## 规矩

- rule-6f23eada867d｜源 Text 里的 emoji 迁成目标 Text 原样保留，不换成 SymbolGlyph 系统符号｜读到：源端 Text("⭐") 这类 emoji 字面文本（如 ListItem 的 leadingContent）；写错：目标写 SymbolGlyph($r('sys.symbol.star_fill')) 一类系统符号替代 emoji
- rule-5ecc319a49f4｜TextView 文字加减号当按钮时按原字形画，不用带圆圈的近似 symbol｜读到：粗体 TextView 的 android:text 就是“-”“+”，充当步进器的减、加按钮（截图里是无圆环的普通字符）；写错：写成 SymbolGlyph($r('sys.symbol.minus_circle')) 之类外形不同的 symbol，减号多了圆环，与加号不对称
- rule-be120d27394c｜把 Text 换成 SymbolGlyph 时，fontColor 传 ResourceColor 数组，不沿用单值｜读到：审计或派工要求把 Text('✓') 这类 Unicode 符号换成 SymbolGlyph($r('sys.symbol.…'))；写错：SymbolGlyph(...) 后面保留原 Text 的单值 .fontColor($r('app.color.…'))，没包成数组
