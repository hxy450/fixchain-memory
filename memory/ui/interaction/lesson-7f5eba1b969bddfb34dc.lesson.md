# SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，未覆写的触发阈值按源依赖版本的库默认值落实

ID：`lesson-7f5eba1b969bddfb34dc` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，转写 Material3 SwipeToDismissBox 的滑删方向与触发阈值、在列表行内自定义滑删手势时

## 适用情境

源端用 enableDismissFromStartToEnd、EndToStart 等枚举描述方向，背景对齐方向与之配合；rememberSwipeToDismissBoxState 未传 positionalThreshold，触发条件来自 material3 库默认、不在源文件里；目标在列表行内用 Stack + PanGesture 一类写法自定义滑删。

## 原因

只凭枚举名加“左滑/右滑”注释容易写反，规格写反后实现者照做，方向整体相反；StartToEnd/EndToStart 是相对布局方向的枚举，RTL 下物理方向相反。阈值来自库默认而不写在源文件里，凭印象写成“半宽”一类比例并自拟时长，短距离快滑或拖过固定距离时的结果会与源端不同。

## 做法

1. 按当前 layoutDirection 推导：LTR 下 EndToStart 是手指从右往左、内容 offset 为负、背景从行尾露出，RTL 下物理方向相反；规格同时写出枚举、手势方向和 offset 符号，并用源码的开关与背景对齐方向核对。
2. 实现时把开关翻成 offset 允许范围：LTR 下只允许 EndToStart 时为 [−行宽, 0]，阈值按 −offset 判断，落定到 −行宽；RTL 下范围、阈值符号与验收手势一起取反。
3. 源端未覆写阈值时，先从版本锁定（libs.versions.toml、compose BOM）确认 material3 版本，再在依赖源码包或 Gradle 缓存中查该版本的 SwipeToDismissBox.kt（SwipeToDismissBoxDefaults 的位置阈值、速度阈值与落定动画）。例：material3 1.4.0-alpha17 下为位移 56dp 或松手速度 125dp/s 任一满足即触发。查不到所用版本的源码时采用该例值并注明版本，版本不同的在报告中列出参数与版本差异，不写成“默认 50%”一类比例。

## 可选检查

- 有设备时按 LTR 左滑，背景应从行尾出现；反向滑动应无反应。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-7ced02d9c41ab6f4919a](../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：diagnosis, recommendation:6
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
- [case-fc6df865cb042aec7af1](../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`
