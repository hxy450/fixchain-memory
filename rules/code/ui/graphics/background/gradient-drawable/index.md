# drawable 里的 <gradient> 渐变（窗口背景、ImageView 着色）

agent 会看到什么：读过的源码里主题的 windowBackground 或 ImageView 的 android:src 是带 <gradient android:startColor / endColor> 的 drawable，可能再用 app:tint 着色；交回的写成单色 backgroundColor、新加的单色颜色键，或用 Image(...).fillColor 给渐变 SVG 着色

## 规矩

- rule-7671664c415b｜主题窗口背景是渐变 drawable 时，页面内容区根用共享常量加 .linearGradient，不压成单色键｜读到：页面规格写「Holo 默认，取不到精确值标待核」，styles.xml 里 parent="android:Theme.Holo"；写错：凭记忆写 .backgroundColor('#FF000000')，或往 color.json 新加 #FF000000 的颜色键给根 Column / NavDestination 用，没查 SDK 也没标待核
- rule-d43a4e523bc5｜ImageView 用 tint 给渐变着色时，用容器 linearGradient，不用 fillColor｜读到：ImageView 带 app:tint（如 ?android:attr/colorBackground 这类主题色），android:src 是白到透明的渐变 shape；写错：目标写成 Image($r('app.media.…')).fillColor(…) 给渐变 SVG 着色；深色主题下留下一条白色亮带
