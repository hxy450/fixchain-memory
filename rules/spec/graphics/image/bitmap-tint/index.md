# 位图上的着色（ColorFilter.tint、setColorFilter）

agent 会看到什么：读到源端 ColorFilter.tint(color)、tint 或 setColorFilter 作用在 drawable 位图上，上游页规格写「.fillColor / .colorFilter」；规格的转换决策或验收条目只写「ColorFilter.tint → Image .fillColor」，没写资源格式和「fillColor 仅 SVG」的前提，或把两者列成任选项

## 规矩

- rule-db5074452132｜规格写位图着色的转换决策时，注明资源格式，只给对它生效的 API 并写明前提｜读到：源端 ColorFilter.tint(color) / tint / setColorFilter 作用在 drawable 位图上；上游页规格写「.fillColor / .colorFilter（染色矩阵或同色 SVG 资源）」；写错：规格的转换决策或验收条目只写「ColorFilter.tint → Image .fillColor」，没写资源格式和「fillColor 仅 SVG」的前提，或把 fillColor / colorFilter 列成并列任选项
