# Compose 的边缘渐隐（fadingEdges / fadingEdge）

agent 会看到什么：读到 Compose 内容上的 .fadingEdges(scrollState)、verticalGradient / Brush.horizontalGradient 做的 fadingEdge 修饰符（常配 horizontalScroll / verticalScroll、drawWithContent + BlendMode.DstIn）；产物里渐隐遮罩条的 linearGradient 方向和终点色、.mask 还是 blendMode(DST_IN) 覆盖层、遮罩上的 hitTestBehavior 和高度

## 规矩

- rule-f30cc83a0faa｜编译报 .mask 不支持渐变时，改用 linearGradient 覆盖层加 blendMode(DST_IN)｜读到：Compose 内容上用 verticalGradient 做的渐隐修饰符（fadingEdge）；或规格把它映射为 linearGradient 遮罩；写错：写成 .mask({ gradient: [...] })（编译不过），或编译修复时删掉整段渐隐、只留一句 TODO(...)
- rule-f667304ce9de｜linearGradient 的 angle 0 指向上方、90 左到右，轴向渐变优先用 direction｜读到：源端 Compose 用 .fadingEdges(scrollState) 配 .horizontalScroll(...) 或 .verticalScroll(...) 做边缘渐隐；或规格写「横向滚动 + fadingEdges（linearGradient 遮罩）」；写错：左右两端的遮罩条写成 .linearGradient({ angle: 0 / 180, ... })，上下两端的写成 angle 90 / 270，横纵整组互换
- rule-48d7ceff67fc｜底色到透明的渐隐遮罩，终点用同 RGB、alpha 为 0 的色，不用 transparent｜读到：源端 .fadingEdges(...) 没给 color（缺省 Color.Unspecified，走 FadeClip），内容自身在边缘淡出、不叠颜色；写错：目标遮罩条写成 .linearGradient({ colors: [[底色, 0], [Color.Transparent, 1]] })，或终点写 'transparent'
- rule-e82e2458f516｜HitTestMode.None 只管写它的节点，渐隐遮罩条把 None 写在有尺寸的绘制节点上｜写错：外包定位的 Row / Column 上写了 .hitTestBehavior(HitTestMode.None) 并注释成整组不参与命中，里面有尺寸的渐变 Column 等子节点仍是缺省 Default，盖住下层可点控件
