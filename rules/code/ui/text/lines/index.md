# 行高、行数与省略

源端有 TextView 的 android:lineHeight、includeFontPadding、maxLines / lines / ellipsize（或都没写）、可能为空的 wrap_content 文本，或 Compose TextStyle 的 lineHeight、Text 的 maxLines / overflow，目标端有 Text 的 .lineHeight、.lineSpacing、maxLines、minLines、textOverflow，或按一行高度算的容器高度和相邻元素定位时

## 触发族

- [文字控件的行数限制和省略](text-max-lines/index.md)（11 条）：源端 TextView 的 android:maxLines / lines / ellipsize、Compose Text 的 maxLines / overflow（或者都没写），对应目标 Text 上的 maxLines、minLines、textOverflow 和测量式截断
- [Compose TextStyle 的 lineHeight](textstyle-line-height/index.md)（6 条）：读到 Compose TextStyle（多在 Typography 里）带 fontSize / lineHeight、没设 lineHeightStyle，产物里是 Text 的 .lineHeight()、.lineSpacing()、主题文件里的行高派生值，或按 lineHeight 常量算出的容器高度
- [可能为空的 wrap_content 文本的行高](empty-text-line-height/index.md)（1 条）：读到 wrap_content 的 TextView（可见或 INVISIBLE）文本可能为空（无标题、空正文、名称丢失），相邻元素靠它的一行高度定位；产物里 Text(this.title) 不处理空串，或改成 Visibility.Hidden 后内容仍是 ''
- [TextView 没写行高时的行距](textview-line-height/index.md)（3 条）：读到 TextView 只有 textAppearance 或 textSize、没写 android:lineHeight 和 android:includeFontPadding（单行撑起行高、多行正文，或 targetSdk < 28 时含日文等回退字体的文字）；产物里对应 Text 有没有 .lineHeight(...)、首末行的 padding，或用 .margin 凑行间距
