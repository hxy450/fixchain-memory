# 按钮和图片的显式宽高

agent 会看到什么：读到按钮或 ImageView 的 android:layout_width / layout_height（固定 dp、@dimen 或 48dp 加 android:padding）；产物里 Image / Button 链上的 .width / .height 数值、padding 是否另加、有没有第二组异常大的尺寸

## 规矩

- rule-f6f05002ccf2｜源端 48dp 按钮带 padding 时，目标宽高写 48 再加 padding，不写成 24 加 padding｜读到：按钮 View 的 android:layout_width / layout_height 为 48dp，另有 android:padding="12dp"；写错：目标写成 .width(24).height(24).padding(12)，把 padding 当成尺寸之外另加
- rule-88dc3fda3024｜同一组件链上出现第二组 .width/.height 且数值异常大时，删掉后加的那组，保留原尺寸｜读到：源端 ImageView 给的是固定 dp（@dimen 引用）或 match_parent 尺寸；写错：Image(...) 的链上已有 .width('18vp').height('18vp') 或 .width('100%').height('100%')，后面又追加了一组 .width(21845).height(1431000589) 这类远超屏幕的整数尺寸
