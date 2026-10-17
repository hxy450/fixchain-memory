# SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，不凭枚举名加“左滑/右滑”注释；未覆写的触发阈值按源依赖版本的库默认值落实

ID：`lesson-7f5eba1b969bddfb34dc` · 版本：3 · 阶段：spec/execute · 主题：[ui/interaction/hit-testing](index.md)

概要：SwipeToDismissBox 方向按手势与偏移符号写明

信号：`SwipeToDismissBox`, `enableDismissFromStartToEnd`, `EndToStart`, `StartToEnd`, `PanGesture`, `rememberSwipeToDismissBoxState`, `positionalThreshold`, `SwipeToDismissBoxDefaults`

## 何时使用

规格提取与界面实现阶段，转写 Material3 SwipeToDismissBox 的滑删方向与触发阈值、在列表行内自定义滑删手势时

## 适用情境

源端用 enableDismissFromStartToEnd、EndToStart 等枚举描述方向，背景对齐方向与之配合；rememberSwipeToDismissBoxState 未传 positionalThreshold，触发条件来自库默认、不在源文件里；目标在列表行内用 Stack + PanGesture 一类写法自定义滑删。

## 原因

只凭枚举名加“左滑/右滑”注释容易写反；规格写反后实现者照做，方向整体相反，实现者即使注意到背景从行尾露出也未必回头核对。阈值来自库默认而不写在源文件里，凭印象写成“半宽”一类比例并自拟时长，短距离快滑或拖过固定距离时的结果会与源端不同。

## 做法

1. 按 LTR 推导：EndToStart 是手指从右往左、内容 offset 为负、背景从行尾露出；规格同时写出枚举、手势方向和 offset 符号，并用源码的开关与背景对齐方向核对。
2. 实现时把开关翻成 offset 允许范围：只允许 EndToStart 时为 [−行宽, 0]，阈值按 −offset 判断，落定到 −行宽。
3. 源端未覆写阈值时，从工程依赖声明确认 material3 版本，按该版本的 SwipeToDismissBoxDefaults 与状态类实现位置阈值、速度阈值与落定动画（来源所用版本为位移 56dp 或松手速度 125dp/s 任一满足即触发）；查不到就登记待核，不写成“默认 50%”一类近似。

## 可选检查

- 有设备时左滑，背景应从行尾出现；反向滑动应无反应。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [编译修复只改报错行，不删功能或换异义替代](../../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [缺枚举的 FontWeight 写数值，不换近名](../../text/typography/lesson-605038b091e03c26c005.lesson.md)（共享 1 张卡）
- [Compose 显隐与尺寸动画逐项落实，不只渐变](../../animation/transitions/lesson-a4e6bcfb28597691c028.lesson.md)（共享 1 张卡）
- [内容定尺寸的父级里不写 100%，描边画在自身](../../layout/intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md)（共享 1 张卡）
- [LazyRow 转可横滑容器，不降成普通 Row](../../layout/scrolling/lesson-caa043fb95ff63e321e2.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-7ced02d9c41ab6f4919a](../../../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：diagnosis, rec-24b9a27737
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
- [case-fc6df865cb042aec7af1](../../../../../store/cases/case-fc6df865cb042aec7af1/725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2.json) · 结论：diagnosis, rec-ea018c5115, rec-c3ba66250d
  卡片版本：`725333df04b7bf7ef507cb28acc9e956d4e070ff49905447493a6f27eec530f2`
