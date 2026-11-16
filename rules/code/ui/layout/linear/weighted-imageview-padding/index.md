# 按 layout_weight 分高、带大内边距的 ImageView

agent 会看到什么：读到纵向 LinearLayout 里 ImageView 写 android:layout_height="0dp" 加 android:layout_weight，同时带 android:padding；产物里是不是写成 Image(...).layoutWeight(...).padding(...)

## 规矩

- rule-9331142eacff｜layout_weight 定高的 ImageView 带大 padding，不直接放到 Image 上｜读到：ImageView 的 android:layout_height="0dp" 加 android:layout_weight，同时带 android:padding（上下之和可能超过分得的槽高，横屏时尤其）；写错：写成 Image(...).layoutWeight(...).padding(...)，把源端 padding 直接放在 Image 上
