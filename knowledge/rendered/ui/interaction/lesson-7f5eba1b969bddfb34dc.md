# SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，不凭枚举名加“左滑/右滑”注释；未覆写的触发阈值按源依赖版本的库默认值落实

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

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 androidx.compose.material3:material3-android 1.4.0（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕LTR 下 SwipeToDismissBox 的 EndToStart 对应手指从右往左滑，内容向负方向移动，背景从行尾露出
- 〔做法第 1、2 步〕PanGesture 的 GestureEvent.offsetX 是相对手指按下处的偏移，单位 vp，从左向右滑为正，反之为负
- 〔做法第 3 步〕应用没有另设 positionalThreshold（rememberSwipeToDismissBoxState 不传该参数）时：material3 1.4.0 的默认位置阈值是 56dp，松手速度阈值 DismissVelocityThreshold 是 125dp/s，任一满足即触发；卡里所用的 1.4.0-alpha17 也按 56dp 和 125dp/s 处理
