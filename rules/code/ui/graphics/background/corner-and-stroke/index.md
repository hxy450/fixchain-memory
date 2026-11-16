# 同一视图上的圆角加描边

agent 会看到什么：读到同一视图同时带圆角和描边（MaterialButton 的 cornerRadius 加 strokeColor、CardView 的 cardCornerRadius 加描边、OutlinedBox）；交回的代码 .borderRadius 后跟不带 radius 的 .border

## 规矩

- rule-1b24fff4888f｜同一视图要圆角加描边时，圆角写进 border 的 radius，不在前面单写 borderRadius｜读到：同一视图同时有圆角和描边：MaterialButton 的 app:cornerRadius + app:strokeColor / app:strokeWidth、CardView 的 app:cardCornerRadius 加描边、TextInputLayout 的 OutlinedBox 样式；写错：.borderRadius(X) 之后紧跟不带 radius 的 .border({ width, color })
