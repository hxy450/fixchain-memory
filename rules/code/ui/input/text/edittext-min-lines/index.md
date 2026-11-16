# 多行 EditText 的最小行数和高度（minLines）

agent 会看到什么：读到 EditText 带 android:minLines、没写 android:gravity；产物里 TextArea 的 minHeight 怎么算、lineHeight 带不带单位、内容不足时文字的竖直对齐

## 规矩

- rule-559e998d2aad｜多行 EditText 带 minLines 时，最小高度用源字体实际行距算，内容不足时竖直居中｜读到：EditText 带 android:minLines（未声明 android:gravity）；写错：TextArea 的 minHeight 按估算行高（如 4/3 em）算，lineHeight 写裸数字，文字顶对齐
