# Spannable 分段着色的文字

agent 会看到什么：读过的源码里用 SpannableString.setSpan(ForegroundColorSpan, start, end, …) 或 Spannable 文本给一段字着色（含可编辑的 EditText）；交回的代码里拆出的 Span 区间、RichEditor 还是 Text / TextArea

## 规矩

- rule-22fd827c061d｜setSpan(start, end) 拆成 Span 时按 end 开区间逐字算着色范围｜读到：SpannableString.setSpan(颜色 span, start, end, flags) 按索引给一段文字着色，end 常写成「前缀字数 + 值长度 + 后缀」的表达式；写错：Text 里拆出的着色 Span 少了区间末尾的字（如后缀字落在基色 Span 里），或多吞了区间外的字
- rule-37700e142d8a｜可编辑的分段着色编辑框用 RichEditor 常驻编辑，不拆成只读 Text 和单色 TextArea 两态｜读到：源端 EditText 常驻可编辑，文本以 Spannable 分段着色，宽度 WRAP_CONTENT；写错：目标写成「着色只读 Text ↔ 点击切换单色 TextArea」两态，编辑态没有颜色；注释却写等价于常驻可编辑的 EditText
