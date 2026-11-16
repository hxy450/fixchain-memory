# 按内容总高导出的长图快照

agent 会看到什么：读到按内容总高 Bitmap.createBitmap 后整体 draw(canvas) 导出长图；产物里只做一次 componentSnapshot.createFromBuilder，或测自然高度的副本放在高度受限的容器里

## 规矩

- rule-b177bd152de9｜源端按内容总高建 Bitmap 导出长图时，目标端超一屏内容分段快照再拼接，并校验高度｜读到：安卓按子 View 累加的总高度 Bitmap.createBitmap(width, height) 后整体 draw(canvas) 导出，保存图高度随内容无上限；写错：目标端只做一次 createFromBuilder 快照，builder 根组件只定宽、高度由内容撑开，注释或交付说明断言「不受可视区域、屏幕边界和裁剪限制」；没有分段，也没有校验返回 PixelMap 的高度
- rule-f2ebe2974999｜测量内容自然高度的副本放进 Scroll，不放在受父容器高度约束的 Stack/Column 里｜写错：用来测内容自然高度、判断快照是否被截断的隐形副本放在高度受限的 Stack 或 Column 里（如 .height(0) 的 Stack），测得高度被父容器可用高度夹紧，与被截断的快照「一致」，分段从不触发
