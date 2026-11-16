# 布局和代码引用的 @drawable 位图

agent 会看到什么：源布局或代码引用 @drawable/…、R.drawable.…（ImageView 的 android:src、TextView 的 android:background），图在 drawable-xxhdpi 等密度目录；目标 resources/base/media 下没有这些原图，页面改成纯 Text，或拿近名、带后缀的别的图顶替

## 规矩

- rule-9823643fc638｜源端 @drawable 位图在目标 media 里没有时，从对应密度目录复制原图引用，或登记待补｜读到：源端布局或代码引用 @drawable/... / R.drawable....，图在 drawable-xxhdpi 等密度目录里；写错：目标 resources 的 media 目录里没有对应图片，也没有登记待补资源，对应位置在 .ets 里写成了纯 Text
