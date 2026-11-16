# 兄弟间距用的单侧外边距

agent 会看到什么：读到 LinearLayout 子项只在一侧写 android:layout_marginStart / layout_marginEnd / layout_marginRight 当兄弟间距；产物里每项两侧对称的 .margin(...)，或 layoutWeight 项上带 .margin

## 规矩

- rule-75a6a0cf26c0｜源只在一侧设外边距时按原样翻译，用 Row 的 space 或单侧 margin，不拆成两侧对称｜读到：顶栏里第一个图标只写 android:layout_marginRight（如 10dp），第二个图标贴父容器的 paddingHorizontal；写错：目标给每个图标都写 .margin({ left: 5, right: 5 }) 这类两侧对称外边距，最右侧外距被放大
- rule-f74206d7be4b｜等权重兄弟带 marginStart 作间距时，间距移到 Row 的 space，不写在 layoutWeight 项上｜读到：水平 LinearLayout 里同级子项都是 android:layout_width="0dp" + android:layout_weight="1"，其中一项用 android:layout_marginStart / layout_marginEnd 承担卡间距；写错：等权重兄弟写成 .layoutWeight(1)，其中一项另带 .margin({ left: <间距> })（或 start / right），各卡宽度不相等
