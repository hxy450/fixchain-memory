# Compose Material 的 Badge 角标

agent 会看到什么：读到 Compose 的 BadgedBox 里 Badge(containerColor = …) { Text(count.toString()) }；产物里 ArkUI Badge({ count, style }) 的 maxCount、字色、字号、badgeSize，或自绘文本加 offset 当角标

## 规矩

- rule-8b0a2870b0b3｜源角标是 Text(count.toString()) 时，ArkUI Badge 显式写 maxCount 和字色字号｜读到：Compose `Badge(containerColor = …) { Text(count.toString()) }`（在 BadgedBox 里）；写错：ArkUI `Badge({ count, style: { badgeColor } })` 没写 maxCount（超过 99 显示 99+），字色、字号、badgeSize 用默认；或者自绘文本加 offset 当角标
