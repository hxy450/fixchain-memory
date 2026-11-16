# skydoves Balloon 气泡

agent 会看到什么：读过的源码里用 skydoves 的 Balloon.Builder（setBackgroundColor、setArrowPosition 等）；交回的代码里用 bindPopup 的 CustomPopupOptions 写气泡底色和 arrowOffset

## 规矩

- rule-fbfaf9a75168｜Balloon 的 setBackgroundColor 迁到 bindPopup 时写 popupColor 并关模糊｜读到：源端 skydoves `Balloon.Builder` 调了 `setBackgroundColor(…)`，颜色作用于整个气泡（含箭头）；写错：目标 `bindPopup` 的 `CustomPopupOptions` 没有 `popupColor`，只给 builder 里的 `Column` 加了 `.backgroundColor(…)` 和 `.borderRadius(…)`；或注释里写「PopupOptions 不支持背景色」
- rule-b33d6710accb｜带布尔异或和三元的箭头位置公式，逐字保留括号、列真值表再写 arrowOffset｜读到：源端 `setArrowPosition(…)` 的参数是 `0.25f + ((a ^ b) ? 0f : 0.5f)` 这类带布尔异或和三元运算的表达式；写错：目标 `arrowOffset` 的条件与源式相反；注释里转述的公式丢了内层括号
