# Compose animateContentSize 与 AnimatedContent+SizeTransform：尺寸变化放进 animateTo 过渡

ID：`lesson-98a6ded89db8f578fd83` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，把 Modifier.animateContentSize 或 AnimatedContent（含 transitionSpec 与 SizeTransform）翻译成 ArkUI 时

## 适用情境

源端容器挂 Modifier.animateContentSize，或用 AnimatedContent(targetState) 配 transitionSpec（如上下滑入滑出）与 using SizeTransform 切换内容；目标用 if/else 或键化 ForEach 承载内容，准备直切或只保留滑入滑出。

## 原因

animateContentSize 与 SizeTransform 让容器尺寸在旧内容与新内容之间过渡；只保留内容的滑入滑出或直切时，容器高度跳变、相邻内容瞬移。AnimatedContent 的新旧内容会同时存在一段时间并各自做入场、出场动画，用一个节点直接改文本就没有这段过渡。

## 做法

1. animateContentSize：把引起内容尺寸变化的状态更新放进 animateTo，让容器尺寸从旧值过渡到新值，曲线与时长取源 animationSpec。
2. AnimatedContent：新旧内容用随目标状态变化的 key（if/else 分支或键化 ForEach）承载，分别挂入场、出场转场，方向条件取自源 transitionSpec，状态切换放进 animateTo；有 SizeTransform 时容器尺寸同样随之过渡，clip = false 时过渡期间不裁切内容。
3. 本步确实做不了时，按动画逐项登记缺口（哪种动画、源参数）交给有写权的后续步骤，不以“视觉细节”省略。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7d5b3583abd06943248f](../../../store/cases/case-7d5b3583abd06943248f/be28e286f2c5961d3c34a8a57df28d77cd5a345f9b4ff620dd610bd4975f4baf.json) · 结论：diagnosis, recommendation:3
  卡片版本：`be28e286f2c5961d3c34a8a57df28d77cd5a345f9b4ff620dd610bd4975f4baf`
