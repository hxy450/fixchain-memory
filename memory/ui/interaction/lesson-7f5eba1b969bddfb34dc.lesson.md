# SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，不凭枚举名加“左滑/右滑”注释

ID：`lesson-7f5eba1b969bddfb34dc` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，转写 Material3 SwipeToDismissBox 的滑删方向、在列表行内自定义滑删手势时

## 适用情境

源端用 enableDismissFromStartToEnd、EndToStart 等枚举描述方向，背景对齐方向与之配合；目标在列表行内用 Stack + PanGesture 一类写法自定义滑删。

## 原因

只凭枚举名加“左滑/右滑”注释容易写反；规格写反后实现者照做，方向整体相反，实现者即使注意到背景从行尾露出也未必回头核对。

## 做法

1. 按 LTR 推导：EndToStart 是手指从右往左、内容 offset 为负、背景从行尾露出；规格同时写出枚举、手势方向和 offset 符号，并用源码的开关与背景对齐方向核对。
2. 实现时把开关翻成 offset 允许范围：只允许 EndToStart 时为 [−行宽, 0]，阈值按 −offset 判断，落定到 −行宽。

## 可选检查

- 有设备时左滑，背景应从行尾出现；反向滑动应无反应。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-fc6df865cb042aec7af1](../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`
