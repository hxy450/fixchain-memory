# 可能为空的 wrap_content 文本的行高

agent 会看到什么：读到 wrap_content 的 TextView（可见或 INVISIBLE）文本可能为空（无标题、空正文、名称丢失），相邻元素靠它的一行高度定位；产物里 Text(this.title) 不处理空串，或改成 Visibility.Hidden 后内容仍是 ''

## 规矩

- rule-a9392a4969a2｜wrap_content 的 TextView 文本可能为空时，目标 Text 用空格或零宽字符兜底保留一行高｜读到：`TextView` 是 `wrap_content`、可见或 INVISIBLE，文本可能为空（无标题、空正文、名称丢失），相邻元素依赖它的一行高度定位；写错：目标 `Text(this.title)` 不处理空串，或已改成 `Visibility.Hidden` 但内容仍是 `''`，空 Text 高度为 0，相邻元素上移
