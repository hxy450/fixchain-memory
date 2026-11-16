# 横向行里 wrap_content 子项的宽度

agent 会看到什么：读到横向 LinearLayout 里 wrap_content 的文字或图片列，和定宽兄弟并排、总宽接近或超过屏宽；产物里 Row 子项写成固定 .width、没有 .flexShrink 或按比例的 layoutWeight

## 规矩

- rule-dfe7b9f36fc9｜横向 LinearLayout 里定宽兄弟后的自适应宽文字，Row 里加 flexShrink(1)｜读到：横向 `<LinearLayout android:orientation="horizontal">`（常见于 layout-land 变体）里固定 dp 的 ImageView 之后，跟一个 android:layout_width="wrap_content" 的多行 TextView；写错：Row 里对应的 Text 只有 fontSize、padding、margin、height，没有 .flexShrink(1)、.layoutWeight(1) 或宽度约束；Row 本身已 .width('100%') 也照样溢出
- rule-c8f126ee4f8c｜并排 wrap_content 图片列总宽接近屏宽时，按固有宽比例 layoutWeight 分列，不写固定 width｜读到：match_parent 的水平 LinearLayout 里并排放 wrap_content 的子列或 ImageView，宽度由 drawable 固有尺寸加 android:layout_marginStart / layout_marginEnd 决定；写错：各列写成 .width(<固有 dp 值>) 的固定宽度，图片也是固定 width，中间夹 Blank().layoutWeight(1) 对齐
