# SpannableString.setSpan(start, end) 拆成 ArkUI Span 时按 end 为开区间逐字核对着色范围

## 何时使用

界面实现阶段，把源端 setSpan 着色、加粗的文字拆成 ArkUI Text + Span 时

## 适用情境

源端用 SpannableString.setSpan(span, start, end, flags) 按字符索引给一段文字着色，常见“固定前缀 + 动态值 + 后缀”的拼接，终点按前缀长度加动态值长度再加偏移计算。

## 例外与边界

- 目标改用属性字符串（StyledString）而不是 Text + Span 时，SpanStyle 用 start 加 length 表示范围：length 取 end − start，不要把源端的 end 直接填进 length。
- 源端几个 span 的范围互相重叠（如着色和加粗各管一段）时，Span 下不能再嵌套子组件，要按所有边界切成互不重叠的平铺段，每段带上覆盖它的全部样式，不能为了对齐某一个 span 的边界丢掉另一个的样式。

## 原因

end 是开区间终点；“前缀长度 + 1 + 值长度”一类写法会把紧随其后的后缀字符一起包进着色段，按“值本身”拆 Span 时容易把后缀留在基色。来源中写者在笔记里记下了 [9, 10+len)，输出仍按 9+len 截断，后缀“分”未着色，后续轮次才合并进着色 Span。

## 做法

1. 拆分前用前缀字数和一个样例值把每个字符的颜色写出来（例：前缀 9 字、值“46”，[9, 10+2) 覆盖“46分”），确认后缀是否在着色段内，再定 Span 边界。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 未用；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕setSpan(what, start, end, flags) 的区间是 [start, end)：end 处的字符不在内，start 等于 end 时长度为 0（SPAN_EXCLUSIVE_EXCLUSIVE 的零长度 span 被 SpannableStringBuilder 忽略），和 CharSequence.subSequence 的 end 不含一致
