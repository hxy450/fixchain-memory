# 位图的 tint 着色（android:tint、ColorFilter.tint）

agent 会看到什么：读到 ImageView 的 android:tint / app:tint、代码里 setColorFilter(color)，或 Compose Image 的 colorFilter = ColorFilter.tint(...)，图源是 png / jpg / webp 位图；产物里 Image 上写的是 .fillColor(...) 还是 .colorFilter(drawing.ColorFilter…)

## 规矩

- rule-740aa175bfa3｜源端给位图做 tint 着色时，目标用 Image.colorFilter，不用 fillColor｜读到：Compose Image(painter = painterResource(R.drawable.…), colorFilter = ColorFilter.tint(color))，drawable 是 png / jpg / webp 位图；写错：目标 Image 上写 .fillColor(颜色)，图源仍是同一张位图
