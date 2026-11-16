# wrap_content 行里 match_parent 高的子项

agent 会看到什么：读到 wrap_content 高的行容器（列表项、弹窗按钮行）里 android:layout_height="match_parent" 的子控件或竖分隔线；产物里这个子项的 .height('100%')、.alignSelf(ItemAlign.Stretch) 和 Row 的高度

## 规矩

- rule-94670fb34eb3｜wrap_content 行里的 match_parent 子项用 alignSelf 拉伸，不写 '100%'｜读到：横向 LinearLayout 的 android:layout_height="wrap_content"，子项 android:layout_height="match_parent"；纵向 LinearLayout 时是 android:layout_width 这一轴；写错：对应的 Row/Column 在这一轴没定尺寸，子项却写了 .height('100%') 或 .width('100%')，内容被撑到父级最大约束
- rule-259ef21585c2｜按钮行里有 match_parent 竖分隔 View 时，先给 Row 定高，再让分隔线 Stretch｜读到：wrap_content 高的弹窗卡片里，按钮行有 layout_height="match_parent" 的竖分隔 View，按钮是 wrap_content + padding；写错：按钮 Row 没写 .height(...)，只给竖 Divider 写 .alignSelf(ItemAlign.Stretch)，卡片被撑成父容器全高
