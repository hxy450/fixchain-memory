# wrap_content 容器按子项定宽

agent 会看到什么：读到 wrap_content 宽的纵向 LinearLayout，或 PopupWindow#setWidth(WRAP_CONTENT) 的弹层，子项里 match_parent 和固定 dp 宽混排；产物里容器宽是不是 Math.max(各子项宽) + padding，有没有把 match_parent 子项自己测出的宽也算进去

## 规矩

- rule-865901193bee｜wrap_content 容器定宽只累加非 match_parent 子项，再用该宽排其余子项｜读到：PopupWindow#setWidth(WindowManager.LayoutParams.WRAP_CONTENT)，弹层内容是纵向 LinearLayout，子项有的 android:layout_width="match_parent"、有的是固定 dp 宽；写错：弹层宽写成 Math.max(各子项宽) + padding，把 match_parent 子项（含自绘控件的偏好长度）也算进去，弹层比源端宽
