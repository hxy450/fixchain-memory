# SpannableString.setSpan(start, end) 拆成 ArkUI Span 时按 end 为开区间逐字核对着色范围

ID：`lesson-eb59a95e5eb219c238b0` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把源端 setSpan 着色、加粗的文字拆成 ArkUI Text + Span 时

## 适用情境

源端用 SpannableString.setSpan(span, start, end, flags) 按字符索引给一段文字着色，常见“固定前缀 + 动态值 + 后缀”的拼接，终点按前缀长度加动态值长度再加偏移计算。

## 原因

end 是开区间终点；“前缀长度 + 1 + 值长度”一类写法会把紧随其后的后缀字符一起包进着色段，按“值本身”拆 Span 时容易把后缀留在基色。来源中写者在笔记里记下了 [9, 10+len)，输出仍按 9+len 截断，后缀“分”未着色，后续轮次才合并进着色 Span。

## 做法

1. 拆分前用前缀字数和一个样例值把每个字符的颜色写出来（例：前缀 9 字、值“46”，[9, 10+2) 覆盖“46分”），确认后缀是否在着色段内，再定 Span 边界。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-701f2e2280bcc31423bd](../../../store/cases/case-701f2e2280bcc31423bd/f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7.json) · 结论：diagnosis, recommendation:3
  卡片版本：`f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7`
